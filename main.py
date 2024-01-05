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


st.markdown('''

# Mega-Sena: um olhar estatístico sobre os sorteios

Você já se perguntou como a distribuição geográfica dos ganhadores se relaciona com o censo populacional? Neste blog, eu vou explorar essas e outras questões usando dados e ferramentas estatísticas. O objetivo não é dar uma fórmula mágica para acertar os números, mas sim satisfazer a curiosidade e o interesse pelos jogos de loteria.

Para realizar as análises, utilizei os dados dos sorteios da Mega-Sena disponíveis no site oficial  e os dados do censo populacional de 2022 do IBGE . Como os dados não estavam em um formato padronizado, eu tive que usar a técnica de **web scraping** para extrair as informações das páginas web. Em seguida, eu usei as seguintes ferramentas para processar, analisar e visualizar os dados:
- Python
- Streamlit
- Plotly
- BeautifulSoup
- Pandas
- Numpy

Espero que você goste das análises e que elas te inspirem a pensar de forma crítica e criativa sobre os números da Mega-Sena. Boa leitura!
            
Os dados da Mega-Sena foram extraídos dos seguintes links:
- https://www.megasena.com
- https://censo2022.ibge.gov.br
''')