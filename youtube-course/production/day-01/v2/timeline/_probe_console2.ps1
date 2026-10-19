Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)

$edit = $null
foreach ($i in $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
  if ($i.Current.ClassName -eq 'Fusion::ConsoleEdit') { $edit = $i; break }
}
if (-not $edit) { throw 'ConsoleEdit not found' }
"PATTERNS:"
foreach ($pt in $edit.GetSupportedPatterns()) { "  $($pt.ProgrammaticName)" }
$r = $edit.Current.BoundingRectangle
"BOUNDS: L=$($r.Left) T=$($r.Top) W=$($r.Width) H=$($r.Height)"
"Enabled=$($edit.Current.IsEnabled) KeyboardFocusable=$($edit.Current.IsKeyboardFocusable)"
"VALUE: '" + $edit.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value + "'"

$walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
$node = $edit
for ($d=0; $d -lt 4; $d++) {
  $node = $walker.GetParent($node)
  if (-not $node) { break }
  "PARENT${d}: $($node.Current.ControlType.ProgrammaticName) class=$($node.Current.ClassName) name='$($node.Current.Name)'"
  $kids = $node.FindAll([System.Windows.Automation.TreeScope]::Children, $all)
  "   siblings/children ($($kids.Count)):"
  foreach ($k in $kids) {
    $n = $k.Current.Name; if ($n.Length -gt 60) { $n = $n.Substring(0,60) }
    "     - $($k.Current.ControlType.ProgrammaticName) class=$($k.Current.ClassName) '$n'"
  }
}
