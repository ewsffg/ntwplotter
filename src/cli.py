import click
import time
import threading
from .network.ping import ping_host
from .network.traceroute import trace_route
from .visualization.terminal_graph import display_graph
from .data.storage import save_results

@click.command()
@click.argument('target', type=str)
@click.option('--count', '-c', default=0, help='Number of pings to send (0 for continuous)')
@click.option('--interval', '-i', default=1.0, help='Seconds between pings')
@click.option('--traceroute/--no-traceroute', default=True, help='Perform traceroute at start')
@click.option('--save', '-s', help='Save results to file')
def main(target, count, interval, traceroute, save):
    """A simple terminal-based NTWPlotter clone."""
    click.echo(f"Starting ntwplot for {target}")
    click.echo("Press Ctrl+C to exit")
    
    # Store results
    results = []
    route = []
    stop_event = threading.Event()
    
    # Perform initial traceroute if enabled
    if traceroute:
        click.echo("Performing traceroute...")
        route = trace_route(target)
        click.echo(f"Discovered {len(route)} hops to destination")
    
    # Start ping thread
    def ping_thread():
        iterations = 0
        while not stop_event.is_set():
            if count > 0 and iterations >= count:
                break
            
            result = ping_host(target)
            results.append(result)
            iterations += 1
            time.sleep(interval)
    
    # Start visualization thread
    def display_thread():
        while not stop_event.is_set():
            if results:
                display_graph(results, route)
            time.sleep(0.5)
    
    ping_worker = threading.Thread(target=ping_thread)
    display_worker = threading.Thread(target=display_thread)
    
    try:
        ping_worker.start()
        display_worker.start()
        
        # Keep main thread alive
        while ping_worker.is_alive():
            ping_worker.join(1)
            
    except KeyboardInterrupt:
        click.echo("\nStopping...")
        stop_event.set()
        
    ping_worker.join()
    display_worker.join()
    
    # Save results if requested
    if save and results:
        click.echo(f"Saving results to {save}...")
        save_results(results, route, save)
        
    click.echo("Done!")

if __name__ == '__main__':
    main()