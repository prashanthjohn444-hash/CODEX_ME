Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Fx {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern void SwitchToThisWindow(IntPtr h, bool alt);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
}
"@
$p = Get-Process Resolve -ErrorAction Stop
$h = [IntPtr]$p.MainWindowHandle
"target hwnd=$h iconic=$([Fx]::IsIconic($h))"

# 1) SwitchToThisWindow
[Fx]::SwitchToThisWindow($h, $true)
Start-Sleep -Milliseconds 900
"after SwitchToThisWindow fg=$([Fx]::GetForegroundWindow()) match=$([Fx]::GetForegroundWindow() -eq $h)"

# 2) minimize/restore trick
if ([Fx]::GetForegroundWindow() -ne $h) {
  [void][Fx]::ShowWindow($h, 6); Start-Sleep -Milliseconds 500   # SW_MINIMIZE
  [void][Fx]::ShowWindow($h, 9); Start-Sleep -Milliseconds 400   # SW_RESTORE
  [void][Fx]::BringWindowToTop($h)
  [void][Fx]::SetForegroundWindow($h)
  Start-Sleep -Milliseconds 900
  "after min/restore fg=$([Fx]::GetForegroundWindow()) match=$([Fx]::GetForegroundWindow() -eq $h)"
}

# 3) taskbar button invoke via UIA
if ([Fx]::GetForegroundWindow() -ne $h) {
  Add-Type -AssemblyName UIAutomationClient
  Add-Type -AssemblyName UIAutomationTypes
  $all = [System.Windows.Automation.Condition]::TrueCondition
  $desk = [System.Windows.Automation.AutomationElement]::RootElement
  $tray = $null
  foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
    try { if ($w.Current.ClassName -eq 'Shell_TrayWnd') { $tray = $w; break } } catch {}
  }
  if ($tray) {
    foreach ($b in $tray.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
      try {
        $nm = $b.Current.Name
        if ($nm -and ($nm -match 'Resolve|Project Manager')) {
          "taskbar button: '$nm' type=$($b.Current.ControlType.ProgrammaticName)"
          $ip = $null
          if ($b.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$ip)) { $ip.Invoke() }
          elseif ($b.TryGetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern, [ref]$ip)) { $ip.Select() }
          Start-Sleep -Milliseconds 1200
          "after taskbar invoke fg=$([Fx]::GetForegroundWindow())"
        }
      } catch {}
    }
  } else { "no taskbar found" }
}
"FINAL fg=$([Fx]::GetForegroundWindow()) target=$h"
