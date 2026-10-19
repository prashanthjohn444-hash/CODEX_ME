Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
"ROOT class=$($root.Current.ClassName) name='$($root.Current.Name)'"
$items = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)
"descendants=$($items.Count)"
$found = @()
foreach ($i in $items) {
  try {
    $n = $i.Current.Name; $c = $i.Current.ClassName
    if ($c -like '*Console*' -or $n -eq 'Console' -or $n -eq 'Workspace' -or $c -eq 'QMenuBar') {
      $found += "class=$c name='$n' type=$($i.Current.ControlType.ProgrammaticName) hwnd=$($i.Current.NativeWindowHandle)"
    }
  } catch {}
}
$found | Select-Object -First 30
