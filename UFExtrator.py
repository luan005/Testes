import pandas as pd
import requests

url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

try:
    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()
    df = pd.DataFrame(dados)

    df_nordeste = df[df['regiao'].apply(lambda r : r['id'] == 2)]

    df_nordeste.to_json("UF_Nordeste.json", orient='records', force_ascii= False, indent=4)

    print("O arquivo 'UF_Nordeste.json' foi gerado")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição : {e}")
except Exception as e:
    print(f"Erro inesperado : {e}")