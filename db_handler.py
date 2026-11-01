# database/db_handler.py

import os
from datetime import datetime
from urllib.parse import urlparse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL পাওয়া যায়নি! .env ফাইল চেক করুন।")
    
    result = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
        cursor_factory=RealDictCursor,
        sslmode="require"
    )
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uptime_logs (
                id SERIAL PRIMARY KEY,
                boot_time TEXT NOT NULL,
                shutdown_time TEXT,
                session_duration_sec REAL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id SERIAL PRIMARY KEY,
                timestamp TEXT NOT NULL,
                app_name TEXT NOT NULL,
                window_title TEXT,
                duration_sec INTEGER DEFAULT 2
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS network_logs (
                id SERIAL PRIMARY KEY,
                timestamp TEXT NOT NULL,
                bytes_sent BIGINT NOT NULL,
                bytes_recv BIGINT NOT NULL,
                mb_used REAL NOT NULL
            );
        """)
        conn.commit()
        print("✅ Database tables ready!")

def log_activity(app_name, window_title, duration_sec=2):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO activity_logs (timestamp, app_name, window_title, duration_sec) VALUES (%s, %s, %s, %s)",
            (timestamp, app_name, window_title, duration_sec)
        )
        conn.commit()

def log_network(bytes_sent, bytes_recv, mb_used):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO network_logs (timestamp, bytes_sent, bytes_recv, mb_used) VALUES (%s, %s, %s, %s)",
            (timestamp, bytes_sent, bytes_recv, mb_used)
        )
        conn.commit()

def log_uptime(boot_time, shutdown_time=None, duration=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO uptime_logs (boot_time, shutdown_time, session_duration_sec) VALUES (%s, %s, %s)",
            (boot_time, shutdown_time, duration)
        )
        conn.commit()