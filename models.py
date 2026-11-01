# database/models.py

CREATE_UPTIME_TABLE = """
CREATE TABLE IF NOT EXISTS uptime_logs (
    id SERIAL PRIMARY KEY,
    boot_time TEXT NOT NULL,
    shutdown_time TEXT,
    session_duration_sec REAL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

CREATE_ACTIVITY_TABLE = """
CREATE TABLE IF NOT EXISTS activity_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    app_name TEXT NOT NULL,
    window_title TEXT,
    duration_sec INTEGER DEFAULT 2
);
"""

CREATE_NETWORK_TABLE = """
CREATE TABLE IF NOT EXISTS network_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    bytes_sent BIGINT NOT NULL,
    bytes_recv BIGINT NOT NULL,
    mb_used REAL NOT NULL
);
"""