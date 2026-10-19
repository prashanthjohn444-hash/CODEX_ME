Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
"===== ALL TOP-LEVEL WINDOWS OF PID ====="
$desk = [System.Windows.Automation.AutomationElement]::RootElement
$wins = $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)
foreach ($w in $wins) {
  try { if ($w.Current.ProcessId -eq $p.Id) { "WINDOW '$($w.Current.Name)' class=$($w.Current.ClassName) hwnd=$($w.Current.NativeWindowHandle)" } } catch {}
}
"===== WORKSPACE MENU ====="
$ws = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all) | Where-Object { $_.Current.ControlType.ProgrammaticName -eq 'ControlType.MenuItem' -and $_.Current.Name -eq 'Workspace' } | Select-Object -First 1
if ($ws) {
  $ws.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand()
  Start-Sleep -Milliseconds 900
  $items = $ws.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)
  foreach ($i in $items) { "WS | $($i.Current.ControlType.ProgrammaticName) | '$($i.Current.Name)'" }
  $ws.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Collapse()
} else { "no Workspace menu" }
