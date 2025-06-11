import pandas as pd
import requests

url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"

try:
    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()

    mesorregioes_nordeste = []
    for mesorregiao in dados:
        try:
            regiao_id = mesorregiao['UF']['regiao']['id']
            if regiao_id == 2:  
                mesorregioes_nordeste.append(mesorregiao)
        except (TypeError, KeyError):
            continue

    df_nordeste = pd.DataFrame(mesorregioes_nordeste)
    df_nordeste.to_json("Mesorregioes_Nordeste.json", orient='records', force_ascii=False, indent=4)

    print("O arquivo 'Mesorregioes_Nordeste.json' foi gerado")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
