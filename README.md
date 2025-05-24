# PingPlotter CLI

A terminal-based network diagnostics tool inspired by PingPlotter.

## Features

- Ping hosts to measure network latency
- Perform traceroute to identify network path
- Live terminal-based graphs
- Statistics on network performance

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pingplotter.git
cd pingplotter

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .