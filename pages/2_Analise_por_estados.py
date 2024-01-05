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
from time import sleep
from tqdm.notebook import tnrange, tqdm
from datetime import datetime
import re
import streamlit.components.v1 as components

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
    response = requests.get(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
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

df_result_all_com_cidades = pd.merge(df_result_all,df[['Concurso','cidade_0']],how='left', left_on='concurso_num', right_on='Concurso')

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

new_list = []
for index, row in df_result_all_com_cidades.iterrows():
    # df_new = parse_list_to_new_rows(row, df_new)
    new_list = parse_list_to_new_rows(row, new_list)

df_result_all_com_cidades_detalhada = pd.DataFrame(new_list)

df_map = df_result_all_com_cidades_detalhada.groupby(by=["cidade_1"])["estado"].count().to_frame().reset_index().rename(columns={'estado':'qtd_ganhadores'})
df_map['cidade_1'] = df_map['cidade_1'].str.upper().str.strip()

df_codigo_ibge['Nome_Município'] = df_codigo_ibge['Nome_Município'].str.upper()

df_merge_codigo = pd.merge(df_map,df_codigo_ibge[['Nome_Município','Código Município Completo']].drop_duplicates(),how='left',left_on='cidade_1',right_on='Nome_Município',)


def create_map_json(estates_list:list):
    geo_json_final = {}
    for idx,state in enumerate(estates_list):
        # importing .json file and checking it
        path = os.path.join(
            "https://raw.githubusercontent.com/tbrugz/geodata-br/master",
            maps_json[state]
            )
        with urlopen(path) as response:
            if idx == 0:
                geo_json_final = json.load(response)
            else:
                geo_json_aux = json.load(response)
                geo_json_final['features'].extend(geo_json_aux['features'])
    return geo_json_final





df_prizes_all['ano'] = df_prizes_all['data'].apply(lambda x:x.year)
df_prizes_all.groupby(by=['ano','numeros_acertados'])['total_de_ganhadores'].sum().reset_index()


fig = px.line(
    df_prizes_all.groupby(by=['ano','numeros_acertados'])['fundo_do_premio'].sum().reset_index(),
    x='ano', y="fundo_do_premio",color='numeros_acertados')
st.write(fig)


fig = px.line(
    df_prizes_all.groupby(by=['ano','numeros_acertados'])['total_de_ganhadores'].sum().reset_index(),
    x='ano', y="total_de_ganhadores",color='numeros_acertados')
st.write(fig)



# Adding population size

try:
    path = 'processed_data/df_prizes_state_all_grouped_prizes_year.parquet'
    df_prizes_state_all_grouped_prizes_year = pd.read_parquet(path)
except:
    df_lat_long_states_br = pd.read_csv('raw_data/lat_long_states_br.csv')
    df_lat_long_states_br['States'] = df_lat_long_states_br['States'].apply(lambda x:sigla_estado[x])

    df_prizes_state_all_detailed = df_prizes_state_all.query("ganhadores_com_5_acertos.notnull()").fillna(0).fillna(0)[['Estado / Distrito Federal','data','ganhadores_com_6_acertos','ganhadores_com_5_acertos','ganhadores_com_4_acertos','total']]
    df_prizes_state_all_detailed['ano'] = df_prizes_state_all_detailed['data'].apply(lambda x:x.year)
    df_prizes_state_all_grouped = df_prizes_state_all_detailed.drop('total',axis=1).set_index(['Estado / Distrito Federal','data','ano']).stack().reset_index().rename(columns={'level_3':'acertos',0:'quantidade'})
    df_prizes_state_all_grouped = df_prizes_state_all_grouped.replace({
        'ganhadores_com_6_acertos':6,
        'ganhadores_com_5_acertos':5,
        'ganhadores_com_4_acertos':4,
        })

    df_prizes_state_all_grouped_prizes = pd.merge(df_prizes_state_all_grouped,df_prizes_all[['data', 'numeros_acertados', 'premio_por_ganhador', 'fundo_do_premio']],how='left',left_on=['data','acertos'],right_on=['data','numeros_acertados']).drop('numeros_acertados',axis=1)
    df_prizes_state_all_grouped_prizes['premio_total_por_estado'] = df_prizes_state_all_grouped_prizes['quantidade'] * df_prizes_state_all_grouped_prizes['premio_por_ganhador']

    df_prizes_state_all_grouped_prizes_year = df_prizes_state_all_grouped_prizes.drop(['data','acertos'],axis=1).groupby(by=['Estado / Distrito Federal', 'ano']).sum().reset_index()
    df_prizes_state_all_grouped_prizes_year = pd.merge(df_prizes_state_all_grouped_prizes_year,df_populacao_uf[['Estado','populacao_adulta']], how='left', left_on='Estado / Distrito Federal',right_on='Estado',sort=False)
    df_prizes_state_all_grouped_prizes_year['premio_por_pessoa_do_estado'] = df_prizes_state_all_grouped_prizes_year['premio_total_por_estado'] / df_prizes_state_all_grouped_prizes_year['populacao_adulta']
    df_prizes_state_all_grouped_prizes_year['quantidade_bilhetes_sorteados_por_pessoa_do_estado'] = df_prizes_state_all_grouped_prizes_year['quantidade'] / df_prizes_state_all_grouped_prizes_year['populacao_adulta']

    sigla_estado_reverse = {v:k for k,v in sigla_estado.items()}
    sigla_estado_reverse['Online']='Online'

    df_prizes_state_all_grouped_prizes_year['estado_sigla'] = df_prizes_state_all_grouped_prizes_year['Estado / Distrito Federal'].apply(lambda x:sigla_estado_reverse[x])
    df_prizes_state_all_grouped_prizes_year = pd.merge(df_prizes_state_all_grouped_prizes_year,df_lat_long_states_br,how='left', left_on=['Estado'], right_on=['States']).drop('States',axis=1)

    path = 'processed_data/df_prizes_state_all_grouped_prizes_year.parquet'
    df_prizes_state_all_grouped_prizes_year.to_parquet(path)


fig = px.bar(
    df_prizes_state_all_grouped_prizes_year,
    x='ano', y="premio_por_pessoa_do_estado",color='Estado / Distrito Federal', text='Estado / Distrito Federal')
st.write(fig)


fig = px.bar(
    df_prizes_state_all_grouped_prizes_year,
    x='ano', y="quantidade_bilhetes_sorteados_por_pessoa_do_estado",color='Estado / Distrito Federal', text='Estado / Distrito Federal')
st.write(fig)


path = "raw_data/brazil_geo.json"
with open(path,'r') as response:
    geo_json_final = json.load(response)

# ano_mapa = 2022
ano_mapa = st.selectbox(
    label='Selecione o ano da Mega-Sena',
    options=[2022,2023],
)
df_prizes_state_all_grouped_prizes_year_map = df_prizes_state_all_grouped_prizes_year.query("estado_sigla != 'Online' & ano==@ano_mapa")

# Create the choropleth_mapbox plot
fig = px.choropleth_mapbox(
    df_prizes_state_all_grouped_prizes_year_map, # data frame
    geojson=geo_json_final, # geojson file
    locations="estado_sigla", # column with state id
    color="premio_por_pessoa_do_estado", # column with sales volume
    color_continuous_scale='Bluered_r',
    hover_name="Estado / Distrito Federal", # column with state name
    mapbox_style="carto-positron", # map style
    zoom=3, # map zoom level
    center = {"lat": -12.0, "lon": -54.0}, # map center
    opacity=0.1, # color opacity
    title=f"Premio por morador adulto para cada estado (R$/pessoa) em {str(ano_mapa)}", # plot title 
    labels={"premio_por_pessoa_do_estado": "Cores de acordo com o<br>premio por morador adulto"} # change the legend title   
)

fig.add_trace(go.Scattermapbox(
    lat=df_prizes_state_all_grouped_prizes_year_map["Latitude"], # column with latitude
    lon=df_prizes_state_all_grouped_prizes_year_map["Longitude"], # column with longitude
    mode='markers+text',
    marker={
        'size': 2 * df_prizes_state_all_grouped_prizes_year_map["premio_por_pessoa_do_estado"],
        'color': df_prizes_state_all_grouped_prizes_year_map["premio_por_pessoa_do_estado"],
        'colorscale': 'Bluered_r',
        },
    # text=df_prizes_state_all_grouped_prizes_year_map["Estado / Distrito Federal"], # column with state name
    # name="Premio por morador adulto", # column with state name

    text=df_prizes_state_all_grouped_prizes_year_map["Estado / Distrito Federal"], # column with state name
    name="", # column with state name
    hovertemplate='%{text} %{hovertext:.1f}',
    hovertext=df_prizes_state_all_grouped_prizes_year_map["premio_por_pessoa_do_estado"],

    ))

fig.update_layout(
    width=800,
    height=800,
)

# Show the plot
st.write(fig)



df_prizes_state_all_grouped_prizes_year_map = df_prizes_state_all_grouped_prizes_year.query("estado_sigla != 'Online' & ano==@ano_mapa")

# Create the choropleth_mapbox plot
fig = px.choropleth_mapbox(
    df_prizes_state_all_grouped_prizes_year_map, # data frame
    geojson=geo_json_final, # geojson file
    locations="estado_sigla", # column with state id
    color="quantidade_bilhetes_sorteados_por_pessoa_do_estado", # column with sales volume
    color_continuous_scale='Bluered_r',
    hover_name="Estado / Distrito Federal", # column with state name
    mapbox_style="carto-positron", # map style
    zoom=3, # map zoom level
    center = {"lat": -12.0, "lon": -54.0}, # map center
    opacity=0.1, # color opacity
    title=f"Quantidade de bilhetes sorteados por morador adulto para cada estado em {str(ano_mapa)}", # plot title 
    labels={"quantidade_bilhetes_sorteados_por_pessoa_do_estado": "Cores de acordo com a<br>quantidade sorteada por<br>morador adulto"} # change the legend title   
)

fig.add_trace(go.Scattermapbox(
    lat=df_prizes_state_all_grouped_prizes_year_map["Latitude"], # column with latitude
    lon=df_prizes_state_all_grouped_prizes_year_map["Longitude"], # column with longitude
    mode='markers+text',
    marker={
        'size': 8 * 10 ** 3 * df_prizes_state_all_grouped_prizes_year_map["quantidade_bilhetes_sorteados_por_pessoa_do_estado"],
        'color': df_prizes_state_all_grouped_prizes_year_map["quantidade_bilhetes_sorteados_por_pessoa_do_estado"],
        'colorscale': 'Bluered_r',
        },
    text=df_prizes_state_all_grouped_prizes_year_map["Estado / Distrito Federal"], # column with state name
    name="", # column with state name
    hovertemplate='%{text} %{hovertext:.4f}',
    hovertext=df_prizes_state_all_grouped_prizes_year_map["quantidade_bilhetes_sorteados_por_pessoa_do_estado"],    
    ))

fig.update_layout(
    width=800,
    height=800,
)

# Show the plot
st.write(fig)

