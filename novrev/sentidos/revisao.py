"""Gera novrev/sentidos/revisao/LANG.xlsx: 3 colunas no próprio idioma (palavra, definição, outros sentidos), ordem VCU14."""
import json,os
from openpyxl import Workbook
from openpyxl.styles import Font,Alignment
H={'en':('Word','Definition','Other meanings'),'pt-BR':('Palavra','Definição','Outros sentidos'),
   'ja':('語','意味','ほかの意味'),'zh':('词','释义','其他意思')}
SEP={'en':', ','pt-BR':', ','ja':'、','zh':'、'}
os.makedirs('novrev/sentidos/revisao',exist_ok=True)
for l in H:
    E=json.load(open(f'v2/{l}-core-v2.json'))['entries']
    by={}
    for e in E:
        for w in [e['text']]+(e.get('alternatives') or []): by.setdefault(w,[]).append(e)
    E.sort(key=lambda e:(e.get('vcu14_rank') or 10**6, e.get('study_priority') or 10**6))
    wb=Workbook(); ws=wb.active; ws.title=l; ws.append(H[l])
    for c in ws[1]: c.font=Font(bold=True)
    for e in E:
        alt=e.get('alternatives') or []
        word=e['text']+(f" ({SEP[l].join(alt)})" if alt else '')
        others=[]; seen={e['english_id']}
        for w in [e['text']]+alt:
            for o in by.get(w,[]):
                if o['english_id'] in seen: continue
                seen.add(o['english_id']); others.append(f"{o['text']}: {o['description']}")
        ws.append([word,e['description'],'\n'.join(others)])
    for col,w in zip('ABC',(28,70,80)): ws.column_dimensions[col].width=w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
    ws.freeze_panes='A2'
    wb.save(f'novrev/sentidos/revisao/{l}.xlsx'); print(l,len(E))
