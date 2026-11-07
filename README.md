# ISHIDA MULTILANG — Distribuição de bibliotecas

**Catálogo público ativo do APK:** [v2/catalog.json](v2/catalog.json) (`schema_version=2`, `kind=ishida-monolingual`). Os arquivos deste catálogo são os únicos que o aplicativo instalado deve interpretar; cada pacote declara URL, versão, contagem e SHA-256.

**LEXICON** é a fonte editorial e de curadoria; **IM-LIBRARIES** guarda os arquivos versionados e seus metadados. O aplicativo consome os pacotes publicados. Os IDs semânticos, classes e relações entre idiomas precisam permanecer estáveis para preservar notas, grupos e histórico.

## Núcleo e VCU100

- `v2/*-core-v2.json`: bibliotecas básicas VCU14 por idioma. Não alterar núcleos públicos sem auditoria específica.
- `v2/vcu100/`: vocabulários profissionais especializados, separados do VCU14 e disponíveis por pacote. Para palavras traduzidas entre dois idiomas, o par usa o mesmo `english_id` e `english_sense_id` e IDs independentes dos núcleos.
- **Nove publicações VCU100 (06/11/2026)** em [v2/vcu100](v2/vcu100) — cada uma possui pacote-par alinhado semanticamente, separado do VCU14: Construction Site EN **178**; Business EN **156**; Healthcare EN **170**; Architecture & Interiors EN **180**; Factory JA **179**; Japanese Tourism JA **175**; Brazil Tourism PT-BR **176**; South America Adventure ES **175**; Mandarin Tourism/Sourcing ZH **168**. Total **1.557 entradas principais + 1.557 pares**, catálogo V2 versão **1.1.11**.
- *Compatibilidade*: o app atual ainda precisa completar instalação automática de dependências, classificação VCU100 e testes de progresso/temas; consultar ISHIDA-MULTILANG #35/#38/#39.
- Pacotes de gírias regionais (`role=regional`) são distintos de VCU100 (`role=specialized`). Não renomear pacotes para fingir independência sem suporte no Flutter.

**Estado:** publicadas em repositório por autorização específica do proprietário. Ainda não homologadas na versão Android; instalação do par, classificação VCU100, TTS/STT, notas e rollback dependem dos testes ISHIDA-MULTILANG #35/#38/#39. Gírias regionais NY/CA/TX/Sul/Blues continuam em curadoria; não inflar o catálogo com termos sem comprovação regional.

## Arquivo histórico

O arquivo da raiz `catalog.json` é **pesquisa antiga em schema 1** e **não é o catálogo do APK**. O experimento de 38 conceitos `core-multilingual-pilot-001` foi removido do ramo ativo em 06/11/2026 por ser obsoleto (permanece recuperável pelo histórico do Git). Os demais conjuntos herdados de fontes externas continuam como materiais históricos não distribuídos pelo app; a existência deles não comprova alinhamento semântico, revisão linguística nem autorização de publicação.

O workflow legado `.github/workflows/build-libraries.yml` (geração automática apenas de schema 1) foi excluído em 07/11/2026, pois não gera pacotes do catálogo ativo. O código `scripts/build_packages.py` e arquivos históricos de fontes públicas foram preservados para auditoria e eventual reaproveitamento; não são instalados pelo APK.

Os fluxos antigos da pasta `packages/` não devem modificar `v2/catalog.json`. Publicações novas passam por LEXICON → pacotes V2 → validação → catálogo V2 e testes Android. Não preencher contagens mínimas com traduções inventadas.
