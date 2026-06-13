#!/usr/bin/env python3
"""
Script de Avaliação de Portabilidade — Fase 3
Projeto: KAREN JONES — Qualidade de Software / UnB FCTE
Métricas: PO-1.1, PO-1.2, PO-2.1, PO-2.2, PO-3.1, PO-3.2, PO-3.3
Subcaracterísticas: Adaptabilidade e Instalabilidade (ISO/IEC 25010)

Passos executados:
  Passo 1 — Preparação do ambiente
  Passo 2 — Testes de Instalabilidade (5 repetições por ambiente)
  Passo 3 — Testes de Adaptabilidade
  Passo 4 — Consolidação e cálculo de métricas
"""

import os
import sys
import csv
import json
import time
import shutil
import platform
import datetime
import subprocess
import statistics
import urllib.request
from pathlib import Path

# ── Configurações gerais ─────────────────────────────────────────────────────

REPETICOES = 5
MODELO = "qwen2.5:3b"
PROMPT_ADAPTABILIDADE = "Explique o que é inteligência artificial em uma frase."
OLLAMA_API = "http://localhost:11434/api/generate"
OLLAMA_API_TAGS = "http://localhost:11434/api/tags"

AMBIENTE = platform.system()  # "Windows" ou "Linux"
NOME_AMBIENTE = "Windows 11" if AMBIENTE == "Windows" else "Zorin OS 18.1 Core"

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = Path("tests/resultados/portabilidade")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_INSTALABILIDADE = OUTPUT_DIR / f"instalabilidade_{TIMESTAMP}.csv"
CSV_ADAPTABILIDADE = OUTPUT_DIR / f"adaptabilidade_{TIMESTAMP}.csv"
CSV_CONSOLIDACAO = OUTPUT_DIR / f"consolidacao_{TIMESTAMP}.csv"
LOG_FILE = OUTPUT_DIR / f"log_portabilidade_{TIMESTAMP}.txt"

# ── Logger ───────────────────────────────────────────────────────────────────

class Logger:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._init_file()

    def _init_file(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("  AVALIAÇÃO DE PORTABILIDADE — FASE 3\n")
            f.write(f"  Projeto  : KAREN JONES — Qualidade de Software / UnB FCTE\n")
            f.write(f"  Ambiente : {NOME_AMBIENTE} ({AMBIENTE})\n")
            f.write(f"  Início   : {datetime.datetime.now().isoformat()}\n")
            f.write("=" * 70 + "\n\n")

    def _write(self, level: str, msg: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{level:7s}] {msg}"
        print(line)
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def info(self, msg):  self._write("INFO",    msg)
    def ok(self, msg):    self._write("OK",      msg)
    def warn(self, msg):  self._write("WARN",    msg)
    def error(self, msg): self._write("ERROR",   msg)
    def step(self, msg):
        sep = "-" * 70
        self._write("STEP",  msg)
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(sep + "\n")

    def section(self, title: str):
        line = "\n" + "=" * 70
        subtitle = f"  {title}"
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(line + "\n" + subtitle + "\n" + "=" * 70 + "\n")
        print(line + "\n" + subtitle + "\n" + "=" * 70)

    def metric(self, metric_id: str, value, criterion: str, passed: bool):
        status = "✓ PASSOU" if passed else "✗ FALHOU"
        msg = f"[{metric_id}] Valor={value} | Critério={criterion} | {status}"
        self._write("MÉTRICA", msg)


log = Logger(LOG_FILE)

# ── Utilitários de sistema ───────────────────────────────────────────────────

def run(cmd: list[str], timeout: int = 300) -> tuple[int, str, str]:
    """Executa um comando e retorna (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except FileNotFoundError:
        return -1, "", f"Comando não encontrado: {cmd[0]}"


def ollama_instalado() -> bool:
    code, out, _ = run(["ollama", "--version"])
    return code == 0 and bool(out)


def ollama_versao() -> str:
    _, out, _ = run(["ollama", "--version"])
    return out or "desconhecida"


def disco_livre_gb() -> float:
    stat = shutil.disk_usage(Path.home())
    return round(stat.free / (1024 ** 3), 2)


def processos_ollama() -> list[str]:
    """Lista PIDs de processos ollama em execução."""
    if AMBIENTE == "Windows":
        code, out, _ = run(["tasklist", "/FI", "IMAGENAME eq ollama.exe"])
        return [l for l in out.splitlines() if "ollama" in l.lower()]
    else:
        code, out, _ = run(["pgrep", "-l", "ollama"])
        return out.splitlines() if code == 0 else []


def arquivos_residuais() -> list[str]:
    """Verifica arquivos residuais do Ollama após desinstalação."""
    residuais = []
    caminhos = []
    if AMBIENTE == "Windows":
        userprofile = os.environ.get("USERPROFILE", "")
        caminhos = [
            Path(userprofile) / ".ollama",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Ollama",
            Path(os.environ.get("PROGRAMFILES", "")) / "Ollama",
        ]
    else:
        home = Path.home()
        caminhos = [
            home / ".ollama",
            Path("/usr/local/bin/ollama"),
            Path("/usr/bin/ollama"),
        ]
    for p in caminhos:
        if p.exists():
            residuais.append(str(p))
    return residuais


def instalar_ollama() -> tuple[bool, float, str]:
    """Instala o Ollama. Retorna (sucesso, tempo_s, erro)."""
    inicio = time.time()
    if AMBIENTE == "Windows":
        # Download do instalador e execução via PowerShell
        ps_cmd = ["powershell", "-Command",
                  "irm https://ollama.com/install.ps1 | iex"]
        code, _, err = run(ps_cmd, timeout=300)
    else:
        bash_cmd = ["bash", "-c",
                    "curl -fsSL https://ollama.com/install.sh | sh"]
        code, _, err = run(bash_cmd, timeout=300)
    tempo = round(time.time() - inicio, 2)
    sucesso = code == 0 and ollama_instalado()
    return sucesso, tempo, err if not sucesso else ""


def desinstalar_ollama() -> tuple[bool, float, str]:
    """Desinstala o Ollama. Retorna (sucesso, tempo_s, erro)."""
    inicio = time.time()
    # Para o serviço se estiver rodando
    if AMBIENTE == "Windows":
        run(["taskkill", "/F", "/IM", "ollama.exe"])
        code, _, err = run(
            ["powershell", "-Command",
             "Get-Package Ollama | Uninstall-Package -Force"],
            timeout=120
        )
        # Fallback: remoção manual
        if code != 0:
            userprofile = os.environ.get("USERPROFILE", "")
            pasta = Path(userprofile) / ".ollama"
            if pasta.exists():
                shutil.rmtree(pasta, ignore_errors=True)
    else:
        run(["pkill", "-f", "ollama"])
        time.sleep(2)
        # Remove binário
        run(["sudo", "rm", "-f", "/usr/local/bin/ollama", "/usr/bin/ollama"])
        # Remove dados
        home = Path.home()
        pasta = home / ".ollama"
        if pasta.exists():
            shutil.rmtree(pasta, ignore_errors=True)
        code = 0
        err = ""
    tempo = round(time.time() - inicio, 2)
    residuais = arquivos_residuais()
    sucesso = not residuais
    return sucesso, tempo, str(residuais) if residuais else ""


def iniciar_servidor_ollama():
    """Garante que o servidor Ollama está rodando."""
    if processos_ollama():
        return  # já rodando
    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(5)  # aguarda inicialização


def baixar_modelo() -> bool:
    """Faz pull do modelo. Retorna True se sucesso."""
    code, _, _ = run(["ollama", "pull", MODELO], timeout=600)
    return code == 0


def inferencia_api(prompt: str) -> tuple[bool, float, str]:
    """
    Executa inferência via API REST do Ollama.
    Retorna (sucesso, tempo_total_s, erro).
    """
    payload = json.dumps({
        "model": MODELO,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            OLLAMA_API,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        inicio = time.time()
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        tempo = round(time.time() - inicio, 2)
        return True, tempo, ""
    except Exception as e:
        return False, -1.0, str(e)


# ── Passo 1: Preparação ──────────────────────────────────────────────────────

def passo1_preparacao():
    log.section("PASSO 1 — Preparação do Ambiente")

    log.step("Verificando sistema operacional")
    log.info(f"SO detectado  : {NOME_AMBIENTE} ({platform.version()})")
    log.info(f"Arquitetura   : {platform.machine()}")
    log.info(f"Python        : {sys.version.split()[0]}")

    log.step("Verificando espaço em disco")
    gb = disco_livre_gb()
    log.info(f"Espaço livre  : {gb} GB")
    if gb < 5:
        log.warn("Espaço em disco baixo (< 5 GB). Download do modelo pode falhar.")

    log.step("Verificando processos em execução do Ollama")
    procs = processos_ollama()
    if procs:
        log.info(f"Processos Ollama ativos: {len(procs)}")
    else:
        log.info("Nenhum processo Ollama em execução.")

    log.step("Verificando residuais de instalações anteriores")
    res = arquivos_residuais()
    if res:
        log.warn(f"Residuais encontrados: {res}")
    else:
        log.ok("Nenhum residual encontrado. Ambiente limpo.")

    log.ok("Passo 1 concluído.")


# ── Passo 2: Testes de Instalabilidade ──────────────────────────────────────

def passo2_instalabilidade() -> list[dict]:
    log.section("PASSO 2 — Testes de Instalabilidade")
    log.info(f"Número de repetições: {REPETICOES}")
    log.info(f"Ambiente: {NOME_AMBIENTE}")

    registros = []

    with open(CSV_INSTALABILIDADE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ambiente", "tentativa",
            "tempo_instalacao_s", "status_instalacao", "erro_instalacao",
            "tempo_desinstalacao_s", "status_desinstalacao", "arquivos_residuais"
        ])
        writer.writeheader()

        for i in range(1, REPETICOES + 1):
            log.step(f"Tentativa {i}/{REPETICOES}")

            # Garante que Ollama NÃO está instalado
            if ollama_instalado():
                log.info("Ollama encontrado — desinstalando antes de iniciar...")
                desinstalar_ollama()

            # 2. Instalação
            log.info("Iniciando instalação do Ollama...")
            ok_inst, t_inst, err_inst = instalar_ollama()
            status_inst = "sucesso" if ok_inst else "falha"
            log.info(f"Instalação: {status_inst} em {t_inst}s")
            if err_inst:
                log.error(f"Erro instalação: {err_inst[:200]}")

            # 3. Verificação pós-instalação
            versao = ollama_versao() if ok_inst else "n/a"
            log.info(f"Versão verificada: {versao}")

            # 4. Desinstalação
            log.info("Iniciando desinstalação...")
            ok_desinst, t_desinst, err_desinst = desinstalar_ollama()
            status_desinst = "sucesso" if ok_desinst else "falha"
            log.info(f"Desinstalação: {status_desinst} em {t_desinst}s")

            res_paths = arquivos_residuais()
            residuais_str = ";".join(res_paths) if res_paths else "nenhum"

            row = {
                "ambiente": NOME_AMBIENTE,
                "tentativa": i,
                "tempo_instalacao_s": t_inst,
                "status_instalacao": status_inst,
                "erro_instalacao": err_inst[:300] if err_inst else "",
                "tempo_desinstalacao_s": t_desinst,
                "status_desinstalacao": status_desinst,
                "arquivos_residuais": residuais_str,
            }
            writer.writerow(row)
            registros.append(row)

    log.ok(f"Passo 2 concluído. CSV salvo: {CSV_INSTALABILIDADE}")
    return registros


# ── Passo 3: Testes de Adaptabilidade ───────────────────────────────────────

def passo3_adaptabilidade() -> list[dict]:
    log.section("PASSO 3 — Testes de Adaptabilidade")

    # 1. Garantir instalação e servidor
    if not ollama_instalado():
        log.info("Ollama não instalado. Instalando para testes de adaptabilidade...")
        ok, _, err = instalar_ollama()
        if not ok:
            log.error(f"Falha ao instalar Ollama: {err}")
            return []

    log.info("Iniciando servidor Ollama...")
    iniciar_servidor_ollama()
    time.sleep(3)

    # 2. Download do modelo
    log.step("Baixando modelo Qwen 2.5 3B")
    ok_pull = baixar_modelo()
    if not ok_pull:
        log.error("Falha ao baixar o modelo. Abortando testes de adaptabilidade.")
        return []
    log.ok(f"Modelo '{MODELO}' disponível.")

    # 3. Execução dos testes de inferência (5 repetições)
    log.step(f"Executando {REPETICOES} inferências para medir desempenho")
    registros = []

    with open(CSV_ADAPTABILIDADE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ambiente", "tentativa", "prompt",
            "tempo_inferencia_s", "status", "erro"
        ])
        writer.writeheader()

        for i in range(1, REPETICOES + 1):
            log.info(f"Inferência {i}/{REPETICOES}")
            ok, tempo, err = inferencia_api(PROMPT_ADAPTABILIDADE)
            status = "sucesso" if ok else "falha"
            if ok:
                log.info(f"  Tempo: {tempo}s — {status}")
            else:
                log.error(f"  Falha: {err[:200]}")

            row = {
                "ambiente": NOME_AMBIENTE,
                "tentativa": i,
                "prompt": PROMPT_ADAPTABILIDADE,
                "tempo_inferencia_s": tempo,
                "status": status,
                "erro": err[:300] if err else "",
            }
            writer.writerow(row)
            registros.append(row)

    log.ok(f"Passo 3 concluído. CSV salvo: {CSV_ADAPTABILIDADE}")
    return registros


# ── Passo 4: Consolidação e cálculo de métricas ─────────────────────────────

def passo4_consolidacao(reg_inst: list[dict], reg_adapt: list[dict]):
    log.section("PASSO 4 — Consolidação e Cálculo de Métricas")

    resultados = {}

    # ── Instalabilidade ───────────────────────────────────────────────────

    if reg_inst:
        total = len(reg_inst)
        ok_inst = sum(1 for r in reg_inst if r["status_instalacao"] == "sucesso")
        ok_desinst = sum(1 for r in reg_inst if r["status_desinstalacao"] == "sucesso")
        tempos_inst = [r["tempo_instalacao_s"] for r in reg_inst if r["status_instalacao"] == "sucesso"]
        tempos_desinst = [r["tempo_desinstalacao_s"] for r in reg_inst if r["status_desinstalacao"] == "sucesso"]
        residuais = [r for r in reg_inst if r["arquivos_residuais"] != "nenhum"]

        taxa_inst = round(ok_inst / total, 4)
        taxa_desinst = round(ok_desinst / total, 4)
        tempo_medio_inst = round(statistics.mean(tempos_inst), 2) if tempos_inst else -1
        tempo_medio_desinst = round(statistics.mean(tempos_desinst), 2) if tempos_desinst else -1

        # Erros por tipo (PO-3.3)
        tipos_erro = {}
        for r in reg_inst:
            if r["erro_instalacao"]:
                chave = r["erro_instalacao"][:60]
                tipos_erro[chave] = tipos_erro.get(chave, 0) + 1
        taxa_max_falha_tipo = max(
            (v / total for v in tipos_erro.values()), default=0.0
        )

        resultados.update({
            "PO-2.1_taxa_sucesso_instalacao": taxa_inst,
            "PO-2.1_criterio": ">= 0.95",
            "PO-2.1_passou": taxa_inst >= 0.95,
            "PO-2.2_taxa_sucesso_desinstalacao": taxa_desinst,
            "PO-2.2_criterio": ">= 0.90",
            "PO-2.2_passou": taxa_desinst >= 0.90,
            "PO-3.1_taxa_sucesso_por_ambiente": taxa_inst,
            "PO-3.1_criterio": ">= 0.95",
            "PO-3.1_passou": taxa_inst >= 0.95,
            "PO-3.3_tempo_medio_instalacao_s": tempo_medio_inst,
            "PO-3.3_tempo_medio_desinstalacao_s": tempo_medio_desinst,
            "PO-3.3_taxa_max_falha_por_tipo": round(taxa_max_falha_tipo, 4),
            "PO-3.3_criterio": "taxa_max_falha_por_tipo <= 0.02",
            "PO-3.3_passou": taxa_max_falha_tipo <= 0.02,
        })

        # Log das métricas de instalabilidade
        log.metric("PO-2.1", f"{taxa_inst:.1%}", ">= 95%", taxa_inst >= 0.95)
        log.metric("PO-2.2", f"{taxa_desinst:.1%}", ">= 90%", taxa_desinst >= 0.90)
        log.metric("PO-3.1", f"{taxa_inst:.1%} no {NOME_AMBIENTE}", ">= 95%", taxa_inst >= 0.95)
        log.metric(
            "PO-3.3",
            f"taxa_erro_max={taxa_max_falha_tipo:.1%}, t_inst_medio={tempo_medio_inst}s",
            "taxa_erro_max <= 2%",
            taxa_max_falha_tipo <= 0.02,
        )

    # ── Adaptabilidade ────────────────────────────────────────────────────

    if reg_adapt:
        total_a = len(reg_adapt)
        ok_a = sum(1 for r in reg_adapt if r["status"] == "sucesso")
        tempos_a = [r["tempo_inferencia_s"] for r in reg_adapt if r["status"] == "sucesso"]

        taxa_exec = round(ok_a / total_a, 4)
        tempo_medio_inf = round(statistics.mean(tempos_a), 2) if tempos_a else -1

        # PO-1.2: Desvio de desempenho — comparação entre plataformas.
        # Como este script roda em um SO por vez, registramos o tempo médio
        # para posterior comparação manual ou combinada.
        resultados.update({
            "PO-1.1_taxa_execucoes_sem_falha": taxa_exec,
            "PO-1.1_criterio": ">= 0.99",
            "PO-1.1_passou": taxa_exec >= 0.99,
            "PO-1.2_tempo_medio_inferencia_s": tempo_medio_inf,
            "PO-1.2_nota": (
                "Desvio relativo entre plataformas calculado ao "
                "combinar resultados de Windows e Linux."
            ),
        })

        log.metric("PO-1.1", f"{taxa_exec:.1%}", ">= 99%", taxa_exec >= 0.99)
        log.info(
            f"[PO-1.2] Tempo médio inferência ({NOME_AMBIENTE}): "
            f"{tempo_medio_inf}s — combine com outro SO para calcular desvio."
        )

    # ── PO-3.2 (desvio relativo entre ambientes) ──────────────────────────
    log.info(
        "[PO-3.2] Desvio relativo entre ambientes = |Taxa(A) - Taxa(B)| / "
        "Taxa_média. Calcule combinando CSVs de ambos os ambientes."
    )
    resultados["PO-3.2_nota"] = (
        "Combine os CSVs de Windows e Linux para calcular "
        "|Taxa(A)-Taxa(B)|/Taxa_media <= 0.05"
    )

    # ── Salva CSV de consolidação ─────────────────────────────────────────
    with open(CSV_CONSOLIDACAO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ambiente", "metrica", "valor", "criterio", "passou"])
        writer.writeheader()
        mapeamento = [
            ("PO-1.1", resultados.get("PO-1.1_taxa_execucoes_sem_falha", "N/A"),
             ">= 0.99", resultados.get("PO-1.1_passou", "N/A")),
            ("PO-1.2_tempo_medio_s", resultados.get("PO-1.2_tempo_medio_inferencia_s", "N/A"),
             "base p/ desvio entre SOs", "N/A (cruzar com outro SO)"),
            ("PO-2.1", resultados.get("PO-2.1_taxa_sucesso_instalacao", "N/A"),
             ">= 0.95", resultados.get("PO-2.1_passou", "N/A")),
            ("PO-2.2", resultados.get("PO-2.2_taxa_sucesso_desinstalacao", "N/A"),
             ">= 0.90", resultados.get("PO-2.2_passou", "N/A")),
            ("PO-3.1", resultados.get("PO-3.1_taxa_sucesso_por_ambiente", "N/A"),
             ">= 0.95", resultados.get("PO-3.1_passou", "N/A")),
            ("PO-3.2", "ver nota", "<= 0.05 (cruzar ambientes)", "N/A (cruzar com outro SO)"),
            ("PO-3.3_taxa_erro_tipo", resultados.get("PO-3.3_taxa_max_falha_por_tipo", "N/A"),
             "<= 0.02", resultados.get("PO-3.3_passou", "N/A")),
        ]
        for metrica, valor, criterio, passou in mapeamento:
            writer.writerow({
                "ambiente": NOME_AMBIENTE,
                "metrica": metrica,
                "valor": valor,
                "criterio": criterio,
                "passou": passou,
            })

    log.ok(f"CSV de consolidação salvo: {CSV_CONSOLIDACAO}")

    # ── Resumo final ──────────────────────────────────────────────────────
    log.section("RESUMO FINAL")
    aprovadas = sum(
        1 for k, v in resultados.items()
        if k.endswith("_passou") and v is True
    )
    reprovadas = sum(
        1 for k, v in resultados.items()
        if k.endswith("_passou") and v is False
    )
    log.info(f"Métricas com resultado: {aprovadas + reprovadas}")
    log.info(f"  ✓ Aprovadas : {aprovadas}")
    log.info(f"  ✗ Reprovadas: {reprovadas}")
    log.info(f"Arquivos gerados:")
    log.info(f"  LOG  : {LOG_FILE}")
    log.info(f"  CSVs : {CSV_INSTALABILIDADE}")
    log.info(f"         {CSV_ADAPTABILIDADE}")
    log.info(f"         {CSV_CONSOLIDACAO}")


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 70)
    print("  AVALIAÇÃO DE PORTABILIDADE — FASE 3")
    print(f"  Ambiente: {NOME_AMBIENTE}")
    print("=" * 70 + "\n")

    passo1_preparacao()
    reg_inst   = passo2_instalabilidade()
    reg_adapt  = passo3_adaptabilidade()
    passo4_consolidacao(reg_inst, reg_adapt)

    print(f"\nLog completo: {LOG_FILE}\n")


if __name__ == "__main__":
    main()
