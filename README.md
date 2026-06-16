# Sistema de Monitoramento de Missao Espacial Experimental .𖥔 ݁ ˖ ᯓ★

**Global Solution 2026 — Ciencia da Computacao**  
**Tema: Solucoes em Energias Renovaveis e Sustentaveis**

---

## Integrantes

| Nome | RM | 
|---|---|
| Gabriel Jurado Nogueira | 571236 |
| Vinicius Torralles Ferreira Conduta | 570911 |
| Mariana Carminato | 573258 |
 ##
 
##LINKS ᯓ★

https://youtu.be/zip88Iyn5ec (video no youtube)

https://globalsolution2-hqqwms2kquf9camwd8bjfy.streamlit.app/(Streamlit)
---

## Descricao do Projeto ᯓ★

Sistema inteligente de monitoramento para controle basico de uma missao espacial experimental. A solucao recebe, interpreta e exibe dados simulados das condicoes operacionais da missao, incluindo temperatura, comunicacao, energia e status dos modulos de operacao.

O sistema aplica conceitos de programacao, algoritmos e pensamento computacional para construir uma plataforma funcional de analise operacional, com geracao automatica de alertas e tomada de decisao automatizada diante de situacoes criticas simuladas.

---

## Estrutura do Projeto ᯓ★

```
missao_espacial.py       # Codigo principal do sistema
dashboard_missao.png     # Dashboard grafico gerado ao final da execucao
README.md                # Este arquivo
entrega.txt              # Arquivo de entrega com integrantes e links
```

---

## Funcionalidades ᯓ★

### Monitoramento de Dados Simulados
- Temperatura interna dos modulos (graus Celsius)
- Nivel de energia dos paineis solares (%)
- Qualidade do sinal de comunicacao (%)
- Pressao interna (kPa)
- Velocidade orbital (km/s)
- Status individual de 5 modulos: Propulsao, Comunicacao, Energia Solar, Suporte de Vida e Navegacao

### Geracao de Alertas Automaticos ᯓ★
O sistema possui dois niveis de alerta:

| Nivel | Temperatura | Energia | Sinal |
|---|---|---|---|
| ATENCAO | >= 65 C | <= 30% | <= 40% |
| CRITICO | >= 80 C | <= 15% | <= 20% |

Para modulos, os status possiveis sao OPERACIONAL, DEGRADADO e FALHA, cada um com alerta correspondente.

### Tomada de Decisao Automatizada ᯓ★
Diante de condicoes criticas, o sistema aciona respostas automaticas:
- Energia critica: reorientacao automatica dos paineis solares
- Temperatura critica: ativacao da ventilacao forcada
- Sinal critico: reconexao na frequencia de backup
- Modulo em falha: ativacao de redundancia e modo de contingencia

### Visualizacao dos Dados ᯓ★
- Saida formatada no terminal a cada ciclo de monitoramento
- Dashboard grafico gerado ao final da execucao com:
  - Grafico de temperatura ao longo dos ciclos
  - Grafico de nivel de energia
  - Grafico de qualidade do sinal
  - Grafico de pressao interna
  - Painel de status dos modulos no ultimo ciclo

---

## Como Executar ᯓ★

### Requisitos
```
Python 3.8+
matplotlib
```

### Instalacao das dependencias
```bash
pip install matplotlib
```

### Execucao
```bash
python missao_espacial.py
```

O sistema ira executar 20 ciclos de monitoramento com intervalo de 0,4 segundos entre cada um e gerar o arquivo `dashboard_missao.png` ao final.

Para alterar o numero de ciclos ou o intervalo, edite a chamada no final do arquivo:
```python
executar_monitoramento(n_ciclos=20, intervalo_segundos=0.4)
```

---

## Contexto: Energias Renovaveis no Espaco

O sistema simula o monitoramento de paineis solares como principal fonte de energia da missao — tecnologia central em satelites e estacoes espaciais. O modulo "Energia Solar" e monitorado continuamente e o sistema aciona reorientacao automatica dos paineis quando a carga cai abaixo de 15%, refletindo a logica real de gestao energetica sustentavel em missoes espaciais.

---

## Exemplo de Saida

```
============================================================
  CICLO 001  |  14:32:05
============================================================

  PARAMETROS OPERACIONAIS
------------------------------------------------------------
  Temperatura   :   43.1 C
  Energia       :   79.8 %
  Sinal         :   67.2 %
  Pressao       :   99.94 kPa
  Velocidade    :    7.733 km/s

  STATUS DOS MODULOS
------------------------------------------------------------
  [OK] Propulsao             OPERACIONAL
  [OK] Comunicacao           OPERACIONAL
  [OK] Energia Solar         OPERACIONAL
  [OK] Suporte de Vida       OPERACIONAL
  [OK] Navegacao             OPERACIONAL

  SEM ALERTAS — Todos os parametros nominais.

  DECISOES AUTOMATIZADAS
------------------------------------------------------------
  [INFO] Todos os parametros dentro dos limites nominais. Missao estavel.
```
