"""Generate a self-contained Lua script for Resolve's internal Lua console."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
plan = json.loads((ROOT / "edit-plan.json").read_text(encoding="utf-8"))


def lua(value):
    if value is None:
        return "nil"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (float, int)):
        return str(value)
    if isinstance(value, str):
        # Long brackets avoid Windows-path and UTF-8 escape issues.
        return "[=[" + value + "]=]"
    if isinstance(value, list):
        return "{" + ",".join(lua(v) for v in value) + "}"
    if isinstance(value, dict):
        return "{" + ",".join("[" + lua(k) + "]=" + lua(v) for k, v in value.items()) + "}"
    raise TypeError(type(value))


template = r'''
local plan = __PLAN__
local root = __ROOT__
local reportPath = root .. [[\timeline\resolve-lua-status.txt]]
local function status(s)
  local f = assert(io.open(reportPath, 'a'))
  f:write(os.date('!%Y-%m-%dT%H:%M:%SZ') .. ' ' .. s .. '\n')
  f:close()
  print(s)
end
local function check(result, description)
  if result == nil or result == false then error(description) end
  return result
end
local function main()
  status('BEGIN')
  local resolve = check(resolve or (bmd and bmd.scriptapp and bmd.scriptapp('Resolve')), 'Resolve API is not available')
  local manager = check(resolve:GetProjectManager(), 'Missing project manager')
  local project = check(manager:GetCurrentProject(), 'Missing active project')
  local oldName = project:GetName()
  if project:GetTimelineCount() ~= 0 then error('Refusing to overwrite a populated project') end
  if oldName ~= 'New Project aPython Day 01 - Course1' and oldName ~= 'Python Day 01 - Course' then
    error('Refusing to modify unrelated project: ' .. tostring(oldName))
  end
  if oldName ~= 'Python Day 01 - Course' then
    check(project:SetName('Python Day 01 - Course'), 'Unable to rename project')
  end
  status('PROJECT Python Day 01 - Course')
  check(project:SetSettings({timelineResolutionWidth='1920', timelineResolutionHeight='1080', timelineFrameRate='30', timelinePlaybackFrameRate='30'}), 'Project settings rejected')
  local pool = check(project:GetMediaPool(), 'Missing media pool')
  local imported = {}
  for _,c in ipairs(plan.clips) do
    if not imported[c.path] then
      local files = pool:ImportMedia({c.path})
      if files == nil or files[1] == nil then error('Media import failed: ' .. c.path) end
      imported[c.path] = files[1]
    end
  end
  status('IMPORTED ' .. tostring(#plan.clips) .. ' placements source files')
  local timeline = check(pool:CreateEmptyTimeline('Day 01 - English lesson'), 'Timeline creation failed')
  check(project:SetCurrentTimeline(timeline), 'Could not set current timeline')
  check(timeline:SetStartTimecode('00:00:00:00'), 'Timeline start TC rejected')
  while timeline:GetTrackCount('video') < 2 do check(timeline:AddTrack('video'), 'Video track creation failed') end
  while timeline:GetTrackCount('audio') < 1 do check(timeline:AddTrack('audio'), 'Audio track creation failed') end
  for i,c in ipairs(plan.clips) do
    local entry={mediaPoolItem=imported[c.path], startFrame=c.source_in_frame,
      endFrame=c.source_in_frame+c.duration_frames-1, recordFrame=c.record_frame,
      trackIndex=c.track, mediaType=(c.kind == 'video' and 1 or 2)}
    local placed = pool:AppendToTimeline({entry})
    if placed == nil or placed[1] == nil then error('Failed to place clip ' .. tostring(i) .. ': ' .. c.path) end
    if i%5==0 then status('PLACED ' .. tostring(i) .. '/' .. tostring(#plan.clips)) end
  end
  for _,mark in ipairs(plan.chapters) do
    timeline:AddMarker(mark.frame, 'Blue', mark.title, 'Day 1 lesson section', 1)
  end
  check(manager:SaveProject(), 'Could not save Resolve project')
  local archive = root .. [[\timeline\Python-Day-01-Course.drp]]
  check(manager:ExportProject('Python Day 01 - Course', archive), 'Could not export DRP')
  status('EXPORTED_DRP ' .. archive)
  local codecs = project:GetRenderCodecs('mp4') or {}
  local codec = nil
  for k,v in pairs(codecs) do
    if tostring(k):find('264') or tostring(v):find('264') then codec=v; break end
  end
  if codec == nil then error('MP4 H.264 codec not available') end
  check(project:SetCurrentRenderFormatAndCodec('mp4', codec), 'Could not select H.264')
  local output = root .. [[\output]]
  os.execute('if not exist "' .. output .. '" mkdir "' .. output .. '"')
  check(project:SetCurrentRenderMode(1), 'Could not set single-clip render mode')
  check(project:SetRenderSettings({SelectAllFrames=true, TargetDir=output, CustomName='python-day-01-english',
     ExportVideo=true, ExportAudio=true, FormatWidth=1920, FormatHeight=1080, FrameRate=30,
     VideoQuality=18000, AudioCodec='aac', AudioSampleRate=48000}), 'Render settings rejected')
  local job = check(project:AddRenderJob(), 'Could not add render job')
  status('QUEUED ' .. tostring(job))
  check(project:StartRendering({job}), 'Could not start Resolve render')
  status('RENDERING ' .. tostring(job))
end
local ok,err = xpcall(main,debug.traceback)
if not ok then status('BLOCKED ' .. tostring(err)) end
'''
(ROOT / "resolve-internal.lua").write_text(template.replace("__PLAN__", lua(plan)).replace("__ROOT__", lua(str(ROOT.parent))), encoding="utf-8")
print("Generated", ROOT / "resolve-internal.lua")
