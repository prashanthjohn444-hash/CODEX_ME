Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Fy {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern void SwitchToThisWindow(IntPtr h, bool alt);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
}
"@
$p = Get-Process Resolve -ErrorAction Stop
$h = [IntPtr]$p.MainWindowHandle
"target hwnd=$h iconic=$([Fy]::IsIconic($h))"
if ([Fy]::IsIconic($h)) { [void][Fy]::ShowWindow($h, 9); Start-Sleep -Milliseconds 700 }
[Fy]::SwitchToThisWindow($h, $true)
Start-Sleep -Milliseconds 900
"fg1=$([Fy]::GetForegroundWindow()) match=$([Fy]::GetForegroundWindow() -eq $h)"
if ([Fy]::GetForegroundWindow() -ne $h) {
  [void][Fy]::SetForegroundWindow($h)
  Start-Sleep -Milliseconds 700
  "fg2=$([Fy]::GetForegroundWindow()) match=$([Fy]::GetForegroundWindow() -eq $h)"
}
