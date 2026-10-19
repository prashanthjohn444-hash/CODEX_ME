Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
$items = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)
"TOTAL DESCENDANTS: $($items.Count)"
foreach ($i in $items) {
  $n = $i.Current.Name
  $ct = $i.Current.ControlType.ProgrammaticName
  try { $ct = $ct.Replace('ControlType.','') } catch {}
  if ($n -match 'Console|Py3|Lua|Python|Exec|Input|Command') {
    if ($n.Length -gt 80) { $n = $n.Substring(0,80) }
    "HIT | $ct | class=$($i.Current.ClassName) | '$n'"
  }
}
"===== EDIT / DOCUMENT CONTROLS ====="
foreach ($i in $items) {
  $ct = $i.Current.ControlType.ProgrammaticName
  if ($ct -match 'Edit|Document|Text$') {
    $n = $i.Current.Name
    if ($n.Length -gt 60) { $n = $n.Substring(0,60) }
    "EDIT | $ct | class=$($i.Current.ClassName) | '$n'"
  }
}
