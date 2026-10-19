param(
  [Parameter(Mandatory=$true)][string]$CodeFile,
  [Parameter(Mandatory=$true)][string]$Marker,
  [int]$TimeoutSec = 900,
  [switch]$NoSubmit
)
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
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
}
"@

$p = Get-Process Resolve -ErrorAction Stop
$all = [System.Windows.Automation.Condition]::TrueCondition
$desk = [System.Windows.Automation.AutomationElement]::RootElement

function Get-ConsoleWin {
  foreach ($w in $desk.FindAll([System.Windows.Automation.TreeScope]::Children, $all)) {
    try { if ($w.Current.ProcessId -eq $p.Id -and $w.Current.ClassName -eq 'Fusion::ConsoleView') { return $w } } catch {}
  }
  $main = [System.Windows.Automation.AutomationElement]::FromHandle($p.MainWindowHandle)
  foreach ($i in $main.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
    if ($i.Current.ClassName -eq 'Fusion::ConsoleView') { return $i }
  }
  return $null
}
function Get-OutText($cw) {
  foreach ($i in $cw.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
    if ($i.Current.ClassName -eq 'QTextEdit') {
      $tp = $null
      if ($i.TryGetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern, [ref]$tp)) {
        return $tp.DocumentRange.GetText(400000)
      }
    }
  }
  return $null
}

$cw = Get-ConsoleWin
if (-not $cw) { throw 'Console (Fusion::ConsoleView) not found. Open Workspace > Console.' }
$cwHwnd = [IntPtr][int]$cw.Current.NativeWindowHandle
if ($cwHwnd -eq [IntPtr]::Zero) { $cwHwnd = [IntPtr][int]$p.MainWindowHandle }

if (-not $NoSubmit) {
  $edit = $null
  foreach ($i in $cw.FindAll([System.Windows.Automation.TreeScope]::Descendants, $all)) {
    if ($i.Current.ClassName -eq 'Fusion::ConsoleEdit') { $edit = $i; break }
  }
  if (-not $edit) { throw 'Console input not found' }
  $vp = $edit.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
  if ($vp.Current.Value -ne '') { $vp.SetValue(''); Start-Sleep -Milliseconds 250 }
  $code = ((Get-Content -Raw -LiteralPath $CodeFile).Trim() -split "`r?`n" | ForEach-Object { $_.Trim() }) -join ' '
  Write-Output "SUBMIT: $code"
  $vp.SetValue($code)
  Start-Sleep -Milliseconds 1500
  $edit.SetFocus()
  Start-Sleep -Milliseconds 400
  $ttid = 0; [void][W32]::GetWindowThreadProcessId($cwHwnd, [ref]$ttid)
  $cur = [W32]::GetCurrentThreadId()
  [void][W32]::AttachThreadInput($cur, $ttid, $true)
  [void][W32]::BringWindowToTop($cwHwnd)
  [void][W32]::SetForegroundWindow($cwHwnd)
  [void][W32]::SetFocus($cwHwnd)
  [void][W32]::AttachThreadInput($cur, $ttid, $false)
  Start-Sleep -Milliseconds 500
  Write-Output ("FOREGROUND_IS_CONSOLE=" + ([W32]::GetForegroundWindow() -eq $cwHwnd))
  $edit.SetFocus()
  Start-Sleep -Milliseconds 300
  [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
}

$deadline = (Get-Date).AddSeconds($TimeoutSec)
$found = $false
$last = ''
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Seconds 5
  $cwNow = Get-ConsoleWin
  $t = Get-OutText $cwNow
  if ($t) {
    $last = $t
    if ($t -match [regex]::Escape($Marker)) { $found = $true; break }
  }
}
Write-Output "MARKER_FOUND=$found"
Write-Output "===== CONSOLE OUTPUT TAIL ====="
if ($last) { Write-Output $last.Substring([Math]::Max(0, $last.Length - 9000)) }
