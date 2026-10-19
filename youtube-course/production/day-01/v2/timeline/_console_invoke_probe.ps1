param([string]$Code, [string]$Marker, [int]$TimeoutSec = 30)
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$desk = [System.Windows.Automation.AutomationElement]::RootElement

function Get-ConsoleRoot {
  foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
    try { if ($w.Current.ProcessId -eq $p.Id -and $w.Current.ClassName -eq 'Fusion::ConsoleView') { return $w } } catch {}
  }
  return $null
}
function Find-Cls($scope, $cls) {
  foreach ($i in $scope.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) { if ($i.Current.ClassName -eq $cls) { return $i } }
  return $null
}

$cr = Get-ConsoleRoot
$host_ = if ($cr) { $cr } else { [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle) }
"CONSOLE_ROOT=$($host_.Current.ClassName)"
$edit = Find-Cls $host_ 'Fusion::ConsoleEdit'
$out  = Find-Cls $host_ 'QTextEdit'
"edit=$($edit -ne $null) out=$($out -ne $null)"
if (-not $edit -or -not $out) { throw 'console widgets missing' }

$vp = $edit.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
if ($vp.Current.Value -ne '') { $vp.SetValue(''); Start-Sleep -Milliseconds 300 }
$before = $out.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern).DocumentRange.GetText(400000)
$vp.SetValue($Code)
Start-Sleep -Milliseconds 400
"calling InvokePattern..."
$edit.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
$deadline = (Get-Date).AddSeconds($TimeoutSec)
$found = $false
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Seconds 2
  $t = $out.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern).DocumentRange.GetText(400000)
  if ($t -match [regex]::Escape($Marker)) { $found = $true; break }
}
$t = $out.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern).DocumentRange.GetText(400000)
"INVOKE_MARKER_FOUND=$found"
"INPUT_VALUE_AFTER='" + $vp.Current.Value + "'"
"===== TAIL ====="
$t.Substring([Math]::Max(0, $t.Length - 1500))
