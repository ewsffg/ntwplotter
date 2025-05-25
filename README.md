# NTWPlotter CLI

Uma ferramenta de diagnóstico de rede baseada em terminal, inspirada no PingPlotter. Monitore e analise o desempenho da sua rede com gráficos ao vivo diretamente no seu terminal.

## Features

- Ping para hosts para medir latência e perda de pacotes na rede
- Execução de traceroute para identificar o caminho da rede e gargalos
- Gráficos ao vivo no terminal com indicadores de desempenho codificados por cores
- Estatísticas detalhadas sobre métricas de desempenho de rede
- Salve resultados em arquivos CSV para análise posterior
- Leve e fácil de usar

## Instalação

```bash
# Clone o repositório
git clone https://github.com/yourusername/ntwplotter.git
cd ntwplotter

# Configure um ambiente virtual
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Instale os pacotes
pip install -e .
```

## Uso
### Monitoramento simples de ping para um host
`ntwplot google.com`

### Monitorar por um número específico de pings
`ntwplot google.com --count 100`

### Alterar o intervalo entre pings (em segundos)
`ntwplot google.com --interval 0.5`

### Desativar o traceroute inicial
`ntwplot google.com --no-traceroute`

### Salvar resultados em um arquivo CSV
`ntwplot google.com --save results.csv`

### Desativar a verificação de conectividade de internet
`ntwplot google.com --no-check-internet`

### Alterar o intervalo de verificação de internet (em segundos)
`ntwplot google.com --internet-check-interval 60`

### Opções de Comando: 
- `TARGET`: O nome do host ou endereço IP a ser monitorado (obrigatório)
- `--count`, -c: Número de pings a serem enviados (padrão: 0 para contínuo)
- `--interval`, -i:  Segundos entre pings (padrão: 1.0)
- `--traceroute/--no-traceroute`: Ativar/desativar traceroute (padrão: ativado)
- `--save`, -s: Salvar resultados no arquivo especificado
- `--check-internet/--no-check-internet`: Ativar/desativar monitoramento de conectividade de internet (padrão: ativado)
- `--internet-check-interval`: Segundos entre verificações de internet (padrão: 30.0)

## Interpretando os Gráficos do NTWPlotter
### Gráfico de Latência
O gráfico principal exibe a latência de rede ao longo do tempo:

- Eixo Y: Tempo de resposta em milissegundos (ms)
- Eixo X: Sequência de pings ao longo do tempo
- Linha do gráfico: Mostra a tendência da latência

### Monitoramento de Conectividade de Internet
O NTWPlotter verifica periodicamente se sua conexão com a internet está ativa, independentemente do host alvo sendo monitorado:

- Exibe notificações quando sua internet cai ou é restaurada
- Registra os momentos exatos de perda e restauração de conexão
- Salva os registros em um arquivo CSV separado quando a opção `--save` é utilizada
- Permite distinguir entre falhas no host alvo e problemas na sua própria conexão

Quando a opção `--save` é utilizada, dois arquivos são gerados:
- `arquivo.csv`: Contém os dados de ping para o host alvo
- `arquivo_internet.csv`: Contém os registros de status da conexão com a internet