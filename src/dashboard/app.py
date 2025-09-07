"""
Web Dashboard untuk Network Monitor
"""
from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime, timedelta
import logging

from config.config import DASHBOARD_CONFIG
from src.database.db_manager import DatabaseManager
from src.monitor.network_monitor import NetworkMonitor

app = Flask(__name__)
app.secret_key = 'network_monitor_secret_key'

# Initialize components
db_manager = DatabaseManager()
network_monitor = NetworkMonitor()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """API untuk mendapatkan statistik"""
    try:
        stats = db_manager.get_connection_stats(hours=24)
        monitoring_stats = network_monitor.get_monitoring_stats()
        
        return jsonify({
            'success': True,
            'data': {
                'connection_stats': stats,
                'monitoring_stats': monitoring_stats
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/connections')
def get_connections():
    """API untuk mendapatkan koneksi terbaru"""
    try:
        limit = request.args.get('limit', 50, type=int)
        connections = db_manager.get_recent_connections(limit)
        
        return jsonify({
            'success': True,
            'data': connections
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/domains')
def get_domains():
    """API untuk mendapatkan top domains"""
    try:
        limit = request.args.get('limit', 10, type=int)
        domains = db_manager.get_top_domains(limit)
        
        return jsonify({
            'success': True,
            'data': domains
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alerts')
def get_alerts():
    """API untuk mendapatkan alerts"""
    try:
        limit = request.args.get('limit', 20, type=int)
        alerts = db_manager.get_recent_alerts(limit)
        
        return jsonify({
            'success': True,
            'data': alerts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/network-info')
def get_network_info():
    """API untuk mendapatkan informasi network"""
    try:
        network_info = network_monitor.get_network_info()
        
        return jsonify({
            'success': True,
            'data': network_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring():
    """API untuk memulai monitoring"""
    try:
        interface = request.json.get('interface', 'eth0')
        network_monitor.interface = interface
        network_monitor.start_monitoring()
        
        return jsonify({
            'success': True,
            'message': f'Monitoring started on interface {interface}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stop-monitoring', methods=['POST'])
def stop_monitoring():
    """API untuk menghentikan monitoring"""
    try:
        network_monitor.stop_monitoring()
        
        return jsonify({
            'success': True,
            'message': 'Monitoring stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/connection-chart')
def get_connection_chart():
    """API untuk data chart koneksi per jam"""
    try:
        # Get connections for last 24 hours grouped by hour
        import sqlite3
        with sqlite3.connect(db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
                FROM network_connections 
                WHERE timestamp >= datetime('now', '-24 hours')
                GROUP BY strftime('%H', timestamp)
                ORDER BY hour
            ''')
            
            data = cursor.fetchall()
            
        # Format data for chart
        chart_data = []
        for hour, count in data:
            chart_data.append({
                'hour': f"{hour}:00",
                'connections': count
            })
        
        return jsonify({
            'success': True,
            'data': chart_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(
        host=DASHBOARD_CONFIG['host'],
        port=DASHBOARD_CONFIG['port'],
        debug=DASHBOARD_CONFIG['debug']
    )
