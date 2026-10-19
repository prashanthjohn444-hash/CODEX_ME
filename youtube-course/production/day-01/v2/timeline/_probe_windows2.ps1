Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$desk = [System.Windows.Automation.AutomationElement]::RootElement
"PID=$($p.Id) MainWindowHandle=$($p.MainWindowHandle)"
"===== TOP-LEVEL WINDOWS (PID) ====="
foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
  try {
    if ($w.Current.ProcessId -eq $p.Id) {
      $r = $w.Current.BoundingRectangle
      "WINDOW '$($w.Current.Name)' class=$($w.Current.ClassName) hwnd=$($w.Current.NativeWindowHandle) L=$([int]$r.Left) T=$([int]$r.Top) W=$([int]$r.Width) H=$([int]$r.Height)"
    }
  } catch {}
}
"===== SEARCH EACH WINDOW FOR ConsoleView / ConsoleEdit ====="
foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
  try {
    if ($w.Current.ProcessId -ne $p.Id) { continue }
    $found = @()
    foreach ($i in $w.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
      $c = $i.Current.ClassName
      if ($c -eq 'Fusion::ConsoleView' -or $c -eq 'Fusion::ConsoleEdit' -or $c -eq 'QTextEdit') {
        $r = $i.Current.BoundingRectangle
        $found += "   $c L=$([int]$r.Left) T=$([int]$r.Top) W=$([int]$r.Width) H=$([int]$r.Height)"
      }
    }
    if ($found.Count -gt 0) { "IN '$($w.Current.Name)':"; $found }
    else { "IN '$($w.Current.Name)': (none)" }
  } catch {}
}
