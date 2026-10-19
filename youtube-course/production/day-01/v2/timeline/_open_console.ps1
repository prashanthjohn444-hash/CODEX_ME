Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)

function FindByName($scope, $name) {
  $items = $scope.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)
  foreach ($i in $items) { if ($i.Current.Name -eq $name) { return $i } }
  return $null
}

$ws = FindByName $root 'Workspace'
$ws.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand()
Start-Sleep -Milliseconds 800
$console = FindByName $ws 'Console'
if (-not $console) { throw 'Console item not found under Workspace' }
"Invoking: $($console.Current.Name)"
$console.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
Start-Sleep -Seconds 3

"===== TOP-LEVEL WINDOWS ====="
$desk = [System.Windows.Automation.AutomationElement]::RootElement
foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
  try { if ($w.Current.ProcessId -eq $p.Id) { "WINDOW '$($w.Current.Name)' class=$($w.Current.ClassName) hwnd=$($w.Current.NativeWindowHandle)" } } catch {}
}
