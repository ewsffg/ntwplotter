import plotext as plt
import time
import os
import shutil
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
    
    # Get terminal size
    terminal_width, terminal_height = shutil.get_terminal_size()
    
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
    
    # Determine optimal graph size based on terminal
    graph_width = terminal_width // 2 - 5  # Adjust for padding
    graph_height = min(15, terminal_height // 3)  # Use at most 1/3 of height
    
    # Configure RTT graph
    plt.clf()
    plt.plot_size(graph_width, graph_height)
    plt.plot(relative_times, rtts, color="red", marker="dot")
    plt.title(f"RTT (ms) - Min: {min_rtt:.1f}, Max: {max_rtt:.1f}, Avg: {avg_rtt:.1f}")
    plt.xlabel("Seconds")
    plt.ylabel("RTT (ms)")

    # Garanta que os limites nunca são iguais (evita divisão por zero)
    x_min = min(relative_times) if relative_times else 0
    x_max = max(relative_times) if relative_times else 10
    if x_min == x_max:
        x_max = x_min + 1  # Adiciona 1 segundo se os limites forem iguais

    plt.xlim(x_min, x_max)
    plt.ylim(0, max(0.1, max_rtt * 1.1))  # Garante valor mínimo de 0.1

    # Display RTT graph
    rtt_canvas = plt.build()
    
    # Configure packet loss graph
    plt.clf()
    plt.plot_size(graph_width, graph_height)
    plt.plot(relative_times, packet_loss, color="yellow", marker="dot")
    plt.title("Packet Loss (%)")
    plt.xlabel("Seconds")
    plt.ylabel("Loss (%)")

    # Mesma proteção contra limites iguais
    plt.xlim(x_min, x_max)
    plt.ylim(0, max(0.1, max(packet_loss) * 1.1 if any(packet_loss) else 10))

    # Display packet loss graph
    loss_canvas = plt.build()
    
    # Split the RTT and packet loss canvases into lines
    rtt_lines = rtt_canvas.split('\n')
    loss_lines = loss_canvas.split('\n')
    
    # Print the graphs side by side
    for i in range(min(len(rtt_lines), len(loss_lines))):
        print(rtt_lines[i] + "    " + loss_lines[i])
    
    # Display statistics
    if results:
        latest = results[-1]
        print(f"\nLatest ping to {latest['host']} at {datetime.fromtimestamp(latest['timestamp']).strftime('%H:%M:%S')}:")
        print(f"Min RTT: {latest['min_rtt']:.2f} ms | Avg RTT: {latest['avg_rtt']:.2f} ms | Max RTT: {latest['max_rtt']:.2f} ms")
        print(f"Packet Loss: {latest['packet_loss']:.1f}% | Jitter: {latest['jitter']:.2f} ms | Status: {'✓ Alive' if latest['is_alive'] else '✗ Down'}")
    
    # Display route information if available
    if route:
        print("\nNetwork path:")
        route_info = []
        for i, hop in enumerate(route):
            status = "✓" if hop['is_alive'] else "✗"
            route_info.append(f"{i+1}. {status} {hop['address']} - {hop['avg_rtt']:.2f} ms")
        
        # Display route in columns if terminal is wide enough
        if terminal_width >= 100:
            mid = (len(route_info) + 1) // 2
            for i in range(mid):
                left = route_info[i]
                right = route_info[i + mid] if i + mid < len(route_info) else ""
                print(f"{left:<40} {right}")
        else:
            for info in route_info:
                print(info)
    
    # Display internet status if available
    if internet_status:
        current_status = internet_status[-1]
        print("\nStatus da Internet:")
        status_text = "✓ Conectado" if current_status['is_connected'] else "✗ Desconectado"
        status_time = datetime.fromtimestamp(current_status['timestamp']).strftime('%H:%M:%S')
        print(f"Estado atual: {status_text} (última verificação: {status_time})")
        
        # If disconnected, show when it was last connected
        if not current_status['is_connected']:
            for status in reversed(internet_status[:-1]):
                if status['is_connected']:
                    disconnect_time = datetime.fromtimestamp(current_status['timestamp']).strftime('%H:%M:%S')
                    last_connected = datetime.fromtimestamp(status['timestamp']).strftime('%H:%M:%S')
                    print(f"Desconectado desde: {disconnect_time} (última conexão: {last_connected})")
                    break