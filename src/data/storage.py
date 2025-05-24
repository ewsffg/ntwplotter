import json
import csv
from datetime import datetime

def save_results(results, route=None, filename=None):
    """Save ping and traceroute results to a file.
    
    Args:
        results: List of ping result dictionaries
        route: List of traceroute hop dictionaries
        filename: Path to save the results
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        host = results[0]['host'] if results else "unknown"
        filename = f"pingplot_{host}_{timestamp}.csv"
    
    # Determine file type based on extension
    if filename.endswith('.json'):
        save_json(results, route, filename)
    else:
        save_csv(results, route, filename)
    
    return filename

def save_json(results, route, filename):
    """Save results as JSON."""
    data = {
        'ping_results': results,
        'traceroute': route
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def save_csv(results, route, filename):
    """Save results as CSV."""
    # Save ping results
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'host', 'min_rtt', 'avg_rtt', 'max_rtt', 
                         'packet_loss', 'jitter', 'is_alive'])
        
        for r in results:
            writer.writerow([
                datetime.fromtimestamp(r['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                r['host'],
                r['min_rtt'],
                r['avg_rtt'],
                r['max_rtt'],
                r['packet_loss'],
                r['jitter'],
                r['is_alive']
            ])
    
    # Save traceroute results if available
    if route:
        route_filename = filename.replace('.csv', '_route.csv')
        with open(route_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['hop', 'address', 'avg_rtt', 'min_rtt', 'max_rtt', 
                             'packet_loss', 'is_alive'])
            
            for i, hop in enumerate(route):
                writer.writerow([
                    i+1,
                    hop['address'],
                    hop['avg_rtt'],
                    hop['min_rtt'],
                    hop['max_rtt'],
                    hop['packet_loss'],
                    hop['is_alive']
                ])