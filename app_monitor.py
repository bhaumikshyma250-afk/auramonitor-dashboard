# background_agent/app_monitor.py

import win32gui
import win32process
import psutil

def get_active_window_details():
    """
    বর্তমানে কোন অ্যাপ খোলা আছে সেটা বের করে।
    """
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return "Unknown", "No Active Window"

        window_title = win32gui.GetWindowText(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        app_name = process.name()

        return app_name, window_title if window_title else "Desktop / Idle"
    except Exception:
        return "System", "Unknown Task"