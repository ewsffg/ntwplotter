import time
from icmplib import ping

def check_internet_connectivity(reliable_hosts=None, timeout=2):
    """
    Verifica se há conectividade com a internet pingando múltiplos hosts confiáveis.
    
    Args:
        reliable_hosts: Lista de hosts confiáveis para verificar a conexão
        timeout: Tempo máximo de espera por resposta
        
    Returns:
        Dictionary com resultado da verificação de internet
    """
    if reliable_hosts is None:
        reliable_hosts = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
    
    for host in reliable_hosts:
        try:
            result = ping(host, count=1, timeout=timeout, privileged=False)
            if result.is_alive:
                return {
                    'timestamp': time.time(),
                    'is_connected': True,
                    'host_checked': host,
                    'rtt': result.avg_rtt
                }
        except Exception:
            continue
    
    # Se chegou aqui, não conseguiu se conectar a nenhum dos hosts
    return {
        'timestamp': time.time(),
        'is_connected': False,
        'host_checked': None,
        'rtt': 0
    }