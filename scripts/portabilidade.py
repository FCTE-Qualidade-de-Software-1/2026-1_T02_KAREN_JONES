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

# Garante que OUTPUT_DIR é absoluto para evitar ambiguidade com CWD
OUTPUT_DIR = Path("tests/resultados/portabilidade").resolve()
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

def run(cmd: list[str], timeout: int = 900) -> tuple[int, str, str]:
    """Executa um comando e retorna (returncode, stdout, stderr)."""
    try:
        # Se for um comando de instalação ou download, evita o capture_output
        # para não congelar o script com buffers interativos ou interfaces gráficas
        if any(x in str(cmd) for x in ["install.ps1", "pull", "Uninstall-Package"]):
            result = subprocess.run(cmd, timeout=timeout)
            return result.returncode, "Executado diretamente", ""
        
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
    if code != 0:
        return False
    # No Windows, "Warning: could not connect to a running Ollama instance"
    # aparece mesmo com Ollama instalado — filtra apenas essa linha
    import re
    linhas = [l for l in out.splitlines()
              if not l.strip().startswith("Warning: could not connect")]
    # Busca qualquer versão X.Y.Z na linha restante
    return any(re.search(r"\d+\.\d+\.\d+", l) for l in linhas)


def ollama_versao() -> str:
    _, out, _ = run(["ollama", "--version"])
    import re
    linhas = [l for l in out.splitlines()
              if not l.strip().startswith("Warning: could not connect")]
    for l in linhas:
        m = re.search(r"(\d+\.\d+\.\d+)", l)
        if m:
            return m.group(1)
    return "desconhecida"


def disco_livre_gb() -> float:
    stat = shutil.disk_usage(Path.home())
    return round(stat.free / (1024 ** 3), 2)


def sudo_disponivel() -> bool:
    """Verifica se sudo -n (não interativo) está disponível."""
    if AMBIENTE == "Windows":
        return True  # Windows não usa sudo
    code, _, _ = run(["sudo", "-n", "true"], timeout=10)
    return code == 0


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
    # Verificação extra: `command -v` detecta o binário mesmo em path não listado
    if AMBIENTE != "Windows":
        code, out, _ = run(["bash", "-c", "command -v ollama"], timeout=10)
        if code == 0 and out.strip():
            caminho = out.strip()
            if caminho not in residuais:
                residuais.append(caminho)
    return residuais


def limpar_caches_sistema():
    """Limpa caches do SO que podem contaminar medições de instalação.
    Operações que exigem sudo são tentadas com sudo -n (não interativo);
    se não disponível, apenas um aviso é emitido."""
    log.step("Limpando caches do sistema")
    sudo_prefix = ["sudo", "-n"]
    if AMBIENTE == "Windows":
        temp = os.environ.get("TEMP", "")
        if temp:
            temp_path = Path(temp)
            if temp_path.exists():
                for item in temp_path.iterdir():
                    try:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item, ignore_errors=True)
                    except Exception:
                        pass
        ps_cache = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "PowerShell"
        if ps_cache.exists():
            shutil.rmtree(ps_cache, ignore_errors=True)
    else:
        # Limpa cache de pacotes apt (instalador do Ollama adiciona repositórios)
        for cmd in [sudo_prefix + ["apt-get", "clean"],
                    sudo_prefix + ["apt-get", "autoclean"]]:
            code, _, _ = run(cmd, timeout=120)
            if code != 0:
                log.warn(f"apt-get limpeza falhou (código {code}) — pode exigir sudo")
        # Limpa diretórios temporários
        for cmd in [sudo_prefix + ["rm", "-rf", "/tmp/*"],
                    sudo_prefix + ["rm", "-rf", "/var/tmp/*"]]:
            code, _, _ = run(cmd, timeout=30)
            if code != 0:
                log.warn(f"Limpeza de temporários falhou (código {code})")
        # Limpa caches de download do usuário
        home = Path.home()
        for cache_dir in [".cache/curl", ".cache/pip", ".cache/wget"]:
            p = home / cache_dir
            if p.exists():
                shutil.rmtree(p, ignore_errors=True)
        # Limpa cache de DNS (systemd-resolved)
        code, _, _ = run(sudo_prefix + ["resolvectl", "flush-caches"], timeout=10)
        if code != 0:
            log.warn("Limpeza de cache DNS falhou — pode exigir sudo")
        # Limpa page cache do kernel para evitar cache de arquivos baixados
        code, _, _ = run(
            sudo_prefix + ["sh", "-c", "sync && echo 3 > /proc/sys/vm/drop_caches"],
            timeout=30
        )
        if code != 0:
            log.warn("Limpeza de page cache falhou — pode exigir sudo")
    log.ok("Caches do sistema limpos.")


def forcar_limpeza() -> bool:
    """Força limpeza total do ambiente: mata processos, remove binários, dados e caches."""
    log.step("Forçando limpeza completa do ambiente")

    # 1. Mata processos ollama com força
    if AMBIENTE == "Windows":
        run(["taskkill", "/F", "/IM", "ollama.exe"], timeout=30)
    else:
        run(["pkill", "-9", "-f", "ollama"], timeout=30)
        time.sleep(1)

    # 2. Remove binários
    if AMBIENTE == "Windows":
        for var in ["LOCALAPPDATA", "PROGRAMFILES", "PROGRAMFILES(X86)"]:
            caminho = Path(os.environ.get(var, "")) / "Ollama"
            if caminho.exists():
                shutil.rmtree(caminho, ignore_errors=True)
    else:
        # Tenta remover via sudo -n
        code, out, err = run(["sudo", "-n", "rm", "-f", "/usr/local/bin/ollama", "/usr/bin/ollama"], timeout=30)
        if code != 0:
            log.warn(f"Remoção do binário via sudo -n falhou (código {code})")
        # Verifica se ollama ainda está acessível em PATH (independe do path específico)
        code_which, out_which, _ = run(["bash", "-c", "command -v ollama"], timeout=10)
        if code_which == 0:
            caminho_ollama = out_which.strip()
            log.warn(f"ollama ainda acessível em '{caminho_ollama}' — tentando remoção direta...")
            try:
                Path(caminho_ollama).unlink(missing_ok=True)
            except PermissionError:
                pass
            # Última tentativa: kill + rm via pkill wrapper
            run(["sudo", "-n", "sh", "-c", f"rm -f {caminho_ollama} /usr/local/bin/ollama /usr/bin/ollama"], timeout=30)
            # Verificação final
            code_final, _, _ = run(["bash", "-c", "command -v ollama"], timeout=10)
            if code_final == 0:
                log.error(f"FALHA CRÍTICA: não foi possível remover ollama em '{caminho_ollama}'")
            else:
                log.ok("Binário ollama removido com sucesso após tentativa adicional.")

    # 3. Remove dados do usuário
    if AMBIENTE == "Windows":
        userprofile = os.environ.get("USERPROFILE", "")
        for pasta in [
            Path(userprofile) / ".ollama",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Ollama",
        ]:
            if pasta.exists():
                shutil.rmtree(pasta, ignore_errors=True)
    else:
        pasta = Path.home() / ".ollama"
        if pasta.exists():
            shutil.rmtree(pasta, ignore_errors=True)

    # 4. Limpa caches do SO
    limpar_caches_sistema()

    # 5. Verifica se realmente limpou
    residuais = arquivos_residuais()
    procs = processos_ollama()
    if residuais or procs:
        log.warn(f"Residual remanescente: {residuais}; processos: {len(procs)}")
        return False
    log.ok("Ambiente completamente limpo.")
    return True


def instalar_ollama() -> tuple[bool, float, float, str]:
    """Instala o Ollama. Retorna (sucesso, tempo_download_s, tempo_instalacao_s, erro).
    Download e instalação são medidos separadamente para evitar que latência
    de rede contamine a métrica de tempo de instalação local."""
    t_download = 0.0
    if AMBIENTE == "Windows":
        # 1. Download do instalador (com retry)
        for tentativa in range(1, 4):
            inicio = time.time()
            ps_dl = [
                "powershell", "-Command",
                "Invoke-WebRequest -Uri https://ollama.com/install.ps1 "
                "-OutFile $env:TEMP\\ollama_install.ps1"
            ]
            code_dl, _, err_dl = run(ps_dl, timeout=120)
            t_download = round(time.time() - inicio, 2)
            if code_dl == 0:
                break
            if tentativa < 3:
                espera = tentativa * 10
                log.warn(f"Download do instalador falhou (tentativa {tentativa}/3). Retry em {espera}s")
                time.sleep(espera)
        else:
            return False, t_download, 0.0, f"Download do instalador após 3 tentativas: {err_dl or 'código ' + str(code_dl)}"

        # 2. Instalação local (sem baixar novamente)
        inicio = time.time()
        ps_install = ["powershell", "-Command", "& $env:TEMP\\ollama_install.ps1"]
        code, _, err = run(ps_install, timeout=900)
        t_instalacao = round(time.time() - inicio, 2)
    else:
        # 1. Download do instalador (com retry)
        for tentativa in range(1, 4):
            inicio = time.time()
            dl_cmd = [
                "curl", "-fsSL", "-o", "/tmp/ollama_install.sh",
                "https://ollama.com/install.sh"
            ]
            code_dl, _, err_dl = run(dl_cmd, timeout=120)
            t_download = round(time.time() - inicio, 2)
            if code_dl == 0:
                break
            if tentativa < 3:
                espera = tentativa * 10
                log.warn(f"Download do instalador falhou (tentativa {tentativa}/3). Retry em {espera}s")
                time.sleep(espera)
        else:
            return False, t_download, 0.0, f"Download do instalador após 3 tentativas: {err_dl or 'código ' + str(code_dl)}"

        # 2. Instalação local (sem baixar novamente)
        log.info("Executando instalador (output no terminal)...")
        install_cmd = ["bash", "/tmp/ollama_install.sh"]
        inicio = time.time()
        try:
            result = subprocess.run(install_cmd, timeout=900)
            code = result.returncode
            err = ""
        except subprocess.TimeoutExpired:
            code = -1
            err = "TIMEOUT após 900s"
        except Exception as e:
            code = -1
            err = str(e)
        t_instalacao = round(time.time() - inicio, 2)

    sucesso = code == 0 and ollama_instalado()
    if not sucesso:
        msg = err if err else f"Falha pós-instalação (código {code})"
        return False, t_download, t_instalacao, msg
    return True, t_download, t_instalacao, ""


def desinstalar_ollama() -> tuple[bool, float, str]:
    """Desinstala o Ollama. Retorna (sucesso, tempo_s, erro)."""
    inicio = time.time()
    erros = []

    # ── 1. Mata todos os processos Ollama ──
    if AMBIENTE == "Windows":
        run(["taskkill", "/F", "/IM", "ollama.exe"], timeout=30)
        time.sleep(1)
    else:
        run(["pkill", "-9", "-f", "ollama"], timeout=30)
        time.sleep(2)
        # Dupla verificação: se ainda houver processo, tenta kill individual
        if processos_ollama():
            run(["kill", "-9"] + [p.split()[0] for p in processos_ollama()], timeout=10)

    # ── 2. Remove binários ──
    if AMBIENTE == "Windows":
        # Tenta desinstalação pelo gerenciador de pacotes
        code, _, err = run(
            ["powershell", "-Command",
             "Get-Package Ollama | Uninstall-Package -Force"],
            timeout=600
        )
        if code != 0:
            erros.append(f"Uninstall-Package falhou (código {code})")
        # Remove de todos os locais conhecidos
        for var in ["LOCALAPPDATA", "PROGRAMFILES", "PROGRAMFILES(X86)"]:
            caminho = Path(os.environ.get(var, "")) / "Ollama"
            if caminho.exists():
                shutil.rmtree(caminho, ignore_errors=True)
    else:
        code, _, _ = run(["sudo", "-n", "rm", "-f", "/usr/local/bin/ollama", "/usr/bin/ollama"], timeout=30)
        if code != 0:
            erros.append("Remoção do binário via sudo falhou (sudo -n não disponível)")

    # ── 3. Remove dados do usuário ──
    if AMBIENTE == "Windows":
        userprofile = os.environ.get("USERPROFILE", "")
        for pasta in [
            Path(userprofile) / ".ollama",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Ollama",
        ]:
            if pasta.exists():
                shutil.rmtree(pasta, ignore_errors=True)
    else:
        pasta = Path.home() / ".ollama"
        if pasta.exists():
            shutil.rmtree(pasta, ignore_errors=True)

    # ── 4. Verifica limpeza com retry ──
    for tentativa in range(3):
        residuais = arquivos_residuais()
        procs = processos_ollama()
        if not residuais and not procs:
            tempo = round(time.time() - inicio, 2)
            return True, tempo, "; ".join(erros) if erros else ""
        if tentativa < 2:
            time.sleep(1)
            if procs and AMBIENTE != "Windows":
                run(["pkill", "-9", "-f", "ollama"], timeout=10)
            if residuais:
                for r in residuais:
                    p = Path(r)
                    if p.exists():
                        shutil.rmtree(p, ignore_errors=True)

    tempo = round(time.time() - inicio, 2)
    msg = f"Residuais: {residuais}; processos: {len(procs)}"
    if erros:
        msg = "; ".join(erros) + " | " + msg
    return False, tempo, msg


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
    """Faz pull do modelo. Retorna True se sucesso. Tenta até 3x com backoff."""
    for tentativa in range(1, 4):
        log.info(f"Pull do modelo (tentativa {tentativa}/3)...")
        code, _, err = run(["ollama", "pull", MODELO], timeout=600)
        if code == 0:
            return True
        if tentativa < 3:
            espera = tentativa * 10
            log.warn(f"Falha no pull (código {code}). Retry em {espera}s: {err[:100]}")
            time.sleep(espera)
    return False


def inferencia_api(prompt: str) -> tuple[bool, float, str]:
    """
    Executa inferência via API REST do Ollama.
    Retorna (sucesso, tempo_total_s, erro).
    Valida que a resposta contém texto gerado (não apenas JSON OK).
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

        # Valida que a resposta contém texto gerado e não apenas metadados
        resposta = body.get("response")
        if not isinstance(resposta, str) or not resposta.strip():
            return False, tempo, "Resposta vazia ou campo 'response' ausente"
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

    log.step("Verificando e sanitizando ambiente")
    procs = processos_ollama()
    res = arquivos_residuais()
    if procs or res:
        log.warn(
            f"Ambiente não limpo: {len(procs)} processo(s), "
            f"{len(res)} residual(is). Forçando limpeza..."
        )
        ok = forcar_limpeza()
        if ok:
            log.ok("Ambiente sanitizado com sucesso.")
        else:
            log.error("Não foi possível limpar completamente o ambiente.")
    else:
        log.ok("Ambiente já limpo. Nenhum residual ou processo encontrado.")

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
            "tempo_download_s", "tempo_instalacao_s",
            "status_instalacao", "erro_instalacao",
            "status_remocao_modelo",
            "tempo_desinstalacao_s", "status_desinstalacao", "arquivos_residuais"
        ])
        writer.writeheader()

        for i in range(1, REPETICOES + 1):
            log.step(f"Tentativa {i}/{REPETICOES}")

            # Garante isolamento total: mata processos, remove binários e caches
            if not forcar_limpeza():
                log.error("Ambiente não pôde ser limpo — abortando iteração.")
                continue

            # 2. Instalação (download e execução local medidos separadamente)
            log.info("Iniciando instalação do Ollama...")
            ok_inst, t_download, t_inst, err_inst = instalar_ollama()
            status_inst = "sucesso" if ok_inst else "falha"
            log.info(f"Download: {t_download}s | Instalação: {t_inst}s | Total: {t_download + t_inst}s")
            if err_inst:
                log.error(f"Erro instalação: {err_inst[:200]}")

            # 3. Verificação pós-instalação
            versao = ollama_versao() if ok_inst else "n/a"
            log.info(f"Versão verificada: {versao}")

            # 3b. Para o serviço Ollama, para que não rode em background
            #     durante a desinstalação e não deixe resíduos em memória
            if ok_inst:
                if AMBIENTE == "Windows":
                    run(["taskkill", "/F", "/IM", "ollama.exe"], timeout=15)
                else:
                    run(["pkill", "-9", "-f", "ollama"], timeout=15)
                time.sleep(1)

            # 3c. Remoção do modelo separadamente do runtime (PO-2.2)
            status_remocao_modelo = "n/a"
            if ok_inst:
                log.info("Verificando se o modelo está presente para remoção separada...")
                code_list, out_list, _ = run(["ollama", "list"], timeout=30)
                if MODELO in out_list:
                    log.info("Removendo modelo (ollama rm) antes de desinstalar o runtime...")
                    code_rm, _, err_rm = run(["ollama", "rm", MODELO], timeout=120)
                    if code_rm == 0:
                        status_remocao_modelo = "sucesso"
                        log.ok("Modelo removido com sucesso.")
                    else:
                        status_remocao_modelo = "falha"
                        log.error(f"Falha ao remover modelo: {err_rm[:200]}")
                else:
                    status_remocao_modelo = "nao_instalado"
                    log.info("Modelo não está instalado — remoção não necessária.")

            # 4. Desinstalação
            log.info("Iniciando desinstalação...")
            ok_desinst, t_desinst, err_desinst = desinstalar_ollama()
            status_desinst = "sucesso" if ok_desinst else "falha"
            log.info(f"Desinstalação: {status_desinst} em {t_desinst}s")

            # 5. Limpa caches do SO entre iterações para não contaminar tempos
            limpar_caches_sistema()

            res_paths = arquivos_residuais()
            residuais_str = ";".join(res_paths) if res_paths else "nenhum"

            row = {
                "ambiente": NOME_AMBIENTE,
                "tentativa": i,
                "tempo_download_s": max(0, t_download),
                "tempo_instalacao_s": max(0, t_inst),
                "status_instalacao": status_inst,
                "erro_instalacao": err_inst[:300] if err_inst else "",
                "status_remocao_modelo": status_remocao_modelo,
                "tempo_desinstalacao_s": max(0, t_desinst),
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
        ok, t_dl, t_inst, err = instalar_ollama()
        if not ok:
            log.error(f"Falha ao instalar Ollama: {err}")
            return []
        log.info(f"Download: {t_dl}s | Instalação: {t_inst}s")

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

    # 3. Warm-up: descarta a primeira inferência (cold start do modelo)
    #    para não contaminar a métrica PO-1.2
    log.step("Warm-up: executando inferência de aquecimento (descartada das métricas)")
    ok_warm, t_warm, err_warm = inferencia_api(PROMPT_ADAPTABILIDADE)
    if ok_warm:
        log.info(f"  Warm-up concluído em {t_warm}s — cache do modelo aquecido")
    else:
        log.warn(f"  Warm-up falhou: {err_warm[:200]}")
        log.warn("  Prosseguindo mesmo assim com as inferências medidas.")

    # 4. Execução dos testes de inferência (5 repetições)
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
        tempos_download = [r["tempo_download_s"] for r in reg_inst if r["status_instalacao"] == "sucesso" and r["tempo_download_s"] >= 0]
        tempos_inst = [r["tempo_instalacao_s"] for r in reg_inst if r["status_instalacao"] == "sucesso" and r["tempo_instalacao_s"] >= 0]
        tempos_desinst = [r["tempo_desinstalacao_s"] for r in reg_inst if r["status_desinstalacao"] == "sucesso" and r["tempo_desinstalacao_s"] >= 0]
        residuais = [r for r in reg_inst if r["arquivos_residuais"] != "nenhum"]

        # Remoção do modelo (PO-2.2 — verificação separada do runtime)
        ok_rm_modelo = sum(1 for r in reg_inst if r.get("status_remocao_modelo") == "sucesso")
        nao_instalado_modelo = sum(1 for r in reg_inst if r.get("status_remocao_modelo") == "nao_instalado")
        falha_rm_modelo = sum(1 for r in reg_inst if r.get("status_remocao_modelo") == "falha")

        taxa_inst = round(ok_inst / total, 4)
        taxa_desinst = round(ok_desinst / total, 4)
        tempo_medio_download = round(statistics.mean(tempos_download), 2) if tempos_download else -1
        tempo_medio_inst = round(statistics.mean(tempos_inst), 2) if tempos_inst else -1
        tempo_medio_desinst = round(statistics.mean(tempos_desinst), 2) if tempos_desinst else -1

        # Variação de tempo (PO-3.3 critério: ≤ 15%)
        if len(tempos_inst) >= 2 and tempo_medio_inst > 0:
            desvio_padrao_inst = statistics.stdev(tempos_inst)
            variacao_tempo_inst = round(desvio_padrao_inst / tempo_medio_inst, 4)
        else:
            variacao_tempo_inst = 0.0

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
            "PO-3.3_tempo_medio_download_s": tempo_medio_download,
            "PO-3.3_tempo_medio_instalacao_s": tempo_medio_inst,
            "PO-3.3_tempo_medio_desinstalacao_s": tempo_medio_desinst,
            "PO-3.3_variacao_tempo_instalacao": variacao_tempo_inst,
            "PO-3.3_criterio_variacao": "<= 0.15",
            "PO-3.3_variacao_passou": variacao_tempo_inst <= 0.15,
            "PO-3.3_taxa_max_falha_por_tipo": round(taxa_max_falha_tipo, 4),
            "PO-3.3_criterio_falha": "taxa_max_falha_por_tipo <= 0.02",
            "PO-3.3_falha_passou": taxa_max_falha_tipo <= 0.02,
        })

        # Log das métricas de instalabilidade
        log.metric("PO-2.1", f"{taxa_inst:.1%}", ">= 95%", taxa_inst >= 0.95)
        log.metric("PO-2.2", f"{taxa_desinst:.1%}", ">= 90%", taxa_desinst >= 0.90)
        log.metric("PO-3.1", f"{taxa_inst:.1%} no {NOME_AMBIENTE}", ">= 95%", taxa_inst >= 0.95)
        log.metric(
            "PO-3.3",
            f"variação={variacao_tempo_inst:.1%}, taxa_erro_max={taxa_max_falha_tipo:.1%}, "
            f"t_inst_medio={tempo_medio_inst}s",
            "variação <= 15% e taxa_erro_max <= 2%",
            variacao_tempo_inst <= 0.15 and taxa_max_falha_tipo <= 0.02,
        )

    # ── Adaptabilidade ────────────────────────────────────────────────────

    if reg_adapt:
        total_a = len(reg_adapt)
        ok_a = sum(1 for r in reg_adapt if r["status"] == "sucesso")
        tempos_a = [r["tempo_inferencia_s"] for r in reg_adapt if r["status"] == "sucesso" and r["tempo_inferencia_s"] >= 0]

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
            ("PO-3.3_t_medio_download_s", resultados.get("PO-3.3_tempo_medio_download_s", "N/A"),
             "(registro, sem critério)", "N/A"),
            ("PO-3.3_t_medio_instalacao_s", resultados.get("PO-3.3_tempo_medio_instalacao_s", "N/A"),
             "(registro, sem critério)", "N/A"),
            ("PO-3.3_variacao_tempo", resultados.get("PO-3.3_variacao_tempo_instalacao", "N/A"),
             "<= 0.15", resultados.get("PO-3.3_variacao_passou", "N/A")),
            ("PO-3.3_taxa_erro_tipo", resultados.get("PO-3.3_taxa_max_falha_por_tipo", "N/A"),
             "<= 0.02", resultados.get("PO-3.3_falha_passou", "N/A")),
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

    if AMBIENTE != "Windows" and not sudo_disponivel():
        print("  sudo não disponível em modo não interativo.")
        print("  Autenticando uma vez para cache de credenciais (sudo -v)...\n")
        # subprocess.run direto (sem capture_output) para que o prompt
        # de senha chegue ao terminal real
        ret = subprocess.run(["sudo", "-v"])
        if ret.returncode != 0:
            print("  ❌ Falha na autenticação sudo. Abortando.")
            sys.exit(1)
        print("  ✓ Autenticação OK — crédulo sudo ativo por ~15min.\n")

    passo1_preparacao()
    reg_inst   = passo2_instalabilidade()
    reg_adapt  = passo3_adaptabilidade()
    passo4_consolidacao(reg_inst, reg_adapt)

    print(f"\nLog completo: {LOG_FILE}\n")


if __name__ == "__main__":
    main()
