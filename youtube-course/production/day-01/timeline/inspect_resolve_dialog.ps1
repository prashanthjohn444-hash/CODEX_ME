Add-Type -AssemblyName UIAutomationClient
Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
public static class WinChildren {
  public delegate bool Callback(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr parent, Callback cb, IntPtr extra);
  [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetClassName(IntPtr h, StringBuilder b, int n);
  [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder b, int n);
  [DllImport("user32.dll")] public static extern int GetDlgCtrlID(IntPtr h);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
}
'@
$r = [System.Windows.Automation.AutomationElement]::FromHandle((Get-Process Resolve).MainWindowHandle)
$pane = $r.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition) | Select-Object -First 1
Write-Output ("UI child: " + $pane.Current.Name + " hwnd=" + $pane.Current.NativeWindowHandle)
$cb = [WinChildren+Callback] {
  param($h,$l)
  $cls = New-Object System.Text.StringBuilder 100
  $txt = New-Object System.Text.StringBuilder 400
  [void][WinChildren]::GetClassName($h,$cls,100)
  [void][WinChildren]::GetWindowText($h,$txt,400)
  if ([WinChildren]::IsWindowVisible($h)) { Write-Output ("$h | " + $cls.ToString() + " | " + [WinChildren]::GetDlgCtrlID($h) + " | " + $txt.ToString()) }
  return $true
}
[void][WinChildren]::EnumChildWindows([IntPtr]$pane.Current.NativeWindowHandle,$cb,[IntPtr]::Zero)
