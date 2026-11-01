# background_agent/uptime_monitor.py

import psutil
from datetime import datetime

def get_system_boot_time():
    """
    কম্পিউটার কখন চালু হয়েছিল সেটা বলে।
    """
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return boot_time