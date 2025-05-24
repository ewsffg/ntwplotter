# NTWPlotter CLI

A terminal-based network diagnostics tool inspired by PingPlotter. Monitor and analyze your network performance with live graphs directly in your terminal.

## Features

- Ping hosts to measure network latency and packet loss
- Perform traceroute to identify network path and bottlenecks
- Live terminal-based graphs with color-coded performance indicators
- Detailed statistics on network performance metrics
- Save results to CSV files for further analysis
- Lightweight and easy to use

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ntwplotter.git
cd ntwplotter

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage
* Simple ping monitoring to a host
ntwplot google.com

### Monitor for a specific number of pings
ntwplot google.com --count 100

### Change the interval between pings (in seconds)
ntwplot google.com --interval 0.5

### Disable the initial traceroute
ntwplot google.com --no-traceroute

### Save results to a CSV file
ntwplot google.com --save results.csv

Command Options:
* `TARGET`: The hostname or IP address to monitor (required)
* `--count`, -c: Number of pings to send (default: 0 for continuous)
* `--interval`, -i: Seconds between pings (default: 1.0)
* `--traceroute/--no-traceroute`: Enable/disable traceroute (default: enabled)
* `--save, -s`: Save results to specified file

