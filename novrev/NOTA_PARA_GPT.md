# NOTA PARA O GPT/CODEX — LEIA ANTES DE QUALQUER AÇÃO (19/11/2026)

**Todas as filas e ordens de revisão antigas estão ENCERRADAS por decisão do dono.** A tarefa agendada horária foi desligada. Não retome QUEUE.csv, nem ordens de serviço antigas de revisão de dicionários, nem PRs de lote dessa fila.

## O que vale agora: NOVREV
- Repositório IM-LIBRARIES, pasta `novrev/` (`NOVREV.md` = regras; `NOVREV_matriz.xlsx` = 1 linha por conceito, 4 IDs).
- Somente **en, pt-BR, ja e zh** (núcleos). Os demais pacotes foram **despublicados** do `v2/catalog.json` (1.3.0, arquivos preservados) e só voltam após passar pela NOVREV.
- Os 4 dicionários serão **reconstruídos do zero por conceito** (`english_id` é a âncora; IDs e ordem preservados; o que já foi conferido — leituras, pinyin, JLPT/HSK, environments, vcu14 — não se perde). Quantidades iguais nos 4. Base = VCU14 (1.060 conceitos nos 4); o resto é VCU14+ (fim da fila, pode ser enxugado).
- Quem reconstrói: Claude, em lotes grandes, com branch/PRs próprios `novrev/*`. **Seu papel:** auditar as PRs `novrev/*` por amostra e por regras (IDs intactos, mesmas quantidades, campos 100% preenchidos, descrição nativa, sem notas de variante). Não reabra revisão linha a linha dos dicionários antigos.
- Não publique nada fora do fluxo NOVREV. Dono: Gabriel Noboru Ishida.
