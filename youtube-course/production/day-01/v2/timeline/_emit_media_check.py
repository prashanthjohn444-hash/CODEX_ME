"""Emit a read-only Console chunk that verifies every planned media file is in the pool.

All paths go inside Lua long strings ([[...]]) so Windows backslashes need no escaping.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
plan = json.loads((HERE / "edit-plan-v2.json").read_text(encoding="utf-8"))
PRELUDE = (
    "local pm=resolve:GetProjectManager() local pr=pm:GetCurrentProject() "
    "local tl=nil for i=1,pr:GetTimelineCount() do local t=pr:GetTimelineByIndex(i) "
    "if t:GetName()==[[Day01-v2-master]] then tl=t end end "
    "local pool=pr:GetMediaPool() local folder=pool:GetRootFolder() "
    "for _,f in ipairs(pool:GetRootFolder():GetSubFolderList()) do "
    "if f:GetName()==[[Day01-v2 Media]] then folder=f end end "
    "local function find(path) local tgt=string.lower(path) "
    "for _,it in ipairs(folder:GetClipList()) do local p=it:GetClipProperty('File Path') "
    "if p and string.lower(p)==tgt then return it end end return nil end "
    "local miss={} "
)
lines = []
for m in plan["media_pool"]:
    lines.append(f"if find([[{m['path']}]])==nil then miss[#miss+1]=[[{m['key']}]] end")
lines.append("print('MEDIACHECK missing='..#miss)")
lines.append("for _,m in ipairs(miss) do print('!!!MISSING '..m) end")
lines.append("print('MEDIACHECK poolcount='..#folder:GetClipList())")
lines.append("print('MEDIACHECK_END_ZZ')")
out = HERE / "console" / "chunk0_media_check.txt"
out.write_text(PRELUDE + " ".join(lines), encoding="utf-8")
print("wrote", out, "checking", len(plan["media_pool"]), "paths")
