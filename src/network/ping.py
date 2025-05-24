import time
from icmplib import ping

def ping_host(host, count=1, timeout=2):
    """Ping a host and return the results.
    
    Args:
        host: The hostname or IP address to ping
        count: Number of ICMP packets to send
        timeout: Maximum time to wait for a response
        
    Returns:
        Dictionary with ping results
    """
    try:
        result = ping(host, count=count, timeout=timeout, privileged=False)
        return {
            'timestamp': time.time(),
            'host': host,
            'min_rtt': result.min_rtt,
            'avg_rtt': result.avg_rtt,
            'max_rtt': result.max_rtt,
            'packet_loss': result.packet_loss,
            'jitter': result.jitter,
            'is_alive': result.is_alive
        }
    except Exception as e:
        return {
            'timestamp': time.time(),
            'host': host,
            'min_rtt': 0,
            'avg_rtt': 0,
            'max_rtt': 0,
            'packet_loss': 100.0,
            'jitter': 0,
            'is_alive': False,
            'error': str(e)
        }