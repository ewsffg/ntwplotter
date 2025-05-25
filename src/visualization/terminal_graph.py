import plotext as plt
import time
import os
from datetime import datetime

def display_graph(results, route=None, max_points=60, internet_status=None):
    """Display a terminal-based graph of ping results.
    
    Args:
        results: List of ping result dictionaries
        route: List of traceroute hop dictionaries
        max_points: Maximum number of points to show on the graph
        internet_status: List of internet connection status dictionaries
    """
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Extract data
    times = [r['timestamp'] for r in results[-max_points:]]
    rtts = [r['avg_rtt'] for r in results[-max_points:]]
    packet_loss = [r['packet_loss'] for r in results[-max_points:]]
    
    # Convert timestamps to relative seconds
    if times:
        start_time = times[0]
        relative_times = [t - start_time for t in times]
    else:
        relative_times = []
    
    # Calculate statistics
    min_rtt = min(rtts) if rtts else 0
    max_rtt = max(rtts) if rtts else 0
    avg_rtt = sum(rtts) / len(rtts) if rtts else 0
    
    # Plot RTT
    plt.clf()
    plt.plot(relative_times, rtts, color="red", marker="dot")
    plt.title(f"Ping Response Time to {results[0]['host'] if results else 'target'}")
    plt.xlabel("Seconds")
    plt.ylabel("RTT (ms)")
    
    # Add statistics as title annotation instead of using text()
    plt.title(f"Ping Response Time to {results[0]['host'] if results else 'target'}\nMin: {min_rtt:.2f} ms, Max: {max_rtt:.2f} ms, Avg: {avg_rtt:.2f} ms")
    plt.show()
    
    # Display packet loss as a separate graph if needed
    if any(p > 0 for p in packet_loss):
        plt.clf()
        plt.plot(relative_times, packet_loss, color="yellow", marker="dot")
        plt.title("Packet Loss (%)")
        plt.xlabel("Seconds")
        plt.ylabel("Loss (%)")
        plt.show()
    
    # Display statistics
    if results:
        latest = results[-1]
        print(f"\nLatest ping to {latest['host']} at {datetime.fromtimestamp(latest['timestamp']).strftime('%H:%M:%S')}:")
        print(f"Min RTT: {latest['min_rtt']:.2f} ms")
        print(f"Avg RTT: {latest['avg_rtt']:.2f} ms")
        print(f"Max RTT: {latest['max_rtt']:.2f} ms")
        print(f"Packet Loss: {latest['packet_loss']:.1f}%")
        print(f"Jitter: {latest['jitter']:.2f} ms")
        print(f"Status: {'✓ Alive' if latest['is_alive'] else '✗ Down'}")
    
    # Display route information if available
    if route:
        print("\nNetwork path:")
        for i, hop in enumerate(route):
            status = "✓" if hop['is_alive'] else "✗"
            print(f"{i+1}. {status} {hop['address']} - {hop['avg_rtt']:.2f} ms")
    
    # Display internet status if available
    if internet_status:
        current_status = internet_status[-1]
        print("\nStatus da Internet:")
        status_text = "✓ Conectado" if current_status['is_connected'] else "✗ Desconectado"
        status_time = datetime.fromtimestamp(current_status['timestamp']).strftime('%H:%M:%S')
        print(f"Estado atual: {status_text} (última verificação: {status_time})")
        
        # If disconnected, show when it was last connected
        if not current_status['is_connected']:
            # Find the last record where it was connected
            for status in reversed(internet_status[:-1]):
                if status['is_connected']:
                    disconnect_time = datetime.fromtimestamp(current_status['timestamp']).strftime('%H:%M:%S')
                    last_connected = datetime.fromtimestamp(status['timestamp']).strftime('%H:%M:%S')
                    print(f"Desconectado desde: {disconnect_time} (última conexão: {last_connected})")
                    break