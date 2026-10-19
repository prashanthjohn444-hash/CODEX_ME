Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32 {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
"@
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$desk = [System.Windows.Automation.AutomationElement]::RootElement
# dismiss any transient popup dialogs (search popup etc.)
foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
  try {
    if ($w.Current.ProcessId -eq $p.Id -and ($w.Current.ClassName -eq 'UiSearchPopupDialog')) {
      $h = [IntPtr][int]$w.Current.NativeWindowHandle
      [void][W32]::SetForegroundWindow($h)
      Start-Sleep -Milliseconds 500
      [System.Windows.Forms.SendKeys]::SendWait('{ESC}')
      Start-Sleep -Milliseconds 700
      "Dismissed $($w.Current.ClassName)"
    }
  } catch {}
}
foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
  try { if ($w.Current.ProcessId -eq $p.Id) { "WINDOW '$($w.Current.Name)' class=$($w.Current.ClassName) hwnd=$($w.Current.NativeWindowHandle)" } } catch {}
}
