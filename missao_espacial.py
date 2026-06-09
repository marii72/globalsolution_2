# =============================================================================
# SISTEMA DE MONITORAMENTO DE MISSAO ESPACIAL EXPERIMENTAL
# Global Solution 2026 - Ciencia da Computacao
#
# Integrantes:
#   Gabriel Jurado Nogueira       RM: 571236
#   Vinicius Torralles F. Conduta RM: 570911
#   Mariana Carminato             RM: 573258
# =============================================================================

import random
import time
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import deque

# ---------------------------------------------------------------------------
# CONFIGURACOES DOS LIMIARES DE ALERTA
# ---------------------------------------------------------------------------
LIMIARES = {
    "temperatura_critica":  80.0,   # graus Celsius
    "temperatura_alerta":   65.0,
    "energia_critica":      15.0,   # % de carga
    "energia_alerta":       30.0,
    "sinal_critico":        20.0,   # % de qualidade de sinal
    "sinal_alerta":         40.0,
}

MODULOS = ["Propulsao", "Comunicacao", "Energia Solar", "Suporte de Vida", "Navegacao"]

# ---------------------------------------------------------------------------
# SIMULACAO DE DADOS
# ---------------------------------------------------------------------------

class SimuladorMissao:
    """Gera dados simulados realistas para os modulos da missao."""

    def __init__(self):
        self.ciclo = 0
        self.temperatura_base = 45.0
        self.energia_base = 80.0
        self.sinal_base = 75.0
        self.status_modulos = {m: "OPERACIONAL" for m in MODULOS}
        self._falha_agendada = None

    def _ruido(self, amplitude=1.0):
        return random.gauss(0, amplitude)

    def _simular_evento_critico(self):
        """Ocasionalmente injeta falhas simuladas para testar o sistema de alertas."""
        chance = random.random()
        if chance < 0.08:
            modulo = random.choice(MODULOS)
            self.status_modulos[modulo] = random.choice(["DEGRADADO", "FALHA"])
        elif chance < 0.15:
            self.energia_base = max(10, self.energia_base - random.uniform(5, 15))
        elif chance < 0.20:
            self.temperatura_base = min(95, self.temperatura_base + random.uniform(5, 18))
        else:
            # Recuperacao gradual
            self.temperatura_base = max(40, self.temperatura_base - 0.5)
            self.energia_base = min(100, self.energia_base + 0.3)
            for m in MODULOS:
                if self.status_modulos[m] == "DEGRADADO" and random.random() < 0.3:
                    self.status_modulos[m] = "OPERACIONAL"

    def coletar(self):
        self.ciclo += 1
        self._simular_evento_critico()

        temperatura = round(self.temperatura_base + self._ruido(2.5), 1)
        energia = round(max(0, min(100, self.energia_base + self._ruido(1.5))), 1)
        sinal = round(max(0, min(100, self.sinal_base + self._ruido(5))), 1)
        pressao = round(101.3 + self._ruido(0.8), 2)
        velocidade = round(7.8 + self._ruido(0.05), 3)  # km/s orbita LEO

        return {
            "ciclo": self.ciclo,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "temperatura": temperatura,
            "energia": energia,
            "sinal": sinal,
            "pressao": pressao,
            "velocidade": velocidade,
            "modulos": dict(self.status_modulos),
        }


# ---------------------------------------------------------------------------
# SISTEMA DE ALERTAS
# ---------------------------------------------------------------------------

class SistemaAlertas:
    """Avalia os dados recebidos e gera alertas automaticos com acoes corretivas."""

    def __init__(self):
        self.historico = []

    def avaliar(self, dados):
        alertas = []

        # Temperatura
        temp = dados["temperatura"]
        if temp >= LIMIARES["temperatura_critica"]:
            alertas.append({
                "nivel": "CRITICO",
                "parametro": "Temperatura",
                "valor": f"{temp} C",
                "acao": "Ativar sistema de resfriamento emergencial e reduzir carga dos modulos."
            })
        elif temp >= LIMIARES["temperatura_alerta"]:
            alertas.append({
                "nivel": "ATENCAO",
                "parametro": "Temperatura",
                "valor": f"{temp} C",
                "acao": "Monitorar tendencia e reduzir consumo energetico preventivamente."
            })

        # Energia
        energia = dados["energia"]
        if energia <= LIMIARES["energia_critica"]:
            alertas.append({
                "nivel": "CRITICO",
                "parametro": "Energia",
                "valor": f"{energia}%",
                "acao": "Desligar modulos nao essenciais. Reorientar paineis solares."
            })
        elif energia <= LIMIARES["energia_alerta"]:
            alertas.append({
                "nivel": "ATENCAO",
                "parametro": "Energia",
                "valor": f"{energia}%",
                "acao": "Verificar eficiencia dos paineis solares e reduzir consumo auxiliar."
            })

        # Sinal
        sinal = dados["sinal"]
        if sinal <= LIMIARES["sinal_critico"]:
            alertas.append({
                "nivel": "CRITICO",
                "parametro": "Sinal",
                "valor": f"{sinal}%",
                "acao": "Reorientar antena. Ativar protocolo de comunicacao de emergencia."
            })
        elif sinal <= LIMIARES["sinal_alerta"]:
            alertas.append({
                "nivel": "ATENCAO",
                "parametro": "Sinal",
                "valor": f"{sinal}%",
                "acao": "Verificar obstrucoes na antena e recalibrar frequencia."
            })

        # Modulos com falha
        for modulo, status in dados["modulos"].items():
            if status == "FALHA":
                alertas.append({
                    "nivel": "CRITICO",
                    "parametro": f"Modulo {modulo}",
                    "valor": "FALHA",
                    "acao": f"Isolar modulo {modulo} e acionar redundancia do sistema."
                })
            elif status == "DEGRADADO":
                alertas.append({
                    "nivel": "ATENCAO",
                    "parametro": f"Modulo {modulo}",
                    "valor": "DEGRADADO",
                    "acao": f"Executar diagnostico completo do modulo {modulo}."
                })

        self.historico.extend(alertas)
        return alertas


# ---------------------------------------------------------------------------
# TOMADA DE DECISAO
# ---------------------------------------------------------------------------

class SistemaDecisao:
    """Implementa logica de decisao automatizada baseada no estado geral da missao."""

    ACOES_AUTOMATICAS = {
        "energia_baixa": "Painel solar reorientado automaticamente para maximizar captacao.",
        "temperatura_alta": "Ventilacao forcada ativada nos compartimentos internos.",
        "sinal_fraco": "Protocolo de reconexao iniciado na frequencia de backup.",
        "modulo_falho": "Redundancia ativada. Sistema operando em modo de contingencia.",
    }

    def decidir(self, dados, alertas):
        decisoes = []
        niveis = [a["nivel"] for a in alertas]

        if dados["energia"] <= LIMIARES["energia_critica"]:
            decisoes.append(("AUTO", self.ACOES_AUTOMATICAS["energia_baixa"]))
        if dados["temperatura"] >= LIMIARES["temperatura_critica"]:
            decisoes.append(("AUTO", self.ACOES_AUTOMATICAS["temperatura_alta"]))
        if dados["sinal"] <= LIMIARES["sinal_critico"]:
            decisoes.append(("AUTO", self.ACOES_AUTOMATICAS["sinal_fraco"]))
        for modulo, status in dados["modulos"].items():
            if status == "FALHA":
                decisoes.append(("AUTO", self.ACOES_AUTOMATICAS["modulo_falho"]))
                break

        if not niveis:
            decisoes.append(("INFO", "Todos os parametros dentro dos limites nominais. Missao estavel."))
        elif "CRITICO" not in niveis:
            decisoes.append(("INFO", "Situacao sob controle. Aguardando normalizacao dos parametros."))

        return decisoes


# ---------------------------------------------------------------------------
# VISUALIZACAO
# ---------------------------------------------------------------------------

def gerar_dashboard(historico_dados, nome_arquivo="dashboard_missao.png"):
    """Gera um dashboard grafico com os ultimos ciclos monitorados."""

    ciclos    = [d["ciclo"]      for d in historico_dados]
    temps     = [d["temperatura"] for d in historico_dados]
    energias  = [d["energia"]    for d in historico_dados]
    sinais    = [d["sinal"]      for d in historico_dados]
    pressoes  = [d["pressao"]    for d in historico_dados]

    DARK  = "#0D1117"
    PANEL = "#161B22"
    BLUE  = "#58A6FF"
    GREEN = "#3FB950"
    AMBER = "#D29922"
    RED   = "#F85149"
    GREY  = "#8B949E"
    WHITE = "#E6EDF3"

    fig = plt.figure(figsize=(14, 9), facecolor=DARK)
    fig.suptitle(
        "SISTEMA DE MONITORAMENTO — MISSAO ESPACIAL EXPERIMENTAL",
        color=WHITE, fontsize=13, fontweight="bold", y=0.97
    )

    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.55, wspace=0.35,
                           left=0.07, right=0.97, top=0.92, bottom=0.07)

    def ax_estilo(ax, titulo):
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=GREY, labelsize=8)
        ax.set_title(titulo, color=WHITE, fontsize=9, fontweight="bold", pad=6)
        ax.set_xlabel("Ciclo", color=GREY, fontsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#30363D")
        ax.grid(color="#21262D", linestyle="--", linewidth=0.6)

    # 1. Temperatura
    ax1 = fig.add_subplot(gs[0, 0])
    ax_estilo(ax1, "Temperatura (C)")
    ax1.plot(ciclos, temps, color=AMBER, linewidth=1.8, label="Temperatura")
    ax1.axhline(LIMIARES["temperatura_alerta"],  color=AMBER, linestyle=":", linewidth=1, alpha=0.7, label=f"Alerta {LIMIARES['temperatura_alerta']}C")
    ax1.axhline(LIMIARES["temperatura_critica"], color=RED,   linestyle="--", linewidth=1, alpha=0.8, label=f"Critico {LIMIARES['temperatura_critica']}C")
    ax1.set_ylabel("Graus Celsius", color=GREY, fontsize=8)
    ax1.legend(fontsize=7, facecolor=PANEL, edgecolor="#30363D", labelcolor=WHITE)

    # 2. Energia
    ax2 = fig.add_subplot(gs[0, 1])
    ax_estilo(ax2, "Nivel de Energia (%)")
    ax2.plot(ciclos, energias, color=GREEN, linewidth=1.8, label="Energia")
    ax2.axhline(LIMIARES["energia_alerta"],  color=AMBER, linestyle=":", linewidth=1, alpha=0.7, label=f"Alerta {LIMIARES['energia_alerta']}%")
    ax2.axhline(LIMIARES["energia_critica"], color=RED,   linestyle="--", linewidth=1, alpha=0.8, label=f"Critico {LIMIARES['energia_critica']}%")
    ax2.set_ylabel("Percentual (%)", color=GREY, fontsize=8)
    ax2.set_ylim(0, 105)
    ax2.legend(fontsize=7, facecolor=PANEL, edgecolor="#30363D", labelcolor=WHITE)

    # 3. Qualidade do Sinal
    ax3 = fig.add_subplot(gs[1, 0])
    ax_estilo(ax3, "Qualidade do Sinal (%)")
    ax3.plot(ciclos, sinais, color=BLUE, linewidth=1.8, label="Sinal")
    ax3.axhline(LIMIARES["sinal_alerta"],  color=AMBER, linestyle=":", linewidth=1, alpha=0.7, label=f"Alerta {LIMIARES['sinal_alerta']}%")
    ax3.axhline(LIMIARES["sinal_critico"], color=RED,   linestyle="--", linewidth=1, alpha=0.8, label=f"Critico {LIMIARES['sinal_critico']}%")
    ax3.set_ylabel("Percentual (%)", color=GREY, fontsize=8)
    ax3.set_ylim(0, 105)
    ax3.legend(fontsize=7, facecolor=PANEL, edgecolor="#30363D", labelcolor=WHITE)

    # 4. Pressao
    ax4 = fig.add_subplot(gs[1, 1])
    ax_estilo(ax4, "Pressao Interna (kPa)")
    ax4.plot(ciclos, pressoes, color="#BC8CFF", linewidth=1.8)
    ax4.set_ylabel("kPa", color=GREY, fontsize=8)

    # 5. Status dos Modulos (ultimo ciclo)
    ax5 = fig.add_subplot(gs[2, :])
    ax5.set_facecolor(PANEL)
    ax5.set_title("Status dos Modulos — Ultimo Ciclo", color=WHITE, fontsize=9, fontweight="bold", pad=6)
    ax5.axis("off")
    for spine in ax5.spines.values():
        spine.set_edgecolor("#30363D")

    ultimo = historico_dados[-1]
    modulos_status = ultimo["modulos"]
    cor_status = {"OPERACIONAL": GREEN, "DEGRADADO": AMBER, "FALHA": RED}

    x_pos = [i / len(MODULOS) + 0.05 for i in range(len(MODULOS))]
    for i, (modulo, status) in enumerate(modulos_status.items()):
        cor = cor_status.get(status, GREY)
        ax5.add_patch(plt.Rectangle((x_pos[i] - 0.01, 0.15), 0.17, 0.6,
                                     facecolor=cor, alpha=0.15,
                                     transform=ax5.transAxes))
        ax5.text(x_pos[i] + 0.075, 0.62, modulo, ha="center", va="center",
                 transform=ax5.transAxes, color=WHITE, fontsize=8, fontweight="bold")
        ax5.text(x_pos[i] + 0.075, 0.35, status, ha="center", va="center",
                 transform=ax5.transAxes, color=cor, fontsize=9, fontweight="bold")

    ts = ultimo["timestamp"]
    fig.text(0.99, 0.01, f"Ultima atualizacao: {ts}  |  Ciclos monitorados: {len(ciclos)}",
             ha="right", va="bottom", color=GREY, fontsize=7)

    plt.savefig(nome_arquivo, dpi=150, facecolor=DARK)
    plt.close()
    print(f"\nDashboard salvo: {nome_arquivo}")


# ---------------------------------------------------------------------------
# EXIBICAO NO TERMINAL
# ---------------------------------------------------------------------------

def exibir_terminal(dados, alertas, decisoes):
    SEP = "-" * 60

    print(f"\n{'=' * 60}")
    print(f"  CICLO {dados['ciclo']:03d}  |  {dados['timestamp']}")
    print('=' * 60)

    print(f"\n  PARAMETROS OPERACIONAIS")
    print(SEP)
    print(f"  Temperatura   : {dados['temperatura']:>6.1f} C")
    print(f"  Energia       : {dados['energia']:>6.1f} %")
    print(f"  Sinal         : {dados['sinal']:>6.1f} %")
    print(f"  Pressao       : {dados['pressao']:>6.2f} kPa")
    print(f"  Velocidade    : {dados['velocidade']:>6.3f} km/s")

    print(f"\n  STATUS DOS MODULOS")
    print(SEP)
    for modulo, status in dados["modulos"].items():
        indicador = "[OK]" if status == "OPERACIONAL" else "[!!]" if status == "DEGRADADO" else "[XX]"
        print(f"  {indicador} {modulo:<20} {status}")

    if alertas:
        print(f"\n  ALERTAS GERADOS ({len(alertas)})")
        print(SEP)
        for a in alertas:
            print(f"  [{a['nivel']}] {a['parametro']}: {a['valor']}")
            print(f"    -> {a['acao']}")
    else:
        print(f"\n  SEM ALERTAS — Todos os parametros nominais.")

    if decisoes:
        print(f"\n  DECISOES AUTOMATIZADAS")
        print(SEP)
        for tipo, descricao in decisoes:
            print(f"  [{tipo}] {descricao}")


# ---------------------------------------------------------------------------
# LOOP PRINCIPAL
# ---------------------------------------------------------------------------

def executar_monitoramento(n_ciclos=20, intervalo_segundos=0.4):
    print("\n" + "=" * 60)
    print("  INICIANDO SISTEMA DE MONITORAMENTO")
    print("  Missao Espacial Experimental — Global Solution 2026")
    print("  Integrantes:")
    print("    Gabriel Jurado Nogueira       RM: 571236")
    print("    Vinicius Torralles F. Conduta RM: 570911")
    print("    Mariana Carminato             RM: 573258")
    print("=" * 60)
    time.sleep(0.5)

    simulador = SimuladorMissao()
    alertas_sys = SistemaAlertas()
    decisao_sys = SistemaDecisao()

    historico = []

    for _ in range(n_ciclos):
        dados    = simulador.coletar()
        alertas  = alertas_sys.avaliar(dados)
        decisoes = decisao_sys.decidir(dados, alertas)

        exibir_terminal(dados, alertas, decisoes)
        historico.append(dados)
        time.sleep(intervalo_segundos)

    # Relatorio final
    total_alertas  = len(alertas_sys.historico)
    criticos       = sum(1 for a in alertas_sys.historico if a["nivel"] == "CRITICO")
    atencoes       = total_alertas - criticos

    print("\n" + "=" * 60)
    print("  RELATORIO FINAL DA MISSAO")
    print("=" * 60)
    print(f"  Ciclos monitorados : {n_ciclos}")
    print(f"  Total de alertas   : {total_alertas}")
    print(f"  Alertas criticos   : {criticos}")
    print(f"  Alertas de atencao : {atencoes}")
    print(f"  Status final:")
    for modulo, status in historico[-1]["modulos"].items():
        print(f"    {modulo:<22} {status}")
    print("=" * 60)

    gerar_dashboard(historico)
    print("\nMonitoramento concluido.")


if __name__ == "__main__":
    executar_monitoramento(n_ciclos=20, intervalo_segundos=0.4)
