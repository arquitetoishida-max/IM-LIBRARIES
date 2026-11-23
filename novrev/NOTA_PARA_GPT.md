# Nota de execução NOVREV — atualização de 23/11/2026

A revisão dos quatro núcleos está pausada. A ordem editorial vigente está na [LEXICON #88](https://github.com/arquitetoishida-max/LEXICON/issues/88). A matriz, os pacotes, os checkpoints e a entrega seguem a [IM-LIBRARIES #505](https://github.com/arquitetoishida-max/IM-LIBRARIES/issues/505). A apresentação das duas faces do Card fica com Claude na [ISHIDA-MULTILANG #122](https://github.com/arquitetoishida-max/ISHIDA-MULTILANG/issues/122).

Quando o proprietário liberar a revisão, Codex confere integralmente os núcleos NOVREV atuais. Preservar entradas corretas e usar as filas anteriores como histórico. A divisão de trabalho e a amostragem da nota de 19/11 se referem à reconstrução anterior. Ver [NOVREV.md](NOVREV.md) para a sequência atual.

## Registro anterior — 19/11/2026

**Todas as filas e ordens de revisão antigas estão ENCERRADAS por decisão do dono.** A tarefa agendada horária foi desligada. Não retome QUEUE.csv, nem ordens de serviço antigas de revisão de dicionários, nem PRs de lote dessa fila.

## O que vale agora: NOVREV
- Repositório IM-LIBRARIES, pasta `novrev/` (`NOVREV.md` = regras; `NOVREV_matriz.xlsx` = 1 linha por conceito, 4 IDs).
- Somente **en, pt-BR, ja e zh** (núcleos). Os demais pacotes foram **despublicados** do `v2/catalog.json` (1.3.0, arquivos preservados) e só voltam após passar pela NOVREV.
- Os 4 dicionários serão **reconstruídos do zero por conceito** (`english_id` é a âncora; IDs e ordem preservados; o que já foi conferido — leituras, pinyin, JLPT/HSK, environments, vcu14 — não se perde). Quantidades iguais nos 4. Base = VCU14 (1.060 conceitos nos 4); o resto é VCU14+ (fim da fila, pode ser enxugado).
- Quem reconstrói: Claude, em lotes grandes, com branch/PRs próprios `novrev/*`. **Seu papel:** auditar as PRs `novrev/*` por amostra e por regras (IDs intactos, mesmas quantidades, campos 100% preenchidos, descrição nativa, sem notas de variante). Não reabra revisão linha a linha dos dicionários antigos.
- Não publique nada fora do fluxo NOVREV. Dono: Gabriel Noboru Ishida.
