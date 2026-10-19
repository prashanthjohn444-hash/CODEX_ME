Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
$cv = $null
foreach ($i in $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
  if ($i.Current.ClassName -eq 'Fusion::ConsoleView') { $cv = $i; break }
}
if (-not $cv) { throw 'ConsoleView not found' }
"CONSOLEVIEW rect: " + $cv.Current.BoundingRectangle.ToString()
$items = $cv.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)
"DESCENDANTS: $($items.Count)"
foreach ($i in $items) {
  $n = $i.Current.Name; if ($n.Length -gt 60) { $n = $n.Substring(0,60) }
  $r = $i.Current.BoundingRectangle
  $ct = $i.Current.ControlType.ProgrammaticName.Replace('ControlType.','')
  "  $ct | class=$($i.Current.ClassName) | aid='$($i.Current.AutomationId)' | '$n' | L=$([int]$r.Left) T=$([int]$r.Top) W=$([int]$r.Width) H=$([int]$r.Height)"
}
"--- QTextEdit output value ---"
foreach ($i in $items) {
  if ($i.Current.ClassName -eq 'QTextEdit') {
    $tp = $null
    if ($i.TryGetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern, [ref]$tp)) {
      "TEXT: '" + $tp.DocumentRange.GetText(4000) + "'"
    }
  }
}
