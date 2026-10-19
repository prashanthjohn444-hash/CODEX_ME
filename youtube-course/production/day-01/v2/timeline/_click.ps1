param([int]$X, [int]$Y, [int]$Clicks = 1, [int]$DelayMs = 120)
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Ms {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
"@
[void][Ms]::SetCursorPos($X, $Y)
Start-Sleep -Milliseconds 250
for ($i = 0; $i -lt $Clicks; $i++) {
  [Ms]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)   # LEFTDOWN
  Start-Sleep -Milliseconds 40
  [Ms]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)   # LEFTUP
  if ($i -lt $Clicks - 1) { Start-Sleep -Milliseconds $DelayMs }
}
"clicked $X,$Y x$Clicks fg=$([Ms]::GetForegroundWindow())"
