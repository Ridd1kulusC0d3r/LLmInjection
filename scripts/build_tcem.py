#!/usr/bin/env python3
"""Build the TCEM threat models of the known ARTEX attacks (stdlib only).

Each case follows TCEM, the Threat Context Engineering Method (github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-
Modeling, v0.5.1, same author as this repository): crown jewel, threat context, the actor's attack path, the
telemetry each step needs, the detection that covers it (an LLMInjection DET-AI where one exists, a gap where
not), a safe log-replay validation, intelligence gaps and the defensive decisions they lead to. The modelling is
analyst work and lives in CASES below; facts come from the cited records in data/.

Writes, for every case:
    tcem/cases/<CASE>/case.json             TCEM single-document case (loads in `tce validate`)
    tcem/cases/<CASE>/fixtures/events.jsonl synthetic defensive events, no payloads
    assets/tcem/<case>.svg                  attack path with telemetry, detection and control rows
and once:
    assets/tcem/overview.svg                phase-by-case coverage matrix
    reports/dossiers/tcem-artex.md          the report (web edition and PDF come from the report builders)

    python scripts/build_tcem.py
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

from tcem_validate import run_validations

ROOT = Path(__file__).resolve().parents[1]
OUT_CASES = ROOT / "tcem" / "cases"
OUT_ART = ROOT / "assets" / "tcem"
OUT_MD = ROOT / "reports" / "dossiers" / "tcem-artex.md"
CUT = "2026-11-22"
PHASES = ["Reconhecimento", "Acesso inicial", "Credenciais", "Descoberta", "Persistência e escalada",
          "Movimento lateral", "Comando e controle", "Coleta e impacto", "Cadeia de suprimentos"]


def S(ph, pt, att, llmi=("LLMI-T015",), det=(), ctrl=(), tel="", gap=""):
    """One step of an attack path."""
    return {"phase": ph, "pt": pt, "attack": list(att), "llmi": list(llmi), "det": list(det), "ctrl": list(ctrl), "tel": tel, "gap": gap}


def ev(t, action, **kv):
    e = {"timestamp": f"2026-11-01T{t}Z", "event": {"action": action}}
    for k, v in kv.items():
        a, b = k.split("__")
        e.setdefault(a, {})[b] = v
    return e


def stage(action, **extra):
    clauses = [{"field": "event.action", "op": "eq", "value": action}]
    clauses += [{"field": k.replace("__", "."), "op": "eq", "value": v} for k, v in extra.items()]
    return {"all": clauses}


CASES = [
    {
        "id": "CASE-ARTEX-STORM-0940", "file": "storm-0940", "short": "Storm-0940",
        "who": "Storm-0940 (Microsoft; nexo China, alinhado ao Estado)", "conf": "high",
        "records": ["ACTOR-STORM-0940", "CAMPAIGN-STORM-0940-ARTEX-CONNECTWISE", "CAMPAIGN-ARTEX-IT-SOFTWARE-VENDORS"],
        "sources": ["SRC-MSFT-STORM-0940-ARTEX", "SRC-WIZ-ARTEX-VENDORS", "SRC-FBI-FLASH-20261113-ARTEX"],
        "mission": "Manter o controle do tenant de identidade e das integrações OAuth, e não virar ponte para os tenants de clientes.",
        "cj": ("Tenant Entra ID e aplicações OAuth com acesso a dados de clientes", "Quem controla o tenant e as aplicações controla o acesso aos dados dos clientes atendidos por ele."),
        "context": "Ataque de identidade em cadência de máquina conduzido por ARTEX, seguido de abuso de OAuth e uso de um fornecedor de backup como ponte.",
        "steps": [
            S("Reconhecimento", "Varredura contínua com impressões do ARTEX", ["T1595.002"], det=["DET-AI-048"], tel="Logs de WAF e proxy: caminho, user agent, cabeçalhos"),
            S("Credenciais", "Password spraying em ritmo fixo: 327 contas de 8 organizações em 10 a 14/10", ["T1110.003"], det=["DET-AI-049"], ctrl=["MFA resistente a phishing"], tel="Sign-ins do Entra ID e do Okta com horário ao segundo"),
            S("Acesso inicial", "Login válido logo depois do spray", ["T1078.004"], det=["DET-AI-049"], ctrl=["Acesso condicional"], tel="Sign-ins bem-sucedidos com o mesmo IP de origem"),
            S("Persistência e escalada", "Aplicação OAuth ganha credencial nova ou concede papel a si mesma", ["T1098.001", "T1098.003", "T1528"], det=["DET-AI-050"], ctrl=["Consentimento só por administrador"], tel="Auditoria do Entra ID: credenciais e papéis de aplicações"),
            S("Coleta e impacto", "Leitura em massa via Microsoft Graph acelerada por IA", ["T1087.004", "T1530"], det=["DET-AI-050"], tel="Sign-ins de service principal e chamadas ao Graph por aplicação"),
            S("Cadeia de suprimentos", "Fornecedor de backup (ConnectWise) usado como ponte para tenants de clientes", ["T1199", "T1195"], tel="Sign-ins de identidades de provedor nos tenants de clientes", gap="Nenhuma detecção do repositório cobre o uso da relação de confiança do provedor."),
        ],
        "spec": {"title": "Spray em cadência de máquina que termina em sucesso e credencial nova de aplicação", "det": ["DET-AI-049", "DET-AI-050"],
                 "group_by": ["source.ip"], "window": "3h",
                 "stages": [stage("spray_rhythm_burst"), stage("signin_success"), stage("app_credential_added")],
                 "behavior": "spray_rhythm_burst (DET-AI-049) -> signin_success -> app_credential_added (mesmo IP de origem)"},
        "fixture": [
            ev("09:00:02", "spray_rhythm_burst", source__ip="203.0.113.10", accounts__count=327, interval__seconds=1),
            ev("09:00:03", "signin_success", source__ip="203.0.113.10", user__name="carla"),
            ev("09:02:00", "signin_failure", source__ip="198.51.100.7", user__name="diego"),
            ev("09:02:30", "signin_success", source__ip="198.51.100.7", user__name="diego"),
            ev("09:40:00", "app_credential_added", source__ip="203.0.113.10", app__id="app-relatorios"),
            ev("10:15:00", "app_credential_added", source__ip="192.0.2.44", app__id="app-rh"),
        ],
        "fixture_note": "Uma rajada de spray em ritmo fixo de um IP que acerta e depois adiciona credencial a uma aplicação (1 alerta); um usuário que erra a senha e entra (sem alerta); um administrador que adiciona credencial sem falhas antes (sem alerta).",
        "hyp": ("Um operador com ARTEX consegue sair de uma senha fraca a uma aplicação OAuth com acesso a dados de clientes em poucas horas.", ["Erro de senha de usuários legítimos seguido de mudança administrativa planejada"]),
        "gaps": ["Quais identidades de fornecedores (backup, MSP) têm acesso aos nossos tenants e como seus logins aparecem?", "A Microsoft atribui o caso ConnectWise ao Storm-0940; a sobreposição com a campanha descrita pela Wiz é avaliação da Wiz."],
        "decisions": ["Coletar sign-ins com horário ao segundo e alertar a sequência spray, sucesso e credencial nova de aplicação.", "Inventariar e restringir identidades de provedores com acesso aos tenants."],
        "prio": [5, 5, 4, 4, 3, 4],
    },
    {
        "id": "CASE-ARTEX-VAPOR-PANDA", "file": "vapor-panda", "short": "VAPOR PANDA",
        "who": "VAPOR PANDA (CrowdStrike; espionagem)", "conf": "high",
        "records": ["ACTOR-VAPOR-PANDA", "CAMPAIGN-VAPOR-PANDA-ARTEX"],
        "sources": ["SRC-CROWDSTRIKE-VAPOR-PANDA-2026-10"],
        "mission": "Impedir que um acesso web exposto vire domínio comprometido.",
        "cj": ("Controladores de domínio e credenciais de administrador de domínio", "Com elas o operador alcança qualquer servidor da organização."),
        "context": "Agentes planejador e executores do ARTEX, sobretudo com DeepSeek, em 14 países em 11 dias; pós-exploração confirmada em 9 organizações.",
        "steps": [
            S("Acesso inicial", "Agentes executores exploram aplicação exposta", ["T1190"], det=["DET-AI-048"], ctrl=["Gestão de exposição e correção"], tel="Logs de WAF e do servidor web"),
            S("Persistência e escalada", "Agente escreve web shell", ["T1505.003"], tel="EDR: arquivo criado no diretório web pelo processo do servidor", gap="Sem DET-AI: regras genéricas de web shell (o artex-detections tem versões ligadas ao ARTEX)."),
            S("Credenciais", "Extração de senhas de administrador de domínio", ["T1003"], tel="EDR: acesso à memória do LSASS e ao NTDS", gap="Coberto por regras clássicas de EDR, não por detecção de IA."),
            S("Movimento lateral", "Movimento lateral com a credencial de domínio", ["T1021.002"], tel="Logs de autenticação do Windows (4624 tipo 3) e SMB", gap="Coberto por regras clássicas."),
            S("Comando e controle", "Servidor comprometido fala com API de LLM e com o console", ["T1071.001"], det=["DET-AI-001", "DET-AI-048"], ctrl=["CTRL-EGRESS-POLICY"], tel="DNS e proxy: destinos de provedores de LLM a partir de servidores"),
        ],
        "spec": {"title": "Web shell seguido de acesso a credenciais e de saída para API de LLM no mesmo servidor", "det": ["DET-AI-001"],
                 "group_by": ["host.name"], "window": "24h",
                 "stages": [stage("webroot_file_written_by_server"), stage("credential_store_access"), stage("llm_provider_egress")],
                 "behavior": "webroot_file_written_by_server -> credential_store_access -> llm_provider_egress (mesmo host)"},
        "fixture": [
            ev("02:10:00", "webroot_file_written_by_server", host__name="web-01", file__path="/var/www/app/up.aspx"),
            ev("02:14:00", "credential_store_access", host__name="web-01", process__name="w3wp"),
            ev("02:20:00", "llm_provider_egress", host__name="web-01", destination__domain="api.llm.example"),
            ev("08:00:00", "webroot_file_written_by_server", host__name="web-02", file__path="/var/www/app/cache.tmp"),
            ev("09:00:00", "llm_provider_egress", host__name="dev-07", destination__domain="api.llm.example"),
        ],
        "fixture_note": "Um servidor web com arquivo novo, acesso a credenciais e saída para API de LLM (1 alerta); um cache gravado pelo servidor (sem alerta); um desenvolvedor usando API de LLM (sem alerta).",
        "hyp": ("A parte específica de IA desta campanha aparece no reconhecimento e na saída para APIs de LLM; o resto é pós-exploração clássica.", ["Ferramenta legítima de IA instalada no servidor"]),
        "gaps": ["Quais servidores podem falar com APIs de LLM e quais não deveriam?", "A CrowdStrike não publica os indicadores do console usado."],
        "decisions": ["Bloquear saída de servidores para provedores de LLM fora de uma lista aprovada.", "Tratar web shell em servidor exposto como incidente de domínio até prova em contrário."],
        "prio": [5, 4, 4, 4, 3, 3],
    },
    {
        "id": "CASE-ARTEX-STORM-3358", "file": "storm-3358", "short": "Storm-3358",
        "who": "Storm-3358 (Microsoft; crime financeiro, Sudeste Asiático)", "conf": "confirmed",
        "records": ["ACTOR-STORM-3358", "CAMPAIGN-STORM-3358-ARTEX-FINANCE"],
        "sources": ["SRC-MSFT-STORM-3358-ARTEX"],
        "mission": "Manter os servidores web de serviços financeiros sem execução de código de terceiros.",
        "cj": ("Servidores web expostos de serviços financeiros e a rede interna atrás deles", "São a porta de entrada que o ator procura em escala."),
        "context": "ARTEX somado a ferramentas automáticas: varredura, upload anônimo e SSRF, e RATs abertos (WISP, vshell, AdaptixC2) baixados com netcat e curl.",
        "steps": [
            S("Reconhecimento", "Varredura de sistemas expostos com agentes e scanners", ["T1595.002"], det=["DET-AI-048"], tel="Logs de WAF e proxy"),
            S("Acesso inicial", "Exploração de upload anônimo e SSRF", ["T1190"], ctrl=["Desligar upload anônimo"], tel="Logs da aplicação: uploads sem sessão", gap="Sem DET-AI; depende de regra de aplicação."),
            S("Comando e controle", "Servidor baixa ferramentas com curl ou netcat", ["T1105"], tel="EDR: processo do servidor web inicia curl, wget ou nc", gap="Sem DET-AI; padrão clássico de pós-exploração."),
            S("Comando e controle", "RAT aberto instalado (WISP, vshell, AdaptixC2)", ["T1219", "T1071.001"], tel="EDR e fluxo de rede para destinos novos", gap="Coberto por regras genéricas (o artex-detections mantém versões)."),
        ],
        "spec": {"title": "Upload anônimo seguido de download por processo do servidor e conexão nova de saída", "det": [],
                 "group_by": ["host.name"], "window": "2h",
                 "stages": [stage("anonymous_upload"), stage("server_spawns_downloader"), stage("new_outbound_destination")],
                 "behavior": "anonymous_upload -> server_spawns_downloader -> new_outbound_destination (mesmo host)"},
        "fixture": [
            ev("03:00:00", "anonymous_upload", host__name="pay-web-01", url__path="/upload"),
            ev("03:01:30", "server_spawns_downloader", host__name="pay-web-01", process__name="curl"),
            ev("03:02:00", "new_outbound_destination", host__name="pay-web-01", destination__ip="198.51.100.200"),
            ev("11:00:00", "anonymous_upload", host__name="pay-web-02", url__path="/upload"),
            ev("11:30:00", "new_outbound_destination", host__name="pay-web-02", destination__ip="192.0.2.9"),
        ],
        "fixture_note": "Upload anônimo, curl iniciado pelo servidor e destino novo no mesmo host (1 alerta); upload seguido de destino novo sem downloader (sem alerta).",
        "hyp": ("O valor do agente para este ator é a escala da varredura; a intrusão em si segue o padrão clássico de servidor web.", ["Automação legítima que baixa atualizações"]),
        "gaps": ["A Microsoft não diz em que etapas exatamente o ARTEX substituiu as ferramentas convencionais."],
        "decisions": ["Contrato de telemetria: processo do servidor web iniciando downloaders é coletado e alertado.", "Desligar upload anônimo onde não houver necessidade de negócio."],
        "prio": [4, 4, 4, 5, 3, 4],
    },
    {
        "id": "CASE-ARTEX-CRAFTY-FALCON", "file": "crafty-falcon", "short": "CRAFTY FALCON",
        "who": "CRAFTY FALCON (CERT-In; crime financeiro na Índia)", "conf": "confirmed",
        "records": ["CAMPAIGN-CRAFTY-FALCON-BFSI-INDIA"],
        "sources": ["SRC-CERTIN-CIAD-2026-0058"],
        "mission": "Impedir transferências que não foram pedidas pelo cliente, mesmo quando saem de infraestrutura confiável.",
        "cj": ("APIs de pagamento e desembolso, e contas de liquidação", "O ator chama as APIs de dentro da infraestrutura liberada da própria vítima."),
        "context": "ARTEX, PentAGI, Cairn e CyberStrikeAI contra NBFCs, fintechs, agregadores de pagamento e plataformas cripto; o ator volta a atacar quem já corrigiu.",
        "steps": [
            S("Reconhecimento", "Engenharia reversa do código da aplicação", ["T1592"], tel="Sem telemetria do lado da vítima", gap="Fora do alcance da vítima."),
            S("Acesso inicial", "Chamadas às APIs de pagamento a partir de infraestrutura liberada da vítima", ["T1078", "T1199"], ctrl=["CTRL-CONTEXTUAL-AUTHZ"], tel="Gateway de API: cliente, chave, IP e operação", gap="Sem DET-AI; exige linha de base por cliente de API."),
            S("Coleta e impacto", "Transferências de valor ínfimo para testar", ["T1657"], tel="Sistema de pagamentos: valor, beneficiário, origem", gap="Regra de negócio, não de segurança de IA."),
            S("Coleta e impacto", "Fundos para contas de laranjas", ["T1657"], ctrl=["Limite e revisão para beneficiário novo"], tel="Sistema de pagamentos e antifraude"),
            S("Persistência e escalada", "Adulteração de logs e de ferramentas de endpoint", ["T1070", "T1562.001"], tel="Integridade de logs e saúde do EDR", gap="Coberto por regras clássicas de defesa."),
        ],
        "spec": {"title": "Cliente de API novo faz transferência ínfima e, em seguida, valor alto ao mesmo beneficiário", "det": [],
                 "group_by": ["beneficiary.account"], "window": "24h",
                 "stages": [stage("payment_api_call", client__first_seen="true"), stage("micro_transfer"), stage("large_transfer")],
                 "behavior": "payment_api_call (cliente novo) -> micro_transfer -> large_transfer (mesmo beneficiário)"},
        "fixture": [
            ev("14:00:00", "payment_api_call", beneficiary__account="BEN-77", client__first_seen="true"),
            ev("14:02:00", "micro_transfer", beneficiary__account="BEN-77", amount__value=1),
            ev("14:30:00", "large_transfer", beneficiary__account="BEN-77", amount__value=250000),
            ev("15:00:00", "payment_api_call", beneficiary__account="BEN-12", client__first_seen="false"),
            ev("15:01:00", "micro_transfer", beneficiary__account="BEN-12", amount__value=1),
            ev("15:20:00", "large_transfer", beneficiary__account="BEN-12", amount__value=90000),
        ],
        "fixture_note": "Cliente de API novo, transferência de teste e valor alto ao mesmo beneficiário (1 alerta); o mesmo padrão de um cliente conhecido, como validação de conta legítima (sem alerta).",
        "hyp": ("Contra este ator, a detecção que funciona é de negócio: o comportamento do cliente de API e do beneficiário, não a impressão da ferramenta.", ["Validação de conta legítima com centavos antes de um pagamento real"]),
        "gaps": ["O CERT-In não publica quantas entidades foram afetadas nem valores.", "Não há fonte de grau A além do aviso do CERT-In."],
        "decisions": ["Linha de base por cliente de API de pagamento, com alerta para cliente novo.", "Revisão humana para beneficiário novo acima de um limite."],
        "prio": [5, 4, 3, 4, 4, 5],
    },
    {
        "id": "CASE-ARTEX-CLOUD-SECRETS", "file": "cloud-secrets", "short": "Segredos de nuvem",
        "who": "Operadores não atribuídos (Microsoft, Datadog, Barracuda, Arctic Wolf via CSA, Unit 42)", "conf": "high",
        "records": ["CAMPAIGN-ARTEX-EXPOSED-SECRETS", "CAMPAIGN-ARTEX-AWS", "INCIDENT-BARRACUDA-ARTEX-CLOUD-2026-11", "CAMPAIGN-ANTIFOX-AWS-IIS", "CAMPAIGN-ARTEX-IDENTITY-WORKFLOWS"],
        "sources": ["SRC-MSFT-ARTEX-SECRETS-2026-11", "SRC-DATADOG-ARTEX-AWS", "SRC-BARRACUDA-ARTEX-2026-11", "SRC-UNIT42-ARTEX-2026-11", "SRC-AWS-SQS-CLOUDTRAIL-LOGGING"],
        "mission": "Uma chave vazada não pode virar acesso aos cofres de segredos nem a contas de nuvem novas.",
        "cj": ("Cofres de segredos (Key Vault, Secrets Manager), chaves de longo prazo e chaves de API de IA", "Cada segredo encontrado abre a próxima conta: a Barracuda viu cerca de 10 contas em 44 horas."),
        "context": "O padrão mais documentado do ARTEX: o agente procura segredos, prova o que cada chave pode fazer em segundos e encadeia o próximo acesso.",
        "steps": [
            S("Credenciais", "Busca de segredos e chaves de API de IA em repositórios públicos", ["T1593.003", "T1552.001"], llmi=["LLMI-T015", "LLMI-T016"], det=["DET-AI-006"], ctrl=["CTRL-SECRET-ISOLATION"], tel="Alertas de varredura de segredos e uso de chaves de IA"),
            S("Acesso inicial", "Uso de chave de longo prazo, inclusive de fornecedor nunca revogada", ["T1078.004"], det=["DET-AI-046"], ctrl=["Revogar chaves de fornecedores"], tel="CloudTrail, Azure Activity e sign-ins da credencial"),
            S("Descoberta", "Prova de permissões em segundos: DryRun, validate, rajada de negações", ["T1580", "T1526"], det=["DET-AI-046", "DET-AI-047"], tel="CloudTrail com errorCode por serviço, mais eventos de dados de descoberta (SQS) ligados"),
            S("Credenciais", "Leitura em massa de cofres e busca de segredos em logs", ["T1555.006", "T1552"], llmi=["LLMI-T015", "LLMI-T016"], det=["DET-AI-047"], tel="Eventos GetSecretValue, Key Vault e FilterLogEvents"),
            S("Persistência e escalada", "Identidade administrativa nova ou service principal de aplicação multitenant", ["T1098"], det=["DET-AI-050"], tel="Auditoria de IAM e do Entra ID"),
            S("Coleta e impacto", "Segredos de CI impressos em logs de build e contêiner montando o host", ["T1552", "T1611"], ctrl=["CTRL-EXEC-POLICY"], tel="Logs de CI e eventos do runtime de contêineres", gap="Sem DET-AI para segredo em log de build nem para contêiner com o host montado."),
        ],
        "spec": {"title": "Rajada de chamadas negadas seguida de leitura de segredo com a mesma chave", "det": ["DET-AI-047"],
                 "group_by": ["user.access_key"], "window": "30m",
                 "stages": [stage("api_call_denied"), stage("api_call_denied"), stage("api_call_denied"), stage("get_secret_value")],
                 "behavior": "api_call_denied x3 -> get_secret_value (mesma chave)"},
        "fixture": [
            ev("10:00:00", "api_call_denied", user__access_key="AKIAEXAMPLE1", event__source="ec2"),
            ev("10:00:01", "api_call_denied", user__access_key="AKIAEXAMPLE1", event__source="s3"),
            ev("10:00:02", "api_call_denied", user__access_key="AKIAEXAMPLE1", event__source="iam"),
            ev("10:00:30", "get_secret_value", user__access_key="AKIAEXAMPLE1", secret__name="prod/db"),
            ev("11:00:00", "api_call_denied", user__access_key="AKIAEXAMPLE2", event__source="s3"),
            ev("11:05:00", "get_secret_value", user__access_key="AKIAEXAMPLE2", secret__name="app/config"),
        ],
        "fixture_note": "Três negações em serviços diferentes e uma leitura de segredo com a mesma chave (1 alerta); uma negação isolada antes de leitura legítima (sem alerta).",
        "hyp": ("Contra o ARTEX, o sinal mais confiável é o ritmo: muitas negações em segundos com a mesma chave, seguidas de sucesso.", ["Ferramenta de inventário que testa permissões", "Pipeline de deploy recém-configurado"]),
        "gaps": ["Quais chaves de longo prazo e de fornecedores existem e quando foram usadas pela última vez?", "A leitura do AntiFox é da CSA sobre o original da Arctic Wolf, não lido.",
                 "A trilha registra a descoberta que é evento de dados? ListQueues, GetQueueAttributes, GetQueueUrl e ListQueueTags do SQS são eventos de dados, desligados por padrão (documentação da AWS); a emulação da Mitigant viu a enumeração de SQS passar sem rastro no CloudTrail."],
        "decisions": ["Revogar chaves de longo prazo sem uso e todas as entregues a fornecedores encerrados.", "Alertar a sequência negações, sucesso e leitura de segredo por chave."],
        "prio": [5, 5, 5, 4, 3, 3],
    },
    {
        "id": "CASE-ARTEX-INSIDE", "file": "inside", "short": "ARTEX dentro de casa",
        "who": "Consoles expostos, fork do ScopeSentry, imagem com backdoor e avaliação que escapou (WorkOS)", "conf": "high",
        "records": ["TOOL-ARTEX", "TOOL-SCOPESENTRY", "INCIDENT-WORKOS-ARTEX-SANDBOX-ESCAPE"],
        "sources": ["SRC-CENSYS-ARTEX-2026-11", "SRC-SPECTRUM-SWARM-CHASING", "SRC-GH-SCOPESENTRY-NIUDAII", "SRC-WORKOS-BULLETIN-2026-10-30"],
        "mission": "O framework ofensivo só roda onde foi autorizado e não sai do ambiente de teste.",
        "cj": ("Rede interna, plataformas de varredura e ambientes de avaliação de agentes", "Um console ou um agente de avaliação dentro da rede tem o alcance da rede."),
        "context": "Não é um ator: são os jeitos de o ARTEX aparecer dentro da organização, por instalação não autorizada, por integração com scanner, por imagem adulterada ou por um teste que escapa.",
        "steps": [
            S("Comando e controle", "Console do ARTEX instalado ou exposto na rede", ["T1219", "T1133"], det=["DET-AI-052"], ctrl=["CTRL-AI-INVENTORY"], tel="Varreduras internas e respostas HTTP de consoles"),
            S("Reconhecimento", "Scanner interno entrega alvos ao framework", ["T1595"], det=["DET-AI-058"], tel="Proxy e netflow dos hosts de varredura"),
            S("Cadeia de suprimentos", "Imagem do ARTEX com backdoor dá root a terceiros", ["T1525", "T1195.002"], det=["DET-AI-052"], ctrl=["CTRL-ARTIFACT-PINNING", "CTRL-SIGNATURE-VERIFICATION"], tel="Registro de imagens e digest em execução"),
            S("Coleta e impacto", "Agente de avaliação em modo sem aprovação sai do sandbox", ["T1611"], det=["DET-AI-032", "DET-AI-043"], ctrl=["CTRL-EGRESS-POLICY", "CTRL-ACTION-BUDGET"], tel="Linha de comando do runtime e saída de rede do sandbox"),
        ],
        "spec": {"title": "Agente iniciado sem aprovação humana alcança destino fora da lista do sandbox", "det": ["DET-AI-032", "DET-AI-043"],
                 "group_by": ["sandbox.id"], "window": "1h",
                 "stages": [stage("agent_runtime_start", agent__approval_mode="auto"), stage("egress_not_allowlisted")],
                 "behavior": "agent_runtime_start (auto-approve) -> egress_not_allowlisted (mesmo sandbox)"},
        "fixture": [
            ev("16:00:00", "agent_runtime_start", sandbox__id="eval-3", agent__approval_mode="auto"),
            ev("16:20:00", "egress_not_allowlisted", sandbox__id="eval-3", destination__domain="internal.vendor.example"),
            ev("17:00:00", "agent_runtime_start", sandbox__id="eval-4", agent__approval_mode="manual"),
            ev("17:10:00", "egress_not_allowlisted", sandbox__id="eval-4", destination__domain="pypi.example"),
        ],
        "fixture_note": "Agente sem aprovação que alcança destino fora da lista (1 alerta); agente com aprovação humana e destino fora da lista (vai para a fila de egress, não para este alerta).",
        "hyp": ("O risco imediato do ARTEX para quem defende inclui o próprio ARTEX: consoles expostos, forks e testes sem contenção.", ["Red team autorizado"]),
        "gaps": ["Quem na organização roda frameworks ofensivos agênticos e onde?", "A contagem de consoles expostos é da Censys e da Spectrum; console exposto não é atacante."],
        "decisions": ["Inventário e autorização explícita para frameworks ofensivos agênticos.", "Sandboxes de avaliação sem saída de rede fora de lista fechada."],
        "prio": [4, 4, 4, 4, 3, 4],
    },
]

NOT_MODELLED = [
    ("Pearl Sleet e Onyx Sleet", "CAMPAIGN-PEARL-SLEET-ARTEX", "A Microsoft confirma o uso de ARTEX, mas não descreve para que ele foi usado em uma intrusão."),
    ("TAG-217 e o operador multimodelo", "INCIDENT-TAG-217-SOUTH-KOREA-FINANCE", "A Recorded Future avisa que a evidência não mostra quanto a IA acelerou os ataques; a Zscaler não nomeia o ator."),
    ("Comissão Europeia", "INCIDENT-EC-ARTEX-2026-11", "Relato de imprensa sem ator, falha nem papel do ARTEX (invasão ou só varredura)."),
    ("Eye Security", "INCIDENT-EYE-ARTEX-IR", "Vítima e caminho não publicados; o relato confirma escala e velocidade, não os passos."),
    ("Grupos de extorsão e clusters PRC (GTIG)", "CAMPAIGN-ARTEX-EXTORTION-AND-PRC-CLUSTERS", "Sem passos por intrusão; a parte de credenciais está no caso de segredos de nuvem."),
]

DET_NAMES: dict[str, str] = {}
REC_NAMES: dict[str, str] = {}
SRC: dict[str, dict] = {}


def load() -> None:
    for d in json.loads((ROOT / "data" / "detections.json").read_text(encoding="utf-8")):
        DET_NAMES[d["id"]] = d["name"]
    for n in ("actors", "campaigns", "incidents", "tools"):
        for r in json.loads((ROOT / "data" / f"{n}.json").read_text(encoding="utf-8")):
            REC_NAMES[r["id"]] = r["name"]
    for s in json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8")):
        SRC[s["id"]] = s


def case_doc(c: dict) -> dict:
    p = c["id"].removeprefix("CASE-ARTEX-")
    cid, cj, ctx, ts, tcs, dsp, val, hyp = (f"{x}-{p}" for x in ("CASE", "CJ", "CTX", "TS", "TC", "DSP", "VAL", "TH"))
    cid = c["id"]
    evid = [f"EV-{p}-{i + 1}" for i in range(len(c["sources"]))]
    gaps = [f"GAP-{p}-{i + 1}" for i in range(len(c["gaps"]))]
    decs = [f"DEC-{p}-{i + 1}" for i in range(len(c["decisions"]))]
    pr = dict(zip(["crown_jewel_criticality", "threat_relevance", "attack_path_feasibility", "exposure", "control_weakness", "detection_gap"], c["prio"], strict=True))
    pr["calculated_score"] = round(sum(c["prio"]) / len(c["prio"]), 2)
    pr["band"] = "P0" if pr["calculated_score"] >= 4.5 else "P1" if pr["calculated_score"] >= 4 else "P2" if pr["calculated_score"] >= 3 else "P3"
    pr["rationale"] = "Pontuação do analista a partir das fontes; ver a hipótese e as lacunas."
    spec = c["spec"]
    refs = sorted({*c["records"], *c["sources"], *(d for s in c["steps"] for d in s["det"]), *spec["det"],
                   *(x for s in c["steps"] for x in s["ctrl"] if x.startswith("CTRL-")), *(t for s in c["steps"] for t in s["llmi"])})
    doc = {
        "version": "0.5",
        "case": {"id": cid, "name": f"ARTEX · {c['short']}", "mission": c["mission"],
                 "decision_context": "Priorizar telemetria, detecção e controles contra os ataques conhecidos do ARTEX.",
                 "scope": ["ai-genai", "artex", "llminjection"], "status": "active"},
        "intelligence_requirements": [{"id": f"IR-{p}", "question": f"Como os ataques de {c['short']} com ARTEX alcançariam {c['cj'][0].lower()} aqui, e veríamos cada passo?",
                                       "decision_supported": "Ordem de investimento em telemetria, detecção e controle.", "stakeholder": "CTI e engenharia de detecção",
                                       "priority": "high", "time_horizon": "90 dias", "linked_crown_jewels": [cj], "information_gap_ids": gaps, "status": "open"}],
        "crown_jewels": [{"id": cj, "name": c["cj"][0], "rationale": c["cj"][1], "criticality": "critical"}],
        "architectures": [{"id": f"ARCH-{p}", "name": c["cj"][0], "nodes": [{"id": f"NODE-{p}", "name": c["cj"][0], "type": "control-plane", "trust_zone": "critical"}], "relationships": []}],
        "evidence_items": [{"id": e, "title": SRC[s]["name"], "source_type": "primary-external" if SRC[s].get("grade") == "A" else "secondary-external",
                            "source": SRC[s].get("publisher", ""), "reference": SRC[s].get("url", ""), "publication_date": SRC[s].get("published") or "",
                            "collected_at": SRC[s].get("last_verified", ""), "claim": f"Relato público usado no caso; registros: {', '.join(c['records'])}.",
                            "evidence_state": "observed" if SRC[s].get("grade") == "A" else "assessed",
                            "source_reliability": "high" if SRC[s].get("grade") == "A" else "medium", "information_credibility": "high" if SRC[s].get("grade") == "A" else "medium",
                            "temporal_relevance": "current", "supports": [hyp], "contradicts": [], "analyst_notes": f"Grau {SRC[s].get('grade')} ({s})."}
                           for e, s in zip(evid, c["sources"], strict=True)],
        "hypotheses": [{"id": hyp, "title": c["hyp"][0], "statement": c["hyp"][0], "rationale": c["context"], "intelligence_requirement_ids": [f"IR-{p}"],
                        "target_crown_jewels": [cj], "supporting_evidence": evid, "contradicting_evidence": [], "alternative_explanations": c["hyp"][1],
                        "assumptions": ["O ambiente modelado tem o ativo crítico descrito."], "confidence": c["conf"] if c["conf"] in ("high", "medium", "low") else "high",
                        "information_gap_ids": gaps, "attack_path_ids": [ts], "status": "supported", "owner": "cti", "created_at": CUT, "review_date": "2026-12-22"}],
        "threat_contexts": [{"id": ctx, "name": f"ARTEX · {c['short']}", "lens_id": "ai-genai", "relevance": c["context"], "status": "active",
                             "crown_jewel_ids": [cj], "architecture_ids": [f"ARCH-{p}"], "scenario_ids": [ts], "intelligence_requirement_ids": [f"IR-{p}"],
                             "confidence": "high", "freshness": "current"}],
        "scenarios": [{"id": ts, "title": spec["title"], "objective": c["mission"], "hypothesis_ids": [hyp], "target_crown_jewels": [cj], "threat_context_ids": [ctx],
                       "attack_path": {"id": f"AP-{p}", "entry_vector": c["steps"][0]["pt"],
                                       "steps": [{"order": i + 1, "behavior": s["pt"], "phase": s["phase"], "attack_techniques": s["attack"],
                                                  "llminjection_techniques": s["llmi"], "llminjection_detections": s["det"], "controls": s["ctrl"],
                                                  "architecture_node_id": f"NODE-{p}", "gap": s["gap"]} for i, s in enumerate(c["steps"])]},
                       "impact": {"business": c["cj"][1], "technical": "Comprometimento do ativo crítico modelado."},
                       "priority": pr, "confidence": "high", "telemetry_requirements": [tcs], "detection_use_cases": [],
                       "detection_specification_ids": [dsp], "validation_ids": [val]}],
        "telemetry_contracts": [{"id": tcs, "title": f"Contrato de observáveis · {c['short']}", "scenario_ids": [ts], "detection_use_case_ids": [],
                                 "behavior": spec["behavior"], "observable": "; ".join(s["tel"] for s in c["steps"]),
                                 "source": "; ".join(dict.fromkeys(s["tel"].split(":")[0] for s in c["steps"])),
                                 "event_or_state_change": spec["stages"][-1]["all"][0]["value"], "entity_identifiers": spec["group_by"],
                                 "required_fields": ["event.action", "timestamp", *spec["group_by"]], "retention": "90d", "latency_target": "<15m",
                                 "normalization": "modelo de evento conceitual do TCE", "integrity_requirements": ["monitorar a saúde da fonte"],
                                 "failure_modes": ["fonte não coletada", "relógio sem precisão de segundos"], "status": "partial",
                                 "owner": "detection-engineering", "review_date": "2026-12-22"}],
        "detection_specifications": [{"id": dsp, "title": spec["title"], "scenario_ids": [ts], "detection_use_case_ids": [], "telemetry_contract_ids": [tcs],
                                      "attack_techniques": sorted({a for s in c["steps"] for a in s["attack"]}), "severity": "high", "status": "ready",
                                      "analytic_concept": {"description": spec["title"], "behavior": spec["behavior"], "observable_effect": "Eventos do mesmo ator em ordem.",
                                                           "entities": spec["group_by"], "benign_alternatives": c["hyp"][1]},
                                      "correlation": {"pattern_id": "ordered-sequence", "window": spec["window"], "group_by": spec["group_by"]},
                                      "validation_logic": {"pattern": "ordered-sequence", "group_by": spec["group_by"], "stages": spec["stages"]},
                                      "implementations": [{"id": d, "type": "llminjection-detection", "platform": "generic", "status": "specification", "reference": f"data/detections.json#{d}"} for d in spec["det"]]
                                      or [{"id": f"tcem-{dsp}", "type": "tcem-spec", "platform": "generic", "status": "specified", "reference": "este caso"}],
                                      "validation_ids": [val], "references": c["sources"], "owner": "detection-engineering", "review_date": "2026-12-22"}],
        "validations": [{"id": val, "title": f"Replay seguro · {c['short']}", "scenario_ids": [ts], "detection_use_case_ids": [], "detection_specification_ids": [dsp],
                         "method": "log-replay", "environment": "fixture defensiva sintética do repositório", "expected_result": "Exatamente uma sequência do mesmo ator.",
                         "fixture": "fixtures/events.jsonl", "expected": {"min_matches": 1, "max_matches": 1}, "actual_result": "", "status": "not-tested",
                         "evidence_refs": [], "tested_at": CUT, "owner": "detection-engineering"}],
        "intelligence_gaps": [{"id": g, "question": q, "affected_requirement_ids": [f"IR-{p}"], "affected_hypothesis_ids": [hyp], "affected_scenario_ids": [ts],
                               "priority": "high", "collection_action": "Coleta interna ou nova fonte primária.", "owner": "cti", "status": "open", "due_date": "2026-12-22"}
                              for g, q in zip(gaps, c["gaps"], strict=True)],
        "decisions": [{"id": d, "title": t, "statement": t, "decision_owner": "segurança", "status": "proposed", "intelligence_requirement_ids": [f"IR-{p}"],
                       "crown_jewel_ids": [cj], "hypothesis_ids": [hyp], "scenario_ids": [ts], "evidence_ids": evid, "detection_use_case_ids": [],
                       "intelligence_gap_ids": gaps, "rationale": c["context"], "created_at": CUT, "review_date": "2026-12-22"} for d, t in zip(decs, c["decisions"], strict=True)],
        "x_llminjection": {"generated_by": "scripts/build_tcem.py", "method": "TCEM v0.5.1 (Cyber-Threat-Context-Modeling, mesmo autor)", "refs": refs,
                           "fixture_note": c["fixture_note"]},
    }
    return doc


# ---------- SVG ----------
INK, PAPER, SIG, SIGS, MUTED, TEAL, LINE = "#15140f", "#f6f5f1", "#b43c0e", "#f7e6dc", "#6b675d", "#1f6f8b", "#d9d5ca"
SANS, MONO = "Inter, Helvetica, Arial, sans-serif", "JetBrains Mono, Menlo, Consolas, monospace"


def wrap(t: str, n: int) -> list[str]:
    out, cur = [], ""
    for w in t.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + ([cur] if cur else [])


def text(x, y, s, size=12, color=INK, weight=400, font=SANS, anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>'


CONF_PT = {"confirmed": "confirmada", "high": "alta", "medium": "média", "low": "baixa"}


def case_svg(c: dict, result: dict) -> str:
    steps, W = c["steps"], 1200
    cw, gap, x0 = (W - 150 - 20) / len(steps) - 14, 14, 150
    H = 530
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Caminho de ataque TCEM: {escape(c["short"])}">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', f'<rect width="{W}" height="64" fill="{INK}"/>',
         text(24, 26, f"TCEM · ARTEX · {c['short'].upper()}", 11, "#e8a07f", 700, MONO), text(24, 50, c["who"], 17, PAPER, 700),
         text(W - 24, 26, f"{c['id']} · confiança {CONF_PT[c['conf']]}", 11, "#b9b5aa", 400, MONO, "end"),
         text(W - 24, 50, f"Ativo crítico: {c['cj'][0]}"[:96], 12, "#e6e2d8", 400, SANS, "end")]
    rows = [("CAMINHO", 84, 150), ("TELEMETRIA", 250, 84), ("DETECÇÃO", 344, 82), ("CONTROLE", 438, 60)]
    for label, y, h in rows:
        o.append(text(20, y + 22, label, 10.5, MUTED, 700, MONO))
        o.append(f'<line x1="20" y1="{y + h + 6}" x2="{W - 20}" y2="{y + h + 6}" stroke="{LINE}"/>')
    for i, s in enumerate(steps):
        x = x0 + i * (cw + gap)
        o.append(f'<rect x="{x}" y="84" width="{cw}" height="150" rx="6" fill="#ffffff" stroke="{INK}" stroke-width="1.2"/>')
        o.append(f'<rect x="{x}" y="84" width="{cw}" height="22" rx="6" fill="{SIG if s["det"] else INK}"/>')
        o.append(f'<rect x="{x}" y="98" width="{cw}" height="8" fill="{SIG if s["det"] else INK}"/>')
        o.append(text(x + 8, 99, f"{i + 1} · {s['phase'].upper()}"[: int(cw / 6.1)], 9.5, "#ffffff", 700, MONO))
        for j, ln in enumerate(wrap(s["pt"], int(cw / 7.0))[:6]):
            o.append(text(x + 8, 124 + j * 15, ln, 11.5, INK, 600))
        o.append(text(x + 8, 226, " ".join(s["attack"])[: int(cw / 6.2)], 9.5, TEAL, 600, MONO))
        if i < len(steps) - 1:
            ax = x + cw
            o.append(f'<path d="M{ax + 2} 159 L{ax + gap - 3} 159 M{ax + gap - 8} 154 L{ax + gap - 3} 159 L{ax + gap - 8} 164" stroke="{INK}" stroke-width="1.5" fill="none"/>')
        for j, ln in enumerate(wrap(s["tel"], int(cw / 6.0))[:4]):
            o.append(text(x + 4, 266 + j * 14, ln, 10.5, INK))
        if s["det"]:
            for j, d in enumerate(s["det"][:2]):
                o.append(f'<rect x="{x}" y="{350 + j * 38}" width="{cw}" height="34" rx="6" fill="{SIG}"/>')
                o.append(text(x + 8, 363 + j * 38, d, 10, "#ffffff", 700, MONO))
                o.append(text(x + 8, 377 + j * 38, wrap(DET_NAMES.get(d, ""), int(cw / 5.6))[0], 9, "#fbe9df", 400))
        else:
            o.append(f'<rect x="{x}" y="350" width="{cw}" height="72" rx="6" fill="none" stroke="{SIG}" stroke-dasharray="5 4" stroke-width="1.4"/>')
            o.append(text(x + 8, 366, "LACUNA", 10, SIG, 700, MONO))
            for j, ln in enumerate(wrap(s["gap"] or "Sem detecção no repositório.", int(cw / 5.6))[:3]):
                o.append(text(x + 8, 381 + j * 13, ln, 9.5, INK))
        for j, ct in enumerate(s["ctrl"][:2]):
            o.append(f'<rect x="{x}" y="{444 + j * 26}" width="{cw}" height="21" rx="4" fill="{SIGS}"/>')
            o.append(text(x + 8, 458 + j * 26, ct[: int(cw / 5.4)], 9, INK, 600, MONO if ct.startswith("CTRL-") else SANS))
    ok = all(r["passed"] for r in result)
    o.append(text(20, H - 12, f"Validação por replay: {'passou' if ok else 'falhou'} ({', '.join(str(r['matches']) for r in result)} alerta) · fixture sintética · {c['spec']['behavior']}"[:170], 10, MUTED, 400, MONO))
    o.append("</svg>")
    return "\n".join(o) + "\n"


def overview_svg() -> str:
    W, left, top, cw, rh = 1200, 210, 112, (1200 - 210 - 20) / len(PHASES), 46
    H = top + rh * len(CASES) + 70
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Cobertura TCEM dos ataques do ARTEX por fase">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', text(20, 30, "ATAQUES CONHECIDOS DO ARTEX · O QUE O REPOSITÓRIO DETECTA EM CADA FASE", 12, SIG, 700, MONO),
         text(20, 54, "Laranja: passo observado com detecção DET-AI. Contorno tracejado: passo observado sem detecção de IA (lacuna). Vazio: não descrito pelas fontes.", 12, INK)]
    for j, ph in enumerate(PHASES):
        for k, ln in enumerate(wrap(ph, 14)):
            o.append(text(left + j * cw + cw / 2, top - 14 + k * 12 - (len(wrap(ph, 14)) - 1) * 12, ln, 10, MUTED, 700, SANS, "middle"))
    for i, c in enumerate(CASES):
        y = top + i * rh
        o.append(text(20, y + 27, c["short"], 13, INK, 700))
        for j, ph in enumerate(PHASES):
            st = [s for s in c["steps"] if s["phase"] == ph]
            x = left + j * cw + 4
            if not st:
                o.append(f'<rect x="{x}" y="{y + 6}" width="{cw - 8}" height="{rh - 12}" rx="4" fill="#ffffff" stroke="{LINE}"/>')
            elif any(s["det"] for s in st):
                dets = sorted({d.removeprefix("DET-AI-") for s in st for d in s["det"]})
                o.append(f'<rect x="{x}" y="{y + 6}" width="{cw - 8}" height="{rh - 12}" rx="4" fill="{SIG}"/>')
                o.append(text(x + (cw - 8) / 2, y + 28, " ".join(dets), 10.5, "#ffffff", 700, MONO, "middle"))
            else:
                o.append(f'<rect x="{x}" y="{y + 6}" width="{cw - 8}" height="{rh - 12}" rx="4" fill="#ffffff" stroke="{SIG}" stroke-dasharray="5 4" stroke-width="1.4"/>')
                o.append(text(x + (cw - 8) / 2, y + 28, "lacuna", 10.5, SIG, 700, MONO, "middle"))
    o.append(text(20, H - 18, f"Fonte: tcem/cases (TCEM v0.5.1) · corte {CUT} · números em cada célula são DET-AI-0xx", 10, MUTED, 400, MONO))
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ---------- report ----------
def report(results: dict[str, list]) -> str:
    n_steps = sum(len(c["steps"]) for c in CASES)
    n_det = sum(1 for c in CASES for s in c["steps"] if s["det"])
    L = ['---', 'pdf: reports/pdf/LLMI-TM-ARTEX.pdf', 'title: "Modelagem de ameaças TCEM: ataques conhecidos do ARTEX"', '---', '',
         '![Masthead](../../assets/reports/masthead-dossier.svg)', '',
         f'<p class="rpt-head"><span>LLMI-TM-ARTEX · v0.1</span><span class="tlp">TLP:CLEAR</span><span>Corte {CUT}</span></p>', '',
         '<div class="injected" markdown="1">',
         'Modelagem feita com o **TCEM, Threat Context Engineering Method** ([Cyber-Threat-Context-Modeling](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling), v0.5.1), '
         'método do mesmo autor deste repositório. Cada caso é um arquivo TCEM em `tcem/cases/` que carrega no próprio toolkit (`tce validate`) '
         'e é validado aqui por `scripts/tcem_validate.py`. Os fatos vêm dos registros e fontes citados; a modelagem (ativo crítico, ordem dos passos, prioridade) é julgamento do analista.',
         '</div>', '',
         '<div class="bluf" markdown="1">',
         f'Seis caminhos de ataque do ARTEX, com {n_steps} passos ao todo. Em {n_det} deles há uma detecção do repositório; nos outros {n_steps - n_det} '
         'a cobertura depende de regras clássicas ou de telemetria de negócio. O ARTEX deixa marca no ritmo (varredura, spray, prova de permissões, '
         'saída para APIs de LLM), e é ali que as detecções de IA funcionam. Depois do acesso, a intrusão volta a ser clássica, e o caso CRAFTY FALCON '
         'mostra que contra fraude a detecção que vale é a de negócio.',
         '</div>', '',
         '## 1. Como ler', '',
         'Cada caso segue a cadeia do TCEM: **ativo crítico → contexto de ameaça → caminho do ator → contrato de telemetria → detecção → validação → decisão**. '
         'No diagrama, a linha de cima é o caminho na ordem das fontes; abaixo de cada passo ficam a telemetria que o torna visível, a detecção do repositório '
         '(laranja) ou a lacuna (tracejado), e os controles que reduzem o passo.', '',
         '| Elemento | O que é |', '|---|---|',
         '| Caminho | Passos observados pelas fontes, em ordem, com técnicas ATT&CK |',
         '| Telemetria | O que precisa ser coletado para ver o passo |',
         '| Detecção | `DET-AI-0xx` do repositório, ou lacuna declarada |',
         '| Validação | Replay de eventos sintéticos contra a lógica da detecção, com resultado esperado |',
         '| Decisão | O que fazer, ligado ao ativo, à hipótese e à evidência |', '',
         '## 2. Visão geral', '', '![Cobertura por fase](../../assets/tcem/overview.svg)', '',
         '| Caso | Quem | Confiança | Passos | Com DET-AI | Validação |', '|---|---|---|---|---|---|']
    for c in CASES:
        r = results[c["id"]]
        L.append(f"| {c['short']} | {c['who']} | {CONF_PT[c['conf']]} | {len(c['steps'])} | {sum(1 for s in c['steps'] if s['det'])} | "
                 f"{'passou' if all(x['passed'] for x in r) else 'falhou'} |")
    for k, c in enumerate(CASES, 3):
        r = results[c["id"]]
        L += ["", f"## {k}. {c['short']}", "", f"**Quem:** {c['who']}. **Registros:** {', '.join(f'`{x}`' for x in c['records'])}.", "",
              f"**Ativo crítico:** {c['cj'][0]}. {c['cj'][1]}", "", c["context"], "",
              f"![Caminho de ataque: {c['short']}](../../assets/tcem/{c['file']}.svg)", "",
              "| # | Fase | Passo | ATT&CK | Detecção | Controle |", "|---|---|---|---|---|---|"]
        for i, s in enumerate(c["steps"], 1):
            det = ", ".join(f"`{d}`" for d in s["det"]) or f"lacuna: {s['gap']}"
            L.append(f"| {i} | {s['phase']} | {s['pt']} | {' '.join(s['attack'])} | {det} | {', '.join(s['ctrl']) or '–'} |")
        L += ["", f"**Hipótese.** {c['hyp'][0]} Alternativas: {'; '.join(c['hyp'][1]).lower()}.", "",
              f"**Validação.** {c['spec']['title']} (`{c['spec']['behavior']}`). {c['fixture_note']} Resultado do replay: "
              f"{', '.join(str(x['matches']) for x in r)} alerta, {'passou' if all(x['passed'] for x in r) else 'falhou'}.", "",
              "**Lacunas de inteligência.** " + " ".join(f"({i}) {g}" for i, g in enumerate(c["gaps"], 1)), "",
              "**Decisões propostas.** " + " ".join(f"({i}) {d}" for i, d in enumerate(c["decisions"], 1)), "",
              f"Arquivo do caso: `tcem/cases/{c['id']}/case.json`."]
    k = 3 + len(CASES)
    L += ["", f"## {k}. O que não foi modelado", "", "| Relato | Registro | Por quê |", "|---|---|---|"]
    L += [f"| {a} | `{b}` | {w} |" for a, b, w in NOT_MODELLED]
    L += ["", f"## {k + 1}. Como reproduzir", "", "```bash", "python3 scripts/build_tcem.py        # gera casos, fixtures, diagramas e este relatório",
          "python3 scripts/tcem_validate.py     # checa estrutura, referências e replay", "tce validate tcem/cases/CASE-ARTEX-STORM-0940   # no toolkit TCEM", "```", "",
          f"## {k + 2}. Fontes", "", "| ID | Publicador | Grau | Data |", "|---|---|---|---|"]
    for sid in sorted({s for c in CASES for s in c["sources"]}):
        s = SRC[sid]
        L.append(f"| [`{sid}`]({s.get('url', '')}) | {s.get('publisher', '')} | {s.get('grade', '')} | {s.get('published') or '–'} |")
    L += ["", "Método: TCEM, Threat Context Engineering Method, v0.5.1 ([repositório](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling)). "
          "Mesmo autor deste repositório: a referência descreve o método usado, não é validação independente.", ""]
    return "\n".join(L)


def main() -> int:
    load()
    OUT_ART.mkdir(parents=True, exist_ok=True)
    results = {}
    for c in CASES:
        d = OUT_CASES / c["id"]
        (d / "fixtures").mkdir(parents=True, exist_ok=True)
        (d / "fixtures" / "events.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in c["fixture"]), encoding="utf-8")
        doc = case_doc(c)
        res = run_validations(doc, d)
        ok = all(r["passed"] for r in res)
        doc["validations"][0].update(status="passed" if ok else "failed",
                                     actual_result=f"{', '.join(str(r['matches']) for r in res)} sequência(s) detectada(s) no replay; esperado 1.")
        (d / "case.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        (OUT_ART / f"{c['file']}.svg").write_text(case_svg(c, res), encoding="utf-8")
        results[c["id"]] = res
        print(f"{c['id']}: {'ok' if ok else 'FAILED'}")
    (OUT_ART / "overview.svg").write_text(overview_svg(), encoding="utf-8")
    OUT_MD.write_text(report(results), encoding="utf-8")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    return 0 if all(all(r["passed"] for r in v) for v in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
