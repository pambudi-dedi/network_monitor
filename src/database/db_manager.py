"""
Database Manager untuk Network Monitor
"""
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json

from config.config import DATABASE_PATH

class DatabaseManager:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DATABASE_PATH
        self.logger = logging.getLogger(__name__)
        self.init_database()
    
    def init_database(self):
        """Initialize database dengan tabel yang diperlukan"""
        try:
            # Pastikan direktori logs ada
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabel untuk menyimpan log koneksi
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS network_connections (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        source_ip TEXT NOT NULL,
                        dest_ip TEXT NOT NULL,
                        dest_port INTEGER,
                        protocol TEXT,
                        dest_domain TEXT,
                        packet_size INTEGER,
                        connection_type TEXT,
                        country TEXT,
                        is_suspicious BOOLEAN DEFAULT 0,
                        raw_data TEXT
                    )
                ''')
                
                # Tabel untuk statistik harian
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS daily_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE UNIQUE,
                        total_connections INTEGER DEFAULT 0,
                        unique_domains INTEGER DEFAULT 0,
                        total_data_mb REAL DEFAULT 0,
                        suspicious_connections INTEGER DEFAULT 0,
                        top_domains TEXT
                    )
                ''')
                
                # Tabel untuk alert
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        alert_type TEXT NOT NULL,
                        message TEXT NOT NULL,
                        severity TEXT DEFAULT 'INFO',
                        is_resolved BOOLEAN DEFAULT 0
                    )
                ''')
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    def insert_connection(self, connection_data: Dict) -> bool:
        """Insert data koneksi baru ke database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO network_connections 
                    (source_ip, dest_ip, dest_port, protocol, dest_domain, 
                     packet_size, connection_type, country, is_suspicious, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    connection_data.get('source_ip'),
                    connection_data.get('dest_ip'),
                    connection_data.get('dest_port'),
                    connection_data.get('protocol'),
                    connection_data.get('dest_domain'),
                    connection_data.get('packet_size'),
                    connection_data.get('connection_type'),
                    connection_data.get('country'),
                    connection_data.get('is_suspicious', False),
                    json.dumps(connection_data.get('raw_data', {}))
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error inserting connection: {e}")
            return False
    
    def get_recent_connections(self, limit: int = 100) -> List[Dict]:
        """Ambil koneksi terbaru"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM network_connections 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error getting recent connections: {e}")
            return []
    
    def get_top_domains(self, limit: int = 10) -> List[Dict]:
        """Ambil domain yang paling sering diakses"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT dest_domain, COUNT(*) as access_count,
                           MAX(timestamp) as last_access
                    FROM network_connections 
                    WHERE dest_domain IS NOT NULL AND dest_domain != ''
                    GROUP BY dest_domain
                    ORDER BY access_count DESC
                    LIMIT ?
                ''', (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error getting top domains: {e}")
            return []
    
    def get_connection_stats(self, hours: int = 24) -> Dict:
        """Ambil statistik koneksi dalam beberapa jam terakhir"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total koneksi
                cursor.execute('''
                    SELECT COUNT(*) FROM network_connections 
                    WHERE timestamp >= datetime('now', '-{} hours')
                '''.format(hours))
                total_connections = cursor.fetchone()[0]
                
                # Koneksi mencurigakan
                cursor.execute('''
                    SELECT COUNT(*) FROM network_connections 
                    WHERE timestamp >= datetime('now', '-{} hours') 
                    AND is_suspicious = 1
                '''.format(hours))
                suspicious_connections = cursor.fetchone()[0]
                
                # Domain unik
                cursor.execute('''
                    SELECT COUNT(DISTINCT dest_domain) FROM network_connections 
                    WHERE timestamp >= datetime('now', '-{} hours')
                    AND dest_domain IS NOT NULL AND dest_domain != ''
                '''.format(hours))
                unique_domains = cursor.fetchone()[0]
                
                # Total data
                cursor.execute('''
                    SELECT SUM(packet_size) FROM network_connections 
                    WHERE timestamp >= datetime('now', '-{} hours')
                '''.format(hours))
                total_data = cursor.fetchone()[0] or 0
                
                return {
                    'total_connections': total_connections,
                    'suspicious_connections': suspicious_connections,
                    'unique_domains': unique_domains,
                    'total_data_mb': round(total_data / (1024 * 1024), 2)
                }
                
        except Exception as e:
            self.logger.error(f"Error getting connection stats: {e}")
            return {}
    
    def insert_alert(self, alert_type: str, message: str, severity: str = 'INFO') -> bool:
        """Insert alert baru"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO alerts (alert_type, message, severity)
                    VALUES (?, ?, ?)
                ''', (alert_type, message, severity))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error inserting alert: {e}")
            return False
    
    def get_recent_alerts(self, limit: int = 50) -> List[Dict]:
        """Ambil alert terbaru"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM alerts 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error getting recent alerts: {e}")
            return []
