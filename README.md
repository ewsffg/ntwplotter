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

### Opções de Comando: 
- `TARGET`: O nome do host ou endereço IP a ser monitorado (obrigatório)
- `--count`, -c: Número de pings a serem enviados (padrão: 0 para contínuo)
- `--interval`, -i:  Segundos entre pings (padrão: 1.0)
- `--traceroute/--no-traceroute`: Ativar/desativar traceroute (padrão: ativado)
- `--save, -s`: Salvar resultados no arquivo especificado

## Interpretando os Gráficos do NTWPlotter
### Gráfico de Latência
O gráfico principal exibe a latência de rede ao longo do tempo:

- Eixo Y: Tempo de resposta em milissegundos (ms)
- Eixo X: Sequência de pings ao longo do tempo
- Linha do gráfico: Mostra a tendência da latência

### Interpretação de Padrões
- Linha estável e baixa: Conexão saudável
- Picos ocasionais: Possível congestionamento temporário
- Picos frequentes: Instabilidade na rede
- Valores constantemente altos: Possível gargalo na conexão
- Lacunas na linha: Pacotes perdidos (packet loss)

### Informações do Traceroute
Se o traceroute estiver ativado, você verá:
- Hops da rede: Cada servidor/roteador no caminho até o destino
- Latência por hop: Identifica onde ocorrem atrasos no caminho da rede

### Estatísticas Úteis
- Mínimo/Máximo/Média: Valores extremos e médios de latência
- Desvio padrão: Indica a estabilidade da conexão (valor menor = mais estável)
- Packet loss: Porcentagem de pacotes perdidos durante o teste

Ao analisar os dados, procure padrões consistentes que possam indicar problemas específicos na sua conexão ou na infraestrutura de rede.