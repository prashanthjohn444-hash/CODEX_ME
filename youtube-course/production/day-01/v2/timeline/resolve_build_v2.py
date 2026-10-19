"""Day 1 v2 — Resolve build planner / generator (canonical build script).

Confirmed API behaviour on this machine (probed live in Resolve's Console):
  * external scripting is disabled, and the Console IS the only way to drive Resolve
  * creating a timeline AND changing its settings inside one Console chunk deadlocks
    the UI thread -> every step is emitted as a separate, small chunk
  * the Console has no `io` library -> progress can only be read from the Console text
  * MediaPool:AppendToTimeline(recordFrame=...) is absolute timeline frames
  * TimelineItem:SetSpeed({Percentage=p, RippleTimeline=true}) KEEPS the source range
    and recomputes the clip length  -> this is how the real captures are stretched
    (the retime stays editable for the user in Retime Controls)
  * an over-long source range is clamped to the media length, so full-length appends
    can simply ask for a huge endFrame (audio source ranges are NOT timeline frames)

Outputs (all inside v2\\timeline):
    edit-plan-v2.json        inputs, frames, cue points, per-section fit
    fit\\S*-hold.mp4         freeze-hold clips (last frame + gentle zoom)
    resolve_build_v2.py      this script
    console\\chunkA..G.txt   the build chunks, run in order in the Resolve Console
"""
from __future__ import annotations

import argparse
import array
import json
import math
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

ROOT = Path(r"C:\Users\lms-work\Documents\Python\youtube-course\production\day-01")
V2 = ROOT / "v2"
OUT = V2 / "timeline"
FIT = OUT / "fit"
CONSOLE = OUT / "console"
VOICE = ROOT / "voice" / "v2"
MANIFEST = VOICE / "manifest.json"
BROLL = ROOT / "broll" / "v2" / "renders"
CAPTURES = ROOT / "screen" / "v2" / "captures"

FFMPEG = ROOT / "broll" / "node_modules" / "ffmpeg-static" / "ffmpeg.exe"
FFPROBE = ROOT / "broll" / "node_modules" / "ffprobe-static" / "bin" / "win32" / "x64" / "ffprobe.exe"

PROJECT_NAME = "python_01"
TIMELINE_NAME = "Day01-v2-master"
MEDIA_FOLDER = "Day01-v2 Media"
FPS = 30
WIDTH, HEIGHT = 1920, 1080
DRP_PATH = OUT / "Python-Day-01-v2.drp"
PLAN_PATH = OUT / "edit-plan-v2.json"

MAX_SLOWDOWN_PCT = 50.0       # never play real footage slower than 2x
MIN_HOLD_FRAMES = 45          # every retimed section ends on at least this much freeze-hold
HOLD_ZOOM = 0.05              # gentle 5% push-in across a freeze-hold
BROLL_DWELL_MIN_HOLD = 90     # extend b-roll dwell only when the section hold > 3 s
BROLL_DWELL_CAP = 300         # ... by at most 10 s
BROLL_CAP_TOTAL = 432         # ... never beyond 14.4 s

TRACKS = {"video": {1: "DEMO CAPTURES", 2: "B-ROLL"},
          "audio": {1: "NARRATION (ADAM)", 2: "SFX/MUSIC"}}

BROLL_FOR_SECTION = {
    "01": "shell-vs-file", "02": "setup-path", "03": "python-uses",
    "04": "interpreter-flow", "05": "prompt-map", "07": "syntax-repair",
    "08": "file-run-cycle", "09": "shell-vs-file", "10": "type-map",
    "11": "challenge-card",
}
CUE_SENTENCE = {"01": 0, "02": 1, "03": 2, "04": 0, "05": 1, "07": 0, "08": 10,
                "09": 0, "10": 4, "11": 0}

EDIT_NOTES = {
    "04": "capture 04 shows real interpreter usage only; the narration talks about "
          "installers. No installation footage is fabricated - voiceover + the "
          "interpreter-flow b-roll carry this stretch.",
    "08": "capture 08 shows real hello.py usage only; the VS Code download/extension "
          "instructions are carried by voiceover + the file-run-cycle b-roll. "
          "No installation footage is fabricated.",
    "09": "capture 09 is the recap demo and intentionally matches section 01's footage; "
          "the shell-vs-file graphic is reused here per the edit map.",
    "holds": "sections whose capture is far shorter than the narration keep the real "
             "capture at no more than 2x slow motion, then hold its last frame with a "
             "gentle push-in; the b-roll dwell is extended over the longest holds.",
}


def log(m: str) -> None:
    print(m, flush=True)


def lua_str(s: str) -> str:
    return "[[" + str(s).replace("]]", "] ]") + "]]"


def fit_speed(src_end: int, target_frames: int) -> tuple:
    """Playback percentage and the stretched frame count Resolve will produce.

    Resolve stretches a clip to ``floor(src_end / (pct/100))`` inclusive frames
    (measured 2026-10-18), so solving for the target length and flooring the
    percentage keeps the stretched clip a hair slower than the exact boundary.
    """
    need = src_end / max(target_frames, 1) * 100.0
    pct = max(math.floor(need * 1e4) / 1e4, MAX_SLOWDOWN_PCT)
    return pct, math.floor(src_end / (pct / 100.0)) + 1


def ffprobe(path: Path, count_frames: bool = False) -> dict:
    cmd = [str(FFPROBE), "-v", "error", "-select_streams", "v:0"]
    if count_frames:
        cmd.append("-count_frames")
    cmd += ["-show_entries",
            "stream=width,height,r_frame_rate,nb_frames,nb_read_frames,duration,codec_name,sample_rate,channels",
            "-show_entries", "format=duration", "-of", "json", str(path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {path}: {res.stderr.strip()}")
    data = json.loads(res.stdout or "{}")
    st = (data.get("streams") or [{}])[0]
    fmt = data.get("format") or {}

    def f(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    def rate(x):
        if not x:
            return None
        a, _, b = str(x).partition("/")
        try:
            return float(a) / float(b) if float(b) else None
        except (TypeError, ValueError, ZeroDivisionError):
            return None

    frames = None
    for k in ("nb_read_frames", "nb_frames"):
        if st.get(k):
            try:
                frames = int(st[k])
                break
            except (TypeError, ValueError):
                pass
    return {"width": st.get("width"), "height": st.get("height"),
            "fps": rate(st.get("r_frame_rate")), "frames": frames,
            "duration_seconds": f(st.get("duration")) or f(fmt.get("duration")),
            "codec": st.get("codec_name"), "sample_rate": st.get("sample_rate"),
            "channels": st.get("channels")}


def wav_frames(path: Path) -> int:
    with wave.open(str(path), "rb") as w:
        return w.getnframes()


def scan_captures(stable_wait: float) -> dict:
    out = {}
    present = []
    for i in range(1, 12):
        sid = f"{i:02d}"
        p = CAPTURES / f"section-{sid}-obs.mkv"
        if p.is_file():
            present.append((sid, p, p.stat().st_size))
        else:
            out[sid] = {"path": str(p), "size_bytes": 0, "complete": False,
                        "reason": "capture file not present"}
    first = {sid: size for sid, _p, size in present}
    if present and stable_wait > 0:
        log(f"  waiting {stable_wait:.0f}s to confirm capture size stability ...")
        time.sleep(stable_wait)
    for sid, p, _ in present:
        size1 = p.stat().st_size if p.is_file() else 0
        info = {"path": str(p), "size_bytes": size1}
        if size1 != first.get(sid) or size1 < 100_000:
            info.update(complete=False, reason=f"size not stable ({first.get(sid)} -> {size1})")
        else:
            pr = ffprobe(p, count_frames=True)
            info.update(pr)
            if not pr.get("frames"):
                info.update(complete=False, reason="no decodable video frames")
            elif pr.get("width") != WIDTH or pr.get("height") != HEIGHT:
                info.update(complete=False, reason=f"resolution {pr.get('width')}x{pr.get('height')}")
            elif not pr.get("fps") or abs(pr["fps"] - FPS) > 0.01:
                info.update(complete=False, reason=f"frame rate {pr.get('fps')}")
            else:
                info.update(complete=True, reason="readable, size-stable, 1920x1080 30fps")
        out[sid] = info
    return out


# ------------------------------------------------------------------ speech / cues
def rms_windows(wav_path: Path, win: float = 0.02):
    with wave.open(str(wav_path), "rb") as w:
        sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    a = array.array("h")
    a.frombytes(raw[: len(raw) // 2 * 2])
    if ch > 1:
        a = a[::ch]
    step = max(1, int(sr * win))
    out = []
    for i in range(0, len(a) - step + 1, step):
        chunk = a[i:i + step]
        acc = 0
        for v in chunk:
            acc += v * v
        out.append(math.sqrt(acc / step))
    return out, win


def speech_segments(wav_path: Path, min_seg=0.15, min_gap=0.30):
    rms, win = rms_windows(wav_path)
    if not rms:
        return []
    thr = max(200.0, 0.08 * max(rms))
    voiced = [(i * win, (i + 1) * win) for i, r in enumerate(rms) if r >= thr]
    if not voiced:
        return []
    merged = [list(voiced[0])]
    for s, e in voiced[1:]:
        if s - merged[-1][1] <= min_gap:
            merged[-1][1] = e
        else:
            merged.append([s, e])
    return [(s, e) for s, e in merged if e - s >= min_seg]


def sentences(text: str):
    out = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            continue
        for chunk in re.split(r"(?<=[.!?])\s+", para):
            s = chunk.strip()
            if s:
                out.append(s)
    return out


def window_speech(segs, start, dur):
    end = start + dur
    total = 0.0
    for s, e in segs:
        lo, hi = max(s, start), min(e, end)
        if hi > lo:
            total += hi - lo
    return total


def cue_seconds(segs, sents, index):
    total_chars = sum(len(s) for s in sents) or 1
    frac = sum(len(s) for s in sents[:index]) / total_chars
    total_speech = sum(e - s for s, e in segs) or 1.0
    target = frac * total_speech
    acc = 0.0
    cue = segs[0][0] if segs else 0.0
    for s, e in segs:
        dur = e - s
        if acc + dur >= target:
            cue = s
            break
        acc += dur
        cue = e
    cue = min((s for s, _ in segs), key=lambda o: abs(o - cue))
    return cue, frac, (sents[index] if sents else "")


# ------------------------------------------------------------------ hold renders
def last_frame_png(src: Path, out_png: Path, last_index: int) -> None:
    res = subprocess.run([str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error",
                          "-i", str(src), "-vf", f"select=eq(n\\,{last_index})",
                          "-frames:v", "1", str(out_png)], capture_output=True, text=True)
    if res.returncode != 0 or not out_png.is_file():
        raise RuntimeError(f"last-frame extract failed for {src}: {res.stderr.strip()}")


def render_hold(png: Path, frames: int, out_mp4: Path, zoom: float = HOLD_ZOOM) -> None:
    vf = (f"zoompan=z='min(1+{zoom}*on/{max(frames - 1, 1)}\\,1+{zoom})'"
          f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
          f"format=yuv420p")
    res = subprocess.run([str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error",
                          "-i", str(png), "-vf", vf, "-frames:v", str(frames), "-r", str(FPS),
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out_mp4)],
                         capture_output=True, text=True)
    if res.returncode != 0 or not out_mp4.is_file():
        raise RuntimeError(f"hold render failed {out_mp4.name}: {res.stderr.strip()}")
    got = ffprobe(out_mp4, count_frames=True)["frames"]
    if got != frames:
        raise RuntimeError(f"{out_mp4.name}: {got} frames, expected {frames}")


def render_broll_dwell(src_mp4: Path, extra_frames: int, out_mp4: Path) -> None:
    png = out_mp4.with_suffix(".last.png")
    info = ffprobe(src_mp4, count_frames=True)
    last_frame_png(src_mp4, png, info["frames"] - 1)
    fc = (f"[0:v]fps={FPS},format=yuv420p[v0];"
          f"[1:v]zoompan=z='min(1+{HOLD_ZOOM}*on/{max(extra_frames - 1, 1)}\\,1+{HOLD_ZOOM})'"
          f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={extra_frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
          f"format=yuv420p[v1];[v0][v1]concat=n=2:v=1:a=0[out]")
    res = subprocess.run([str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error",
                          "-i", str(src_mp4), "-i", str(png), "-filter_complex", fc,
                          "-map", "[out]", "-r", str(FPS), "-c:v", "libx264",
                          "-preset", "veryfast", "-crf", "18", str(out_mp4)],
                         capture_output=True, text=True)
    if res.returncode != 0 or not out_mp4.is_file():
        raise RuntimeError(f"dwell render failed {out_mp4.name}: {res.stderr.strip()}")
    png.unlink(missing_ok=True)
    want = info["frames"] + extra_frames
    got = ffprobe(out_mp4, count_frames=True)["frames"]
    if got != want:
        raise RuntimeError(f"{out_mp4.name}: {got} frames, expected {want}")


# ------------------------------------------------------------------ lua helpers
PRELUDE = (
    "local pm=resolve:GetProjectManager() local pr=pm:GetCurrentProject() "
    "local tl=nil for i=1,pr:GetTimelineCount() do local t=pr:GetTimelineByIndex(i) "
    f"if t:GetName()=={lua_str(TIMELINE_NAME)} then tl=t end end "
    "if tl==nil then print('ERR no timeline') end "
    "local pool=pr:GetMediaPool() local folder=pool:GetRootFolder() "
    "for _,f in ipairs(pool:GetRootFolder():GetSubFolderList()) do "
    f"if f:GetName()=={lua_str(MEDIA_FOLDER)} then folder=f end end "
    "local function find(path) local tgt=string.lower(path) "
    "for _,it in ipairs(folder:GetClipList()) do local p=it:GetClipProperty('File Path') "
    "if p and string.lower(p)==tgt then return it end end return nil end "
    "local function app(list) local r=pool:AppendToTimeline(list) "
    "if r==nil or r[1]==nil then print('ERR append failed') return nil end return r[1] end "
    "local function label(s) local o={} for w in string.gmatch(s,'[^,]+') do o[#o+1]=w end print(table.concat(o,',')) end "
)


def emit_chunks(plan: dict) -> list[Path]:
    CONSOLE.mkdir(parents=True, exist_ok=True)
    written = []

    def write(name, lines, tag):
        body = PRELUDE + " ".join(lines) + f" print('{tag}_END_ZZ')"
        p = CONSOLE / name
        p.write_text(body, encoding="utf-8")
        written.append(p)

    # A ------------------------------------------------------------------ tracks
    a = ["for _,k in ipairs({'video','audio'}) do for ti=1,tl:GetTrackCount(k) do "
         "local its=tl:GetItemListInTrack(k,ti) if #its>0 then print('A del '..k..ti..'='..tostring(tl:DeleteClips(its))) end end end",
         "tl:DeleteMarkersByColor('All')",
         "for _=1,4 do if tl:GetTrackCount('video')>2 then tl:DeleteTrack('video',tl:GetTrackCount('video')) end end",
         "for _=1,4 do if tl:GetTrackCount('audio')>2 then tl:DeleteTrack('audio',tl:GetTrackCount('audio')) end end",
         "for _=1,4 do if tl:GetTrackCount('video')<2 then tl:AddTrack('video') end end",
         "for _=1,4 do if tl:GetTrackCount('audio')<2 then tl:AddTrack('audio') end end",
         "print('A tracks v='..tl:GetTrackCount('video')..' a='..tl:GetTrackCount('audio'))"]
    for kind in ("video", "audio"):
        for idx, name in sorted(TRACKS[kind].items()):
            a.append(f"print('A name {kind}{idx}='..tostring(tl:SetTrackName('{kind}',{idx},{lua_str(name)}))"
                     f"..' -> '..tostring(tl:GetTrackName('{kind}',{idx})))")
    a.append("print('A fps='..tostring(tl:GetSetting('timelineFrameRate'))..' start='..tl:GetGetStartPlaceholder())"
             .replace("GetGetStartPlaceholder()", "GetStartFrame()"))
    a.append("print('A save='..tostring(pm:SaveProject()))")
    write("chunkA_tracks.txt", a, "A")

    # B/C ------------------------------------------------------------ V1 captures
    def v1_lines(sections):
        ls = []
        for sec in sections:
            start = sec["record_frame"]
            se = sec["slot_end_frame"] - 1
            request = sec["trim_end_frame"] if sec["mode"] == "trim" else sec["capture_frames"] - 1
            ls.append(f"do local cap=find({lua_str(sec['media_path'])})")
            ls.append("if cap==nil then print('B " + sec["id"] + " MISSING CAPTURE') else")
            ls.append(f"local x=app({{{{mediaPoolItem=cap,startFrame=0,endFrame={request},"
                      f"recordFrame={start},trackIndex=1,mediaType=1}}}})")
            ls.append(f"x:SetName({lua_str(sec['capture_label'])})")
            if sec["mode"] == "retime":
                ls.append(f"print('B {sec['id']} pct='..tostring(x:SetSpeed({{Percentage={sec['speed_pct']},"
                          f"RippleTimeline=true}}))..' end='..x:GetEnd())")
            else:
                ls.append(f"print('B {sec['id']} trim end='..x:GetEnd())")
            # Fill whatever is left of the slot with a frozen tail, so the section
            # always ends exactly on its slot boundary no matter how Resolve
            # rounds the retimed length (measured: the stretch formula is
            # floor(src_end / speed) but the Percentage is quantised, which can
            # land one frame short at an exact-fit boundary).
            ls.append(f"local se={se} local hl=se-x:GetEnd()")
            ls.append("if hl>0 then")
            if sec.get("hold_path"):
                ls.append(f"local h=app({{{{mediaPoolItem=find({lua_str(sec['hold_path'])}),startFrame=0,"
                          f"endFrame=hl-1,recordFrame=x:GetEnd()+1,trackIndex=1,mediaType=1}}}})")
                ls.append(f"h:SetName({lua_str(sec['hold_label'])})")
            else:
                ls.append(f"local lo={request}-hl+1 if lo<0 then lo=0 end "
                          f"local h=app({{{{mediaPoolItem=cap,startFrame=lo,endFrame={request},"
                          f"recordFrame=x:GetEnd()+1,trackIndex=1,mediaType=1}}}})")
                ls.append(f"h:SetName([[S{sec['id']} TAIL last frame (slot fill)]])")
                ls.append(f"if hl>8 then print('B {sec['id']} WARN long-tail hl='..hl) end")
            ls.append(f"print('B {sec['id']} fill hl='..hl..' end='..h:GetEnd()..' want='..se)")
            ls.append(f"if h:GetEnd()~=se then print('B {sec['id']} FILL-MISMATCH end='..h:GetEnd()"
                      f"..' want='..se..' hl='..hl) end")
            ls.append(f"else print('B {sec['id']} exact end='..x:GetEnd()..' want='..se) end")
            ls.append("end end")
        return ls

    sections = plan["sections_media"]
    write("chunkB_v1_01_06.txt", v1_lines([s for s in sections if s["id"] <= "06"]), "B")
    write("chunkC_v1_07_11.txt", v1_lines([s for s in sections if s["id"] > "06"]), "C")

    # D ---------------------------------------------------------------- V2 b-roll
    d = []
    for b in plan["broll_placements"]:
        d.append(f"do local b=find({lua_str(b['media_path'])}) if b==nil then print('D {b['section']} MISSING') else "
                 f"local x=app({{{{mediaPoolItem=b,startFrame=0,endFrame={b['dwell_frames'] - 1},"
                 f"recordFrame={b['record_frame']},")
        d.append(f"trackIndex=2,mediaType=1}}}}) x:SetName({lua_str(b['label'])}) "
                 f"local w={b['record_frame'] + b['dwell_frames'] - 1} "
                 f"if x:GetEnd()~=w then print('D {b['section']} MISMATCH start='..x:GetStart()..' end='..x:GetEnd()"
                 f"..' want='..w) else print('D {b['section']} ok start='..x:GetStart()..' end='..x:GetEnd()"
                 f"..' want='..w) end end end")
    write("chunkD_v2_broll.txt", d, "D")

    # E ------------------------------------------------------------- A1 narration
    # Audio-only media carries its own frame rate (24 fps as imported), so the
    # AppendToTimeline source range is in MEDIA frames while recordFrame is in
    # timeline frames: timeline_length ~= request * 30/24.  Sample-count
    # rounding inside Resolve makes the exact length unpredictable by +/-1
    # frame, which is far inside the 0.5 s join tolerance, so each narration
    # clip is a single append - no probe clip, no re-append churn (a large
    # probe clip wedged the app on 2026-10-18).
    e = []
    for sec in plan["sections_media"]:
        slot = sec["slot_frames"]
        request = int(slot * 24 / FPS + 0.5)
        e.append(f"do local w=find({lua_str(sec['wav_path'])})")
        e.append(f"if w==nil then print('E {sec['id']} MISSING') else")
        e.append(f"local slot={slot} local x=app({{{{mediaPoolItem=w,startFrame=0,endFrame={request},"
                 f"recordFrame={sec['record_frame']},trackIndex=1,mediaType=2}}}})")
        e.append("local len=x:GetEnd()-x:GetStart()+1")
        e.append(f"x:SetName({lua_str(sec['narration_label'])})")
        e.append(f"if len~=slot then print('E {sec['id']} NEAR start='..x:GetStart()..' len='..len"
                 f"..' want='..slot..' diff='..(len-slot)) else print('E {sec['id']} exact start='..x:GetStart()"
                 f"..' len='..len) end")
        e.append("end end")
    e.append("local ai=tl:GetItemListInTrack('audio',1) if #ai>0 then print('E a1LastEnd='..ai[#ai]:GetEnd()) end")
    e.append("print('E tlEnd='..tl:GetEndFrame())")
    write("chunkE_a1_narration.txt", e, "E")

    # F --------------------------------------------------------------- markers
    f = [f"print('F marker={lua_str(m['name'])}='..tostring(tl:AddMarker({m['frame']},'Blue',"
         f"{lua_str(m['name'])},{lua_str(m['note'])},1)))" for m in plan["markers"]]
    f.append("local mc=0 for _ in pairs(tl:GetMarkers()) do mc=mc+1 end print('F markers='..mc)")
    f.append("print('F save='..tostring(pm:SaveProject()))")
    write("chunkF_markers.txt", f, "F")

    # G ------------------------------------------------------- verify + export
    g = ["print('G project='..pr:GetName()..' fps='..tostring(tl:GetSetting('timelineFrameRate'))"
         "..' res='..tostring(tl:GetSetting('timelineResolutionWidth'))..'x'..tostring(tl:GetSetting('timelineResolutionHeight'))"
         "..' start='..tl:GetStartFrame()..' end='..tl:GetEndFrame())",
         "for _,k in ipairs({'video','audio'}) do for i=1,tl:GetTrackCount(k) do "
         "local its=tl:GetItemListInTrack(k,i) local cov=0 local gap=0 local pos=tl:GetStartFrame() "
         "for _,it in ipairs(its) do if it:GetStart()>pos then gap=gap+(it:GetStart()-pos) end "
         "cov=cov+it:GetDuration() pos=it:GetEnd()+1 end "
         "print('G '..k..i..' name='..tostring(tl:GetTrackName(k,i))..' items='..#its..' end='..(pos-1)..' gaps='..gap) end end",
         "for fr,inf in pairs(tl:GetMarkers()) do print('G marker '..fr..' '..tostring(inf.name)) end"]
    g.append("local mc=0 for _ in pairs(tl:GetMarkers()) do mc=mc+1 end print('G markerCount='..mc)")
    g.append("print('G pool='..#folder:GetClipList())")
    for sec in plan["sections_media"]:
        g.append(f"do local a={sec['record_frame']} local b={sec['slot_end_frame'] - 1} local cov=0 "
                 f"for _,it in ipairs(tl:GetItemListInTrack('video',1)) do local s=it:GetStart() local e=it:GetEnd() "
                 f"if e>=a and s<=b then local lo=s if lo<a then lo=a end local hi=e if hi>b then hi=b end "
                 f"cov=cov+(hi-lo+1) end end "
                 f"if cov~={sec['slot_frames']} then print('G S{sec['id']} COVERGAP cov='..cov..' want={sec['slot_frames']}') "
                 f"else print('G S{sec['id']} covered='..cov..' slots={sec['slot_frames']}') end end")
    g.append(f"print('G export='..tostring(pm:ExportProject(pr:GetName(),{lua_str(str(DRP_PATH))})))")
    write("chunkG_verify_export.txt", g, "G")
    return written


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stable-wait", type=float, default=0.0)
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    FIT.mkdir(parents=True, exist_ok=True)
    problems = []

    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sections = sorted(man["sections"], key=lambda s: s["id"])
    log(f"narration: {len(sections)} sections, {man['concatenated_audio']['duration_seconds']}s, "
        f"voice={man['voice_name']}")

    sec_plan = []
    prev_end = 0
    for s in sections:
        sid = s["id"]
        sf, ef = int(round(float(s["start_seconds"]) * FPS)), int(round(float(s["end_seconds"]) * FPS))
        if sf != prev_end:
            problems.append(f"S{sid} rounded start {sf} != prev end {prev_end}; forced")
            sf = prev_end
        sec_plan.append({"id": sid, "title": s["title"], "text": s["text"],
                         "wav": str(VOICE / s["file"]),
                         "narration_duration": round(float(s["end_seconds"]) - float(s["start_seconds"]), 3),
                         "record_frame": sf, "slot_end_frame": ef, "frames": ef - sf})
        prev_end = ef
    total_frames = prev_end
    log(f"slots: {total_frames} frames = {total_frames / FPS:.3f}s "
        f"(narration {man['concatenated_audio']['duration_seconds']}s)")

    broll_info = {}
    for stem in sorted(set(BROLL_FOR_SECTION.values())):
        p = BROLL / f"{stem}.mp4"
        if not p.is_file():
            problems.append(f"b-roll missing {p}")
            continue
        broll_info[stem] = {"path": str(p), **ffprobe(p, count_frames=True)}
        log(f"broll {stem}: {broll_info[stem]['frames']}f {broll_info[stem]['duration_seconds']}s")

    caps = scan_captures(args.stable_wait)
    complete = [k for k, v in caps.items() if v.get("complete")]
    missing = {k: v for k, v in caps.items() if not v.get("complete")}
    log(f"captures complete: {complete}")
    log(f"captures missing/incomplete: {sorted(missing)}")

    # ---- per-section fit -------------------------------------------------------
    media_pool, sections_media, v1_clips = [], [], []
    for sp in sec_plan:
        sid = sp["id"]
        slot = sp["frames"]
        cap = caps.get(sid) or {}
        rec = {"id": sid, "slot_frames": slot, "record_frame": sp["record_frame"],
               "slot_end_frame": sp["slot_end_frame"], "media_path": cap.get("path", ""),
               "wav_path": sp["wav"], "trim_end_frame": None, "hold_path": None}
        if not cap.get("complete"):
            problems.append(f"S{sid} capture not usable: {cap.get('reason')}")
            sections_media.append({**rec, "mode": "placeholder", "capture_frames": 0,
                                   "speed_pct": 100.0, "speed_multiplier": 1.0,
                                   "stretched_frames": slot, "hold_frames": 0,
                                   "capture_label": f"S{sid} PLACEHOLDER - CAPTURE PENDING",
                                   "hold_label": "", "narration_label": f"S{sid} NARRATION (ADAM)",
                                   "fill": "placeholder"})
            continue
        cap_frames = int(cap["frames"])
        src_end = cap_frames - 1
        if cap_frames > slot:
            mode, pct, src_out = "trim", 100.0, slot - 1
            stretched, hold = slot, 0
        else:
            mode = "retime"
            # Fill the slot with the capture; when that would leave less than
            # MIN_HOLD_FRAMES of tail, aim a little slower (or, for a capture
            # nearly as long as its slot, a hair faster) so the section ends on
            # a real freeze-hold.  Two Resolve quirks force this:
            #   * SetSpeed quantises Percentage, so the stretched length can land
            #     one frame short of an exact-fit target;
            #   * AppendToTimeline wedges the UI thread on a 1-frame source range.
            # Keeping every tail a proper hold means no build-time slot fill is
            # ever only a frame or two long.
            pct, stretched = fit_speed(src_end, slot - 1)
            hold = slot - stretched
            if hold < MIN_HOLD_FRAMES:
                pct, stretched = fit_speed(src_end, slot - MIN_HOLD_FRAMES)
                hold = slot - stretched
            if hold < 0:
                hold, stretched = 0, slot
            src_out = None
        rec.update(mode=mode, capture_frames=cap_frames, speed_pct=pct,
                   speed_multiplier=round(100.0 / pct, 4), stretched_frames=stretched,
                   hold_frames=hold, trim_end_frame=(src_out if mode == "trim" else None),
                   capture_label=(f"S{sid} DEMO {cap_frames / FPS:.1f}s"
                                  + (f" @{pct:.1f}% ({100.0 / pct:.2f}x slow)"
                                     if abs(pct - 100) > 0.01 else " TRIMMED TO SLOT")
                                  + (f" + HOLD" if hold else "")),
                   hold_label=(f"S{sid} HOLD last frame {hold / FPS:.1f}s (gentle zoom)" if hold else ""),
                   narration_label=f"S{sid} NARRATION (ADAM)",
                   narration_frames=sp["frames"],
                   fill=("capture-trimmed-to-slot" if mode == "trim"
                         else ("capture-retimed-hold" if hold else "capture-retimed")))
        if hold:
            hp = FIT / f"S{sid}-hold.mp4"
            if not args.no_render or not hp.is_file():
                png = FIT / f"S{sid}-last.png"
                last_frame_png(Path(cap["path"]), png, cap_frames - 1)
                render_hold(png, hold, hp)
                png.unlink(missing_ok=True)
                log(f"  S{sid}: retime {pct:.4f}% -> {stretched}f + freeze-hold {hold}f "
                    f"({hold / FPS:.2f}s)")
            got = ffprobe(hp, count_frames=True)["frames"]
            if got != hold:
                problems.append(f"S{sid} hold file is {got}f, expected {hold}")
            rec["hold_path"] = str(hp)
        sections_media.append({**rec, "narration_frames": sp["frames"]})
        if abs((stretched + hold) - slot) > 0:
            problems.append(f"S{sid} fill {stretched}+{hold} != slot {slot}")

    if not args.no_render:
        # any hold file left over from an earlier run for a section that no longer needs one
        for p in FIT.glob("S*-hold.mp4"):
            sid = p.name[1:3]
            sec = next((s for s in sections_media if s["id"] == sid), None)
            if sec and not sec.get("hold_path"):
                log(f"  removing stale {p.name}")

    # ---- V2 b-roll -------------------------------------------------------------
    hold_by_section = {s["id"]: s.get("hold_frames", 0) for s in sections_media}
    broll_placements = []
    for sp in sec_plan:
        sid = sp["id"]
        stem = BROLL_FOR_SECTION.get(sid)
        if not stem or stem not in broll_info:
            continue
        info = broll_info[stem]
        clip_frames = int(info["frames"])
        segs = speech_segments(VOICE / f"section-{sid}.wav")
        sents = sentences(sp["text"])
        idx = min(CUE_SENTENCE[sid], max(0, len(sents) - 1))
        cue_rel, _frac, sent_text = cue_seconds(segs, sents, idx)
        cue_frame = sp["record_frame"] + int(round(cue_rel * FPS))
        speech_win = window_speech(segs, cue_rel, clip_frames / FPS)
        coverage = speech_win / (clip_frames / FPS)

        hold = hold_by_section.get(sid, 0)
        extra = 0
        if hold > BROLL_DWELL_MIN_HOLD:
            extra = max(0, min(hold, BROLL_DWELL_CAP, BROLL_CAP_TOTAL - clip_frames))
        limit = sp["slot_end_frame"] - cue_frame
        play = min(clip_frames, max(1, limit))
        dwell = min(play + extra, limit)
        extra = dwell - play
        media_path = info["path"]
        label = f"S{sid} BROLL {stem}"
        if extra > 0:
            dp = FIT / f"broll-{stem}-dwell-S{sid}.mp4"
            if not dp.is_file():
                render_broll_dwell(Path(info["path"]), extra, dp)
                log(f"  S{sid}: b-roll {stem} dwell +{extra}f over the hold")
            got = ffprobe(dp, count_frames=True)["frames"]
            media_path = str(dp)
            label += f" (+{(got - clip_frames) / FPS:.1f}s dwell)"
        broll_placements.append({
            "section": sid, "stem": stem, "media_path": media_path,
            "source_path": info["path"], "record_frame": cue_frame, "label": label,
            "cue_sentence_index": idx, "cue_sentence": sent_text,
            "cue_relative_seconds": round(cue_rel, 3),
            "absolute_start_seconds": round(sp["record_frame"] / FPS + cue_rel, 3),
            "clip_frames": clip_frames, "dwell_frames": dwell,
            "dwell_extra_frames": extra, "dwell_seconds": round(dwell / FPS, 3),
            "speech_coverage": round(coverage, 3),
            "dwell_extended_for_hold": bool(extra),
            "note": "edit map reuse of the section 01 graphic (recap)" if sid == "09" else "",
        })
        if coverage < 0.5:
            problems.append(f"b-roll S{sid} only {coverage * 100:.0f}% over speech")
        if cue_frame + dwell > sp["slot_end_frame"]:
            problems.append(f"b-roll S{sid} dwell overruns its section")

    # ---- media pool / markers --------------------------------------------------
    for sec in sections_media:
        if sec["media_path"]:
            media_pool.append({"key": f"capture-S{sec['id']}", "path": sec["media_path"]})
        if sec.get("hold_path"):
            media_pool.append({"key": f"hold-S{sec['id']}", "path": sec["hold_path"]})
        media_pool.append({"key": f"narration-S{sec['id']}", "path": sec["wav_path"]})
    for b in broll_placements:
        media_pool.append({"key": f"broll-S{b['section']}", "path": b["media_path"]})
    uniq = {}
    for m in media_pool:
        uniq.setdefault(m["path"], m)
    media_pool = list(uniq.values())

    markers = [{"frame": sp["record_frame"], "name": f"S{sp['id']}", "note": sp["title"]}
               for sp in sec_plan]

    plan = {
        "project_name": PROJECT_NAME, "timeline_name": TIMELINE_NAME,
        "media_folder": MEDIA_FOLDER,
        "spec": {"width": WIDTH, "height": HEIGHT, "fps": FPS},
        "fit_policy": {
            "max_slowdown_pct": MAX_SLOWDOWN_PCT,
            "retime": "TimelineItem:SetSpeed({Percentage=p, RippleTimeline=true}) keeps the "
                      "source range and recomputes the clip length, so the real capture is "
                      "stretched ON THE TIMELINE CLIP and stays editable in Retime Controls",
            "remainder": "a section-labelled freeze-hold clip (real last frame + gentle "
                         f"{HOLD_ZOOM * 100:.0f}% push-in) fills the rest of the slot",
            "broll_dwell_min_hold_frames": BROLL_DWELL_MIN_HOLD,
            "broll_dwell_cap_frames": BROLL_DWELL_CAP,
        },
        "rounding_rule": "start_frame=round(start_seconds*30), slots contiguous; "
                         "max rounding error 0.5 frame = 0.0167 s",
        "voice": man.get("voice_name"),
        "total_frames": total_frames, "total_seconds": round(total_frames / FPS, 3),
        "narration_seconds": man["concatenated_audio"]["duration_seconds"],
        "sections_media": sections_media, "broll_placements": broll_placements,
        "media_pool": media_pool, "markers": markers, "tracks": TRACKS,
        "captures": caps, "missing_or_incomplete_captures": sorted(missing),
        "edit_notes": EDIT_NOTES, "problems": problems,
    }
    PLAN_PATH.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    chunks = emit_chunks(plan)
    holds = sum(1 for s in sections_media if s.get("hold_frames"))
    log(f"media pool files: {len(media_pool)} | V2 placements: {len(broll_placements)} | "
        f"markers: {len(markers)} | holds: {holds}")
    log(f"wrote {PLAN_PATH.name} and {len(chunks)} console chunks")
    if problems:
        log("PROBLEMS: " + "; ".join(problems))
    return 0


if __name__ == "__main__":
    sys.exit(main())
