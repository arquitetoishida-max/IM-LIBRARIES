# Auditoria de sentidos (IM-LIBRARIES #512)
Concluída: todas as 3.468 palavras da lista foram passadas (posições 0–3468). Os últimos trechos eram em grande parte formas verbais, gírias, regionais e IDs já criados pelo NOVREV, sem sentidos faltando.
Novos IDs: en:000004420–4517 (98 sentidos que faltavam, um por ID, nos 4 idiomas). Pacotes: 3.962 entradas.
Pendentes sem equivalente nos 4 idiomas: *to* (infinitivo), *do* (auxiliar), *that* (conjunção integrante).
Fontes: dicionários existentes e conhecimento editorial; sem pesquisa online palavra por palavra.
Próxima etapa: segunda passada (descrições e alternativas independentes por idioma, issue #512), por prioridade, coluna a coluna.
Método: novo ID = gerador + `apply.py`; validar com pytest, validate_vcu100_catalog.py e check.py; branch novrev/auditoria-sentidos; sem merge, sem APK.

## Segunda passada (descrições e alternativas por idioma)
Coluna JA, top 700 por prioridade: 562 verbetes reescritos (descrição com usos principais + alternativas). Coluna JA concluída (top 700); depois ZH (553), EN (457), PT (111). Lista: `python3 sp.py <col> 0 60 <limite>` (ver novrev/tools/sp.py).
