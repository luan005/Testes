import json
import sqlite3

with open('dados_pb_pe_rn.json', encoding='utf-8') as f:
    dados = json.load(f)

conn = sqlite3.connect('censoescolar.db')
cursor = conn.cursor()

inseridos = 0
ignorados = 0

for inst in dados:
    try:
        qt_mat_bas = inst.get('QT_MAT_BAS')
        if qt_mat_bas in [None, "", "NaN"]:
            qt_mat_bas = "0"

        values = (
            inst.get('NO_REGIAO', ''),
            inst.get('SG_UF', ''),
            inst.get('NO_MUNICIPIO', ''),
            inst.get('NO_MESORREGIAO', ''),
            inst.get('NO_MICRORREGIAO', ''),
            inst.get('CO_ENTIDADE', ''),
            qt_mat_bas,
            inst.get('CO_REGIAO', ''),
            inst.get('CO_UF', ''),
            inst.get('CO_MUNICIPIO', ''),
            inst.get('CO_MICRORREGIAO', ''),
            inst.get('CO_MESORREGIAO', '')
        )

        cursor.execute('''
            INSERT INTO tb_instituicao (
                no_regiao, sg_uf, no_municipio, no_mesorregiao, no_microrregiao,
                co_entidade, qt_mat_bas, co_regiao, co_uf, co_municipio, co_microrregiao, co_mesorregiao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', values)
        inseridos += 1

    except Exception as e:
        ignorados += 1
        print(f"Ignorado por erro: {e}")

conn.commit()
conn.close()

print(f" {inseridos} registros inseridos com sucesso. {ignorados} foram ignorados por erro.")
