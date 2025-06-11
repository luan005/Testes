import pandas as pd
import requests

url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"

try:
    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()

    microrregioes_nordeste = []
    for microrregiao in dados:
        try:
            regiao_id = microrregiao['mesorregiao']['UF']['regiao']['id']
            if regiao_id == 2:  
                microrregioes_nordeste.append(microrregiao)
        except (TypeError, KeyError):
            continue

    df_nordeste = pd.DataFrame(microrregioes_nordeste)
    df_nordeste.to_json("Microrregioes_Nordeste.json", orient='records', force_ascii=False, indent=4)

    print("O arquivo 'Microrregioes_Nordeste.json' foi gerado")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
