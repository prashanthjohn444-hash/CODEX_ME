Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Ka {
  [DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint flags);
}
"@
# ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED: keep the display up
# so the idle screen saver cannot lock the session while the build runs.
for ($i = 0; $i -lt 180; $i++) {
  [void][Ka]::SetThreadExecutionState([uint32]0x80000003)
  Start-Sleep -Seconds 20
}
