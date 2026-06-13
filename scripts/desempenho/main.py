import os
import subprocess
import sys
import time
import csv
import statistics
from datetime import datetime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ns_to_ms(ns):
    return round(ns / 1_000_000, 2)


def summarize(values):
    if not values:
        return None, None, None
    mean = round(statistics.mean(values), 2)
    median = round(statistics.median(values), 2)
    desvio = round(statistics.pstdev(values), 2) if len(values) > 1 else 0.0
    return mean, median, desvio


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def to_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Consolidação: ED-1.x e ED-2.x  (resultados_estatisticas.csv do finalTTFT)
# ---------------------------------------------------------------------------

def load_ed1_ed2(stats_path):
    """
    Lê resultados_estatisticas.csv gerado pelo finalTTFT.py e devolve um
    dicionário  metric -> {"mean", "median", "desvio"}.
    """
    rows = read_csv(stats_path)
    data = {}
    for row in rows:
        data[row["metric"]] = {
            "mean":   to_float(row.get("mean")),
            "median": to_float(row.get("median")),
            "desvio": to_float(row.get("desvio")),
        }
    return data


def load_mlt_from_stats(stats):
    """
    ED-1.3 – Model Load Time (MLT).
    Lê diretamente do dict já carregado por load_ed1_ed2(), que usa
    resultados_estatisticas.csv — já com menor/maior TTFT descartados.
    """
    mlt = stats.get("load_duration_ms", {})
    return mlt.get("mean"), mlt.get("median"), mlt.get("desvio")


# ---------------------------------------------------------------------------
# Consolidação: ED-3.x  (capacity_resumo.csv do capacityTTFT)
# ---------------------------------------------------------------------------

def load_ed3(resumo_path):
    """
    Lê capacity_resumo.csv e devolve lista de dicts com as métricas ED-3.1 e ED-3.2.
    """
    return read_csv(resumo_path)


# ---------------------------------------------------------------------------
# Geração do CSV final
# ---------------------------------------------------------------------------

FIELDNAMES = [
    "ed_id",
    "nome",
    "dimensao",
    "descricao",
    "contexto",
    "mean",
    "median",
    "desvio",
    "unidade",
    "observacao",
]


def build_rows(stats, mlt_mean, mlt_median, mlt_desvio, ed3_rows):
    rows = []

    # ---- ED-1.1 TTFT -------------------------------------------------------
    ttft = stats.get("ttft_ms", {})
    rows.append({
        "ed_id":      "ED-1.1",
        "nome":       "Time to First Token (TTFT)",
        "dimensao":   "Comportamento Temporal",
        "descricao":  "Tempo entre o envio do prompt e a chegada do primeiro token de resposta",
        "contexto":   "prompt fixo ~256 tokens",
        "mean":       ttft.get("mean"),
        "median":     ttft.get("median"),
        "desvio":     ttft.get("desvio"),
        "unidade":    "ms",
        "observacao": "",
    })

    # ---- ED-1.2 TPS ---------------------------------------------------------
    tps = stats.get("tps", {})
    rows.append({
        "ed_id":      "ED-1.2",
        "nome":       "Tokens por Segundo (TPS)",
        "dimensao":   "Comportamento Temporal",
        "descricao":  "Taxa de geração de tokens após o primeiro token",
        "contexto":   "prompt fixo ~256 tokens",
        "mean":       tps.get("mean"),
        "median":     tps.get("median"),
        "desvio":     tps.get("desvio"),
        "unidade":    "tokens/s",
        "observacao": "",
    })

    # ---- ED-1.3 MLT ---------------------------------------------------------
    rows.append({
        "ed_id":      "ED-1.3",
        "nome":       "Latência de Carregamento do Modelo (MLT)",
        "dimensao":   "Comportamento Temporal",
        "descricao":  "Diferença entre tempo de carregamento do modelo e tempo de início da inferência",
        "contexto":   "prompt fixo ~256 tokens",
        "mean":       mlt_mean,
        "median":     mlt_median,
        "desvio":     mlt_desvio,
        "unidade":    "ms",
        "observacao": "Proxy: load_duration reportado pelo Ollama",
    })

    # ---- ED-2.1 RAM ---------------------------------------------------------
    ram = stats.get("peak_ollama_ram_used_mb", {})
    rows.append({
        "ed_id":      "ED-2.1",
        "nome":       "Consumo de RAM",
        "dimensao":   "Utilização de Recursos",
        "descricao":  "Máximo de memória RAM consumida durante a execução",
        "contexto":   "prompt fixo ~256 tokens",
        "mean":       ram.get("mean"),
        "median":     ram.get("median"),
        "desvio":     ram.get("desvio"),
        "unidade":    "MB",
        "observacao": "Pico de RAM do processo Ollama",
    })

    # ---- ED-2.2 CPU ---------------------------------------------------------
    cpu = stats.get("avg_ollama_cpu_percent", {})
    rows.append({
        "ed_id":      "ED-2.2",
        "nome":       "Uso Médio de CPU",
        "dimensao":   "Utilização de Recursos",
        "descricao":  "Percentual de utilização da CPU durante a execução",
        "contexto":   "prompt fixo ~256 tokens",
        "mean":       cpu.get("mean"),
        "median":     cpu.get("median"),
        "desvio":     cpu.get("desvio"),
        "unidade":    "%",
        "observacao": "CPU normalizada pelo número de núcleos",
    })

    # ---- ED-2.3 REI ---------------------------------------------------------
    rei = stats.get("rei", {})
    rows.append({
        "ed_id":      "ED-2.3",
        "nome":       "Índice de Eficiência de Recursos (REI)",
        "dimensao":   "Utilização de Recursos",
        "descricao":  "Relação entre a taxa de geração de tokens e o consumo de recursos (CPU * RAM)",
        "contexto":   "prompt fixo ~256 tokens",
        "mean":       rei.get("mean"),
        "median":     rei.get("median"),
        "desvio":     rei.get("desvio"),
        "unidade":    "tokens/s por (GB * %CPU)",
        "observacao": "REI = TPS / (RAM_GB * CPU%)",
    })

    # ---- ED-3.1 CSF ---------------------------------------------------------
    for r in ed3_rows:
        csf = to_float(r.get("csf"))
        ttft_mean = to_float(r.get("ttft_ms_mean"))
        ttft_med  = to_float(r.get("ttft_ms_median"))
        ttft_dev  = to_float(r.get("ttft_ms_desvio"))
        tokens    = r.get("prompt_eval_count_mean", "")
        label     = r.get("context_label", "")
        rows.append({
            "ed_id":      "ED-3.1",
            "nome":       "Fator de Escalonamento de Contexto (CSF)",
            "dimensao":   "Capacidade",
            "descricao":  "TTFT com diferentes tamanhos de contexto comparado com baseline ~256 tokens",
            "contexto":   f"{label} (~{tokens} tokens)",
            "mean":       ttft_mean,
            "median":     ttft_med,
            "desvio":     ttft_dev,
            "unidade":    "ms",
            "observacao": f"CSF={csf}" if csf is not None else "",
        })

    # ---- ED-3.2 KVCGR -------------------------------------------------------
    for r in ed3_rows:
        kvcgr    = to_float(r.get("kvcgr_mb_per_token"))
        peak_ram = to_float(r.get("peak_ollama_ram_used_mb_mean"))
        label    = r.get("context_label", "")
        tokens   = r.get("prompt_eval_count_mean", "")

        if kvcgr is None:
            obs = "baseline (sem delta)"
        else:
            obs = f"RAM pico={peak_ram} MB"

        rows.append({
            "ed_id":      "ED-3.2",
            "nome":       "Taxa de Crescimento do KV Cache (KVCGR)",
            "dimensao":   "Capacidade",
            "descricao":  "Crescimento de RAM de pico em relação ao baseline ~256 tokens, por token adicionado",
            "contexto":   f"{label} (~{tokens} tokens)",
            "mean":       kvcgr,
            "median":     None,
            "desvio":     None,
            "unidade":    "MB/token",
            "observacao": obs,
        })

    return rows


# ---------------------------------------------------------------------------
# Orquestração principal
# ---------------------------------------------------------------------------

def run_script(script_path, cwd, label):
    print(f"\n{'='*60}")
    print(f"  Executando: {label}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=cwd,
        check=False,
    )
    if result.returncode != 0:
        print(f"  [AVISO] {os.path.basename(script_path)} encerrou com código {result.returncode}")
    else:
        print(f"  [OK] {label} concluído.")
    return result.returncode


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    monitor_script  = os.path.join(script_dir, "monitor.py")
    ttft_script     = os.path.join(script_dir, "finalTTFT.py")
    capacity_script = os.path.join(script_dir, "capacityTTFT.py")

    for path in [monitor_script, ttft_script, capacity_script]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    # ------------------------------------------------------------------
    # Inicia monitor em background (única instância para os dois testes)
    # ------------------------------------------------------------------
    print("Iniciando monitor de recursos...")
    monitor_proc = subprocess.Popen(
        [sys.executable, monitor_script],
        cwd=script_dir,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    try:
        time.sleep(3)  # aguarda monitor estabilizar

        # ------------------------------------------------------------------
        # Fase 1 – Prompt fixo: TTFT / TPS / MLT / RAM / CPU / REI (ED-1 e ED-2)
        # ------------------------------------------------------------------
        run_script(ttft_script, script_dir, "Teste de prompt fixo (ED-1 / ED-2) — finalTTFT.py")

        # Pequena pausa entre os testes para o KV cache "esfriar"
        print("\nAguardando 5 s antes do teste de capacidade...")
        time.sleep(5)

        # ------------------------------------------------------------------
        # Fase 2 – Prompts com tamanhos variados: CSF / KVCGR (ED-3)
        # ------------------------------------------------------------------
        run_script(capacity_script, script_dir, "Teste de capacidade (ED-3) — capacityTTFT.py")

    except KeyboardInterrupt:
        print("\nInterrupção recebida. Encerrando processos...")
    finally:
        if monitor_proc.poll() is None:
            print("\nFinalizando monitor...")
            monitor_proc.terminate()
            try:
                monitor_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                monitor_proc.kill()
        print("Processos encerrados.")

    # ------------------------------------------------------------------
    # Consolidação dos resultados → resultados_desempenho.csv
    # ------------------------------------------------------------------
    print("\nConsolidando resultados em resultados_desempenho.csv ...")

    telemetria_dir = os.path.join(script_dir, "telemetria")
    stats_path  = os.path.join(telemetria_dir, "resultados_estatisticas.csv")
    resumo_path = os.path.join(telemetria_dir, "capacity_resumo.csv")
    output_path = os.path.join(script_dir, "resultados_desempenho.csv")

    # resultados_estatisticas.csv ja contem apenas runs com menor/maior TTFT descartados
    stats                      = load_ed1_ed2(stats_path)
    mlt_mean, mlt_med, mlt_dev = load_mlt_from_stats(stats)
    ed3_rows                   = load_ed3(resumo_path)

    rows = build_rows(stats, mlt_mean, mlt_med, mlt_dev, ed3_rows)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Salvo em: {output_path}")
    print(f"  Total de linhas: {len(rows)}")

    # ------------------------------------------------------------------
    # Resumo no terminal
    # ------------------------------------------------------------------
    print("\n=== RESUMO — resultados_desempenho.csv ===")
    header = f"{'ED':<8} | {'Contexto':<22} | {'Mean':>12} | {'Median':>10} | {'Desvio':>8} | Unidade"
    print(header)
    print("-" * len(header))
    for r in rows:
        mean   = r['mean']   if r['mean']   is not None else "-"
        median = r['median'] if r['median'] is not None else "-"
        desvio = r['desvio'] if r['desvio'] is not None else "-"
        print(
            f"{r['ed_id']:<8} | {str(r['contexto']):<22} | "
            f"{str(mean):>12} | {str(median):>10} | {str(desvio):>8} | {r['unidade']}"
        )


if __name__ == "__main__":
    main()