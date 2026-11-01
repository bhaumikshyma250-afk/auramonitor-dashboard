# dashboard/app.py

import streamlit as st
import pandas as pd
import os
import time
import psutil
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AuraMonitor | System Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}
#MainMenu, footer, header {visibility: hidden;}
.glass-card {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 20px 22px;
    margin-bottom: 8px;
}
.metric-label {
    font-size: 12px;
    color: #94a3b8;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #c4b5fd;
}
.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #e0e7ff;
    margin-bottom: 4px;
}
.sub-title {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 24px;
}
.stButton > button {
    background: rgba(239, 68, 68, 0.15) !important;
    border: 1px solid rgba(239, 68, 68, 0.4) !important;
    color: #fca5a5 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

def load_data(query):
    if not DATABASE_URL:
        return pd.DataFrame()
    try:
        import psycopg2
        result = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port,
            sslmode="require",
            connect_timeout=8
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"DB Error: {e}")
        return pd.DataFrame()

def clear_all_logs():
    try:
        import psycopg2
        result = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port,
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute("DELETE FROM activity_logs")
        cur.execute("DELETE FROM network_logs")
        cur.execute("DELETE FROM uptime_logs")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(str(e))
        return False

# Load Data
activity_df = load_data("SELECT * FROM activity_logs ORDER BY id DESC LIMIT 400")
network_df = load_data("SELECT * FROM network_logs ORDER BY id DESC LIMIT 250")
uptime_df = load_data("SELECT * FROM uptime_logs ORDER BY id DESC LIMIT 15")

total_logs = len(activity_df)
total_data = round(network_df['mb_used'].sum(), 2) if not network_df.empty and 'mb_used' in network_df.columns else 0.0
unique_apps = activity_df['app_name'].nunique() if not activity_df.empty and 'app_name' in activity_df.columns else 0

boot = psutil.boot_time()
up_sec = time.time() - boot
uptime_str = f"{int(up_sec // 3600)}h {int((up_sec % 3600) // 60)}m"

# Header
st.markdown('<div class="main-title">◈ AuraMonitor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-time System Intelligence Dashboard • Live</div>', unsafe_allow_html=True)

# Metrics
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="glass-card"><div class="metric-label">Activity Logs</div><div class="metric-value">{total_logs}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="glass-card"><div class="metric-label">Bandwidth (MB)</div><div class="metric-value">{total_data}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="glass-card"><div class="metric-label">Unique Apps</div><div class="metric-value">{unique_apps}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="glass-card"><div class="metric-label">Uptime</div><div class="metric-value">{uptime_str}</div></div>', unsafe_allow_html=True)

st.write("")

# Charts (Streamlit native - stable)
left, right = st.columns(2)

with left:
    st.subheader("App Usage")
    if not activity_df.empty and 'app_name' in activity_df.columns:
        app_sum = activity_df.groupby('app_name')['duration_sec'].sum().sort_values(ascending=False).head(6)
        st.bar_chart(app_sum)
    else:
        st.info("Waiting for activity data...")

with right:
    st.subheader("Bandwidth Stream")
    if not network_df.empty and 'mb_used' in network_df.columns:
        st.line_chart(network_df['mb_used'].tail(50).reset_index(drop=True))
    else:
        st.info("Waiting for network data...")

st.markdown("---")

# Tables
tab1, tab2, tab3 = st.tabs(["Activity Logs", "Network Logs", "Uptime"])

with tab1:
    if not activity_df.empty:
        st.dataframe(activity_df.head(60), use_container_width=True, height=300)
    else:
        st.warning("No activity logs.")

with tab2:
    if not network_df.empty:
        st.dataframe(network_df.head(60), use_container_width=True, height=300)
    else:
        st.warning("No network logs.")

with tab3:
    st.write(f"Current Uptime: **{uptime_str}**")
    if not uptime_df.empty:
        st.dataframe(uptime_df, use_container_width=True)
    else:
        st.warning("No uptime data.")

st.markdown("---")

# Delete Button
st.subheader("Control Panel")
if st.button("🗑️ Clear All Logs", use_container_width=True):
    if clear_all_logs():
        st.success("All logs cleared!")
        time.sleep(1)
        st.rerun()