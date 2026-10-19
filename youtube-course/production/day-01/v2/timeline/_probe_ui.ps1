Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
"PID=$($p.Id) TITLE=$($p.MainWindowTitle)"
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
"ROOT Name='$($root.Current.Name)' Class='$($root.Current.ClassName)'"
$all = [System.Windows.Automation.Condition]::TrueCondition
function Dump($el, $depth, $maxDepth) {
  if ($depth -gt $maxDepth) { return }
  $kids = $el.FindAll([System.Windows.Automation.TreeScope]::Children, $all)
  foreach ($k in $kids) {
    $n = $k.Current.Name
    if ($n.Length -gt 90) { $n = $n.Substring(0,90) }
    ("{0}{1} | {2} | '{3}'" -f ('  ' * $depth), $k.Current.ControlType.ProgrammaticName, $k.Current.ClassName, $n)
    Dump $k ($depth+1) $maxDepth
  }
}
Dump $root 0 2
"===== MENUBAR ITEMS ====="
$menus = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all) | Where-Object { $_.Current.ControlType.ProgrammaticName -eq 'ControlType.MenuItem' }
foreach ($m in $menus) { "MENUITEM '$($m.Current.Name)' id=$($m.Current.AutomationId)" }
