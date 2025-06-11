import pandas as pd
import requests

url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

try:
    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()

    municipios_nordeste = []
    for municipio in dados:
        try:
            regiao_id = municipio['microrregiao']['mesorregiao']['UF']['regiao']['id']
            if regiao_id == 2:  
                municipios_nordeste.append(municipio)
        except (TypeError, KeyError):
            continue

    df_nordeste = pd.DataFrame(municipios_nordeste)
    df_nordeste.to_json("Municipios_Nordeste_ID.json", orient='records', force_ascii=False, indent=4)

    print("O arquivo 'Municipios_Nordeste_ID.json' foi gerado")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
