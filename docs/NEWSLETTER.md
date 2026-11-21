# Feed, edição semanal e e-mail

## O que já funciona

- **Feeds no site:** `feed.xml` (Atom) e `feed.json` (JSON Feed 1.1), gerados a cada build por `scripts/build_feed.py`. Entram todos os relatórios (relatório de inteligência, dossiês, Tendências da semana e Threat Landscape mensal), além dos incidentes, campanhas e entradas no CISA KEV dos últimos 60 dias. O `index.html` anuncia os dois feeds, então leitores RSS os encontram pelo endereço do site.
- **Edição semanal:** `scripts/build_weekly.py` gera o rascunho de `reports/trends/AAAA-Www.md` a partir dos datasets e dos digests diários da janela de sete dias. Ele preenche os números, a tabela de sinais (fonte e selo de cada um), as técnicas e ferramentas que apareceram e a versão curta para o LinkedIn. As seções analíticas (BLUF, contraponto, segunda-feira do defensor, Camada 8, para acompanhar) saem marcadas com `A PREENCHER`, e o teste `test_published_editions_have_no_unfilled_sections` impede publicar a edição com essas marcas.
- **Cadência:** a tarefa agendada "LLmInjection Tendências da semana" roda às terças às 18h17 (Brasília). Ela gera o rascunho, escreve as seções analíticas só a partir dos sinais listados e abre o PR `weekly/AAAA-Www`. Quem revisa mescla na quarta de manhã: o Pages publica a página, o PDF por impressão e a entrada no feed.

## Por que quarta-feira, 8h

Para público B2B de segurança, terça a quinta pela manhã é a janela de maior abertura. A quarta tem duas vantagens: cai um dia depois do Patch Tuesday (segunda terça do mês), então a edição já inclui o que a Microsoft e outros fornecedores publicaram, e pega a semana em andamento sem competir com a caixa de entrada cheia de segunda-feira.

## E-mail para quem quiser receber

O site é estático, então a lista de e-mails fica num serviço de RSS-para-e-mail que lê o `feed.xml` e envia sozinho a cada entrada nova:

1. Crie a conta num serviço com plano gratuito: Buttondown (RSS-to-email), follow.it ou campanhas RSS do Mailchimp.
2. Aponte o serviço para `https://ridd1kulusc0d3r.github.io/LLmInjection/feed.xml` e escolha envio semanal às quartas, 8h (America/Sao_Paulo).
3. Copie o endereço público do formulário de inscrição e coloque em `site/subscribe.json` (`email_form_action` e, se o serviço exigir outro nome, `email_field`). A área "Assinar" da aba Relatórios passa a mostrar o campo de e-mail.

**Configurado (2026-11-21):** Buttondown, conta `LLminjection`. O formulário do site envia para `https://buttondown.com/api/emails/embed-subscribe/LLminjection` (campo `email`), e o arquivo público das edições fica em <https://buttondown.com/LLminjection>, linkado ao lado dos feeds. Para o envio automático, ative no Buttondown a automação RSS-to-email com o `feed.xml` acima. Sem `email_form_action`, a área "Assinar" volta a mostrar só os feeds.

## Comandos

```bash
python scripts/build_weekly.py --end 2026-11-24   # rascunho da semana que termina em 24/11
python scripts/build_feed.py --out _site --reports _site/reports.json
```
