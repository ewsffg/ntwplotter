import click
import time
import threading
from .network.ping import ping_host
from .network.traceroute import trace_route
from .visualization.terminal_graph import display_graph
from .data.storage import save_results
from .network.internet_check import check_internet_connectivity

@click.command()
@click.argument('target', type=str)
@click.option('--count', '-c', default=0, help='Number of pings to send (0 for continuous)')
@click.option('--interval', '-i', default=1.0, help='Seconds between pings')
@click.option('--traceroute/--no-traceroute', default=True, help='Perform traceroute at start')
@click.option('--save', '-s', help='Save results to file')
@click.option('--check-internet/--no-check-internet', default=True, help='Monitor internet connectivity')
@click.option('--internet-check-interval', default=5.0, help='Seconds between internet checks')
def main(target, count, interval, traceroute, save, check_internet, internet_check_interval):
    """A simple terminal-based NTWPlotter clone."""
    click.echo(f"Starting ntwplot for {target}")
    click.echo("Press Ctrl+C to exit")
    
    # Store results
    results = []
    route = []
    internet_status = []
    last_internet_status = True
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
                display_graph(results, route, internet_status=internet_status)
            time.sleep(0.5)
    
    # Thread para verificar a conectividade da internet
    def internet_check_thread():
        while not stop_event.is_set():
            status = check_internet_connectivity()
            nonlocal last_internet_status
            
            # Registre apenas quando o status mudar ou a cada 5 minutos
            if status['is_connected'] != last_internet_status or len(internet_status) == 0 or \
               (internet_status and time.time() - internet_status[-1]['timestamp'] > 30):
                internet_status.append(status)
                if status['is_connected'] != last_internet_status:
                    if status['is_connected']:
                        click.echo(f"\nConexão com a internet restaurada em {datetime.fromtimestamp(status['timestamp']).strftime('%H:%M:%S')}")
                    else:
                        click.echo(f"\nConexão com a internet perdida em {datetime.fromtimestamp(status['timestamp']).strftime('%H:%M:%S')}")
                
                last_internet_status = status['is_connected']
            
            time.sleep(internet_check_interval)
    
    ping_worker = threading.Thread(target=ping_thread)
    display_worker = threading.Thread(target=display_thread)
    
    # Inicie o thread de verificação de internet se habilitado
    internet_worker = None
    if check_internet:
        internet_worker = threading.Thread(target=internet_check_thread)
        internet_worker.start()
    
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
    
    # Aguarde o thread de internet também
    if internet_worker:
        internet_worker.join()
    
    # Save results if requested
    if save and results:
        click.echo(f"Saving results to {save}...")
        save_results(results, route, save)
        
        # Salve os registros de internet se existirem
        if internet_status:
            internet_file = save_internet_status(internet_status, save)
            click.echo(f"Internet status saved to {internet_file}")
        
    click.echo("Done!")

if __name__ == '__main__':
    main()