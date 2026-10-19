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
$cinema = $null
foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
  try { if ($w.Current.ProcessId -eq $p.Id -and $w.Current.ClassName -eq 'UiCinemaViewerDialog') { $cinema = $w } } catch {}
}
if ($cinema) {
  $h = [IntPtr][int]$cinema.Current.NativeWindowHandle
  "Found cinema viewer hwnd=$h - sending ESC"
  [void][W32]::SetForegroundWindow($h)
  Start-Sleep -Milliseconds 700
  [System.Windows.Forms.SendKeys]::SendWait('{ESC}')
  Start-Sleep -Seconds 2
} else { "No cinema viewer found." }
"===== WINDOWS AFTER ====="
foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
  try { if ($w.Current.ProcessId -eq $p.Id) { "WINDOW '$($w.Current.Name)' class=$($w.Current.ClassName) hwnd=$($w.Current.NativeWindowHandle)" } } catch {}
}
