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

O código atual do aplicativo pode precisar de um adaptador ao novo esquema de conceitos. **Não habilitar este pacote para usuários finais antes de validar o importador e a revisão das traduções.** Futuros pacotes de até 1.500 palavras por idioma serão construídos após seleção e verificação de fontes e licenças.
