#!/usr/bin/env python3
# guard_tool_output.py - redige segredos na SAÍDA de ferramentas (MCP) antes de chegarem ao agente/LLM.
# Ligado a CVE-2026-135614 (ECS MCP Server) e ao caso Dragos/OpenRouter. Heurístico; não testado em produção.
import json, re, sys
NOME = re.compile(r"pass(word)?|secret|token|api[_-]?key|private[_-]?key|credential|dsn", re.I)
PADROES = [re.compile(p) for p in (
    r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",        # access key id da AWS
    r"\bsk-[A-Za-z0-9_-]{20,}\b",            # chaves estilo OpenAI/OpenRouter
    r"\bgh[pousr]_[A-Za-z0-9]{30,}\b",       # tokens do GitHub
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",   # chave privada PEM
    r"\b[a-z][a-z0-9+.-]*://[^\s:/@]+:[^\s@]+@")]  # URL com usuário:senha
def limpar(no, chave=""):
    """Devolve (objeto_limpo, nº_de_redações). Trata o formato ECS {"name": X, "value": Y}."""
    if isinstance(no, dict):
        nome, n, saida = str(no.get("name", chave)), 0, {}
        for k, v in no.items():
            sensivel = (k in ("value", "valueFrom") and NOME.search(nome)) or (NOME.search(k) and isinstance(v, str))
            saida[k], m = ("[REDIGIDO]", 1) if sensivel else limpar(v, k)
            n += m
        return saida, n
    if isinstance(no, list):
        pares = [limpar(x, chave) for x in no]
        return [p[0] for p in pares], sum(p[1] for p in pares)
    if isinstance(no, str):
        return re.subn("|".join(p.pattern for p in PADROES), "[REDIGIDO]", no)
    return no, 0

if __name__ == "__main__":
    dado, total = limpar(json.load(sys.stdin))
    print(json.dumps(dado, ensure_ascii=False)); print(f"[guard] {total} redação(ões)", file=sys.stderr)
