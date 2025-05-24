from icmplib import traceroute as icmp_traceroute

def trace_route(host, max_hops=30, timeout=2):
    """Perform a traceroute to the target host.
    
    Args:
        host: The hostname or IP address to trace
        max_hops: Maximum number of hops to probe
        timeout: Maximum time to wait for a response
        
    Returns:
        List of dictionaries with hop information
    """
    try:
        hops = icmp_traceroute(host, max_hops=max_hops, timeout=timeout, privileged=False)
        result = []
        
        for hop in hops:
            result.append({
                'distance': hop.distance,
                'address': hop.address,
                'avg_rtt': hop.avg_rtt,
                'min_rtt': hop.min_rtt,
                'max_rtt': hop.max_rtt,
                'packet_loss': hop.packet_loss,
                'is_alive': hop.is_alive
            })
        
        return result
    except Exception as e:
        print(f"Traceroute error: {e}")
        return []