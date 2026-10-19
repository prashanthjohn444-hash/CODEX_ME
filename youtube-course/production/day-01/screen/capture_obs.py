"""Capture actual VS Code/PowerShell demonstrations via the dedicated OBS scene.

Run from the active Windows desktop. Never treats a graphic as a captured demo.
The 11 OBS takes follow narration-section lengths; action timings are editorial,
not speech synchronization. A real editor should trim and align each take.
"""
import ctypes
import datetime
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
CAPTURES = ROOT / "captures"
VOICE = ROOT.parent / "voice" / "manifest.json"
RESULT = ROOT / "obs-capture-results.json"
PS = "powershell.exe"
USER32 = ctypes.windll.user32
FFPROBE = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffprobe.exe"))
OBS_LABEL = "OBS 32.2.2 - Profile: Python30Days-Day01 - Scenes: Python30Days-Day01"


def save(data):
    RESULT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def obs_button(name):
    script = f"""
Add-Type -AssemblyName UIAutomationClient
$r=[System.Windows.Automation.AutomationElement]::RootElement
$win=$r.FindFirst([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty,'{OBS_LABEL}'))
if(!$win){{throw 'Dedicated OBS window is missing'}}
$buttons=$win.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty,'{name}'))
if(!$buttons -or $buttons.Count -lt 1){{throw 'OBS button missing: {name}'}}
$buttons.Item(0).GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
"""
    subprocess.run([PS, "-NoProfile", "-Command", script], check=True, timeout=25)


def click(x, y):
    USER32.SetCursorPos(x, y)
    USER32.mouse_event(2, 0, 0, 0, 0)
    USER32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(.25)


def key(code, ctrl=False):
    if ctrl:
        USER32.keybd_event(0x11, 0, 0, 0)
    USER32.keybd_event(code, 0, 0, 0)
    USER32.keybd_event(code, 0, 2, 0)
    if ctrl:
        USER32.keybd_event(0x11, 0, 2, 0)
    time.sleep(.18)


def paste(text):
    # Keep clipboard text out of command-line arguments; use stdin through a
    # small PowerShell process to avoid quoting commands as PowerShell code.
    script = "$input | Set-Clipboard"
    subprocess.run([PS, "-NoProfile", "-Command", script], input=text,
                   text=True, check=True, timeout=20)
    key(0x56, ctrl=True)


def focus_editor():
    # OBS occupies the left side of the desktop; click the visible right-hand
    # VS Code region to bring the isolated editor forward without capturing OBS.
    click(1600, 370)


def file(name):
    focus_editor()
    key(0x50, ctrl=True)
    paste(name)
    key(0x0D)
    time.sleep(.7)


def terminal(cmd):
    click(1140, 780)
    paste(cmd)
    key(0x0D)
    time.sleep(1.1)


def run_steps(index):
    if index == 1:
        file("expression_only.py")
        terminal("python")
        terminal("10 + 20")
        terminal("exit()")
        terminal("python expression_only.py")
        file("printed_expression.py")
        terminal("python printed_expression.py")
    elif index == 2:
        file("hello.py")
        terminal("python hello.py")
    elif index == 3:
        file("hello.py")
        terminal("python hello.py")
    elif index == 4:
        terminal("python --version")
        terminal("py --version")
    elif index == 5:
        terminal("python")
        terminal("10 + 20")
        terminal("exit()")
        terminal("python hello.py")
    elif index == 6:
        terminal("python")
        for command in ["10 + 20", "10 - 3", "4 * 5", "print('Hello, Python!')", "exit()"]:
            terminal(command)
    elif index == 7:
        file("broken_example.py")
        terminal("python broken_example.py")
        # Repair the file inside the actual editor, then run the saved script.
        click(620, 100)
        key(0x23)  # End, while editor focus is on line 1.
        paste(")")
        key(0x53, ctrl=True)
        terminal("python broken_example.py")
    elif index == 8:
        file("hello.py")
        terminal("python hello.py")
        file("printed_expression.py")
        terminal("python printed_expression.py")
    elif index == 9:
        file("expression_only.py")
        terminal("python expression_only.py")
        file("printed_expression.py")
        terminal("python printed_expression.py")
    elif index == 10:
        file("types_preview.py")
        terminal("python types_preview.py")
    elif index == 11:
        file("hello.py")
        terminal("python hello.py")


def main():
    manifest = json.loads(VOICE.read_text(encoding="utf-8"))
    if manifest["status"] != "completed":
        raise RuntimeError("Narration sections are not complete")
    # This is a dedicated new capture set. Never overwrite an earlier OBS take.
    state = {"status": "capturing", "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "recorder": "OBS Studio 32.2.2", "editor": "VS Code", "kind": "authentic desktop capture",
             "captures": [], "warnings": ["Editorial trims and visual sync to narration remain necessary."]}
    save(state)
    focus_editor()
    # Dismiss only the temporary VS Code extension suggestion, not project content.
    click(1895, 922)
    for section in manifest["sections"]:
        index = int(section["id"])
        dest = CAPTURES / f"section-{index:02d}-obs.mkv"
        if dest.exists():
            # Resume a verified, nonempty take. Never re-record over completed footage.
            subprocess.run([str(FFPROBE), "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1", str(dest)],
                           capture_output=True, text=True, check=True, timeout=15)
            state["captures"].append({"section": index, "path": str(dest),
                                      "duration_seconds": float(subprocess.check_output(
                                          [str(FFPROBE), "-v", "error", "-show_entries", "format=duration",
                                           "-of", "default=noprint_wrappers=1:nokey=1", str(dest)],
                                          text=True).strip()), "fps": 30, "width": 1920,
                                      "height": 1080, "action": section["title"],
                                      "bytes": dest.stat().st_size})
            save(state)
            continue
        before = set(CAPTURES.glob("*.mkv"))
        obs_button("Start Recording")
        started = time.monotonic()
        try:
            focus_editor()
            run_steps(index)
            # Each take covers its spoken passage, without claiming precise sync.
            # A few extra seconds provide edit handles around the real interactions.
            wait = section["audio"]["duration_seconds"] + 3 - (time.monotonic() - started)
            if wait > 0:
                time.sleep(wait)
        finally:
            obs_button("Stop Recording")
        time.sleep(1)
        new = list(set(CAPTURES.glob("*.mkv")) - before)
        if len(new) != 1:
            raise RuntimeError(f"Expected one new OBS recording for section {index}; found {new}")
        raw = new[0]
        for attempt in range(40):
            try:
                raw.rename(dest)
                break
            except PermissionError:
                if attempt == 39:
                    raise
                time.sleep(.3)
        proc = subprocess.run([str(FFPROBE), "-v", "error", "-show_entries",
                               "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", str(dest)],
                              capture_output=True, text=True, check=True, timeout=15)
        info = json.loads(proc.stdout)
        streams = info["streams"]
        video = next(s for s in streams if s["codec_type"] == "video")
        if (video["width"], video["height"], video["r_frame_rate"]) != (1920, 1080, "30/1"):
            raise RuntimeError(f"Bad OBS recording properties: {video}")
        state["captures"].append({"section": index, "path": str(dest),
                                  "duration_seconds": float(info["format"]["duration"]),
                                  "fps": 30, "width": 1920, "height": 1080,
                                  "action": section["title"], "bytes": dest.stat().st_size})
        save(state)
    state["status"] = "captured_pending_visual_review"
    state["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(state)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        if RESULT.exists():
            state = json.loads(RESULT.read_text(encoding="utf-8"))
            state["status"] = "failed"
            state["error"] = repr(exc)
            save(state)
        raise
