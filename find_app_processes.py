#!/usr/bin/env python3
"""
Find Application Processes
Script untuk menemukan nama proses aplikasi yang sedang berjalan
"""
import psutil
import argparse
import subprocess
import re
from typing import List, Dict

def find_processes_by_name(name: str) -> List[Dict]:
    """Temukan proses berdasarkan nama"""
    processes = []
    name_lower = name.lower()
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'exe']):
        try:
            proc_info = proc.info
            
            # Check process name
            if name_lower in proc_info['name'].lower():
                processes.append({
                    'pid': proc_info['pid'],
                    'name': proc_info['name'],
                    'exe': proc_info['exe'],
                    'cmdline': ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else ''
                })
            
            # Check command line
            if proc_info['cmdline']:
                cmdline_str = ' '.join(proc_info['cmdline']).lower()
                if name_lower in cmdline_str and proc_info['pid'] not in [p['pid'] for p in processes]:
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'exe': proc_info['exe'],
                        'cmdline': ' '.join(proc_info['cmdline'])
                    })
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    return processes

def find_processes_by_network() -> List[Dict]:
    """Temukan proses yang memiliki koneksi jaringan"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            proc_info = proc.info
            connections = proc_info['connections']
            
            if connections:
                processes.append({
                    'pid': proc_info['pid'],
                    'name': proc_info['name'],
                    'connections': len(connections)
                })
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    return processes

def find_processes_by_port(port: int) -> List[Dict]:
    """Temukan proses yang menggunakan port tertentu"""
    processes = []
    
    try:
        # Use netstat to find processes using specific port
        result = subprocess.run(['netstat', '-tulpn'], capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if f':{port}' in line:
                    parts = line.split()
                    if len(parts) > 6:
                        pid_program = parts[6]
                        if '/' in pid_program:
                            pid = pid_program.split('/')[0]
                            program = pid_program.split('/')[1]
                            
                            try:
                                proc = psutil.Process(int(pid))
                                processes.append({
                                    'pid': int(pid),
                                    'name': program,
                                    'exe': proc.exe(),
                                    'cmdline': ' '.join(proc.cmdline())
                                })
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                continue
    
    except Exception as e:
        print(f"Error finding processes by port: {e}")
    
    return processes

def get_network_connections() -> List[Dict]:
    """Dapatkan semua koneksi jaringan aktif"""
    connections = []
    
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            proc_info = proc.info
            proc_connections = proc_info['connections']
            
            for conn in proc_connections:
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    connections.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'local_address': conn.laddr.ip if conn.laddr else None,
                        'local_port': conn.laddr.port if conn.laddr else None,
                        'remote_address': conn.raddr.ip,
                        'remote_port': conn.raddr.port,
                        'status': conn.status
                    })
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    return connections

def find_common_apps() -> Dict[str, List[Dict]]:
    """Temukan aplikasi umum yang sedang berjalan"""
    common_apps = {
        'browsers': ['chrome', 'firefox', 'safari', 'edge', 'opera'],
        'gaming': ['steam', 'discord', 'epic', 'origin', 'battle.net'],
        'media': ['spotify', 'vlc', 'youtube', 'netflix'],
        'communication': ['telegram', 'whatsapp', 'slack', 'zoom', 'teams'],
        'development': ['code', 'git', 'docker', 'node', 'python'],
        'system': ['systemd', 'dbus', 'networkmanager']
    }
    
    found_apps = {}
    
    for category, apps in common_apps.items():
        found_apps[category] = []
        for app in apps:
            processes = find_processes_by_name(app)
            if processes:
                found_apps[category].extend(processes)
    
    return found_apps

def display_processes(processes: List[Dict], title: str):
    """Tampilkan daftar proses"""
    print(f"\n{title}")
    print("=" * 60)
    
    if not processes:
        print("No processes found")
        return
    
    for proc in processes:
        print(f"PID: {proc['pid']}")
        print(f"Name: {proc['name']}")
        if 'exe' in proc and proc['exe']:
            print(f"Executable: {proc['exe']}")
        if 'cmdline' in proc and proc['cmdline']:
            print(f"Command: {proc['cmdline'][:100]}...")
        if 'connections' in proc:
            print(f"Connections: {proc['connections']}")
        print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description='Find Application Processes')
    parser.add_argument('--name', '-n', help='Search processes by name')
    parser.add_argument('--port', '-p', type=int, help='Search processes by port')
    parser.add_argument('--network', '-net', action='store_true', help='Show processes with network connections')
    parser.add_argument('--common', '-c', action='store_true', help='Show common applications')
    parser.add_argument('--all', '-a', action='store_true', help='Show all network connections')
    
    args = parser.parse_args()
    
    print("🔍 Application Process Finder")
    print("=" * 60)
    
    if args.name:
        processes = find_processes_by_name(args.name)
        display_processes(processes, f"Processes matching '{args.name}'")
    
    if args.port:
        processes = find_processes_by_port(args.port)
        display_processes(processes, f"Processes using port {args.port}")
    
    if args.network:
        processes = find_processes_by_network()
        display_processes(processes, "Processes with network connections")
    
    if args.common:
        found_apps = find_common_apps()
        for category, processes in found_apps.items():
            if processes:
                display_processes(processes, f"Common {category.title()} Applications")
    
    if args.all:
        connections = get_network_connections()
        print(f"\nAll Network Connections ({len(connections)} total)")
        print("=" * 60)
        
        # Group by process
        by_process = {}
        for conn in connections:
            key = f"{conn['name']} (PID {conn['pid']})"
            if key not in by_process:
                by_process[key] = []
            by_process[key].append(conn)
        
        for process, conns in by_process.items():
            print(f"\n{process}:")
            for conn in conns[:5]:  # Show first 5 connections
                print(f"  {conn['local_address']}:{conn['local_port']} -> {conn['remote_address']}:{conn['remote_port']}")
            if len(conns) > 5:
                print(f"  ... and {len(conns) - 5} more connections")
    
    if not any([args.name, args.port, args.network, args.common, args.all]):
        print("Usage examples:")
        print("  python3 find_app_processes.py --name discord")
        print("  python3 find_app_processes.py --port 443")
        print("  python3 find_app_processes.py --network")
        print("  python3 find_app_processes.py --common")
        print("  python3 find_app_processes.py --all")

if __name__ == '__main__':
    main()
