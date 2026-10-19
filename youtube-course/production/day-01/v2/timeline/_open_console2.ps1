Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$root = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
"root class=$($root.Current.ClassName) name='$($root.Current.Name)'"

function Find-All($scope, $pred) {
  $res = @()
  foreach ($i in $scope.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
    try { if (& $pred $i) { $res += $i } } catch {}
  }
  return $res
}

# is a console already present?
$cv = Find-All $root { param($i) $i.Current.ClassName -eq 'Fusion::ConsoleView' }
"existing ConsoleView count=$($cv.Count)"

if ($cv.Count -eq 0) {
  $ws = Find-All $root { param($i) $i.Current.Name -eq 'Workspace' -and $i.Current.ControlType.ProgrammaticName -eq 'ControlType.MenuItem' }
  "Workspace menu items=$($ws.Count)"
  if ($ws.Count -gt 0) {
    $pat = $ws[0].GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
    $pat.Expand()
    Start-Sleep -Milliseconds 1200
    $desk = [System.Windows.Automation.AutomationElement]::RootElement
    $found = $null
    foreach ($scope in @($ws[0], $desk)) {
      foreach ($i in $scope.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
        try {
          if ($i.Current.Name -eq 'Console' -and $i.Current.ControlType.ProgrammaticName -eq 'ControlType.MenuItem') { $found = $i; break }
        } catch {}
      }
      if ($found) { break }
    }
    if ($found) {
      "invoking Console menu item"
      $found.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
      Start-Sleep -Seconds 3
    } else { "Console menu item not found after expanding Workspace" }
  }
}

Start-Sleep -Seconds 1
$root2 = [System.Windows.Automation.AutomationElement]::FromHandle((Get-Process Resolve).MainWindowHandle)
$cv2 = Find-All $root2 { param($i) $i.Current.ClassName -eq 'Fusion::ConsoleView' }
"ConsoleView now=$($cv2.Count)"
foreach ($c in $cv2) {
  "  console class=$($c.Current.ClassName) hwnd=$($c.Current.NativeWindowHandle)"
  $kids = Find-All $c { param($i) $i.Current.ClassName -eq 'Fusion::ConsoleEdit' -or $i.Current.ClassName -eq 'QTextEdit' }
  foreach ($k in $kids) { "     child cls=$($k.Current.ClassName)" }
}
