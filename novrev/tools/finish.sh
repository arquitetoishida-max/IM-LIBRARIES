#!/bin/bash
# finish.sh "991–1050" "texto do log" "1051" "en:000003182"
cd /home/claude/im-libraries || exit 1
python3 /home/claude/tools/check.py || exit 1
python3 -m pytest -q tests 2>&1 | tail -1
python3 scripts/validate_vcu100_catalog.py 2>&1 | grep -E "PASS|FAIL|ERROR"
NID=$(python3 -c "import openpyxl;m=list(openpyxl.load_workbook('novrev/NOVREV_matriz.xlsx',read_only=True)['NOVREV'].iter_rows(values_only=True));print(m[$3][1])")
for k in 1 2 3 4 5 6 7 8; do :; done
python3 /home/claude/tools/log.py "$1" "$2" "Retomar na posição $3, \`$NID\` (próximo ID da fila)."
sed -i -E "s/As posições 1–[0-9]+ foram percorridas\./As posições 1–$(( $3 - 1 )) foram percorridas./" novrev/NOVREV.md
git add -A && git commit -q -m "NOVREV: revisar posições $1 [skip ci]

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KgvxidCRZHcgiyJyjgSxaL"
git fetch -q --depth=1 origin novrev/revisao-quatro-nucleos 2>/dev/null; echo "remote: $(git rev-parse --short FETCH_HEAD) local-parent: $(git rev-parse --short HEAD~1)"
git -c push.negotiate=true push -q origin novrev/revisao-quatro-nucleos 2>&1 | grep -vi "moved\|new location\|^remote: *$"
