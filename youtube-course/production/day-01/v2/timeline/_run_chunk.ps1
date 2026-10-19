param(
  [Parameter(Mandatory = $true)][string]$Chunk,
  [Parameter(Mandatory = $true)][string]$Marker,
  [int]$TimeoutSec = 300,
  [string]$Tag = ""
)
$dir = "C:\Users\lms-work\Documents\Python\youtube-course\production\day-01\v2\timeline"
$out = powershell -ExecutionPolicy Bypass -File "$dir\_console_run2.ps1" -CodeFile "$dir\console\$Chunk" -Marker $Marker -TimeoutSec $TimeoutSec 2>&1
$out | Out-File "$dir\_last_chunk.log" -Encoding UTF8
$tag = if ($Tag) { $Tag } else { $Chunk.Substring(5, 1) }
"--- $Chunk (log: _last_chunk.log, $($out.Count) lines) ---"
$out | Select-String -Pattern "^(MARKER_FOUND=|ERR |!!!|WARN )" | ForEach-Object { $_.Line }
$out | Select-String -Pattern "^$tag " | ForEach-Object { $_.Line } | Select-Object -Last 40
