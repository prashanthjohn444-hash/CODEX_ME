Add-Type -AssemblyName Microsoft.VisualBasic
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Fg2 {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SystemParametersInfo(uint a, uint b, IntPtr c, uint d);
}
"@
# allow our background process to steal focus
[void][Fg2]::SystemParametersInfo(0x2001, 0, [IntPtr]::Zero, 2)
$p = Get-Process Resolve -ErrorAction Stop
$h = [IntPtr]$p.MainWindowHandle
$fg = [Fg2]::GetForegroundWindow()
$fgTid = 0; [void][Fg2]::GetWindowThreadProcessId($fg, [ref]$fgTid)
$cur = [Fg2]::GetCurrentThreadId()
[void][Fg2]::AttachThreadInput($cur, $fgTid, $true)
[void][Fg2]::ShowWindow($h, 9)
[void][Fg2]::BringWindowToTop($h)
$ok = [Fg2]::SetForegroundWindow($h)
[void][Fg2]::AttachThreadInput($cur, $fgTid, $false)
Start-Sleep -Milliseconds 900
"attached=$ok nowFg=$([Fg2]::GetForegroundWindow()) target=$h match=$([Fg2]::GetForegroundWindow() -eq $h)"
