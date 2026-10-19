Add-Type -AssemblyName UIAutomationClient
$p = Get-Process Resolve -ErrorAction Stop
$r = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
$all = [System.Windows.Automation.Condition]::TrueCondition
$children = $r.FindAll([System.Windows.Automation.TreeScope]::Children, $all)
$timeline = $children | Where-Object { $_.Current.ControlType.ProgrammaticName -eq 'ControlType.MenuItem' -and $_.Current.Name -like 'Timeline*' } | Select-Object -First 1
if (-not $timeline) {
  $menu = $children | Where-Object { $_.Current.ControlType.ProgrammaticName -eq 'ControlType.MenuBar' } | Select-Object -First 1
  if (-not $menu) { throw 'Neither a Resolve menu bar nor an Import popup was exposed.' }
  $file = $menu.FindAll([System.Windows.Automation.TreeScope]::Children, $all) | Where-Object { $_.Current.Name -eq 'File' } | Select-Object -First 1
  $file.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand()
  $import = $file.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all) | Where-Object { $_.Current.Name -eq 'Import' } | Select-Object -First 1
  $import.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand()
  $timeline = $import.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all) | Where-Object { $_.Current.Name -like 'Timeline*' } | Select-Object -First 1
}
if (-not $timeline) { throw 'Resolve did not expose Import / Timeline.' }
Write-Output ('Invoking menu item: ' + $timeline.Current.Name)
$timeline.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
