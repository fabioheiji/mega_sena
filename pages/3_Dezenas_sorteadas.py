from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from itertools import chain

from urllib.request import urlopen
import plotly
import plotly.express as px
import json
import plotly.graph_objects as go
import os
import re
from time import sleep
# from tqdm import tqdm, tnrange, tqdm_notebook
from tqdm.notebook import tnrange, tqdm
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

correct_names = {
    'BERNARDO DO CAMPO':'SÃO BERNARDO DO CAMPO',
    'GOIANIA':'GOIÂNIA',
    'MONGAGUA':'MONGAGUÁ',
    'SAO PAULO':'SÃO PAULO',
    'SALVADOR E VALENÇA':'SALVADOR, VALENÇA',
    'SANTO ANTÔNIO DE PÁDUA E RIO DE JANEIRO':'SANTO ANTÔNIO DE PÁDUA, RIO DE JANEIRO',
    'SIMOES FILHO':'SIMÕES FILHO',
    'URUCANIA':'URUCÂNIA',
    'URUÇUCA E CRUZ DAS ALMAS':'URUÇUCA, CRUZ DAS ALMAS',
    'VILA VELHA E VITÓRIA':'VILA VELHA, VITÓRIA',
    'VOTORANTIM E SÃO PAULO':'VOTORANTIM, SÃO PAULO',
    'AMERICANA E SÃO PAULO':'AMERICANA, SÃO PAULO',
    'ATIBAIA E BEBEDOURO':'ATIBAIA, BEBEDOURO',
    'BELEM':'BELÉM',
    'BRASILIA':'BRASÍLIA',
    'BALNEARIO CAMBORIU':'BALNEÁRIO CAMBORIÚ',
    'BALNEÁRIO CAMBORIU':'BALNEÁRIO CAMBORIÚ',
    'CAPITAL':'RIO DE JANEIRO',
    'COUNT E CARMO DO CAJURU':'CARMO DO CAJURU',
    'CRICIUMA':'CRICIÚMA',
    'CURITIBA E PALOTINA':'CURITIBA, PALOTINA',
    'FLORIANOPOLIS':'FLORIANÓPOLIS',
    'FAZENDA RIO GRANDE E PINHAIS':'FAZENDA RIO GRANDE, PINHAIS',
    'FRANCA E SÃO PAULO':'FRANCA, SÃO PAULO',
    'GUAIRA':'GUAÍRA',
    'GUAIRÁ':'GUAÍRA',
    'GUARULHOS E RIBEIRÃO PRETO':'GUARULHOS, RIBEIRÃO PRETO',
    'GUARULHOS E SÃO PAULO':'GUARULHOS, SÃO PAULO',
    'ITANHANGA':'ITANHANGÁ',
    'IBIÚNA E SERTÃOZINHO':'IBIÚNA, SERTÃOZINHO',
    'IPUIUNA':'IPUIÚNA',
    'ITAÍ E SÃO PAULO':'ITAÍ, SÃO PAULO',
    'ITU E SANTA CRUZ DA CONCEIÇÃO':'ITU, SANTA CRUZ DA CONCEIÇÃO',
    'JUNDIAÍ E SÃO CAETANO DO SUL':'JUNDIAÍ, SÃO CAETANO DO SUL',
    'JUNDIAÍ E SÃO PAULO':'JUNDIAÍ, SÃO PAULO',
    'MACEIO':'MACEIÓ',
    "NOVA BRASILANDIA D'OESTE":"NOVA BRASILÂNDIA D'OESTE",
    'ONLINE':'ONLINE',
    'PIRACICABA E SÃO PAULO':'PIRACICABA, SÃO PAULO',
    'PORTO ALEGRE E SANTA MARIA':'PORTO ALEGRE, SANTA MARIA',
    'PUNTA PORÁ':'PONTA PORÃ',
    'RIO GRANDE DO SUL':'ONLINE',
    'SAO FRANCISCO DO CONDE':'SÃO FRANCISCO DO CONDE',
    'SEROPÉDICA E RIO DE JANEIRO':'SEROPÉDICA, RIO DE JANEIRO',
    'SÃO BERNARDO DO CAMPO E LEME':'SÃO BERNARDO DO CAMPO, LEME',
    'SÃO BERNARDO DO CAMPO E SÃO PAULO':'SÃO BERNARDO DO CAMPO, SÃO PAULO',
    'SÃO JOSÉ DOS PINHOS':'SÃO JOSÉ DOS PINHAIS',
    'SÃO JOÃO DO TRIUNFO E RIO AZUL':'SÃO JOÃO DO TRIUNFO, RIO AZUL',
    'TAUBATÉ E CAPITAL':'TAUBATÉ, SÃO PAULO',
    'TAUBATÉ E CAPIVARI':'TAUBATÉ, CAPIVARI',
    'TUPASSI':'TUPÃSSI',
    'UBERLANDIA':'UBERLÂNDIA',
    'URUARA':'URUARÁ'
}

sigla_estado = {
    'AC': 'Acre',
    'AM': 'Amazonas',
    'AP': 'Amapá',
    'PA': 'Pará',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'TO': 'Tocantins',
    'AL': 'Alagoas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'MA': 'Maranhão',
    'PB': 'Paraíba',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RN': 'Rio Grande do Norte',
    'SE': 'Sergipe',
    'ES': 'Espírito Santo',
    'MG': 'Minas Gerais',
    'RJ': 'Rio de Janeiro',
    'SP': 'São Paulo',
    'PR': 'Paraná',
    'RS': 'Rio Grande do Sul',
    'SC': 'Santa Catarina',
    'DF': 'Distrito Federal',
    'GO': 'Goiás',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'BR': 'Brasil'
}

maps_json = {
    # Região Norte

    "Acre":"geojson/geojs-12-mun.json",
    "Amazonas":"geojson/geojs-13-mun.json",
    "Amapá":"geojson/geojs-16-mun.json",
    "Pará":"geojson/geojs-15-mun.json",
    "Rondônia":"geojson/geojs-11-mun.json",
    "Roraima":"geojson/geojs-14-mun.json",
    "Tocantins":"geojson/geojs-17-mun.json",
    # Região Nordeste

    "Alagoas":"geojson/geojs-27-mun.json",
    "Bahia":"geojson/geojs-29-mun.json",
    "Ceará":"geojson/geojs-23-mun.json",
    "Maranhão":"geojson/geojs-21-mun.json",
    "Paraíba":"geojson/geojs-25-mun.json",
    "Pernambuco":"geojson/geojs-26-mun.json",
    "Piauí":"geojson/geojs-22-mun.json",
    "Rio Grande do Norte":"geojson/geojs-24-mun.json",
    "Sergipe":"geojson/geojs-28-mun.json",
    # Região Sudeste

    "Espírito Santo":"geojson/geojs-32-mun.json",
    "Minas Gerais":"geojson/geojs-31-mun.json",
    "Rio de Janeiro":"geojson/geojs-33-mun.json",
    "São Paulo":"geojson/geojs-35-mun.json",
    # Região Sul

    "Paraná":"geojson/geojs-41-mun.json",
    "Rio Grande do Sul":"geojson/geojs-43-mun.json",
    "Santa Catarina":"geojson/geojs-42-mun.json",
    
    # Região Centro-Oeste
    "Distrito Federal":"geojson/geojs-53-mun.json",
    "Goiás":"geojson/geojs-52-mun.json",
    "Mato Grosso":"geojson/geojs-51-mun.json",
    "Mato Grosso do Sul":"geojson/geojs-50-mun.json",
    
    # Brasil
    "Brasil":"geojson/geojs-100-mun.json"
}

def get_bs4(url:str):
    need_to_request = True
    while need_to_request:
        try:
            response = requests.get(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
            need_to_request = False
        except:
            sleep(10)

    return BeautifulSoup(response.content)

def parse_numbers(x:pd.Series):
    numeros_acertados = int(x['Números acertados'].split(' acertos')[0].strip())
    premio_por_ganhador = float(x['Prêmio por ganhador'].split('R$ ')[1].strip().replace('.','').replace(',','.'))
    total_de_ganhadores = int(x['Total de ganhadores'].strip().replace('.',''))
    fundo_do_premio = float(x['Fundo do prêmio'].split('R$ ')[1].strip().replace('.','').replace(',','.'))
    data = datetime.strptime(x['data'].strip(),'%d/%m/%Y')
    return [
        numeros_acertados,
        premio_por_ganhador,
        total_de_ganhadores,
        fundo_do_premio,
        data
    ]

def remove_comma(x:str):
    try:
        return int(x.replace(',',''))
    except:
        return np.nan

def parse_numbers_states(x:pd.Series):
    ganhadores_com_6_acertos = remove_comma(x['Ganhadores com 6 acertos'])        
    ganhadores_com_5_acertos = remove_comma(x['Ganhadores com 5 acertos'])
    ganhadores_com_4_acertos = remove_comma(x['Ganhadores com 4 acertos'])
    total = remove_comma(x['Total'])
    data = datetime.strptime(x['data'].strip(),'%d/%m/%Y')
    return [
        ganhadores_com_6_acertos,
        ganhadores_com_5_acertos,
        ganhadores_com_4_acertos,
        total,
        data
    ]


df_codigo_ibge = pd.read_excel('raw_data/DTB_2022/RELATORIO_DTB_BRASIL_DISTRITO.xls',skiprows=6)

try:
    # df_result_all = pd.read_csv('historico_ganhadores_importado.csv',index_col=0)
    df_result_all = pd.read_parquet('processed_data/result_all.parquet')
    df_prizes_all = pd.read_parquet('processed_data/prizes_all.parquet')
    df_prizes_state_all = pd.read_parquet('processed_data/prizes_state_all.parquet')    
except:
    parar = False
    result_all = {}
    df_prizes_all = pd.DataFrame()
    df_prizes_state_all = pd.DataFrame()    

    years = np.linspace(1996,2023,1+2023-1996,dtype=int)
    for ano_mega_idx in tnrange(1+2023-1996, desc='Anos da Mega-Sena'):
        ano_mega = years[ano_mega_idx]
    # for ano_mega in np.linspace(1996,2023,1+2023-1996,dtype=int):
        soup = get_bs4(url = f"https://www.megasena.com/resultados/ano-{str(ano_mega)}")
        sleep(1)
        sorteios = soup.find_all('ul', {"class": 'balls -lg'})
        sorteios = soup.find_all("tr",{"class": ''})
        # for sorteio in sorteios:
        for sorteio_idx in tnrange(len(sorteios), desc=f'Sorteios Mega-Sena ano {str(ano_mega)}'):
            sorteio = sorteios[sorteio_idx]
            p = sorteio.find('td',{'class','mobTitle'},recursive=True)
            if p:
                # result_all.append(sorteio)
                date = sorteio.find("div",{"class","date"}).string
                result_all[date] = {}
                sorteio_numbers = []
                for number in sorteio.find_all('li'):
                    sorteio_numbers.append(number.string)
                result_all[date]['n_sorteados'] = sorteio_numbers

                url_sufixo_concurso = sorteio.find_all("td")[0].find("a").get("href")
                result_all[date]["concurso"] = url_sufixo_concurso
                url_ganhador = "https://www.megasena.com"+url_sufixo_concurso
                soup_ganhador = get_bs4(url=url_ganhador)                
                sleep(2)
                quantidade_ganhadores = sorteio.find_all("td")[-1].string.strip()

                prizes = soup_ganhador.find_all('table',{'class':'_numbers -right table-col-4 mobFormat'})[0].find('tbody').find_all(string=re.compile("[^\n]"))
                columns_name_prizes = soup_ganhador.find_all('table',{'class':'_numbers -right table-col-4 mobFormat'})[0].find('thead').find_all(string=re.compile("[^\n]"))
                df_prizes = pd.DataFrame(np.array(prizes).reshape(3,-1),columns=columns_name_prizes)
                df_prizes['data'] = date
                df_prizes_all = pd.concat([df_prizes_all,df_prizes])
                try:
                    prizes_state = soup_ganhador.find_all('table',{'class':"_numbers -right mobFormat"})[0].find('tbody').find_all(string=re.compile("[^\n]"))
                    columns_name_prizes_state = soup_ganhador.find_all('table',{'class':"_numbers -right mobFormat"})[0].find('thead').find_all(string=re.compile("[^\n]"))
                    df_prizes_state = pd.DataFrame(np.array(prizes_state).reshape(-1,len(columns_name_prizes_state)),columns=columns_name_prizes_state)  
                    df_prizes_state['data'] = date
                    df_prizes_state_all = pd.concat([df_prizes_state_all,df_prizes_state],axis=0, ignore_index=True, sort=False)
                except:
                    pass


                if (quantidade_ganhadores != "Acumulado"):

                    result_all[date]["teve_ganhador"] = True
                    result_all[date]["ganhador"]=url_ganhador
                    result_all[date]["quantidade_ganhadores"]=quantidade_ganhadores
                    # break
                    try:
                        estados_ganhadores = soup_ganhador.find("div",{"class","winning-locations box"}).find_all("div","gen-box")
                        result_all[date]["estado_ganhador"] = [estado.string.strip() for estado in estados_ganhadores]
                    except:
                        result_all[date]["estado_ganhador"] = np.nan
    df_result_all = pd.DataFrame(result_all).transpose()
    df_result_all.to_parquet('processed_data/result_all.parquet')

    df_prizes_all.to_parquet('processed_data/prizes_all.parquet')
    df_prizes_state_all.to_parquet('processed_data/prizes_state_all.parquet')

df_prizes_all = df_prizes_all.reset_index(drop=True)
df_prizes_state_all = df_prizes_state_all.reset_index(drop=True)
# Parse the values
df_prizes_all[["numeros_acertados","premio_por_ganhador","total_de_ganhadores","fundo_do_premio","data"]] = df_prizes_all.apply(parse_numbers, axis=1, result_type='expand').reset_index(drop=True)
df_prizes_state_all[['ganhadores_com_6_acertos','ganhadores_com_5_acertos','ganhadores_com_4_acertos','total','data']] = df_prizes_state_all.apply(parse_numbers_states, axis=1, result_type='expand').reset_index(drop=True)

df_populacao_uf = pd.read_excel('raw_data/populacao_censo_2022.xlsx')
df_populacao_uf['populacao_adulta'] = df_populacao_uf.iloc[:,[1,*range(5,df_populacao_uf.shape[1])]].sum(axis=1)

df_lat_long_states_br = pd.read_csv('raw_data/lat_long_states_br.csv')
df_lat_long_states_br['States'] = df_lat_long_states_br['States'].apply(lambda x:sigla_estado[x])

def parse_num_cities(x):
    try:
        return len(x)
    except:
        return x

def check_city_exist(location:str):

    location_list = location.split(',')

    # replace some worng city names by the correct ones
    for idx,original_str in enumerate(location_list):
        if original_str in correct_names.keys():
            location_list[idx] = correct_names[original_str]
    
    # merge and split again because there are some corrections that one location result in more locations separated by comma
    location_list = ', '.join(location_list).split(',')

    if len(location_list) > 1:
        return location_list[0:-1]
    else:
        return [np.nan]

def get_cities(x:list):
    try:
        return [check_city_exist(location.upper()) for location in x]
    except:
        return [[np.nan]]
def check_state_exist(location:str):
    location_list = location.split(',')
    if len(location_list) > 1:
        return location_list[-1]
    else:
        return location_list[0]

def get_states(x:list):
    try:
        estados = [check_state_exist(location.upper()) for location in x] 
        return estados
    except:
        return np.nan



df_result_all["estado_ganhador_number"] = df_result_all["estado_ganhador"].apply(lambda x:parse_num_cities(x))
df_result_all["cidade"] = df_result_all["estado_ganhador"].apply(lambda x:get_cities(x))
df_result_all["cidade"] = df_result_all["cidade"].apply(lambda x:list(chain.from_iterable(x)))
df_result_all["estado"] = df_result_all["estado_ganhador"].apply(lambda x:get_states(x))
df_result_all["concurso_num"] = df_result_all["concurso"].apply(lambda x:x.split('/')[-1])

def has_nan(x):
    try:
        return x.index(np.nan) >= 0
    except:
        return False

winner_no_cities = df_result_all[df_result_all["cidade"].apply(lambda x:has_nan(x))].query("teve_ganhador.notnull()")

df_concurso_sem_cidade = winner_no_cities["concurso"].apply(lambda x:x.split("/")[-1]).to_frame()

concurso_sem_cidade = df_concurso_sem_cidade["concurso"].astype(int).to_list()

def get_city_from_location(x):
    try:
        locations_list:list[str] = x.split(";")

        # locations_list:list[str] = x.split(";")
        city_list: list[str] = []
        for location in locations_list:
            if ('ELETRONICO' not in location.strip() and "/" in location.strip()):
                aux = location.split("/")[0].strip()

                city_list.append(aux)
            else:
                city_list.append(np.nan)
        return city_list
    except:
        return [np.nan]
    
path = "raw_data/Mega-Sena.xlsx"
df = pd.read_excel(path)

df['cidade_0'] = df["Cidade / UF"].apply(lambda x:get_city_from_location(x))

df_result_all["concurso_num"] = df_result_all["concurso_num"].astype(int)

df_result_all_com_cidades = pd.merge(df_result_all.reset_index().rename(columns={'index':'data'}),df[['Concurso','cidade_0']],how='left', left_on='concurso_num', right_on='Concurso')

def correct_wrong_name(aux:str, city_list:list[str]):
    if aux in correct_names.keys():
        aux = correct_names[aux]
        aux_list:list[str]  = aux.split(',')
        for aux_unit in aux_list:
            city_list.append(aux_unit)
    else:                
        # merge and split again because there are some corrections that one location result in more locations separated by comma
        city_list.append(aux)    
    return city_list


def final_city(x):

    city_list = []
    try:
        for idx,city in enumerate(x['cidade']):
            if (city is np.nan):                
                aux = x['cidade_0'][idx].strip()
                city_list = correct_wrong_name(aux, city_list)
            else:                
                city_list = correct_wrong_name(city.strip(), city_list)             
        return city_list
    except:
        return x['cidade']
df_result_all_com_cidades['cidade_1'] = df_result_all_com_cidades.apply(lambda x:final_city(x),axis=1)

def parse_list_to_new_rows(x:pd.Series, new_list:list):
    try:
        for city,state in zip(x["cidade_1"],x["estado"]):
            aux = x.copy()
            aux['cidade_1'] = city
            aux['estado'] = state
            new_list.append(aux.to_dict())
    except:
        for city in x["cidade_1"]:
            aux = x.copy()
            aux['cidade_1'] = city
            new_list.append(aux.to_dict())

    return new_list

def state_strip(x:str):
    try:
        return x.strip()
    except:
        return x

new_list = []
for index, row in df_result_all_com_cidades.iterrows():
    # df_new = parse_list_to_new_rows(row, df_new)
    new_list = parse_list_to_new_rows(row, new_list)

df_result_all_com_cidades_detalhada = pd.DataFrame(new_list)

df_map = df_result_all_com_cidades_detalhada.groupby(by=["cidade_1"])["estado"].count().to_frame().reset_index().rename(columns={'estado':'qtd_ganhadores'})
df_map['cidade_1'] = df_map['cidade_1'].str.upper().str.strip()

df_codigo_ibge['Nome_Município'] = df_codigo_ibge['Nome_Município'].str.upper()

df_merge_codigo = pd.merge(df_map,df_codigo_ibge[['Nome_Município','Código Município Completo']].drop_duplicates(),how='left',left_on='cidade_1',right_on='Nome_Município',)

df_result_all_com_cidades_detalhada[['1','2','3','4','5','6']] = pd.DataFrame(df_result_all_com_cidades_detalhada['n_sorteados'].apply(lambda x:list(x)).to_list())
df_result_all_com_cidades_detalhada['data'] = df_result_all_com_cidades_detalhada['data'].apply(lambda x:datetime.strptime(x.strip(),'%d/%m/%Y'))
df_result_all_com_cidades_detalhada['ano'] = df_result_all_com_cidades_detalhada['data'].apply(lambda x:x.year)
df_result_all_com_cidades_detalhada['ano_str'] = df_result_all_com_cidades_detalhada['ano'].apply(lambda x:str(x))
df_result_all_com_cidades_detalhada['estado'] = df_result_all_com_cidades_detalhada['estado'].apply(state_strip)

df_dezenas_por_concurso = df_result_all_com_cidades_detalhada.set_index(['data','ano','concurso_num','ano_str'])[['1', '2', '3', '4', '5', '6']].stack().reset_index().rename(columns={'level_4':'dezena',0:'numero_sorteado'}).sort_values('data').reset_index(drop=True)
df_dezenas_por_concurso['numero_sorteado'] = df_dezenas_por_concurso['numero_sorteado'].apply(lambda x:int(x))

fig = px.line(
    df_dezenas_por_concurso,
    x='data', y="numero_sorteado",color='dezena',
    title='Dezenas Sorteadas por Sorteio')

st.write(fig)


fig = px.box(df_dezenas_por_concurso, x="dezena", y="numero_sorteado",
             title='Box plot de todas as dezenas sorteadas da MegaSena')
fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
st.write(fig)
