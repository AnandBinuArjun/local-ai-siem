import subprocess
import json
import socket
from typing import Generator
from aisiem.storage.models import RawLog

def get_hostname():
    return socket.gethostname()

def collect_windows_events(log_name="Security", max_events=10) -> Generator[RawLog, None, None]:
    """
    Collects Windows Event Logs using PowerShell.
    Note: 'Security' logs usually require Administrator privileges.
    """
    cmd = [
        "powershell", "-Command",
        f"Get-WinEvent -LogName {log_name} -MaxEvents {max_events} -ErrorAction SilentlyContinue | Select-Object -Property * | ConvertTo-Json -Depth 1"
    ]
    try:
        # encoding='utf-8' might fail if PS uses different encoding, but let's try
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # If Security fails (e.g. access denied), try Application as fallback for demo
            if log_name == "Security":
                print(f"Failed to read Security logs (Access Denied?). Trying Application logs.")
                yield from collect_windows_events("Application", max_events)
                return
            else:
                print(f"Error running PowerShell: {result.stderr}")
                return

        if not result.stdout.strip():
            return

        try:
            events = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("Failed to decode JSON from PowerShell output")
            return

        if not isinstance(events, list):
            events = [events]
        
        hostname = get_hostname()
        
        for event in events:
            yield RawLog(
                source=f"win.eventlog.{log_name.lower()}",
                raw=json.dumps(event),
                host=hostname
            )
            
    except Exception as e:
        print(f"Error collecting {log_name}: {e}")

if __name__ == "__main__":
    print("Collecting events...")
    for log in collect_windows_events(max_events=5):
        print(f"Got log from {log.source} at {log.ingest_ts}")
