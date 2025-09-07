#!/usr/bin/env python3
"""
Test script untuk Application Monitor
"""
import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.monitor.process_monitor import ProcessMonitor

def test_process_monitor():
    """Test ProcessMonitor functionality"""
    print("🧪 Testing Process Monitor...")
    
    monitor = ProcessMonitor()
    
    # Test getting processes
    print("\n1. Testing process detection:")
    
    # Test Discord
    discord_processes = monitor.get_discord_processes()
    print(f"   Discord processes: {len(discord_processes)}")
    
    # Test generic process search
    test_apps = ['chrome', 'firefox', 'discord', 'steam', 'spotify']
    
    for app in test_apps:
        processes = monitor.get_process_by_name(app)
        print(f"   {app}: {len(processes)} processes")
        if processes:
            for proc in processes[:2]:  # Show first 2 processes
                print(f"     - PID {proc['pid']}: {proc['name']}")
    
    # Test connections
    print("\n2. Testing connection detection:")
    
    # Get all processes with connections
    all_processes = []
    for app in test_apps:
        processes = monitor.get_process_by_name(app)
        all_processes.extend(processes)
    
    total_connections = 0
    for proc in all_processes:
        connections = proc['connections']
        total_connections += len(connections)
        if connections:
            print(f"   {proc['name']} (PID {proc['pid']}): {len(connections)} connections")
            for conn in connections[:2]:  # Show first 2 connections
                if conn['remote_address']:
                    print(f"     -> {conn['remote_address']}:{conn['remote_port']}")
    
    print(f"\n   Total connections found: {total_connections}")
    
    # Test Discord specific monitoring
    print("\n3. Testing Discord monitoring:")
    
    if discord_processes:
        discord_connections = monitor.get_discord_connections()
        print(f"   Discord connections: {len(discord_connections)}")
        
        if discord_connections:
            print("   Recent Discord connections:")
            for conn in discord_connections[:5]:
                print(f"     {conn['local_address']}:{conn['local_port']} -> {conn['remote_address']}:{conn['remote_port']}")
        
        # Test analysis
        analysis = monitor.get_discord_destinations_analysis()
        print(f"   Unique destinations: {analysis['total_destinations']}")
        
        if analysis['destinations']:
            print("   Top destinations:")
            for ip, info in list(analysis['destinations'].items())[:3]:
                ports_str = ", ".join(map(str, info['ports']))
                print(f"     {ip} - Ports: {ports_str} - Connections: {info['connections']}")
    else:
        print("   Discord not running")
    
    print("\n✅ Process Monitor test completed!")

def test_app_monitoring():
    """Test application monitoring functionality"""
    print("\n🎯 Testing Application Monitoring...")
    
    monitor = ProcessMonitor()
    
    # Test monitoring different apps
    test_apps = ['discord', 'chrome', 'firefox']
    
    for app in test_apps:
        print(f"\n📱 Testing {app} monitoring:")
        
        processes = monitor.get_process_by_name(app)
        if processes:
            print(f"   ✅ {app} found: {len(processes)} processes")
            
            # Get network stats
            stats = monitor.get_network_stats_for_process(app)
            print(f"   📊 Stats:")
            print(f"     - Total connections: {stats['total_connections']}")
            print(f"     - Unique destinations: {stats['unique_destinations']}")
            print(f"     - Ports used: {len(stats['ports_used'])}")
            
            if stats['destinations']:
                print(f"     - Sample destinations: {stats['destinations'][:3]}")
        else:
            print(f"   ❌ {app} not found")
    
    print("\n✅ Application monitoring test completed!")

def simulate_monitoring():
    """Simulate monitoring session"""
    print("\n🔄 Simulating monitoring session...")
    
    monitor = ProcessMonitor()
    
    # Find any running application
    test_apps = ['discord', 'chrome', 'firefox', 'steam', 'spotify']
    running_app = None
    
    for app in test_apps:
        processes = monitor.get_process_by_name(app)
        if processes:
            running_app = app
            break
    
    if not running_app:
        print("   No test applications running")
        return
    
    print(f"   Monitoring {running_app} for 10 seconds...")
    
    start_time = time.time()
    destinations = {}
    
    while time.time() - start_time < 10:
        if running_app.lower() == 'discord':
            connections = monitor.get_discord_connections()
        else:
            processes = monitor.get_process_by_name(running_app)
            connections = []
            for proc in processes:
                proc_connections = monitor._get_process_connections(proc['pid'])
                for conn in proc_connections:
                    if conn['remote_address'] and conn['remote_port']:
                        connections.append({
                            'remote_address': conn['remote_address'],
                            'remote_port': conn['remote_port']
                        })
        
        # Update destinations
        for conn in connections:
            dest_ip = conn['remote_address']
            if dest_ip:
                if dest_ip not in destinations:
                    destinations[dest_ip] = {'connections': 0, 'ports': set()}
                destinations[dest_ip]['connections'] += 1
                destinations[dest_ip]['ports'].add(conn['remote_port'])
        
        elapsed = int(time.time() - start_time)
        print(f"\r   [{elapsed:2d}s] Connections: {len(connections):3d} | Destinations: {len(destinations):3d}", end="", flush=True)
        time.sleep(1)
    
    print(f"\n\n   📊 {running_app.upper()} Monitoring Results:")
    print(f"   Total connections: {len(connections)}")
    print(f"   Unique destinations: {len(destinations)}")
    
    if destinations:
        print("   Top destinations:")
        for ip, info in list(destinations.items())[:3]:
            ports_str = ", ".join(map(str, info['ports']))
            print(f"     {ip} - Ports: {ports_str} - Connections: {info['connections']}")
    
    print("\n✅ Monitoring simulation completed!")

def main():
    print("=" * 60)
    print("🧪 APPLICATION MONITOR TEST SUITE")
    print("=" * 60)
    
    try:
        # Test process monitor
        test_process_monitor()
        
        # Test app monitoring
        test_app_monitoring()
        
        # Simulate monitoring
        simulate_monitoring()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\n💡 Usage Examples:")
        print("   python3 main.py --app-monitor discord --app-duration 300")
        print("   python3 main.py --app-monitor chrome --app-duration 600")
        print("   python3 discord_monitor.py --continuous")
        print("   python3 discord_monitor.py --status")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
