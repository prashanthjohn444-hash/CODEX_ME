Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
"MAINWINDOW name='$($root.Current.Name)'"
$cv = $null
foreach ($i in $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
  if ($i.Current.ClassName -eq 'Fusion::ConsoleView') { $cv = $i; break }
}
if (-not $cv) { "NO ConsoleView"; exit }
"ConsoleView rect: " + $cv.Current.BoundingRectangle.ToString()
$items = $cv.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)
"DESC: $($items.Count)"
foreach ($i in $items) {
  $n = $i.Current.Name; if ($n.Length -gt 40) { $n = $n.Substring(0,40) }
  $r = $i.Current.BoundingRectangle
  $ct = $i.Current.ControlType.ProgrammaticName.Replace('ControlType.','')
  $pats = ($i.GetSupportedPatterns() | ForEach-Object { $_.ProgrammaticName.Split('.')[0] }) -join ','
  "  $ct | $($i.Current.ClassName) | '$n' | L=$([int]$r.Left) T=$([int]$r.Top) W=$([int]$r.Width) H=$([int]$r.Height) | $pats"
}
"ALL QTextEdit in main window:"
$n = 0
foreach ($i in $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
  if ($i.Current.ClassName -eq 'QTextEdit') { $n++; "  #$n rect=" + $i.Current.BoundingRectangle.ToString() }
}
"count=$n"
