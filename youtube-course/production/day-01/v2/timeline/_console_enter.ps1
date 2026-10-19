param([string]$Marker, [int]$TimeoutSec = 30)
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32 {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern IntPtr SetFocus(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern IntPtr GetFocus();
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
}
"@
$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$desk = [System.Windows.Automation.AutomationElement]::RootElement
$cr = $null
foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
  try { if ($w.Current.ProcessId -eq $p.Id -and $w.Current.ClassName -eq 'Fusion::ConsoleView') { $cr = $w } } catch {}
}
if (-not $cr) { throw 'ConsoleView top-level window not found' }
$h = [IntPtr][int]$cr.Current.NativeWindowHandle
"ConsoleView hwnd=$h"

# Attach thread input trick to reliably set foreground
$fg = [W32]::GetForegroundWindow()
$fpid = 0; $ftid = [W32]::GetWindowThreadProcessId($fg, [ref]$fpid)
$tpid = 0; $ttid = [W32]::GetWindowThreadProcessId($h, [ref]$tpid)
$cur = [W32]::GetCurrentThreadId()
[void][W32]::AttachThreadInput($cur, $ttid, $true)
[void][W32]::BringWindowToTop($h)
[void][W32]::SetForegroundWindow($h)
[void][W32]::SetFocus($h)
[void][W32]::AttachThreadInput($cur, $ttid, $false)
Start-Sleep -Milliseconds 700
"FOREGROUND_NOW=" + ([W32]::GetForegroundWindow() -eq $h)

# Ensure the console input widget has keyboard focus
foreach ($i in $cr.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
  if ($i.Current.ClassName -eq 'Fusion::ConsoleEdit') { $i.SetFocus(); "SetFocus on ConsoleEdit"; break }
}
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait('{ENTER}')

$out = $null
foreach ($i in $cr.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) { if ($i.Current.ClassName -eq 'QTextEdit') { $out = $i; break } }
$deadline = (Get-Date).AddSeconds($TimeoutSec); $found = $false
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Seconds 2
  $t = $out.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern).DocumentRange.GetText(400000)
  if ($t -match [regex]::Escape($Marker)) { $found = $true; break }
}
$t = $out.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern).DocumentRange.GetText(400000)
"ENTER_MARKER_FOUND=$found"
$t.Substring([Math]::Max(0, $t.Length - 1500))
