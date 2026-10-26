# ISHIDA MULTILANG — Bibliotecas de idiomas

Este repositório público distribui pacotes de vocabulário para o aplicativo ISHIDA MULTILANG.

## Piloto publicado
- **38 conceitos** com campos completos em 8 idiomas/variantes: `pt-BR`, `pt-PT`, `en`, `ja`, `it`, `es`, `fr` e `de`.
- `pt-BR`: **Port. (Brasileiro)**, bandeira Brasil.
- `pt-PT`: **Portugues**, bandeira Portugal.
- Não há frequência real ainda; níveis JLPT herdados da base do aplicativo são comunitários, não oficiais.
- **Status: piloto técnico, não validado para distribuição geral**. Traduções complementares exigem revisão linguística.

Arquivos:
- [catalog.json](catalog.json): índice de pacotes realmente presentes.
- [packages/core-multilingual-pilot-001.json](packages/core-multilingual-pilot-001.json): pacote inicial de 38 conceitos.

As entradas de partida derivam do `starterWords` do aplicativo; traduções para outros idiomas foram acrescentadas como piloto para testar o formato. Nenhum dicionário externo ou corpus de frequência foi redistribuído aqui.

O código atual do aplicativo pode precisar de um adaptador ao novo esquema de conceitos. **Não habilitar este pacote para usuários finais antes de validar o importador e a revisão das traduções.** Futuros pacotes de até 2.000 entradas (palavras e expressões) por idioma serão construídos após seleção e verificação de fontes e licenças.

## Expansão automática — meta 2.000

O fluxo em `.github/workflows/build-libraries.yml` utiliza `scripts/build_packages.py` para preparar até 2.000 registros de fontes públicas por idioma. Os IDs `kaikki-<idioma>:<lema>` e `cedict:<termo>:<leitura>` são identificadores **de fonte**, não identificadores internacionais de conceitos. Correspondência entre idiomas exige revisão por sentido.

A expansão automática tem, inicialmente, traduções/definições **para o inglês**, não traduções completas entre quaisquer dois idiomas. Aplicar filtro estrito por par no aplicativo. Só considerar um pacote publicável após conferir integralidade, licenças, legibilidade das traduções e compatibilidade com o schema do app. A geração em Actions não garante disponibilidade dos arquivos até o workflow terminar e comitar os resultados.
