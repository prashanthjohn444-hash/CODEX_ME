Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
function FindByName($scope, $name) {
  foreach ($i in $scope.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) { if ($i.Current.Name -eq $name) { return $i } }
  return $null
}
$ws = FindByName $root 'Workspace'
if (-not $ws) { throw 'no Workspace menu' }
$ws.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand()
Start-Sleep -Milliseconds 900
$scripts = FindByName $ws 'Scripts'
if ($scripts) {
  "Scripts menu found; expanding"
  $scripts.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand()
  Start-Sleep -Milliseconds 1200
  foreach ($i in $scripts.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
    if ($i.Current.ControlType.ProgrammaticName -eq 'ControlType.MenuItem') { "SCRIPT_ITEM '$($i.Current.Name)'" }
  }
} else { "no Scripts menu" }
$ws.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Collapse()
