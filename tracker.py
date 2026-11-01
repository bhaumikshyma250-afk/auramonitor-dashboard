# background_agent/tracker.py

import time
from background_agent.app_monitor import get_active_window_details
from background_agent.network_monitor import NetworkTracker
from background_agent.uptime_monitor import get_system_boot_time
from database.db_handler import log_activity, log_network, log_uptime, init_db

def start_background_tracker():
    print("🚀 AuraMonitor Tracker চালু হচ্ছে...")

    try:
        init_db()
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return

    try:
        boot_time = get_system_boot_time()
        print(f"💻 System Boot Time: {boot_time}")
        log_uptime(boot_time=boot_time)
    except Exception as e:
        print(f"⚠️ Uptime Log Error: {e}")

    network_tracker = NetworkTracker()
    print("✅ Tracker এক্টিভ... (বন্ধ করতে Ctrl + C চাপুন)")

    try:
        while True:
            try:
                # ১. Active App ট্র্যাক
                app_name, window_title = get_active_window_details()
                log_activity(app_name, window_title, duration_sec=2)

                # ২. Network ট্র্যাক
                sent, recv, mb_used = network_tracker.get_network_usage()
                log_network(sent, recv, mb_used)

                print(f"[Live] App: {app_name} | Data: {mb_used} MB")

            except Exception as inner_error:
                print(f"⚠️ Error: {inner_error}")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n🛑 Tracker বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    start_background_tracker()