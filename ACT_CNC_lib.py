from GoogleNews import GoogleNews
from random import randrange
import pandas as pd

from datetime import datetime
from datetime import date
import pytz
import time

from deep_translator import GoogleTranslator
import requests
import json

def En2Pt(palavraEN):
    tradutor = GoogleTranslator(source= "en", target= "pt")
    traducaoPT = tradutor.translate(palavraEN)
    return traducaoPT
    
def CNC():
    # C = Cotações
    # N = Notícias
    # C = Clima
    
    datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
    CNC.Data_Hora = datetime_br.strftime('%d/%m/%Y %H:%M:%S')
    CNC.Data_Atual = datetime_br.strftime('%d/%m/%Y')

    #COTAÇÕES
    requisicao1 = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
    cotacaoUS = requisicao1.json() 
    requisicao2 = requests.get('https://economia.awesomeapi.com.br/all/EUR-BRL')
    cotacaoEUR = requisicao2.json()
    requisicao3 = requests.get('https://economia.awesomeapi.com.br/all/CNY-BRL')
    cotacaoCNY = requisicao3.json()    

    CNC.USD_DataHora = cotacaoUS['USD']['create_date']
    CNC.USD_Cotacao  = cotacaoUS['USD']['bid']
    CNC.USD_Variacao = cotacaoUS['USD']['pctChange']
    
    CNC.EUR_DataHora = cotacaoEUR['EUR']['create_date']
    CNC.EUR_Cotacao  = cotacaoEUR['EUR']['bid']
    CNC.EUR_Variacao = cotacaoEUR['EUR']['pctChange'] 

    CNC.CNY_DataHora = cotacaoCNY['CNY']['create_date']
    CNC.CNY_Cotacao  = cotacaoCNY['CNY']['bid']
    CNC.CNY_Variacao = cotacaoCNY['CNY']['pctChange']  
    
    #NOTÍCIAS
    googlenews = GoogleNews()
    googlenews.set_lang('pt')
    #googlenews.set_lang('en')
    googlenews.set_period('3d')
    #googlenews.set_time_range('02/01/2020','02/28/2020')
    googlenews.set_encode('utf-8')
    googlenews.get_news('a')

    resp = googlenews.results(sort=True)

    df = pd.DataFrame(resp)
    MeiosMaisCitados = df['media'].value_counts()
    filtro = lambda x: x["media"] == MeiosMaisCitados.index[0]
    filtrados = list(filter(filtro , resp))
    dfFILTER = pd.DataFrame(filtrados)
    CincoMais = dfFILTER.head(5)
    CNC.CincoMais = CincoMais
    indice = randrange(5)
    Noticia_Selecionada = CincoMais['title'][indice]
    Noticia_Selecionada = Noticia_Selecionada.replace(str(MeiosMaisCitados.index[0]),"",1)
    CNC.Noticia_Selecionada = Noticia_Selecionada.replace("Mais","",1)
    CNC.Link_Selecionado = CincoMais['link'][indice]
    #url = "https://www.streamlit.io"
    #st.write("check out this [link](%s)" % url)

    #PREVISÃO DO TEMPO
    API_KEY = "a30bd09c7884982c30901f15edb9a21e"
    city_name = "Jundiaí"
    CNC.cidade = city_name
    LINK = "https://api.openweathermap.org/data/3.0/onecall?q={Cidade}&appid={API_KEY}"
    api_key = "a30bd09c7884982c30901f15edb9a21e"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    # "404" means city is not found
    if x["cod"] != "404":
        # store the value of "main"
        # key in variable y
        y = x["main"]
        # to the "temp" key of y
        current_temperature = y["temp"]
        CNC.Temp_K = current_temperature
        # to the "pressure" key of y
        current_pressure = y["pressure"]
        CNC.Pressao = current_pressure
        # to the "humidity" key of y
        current_humidity = y["humidity"]
        CNC.Umidade = current_humidity
        # store the value of "weather"
        # key in variable z
        z = x["weather"]
        # the "description" is a key at
        # the 0th index of z
        weather_description = z[0]["description"]
        CNC.Temp_C = round(float(current_temperature) - 273.15, 3)
        tradutor = GoogleTranslator(source= "en", target= "pt")
        CNC.Descricao_clima_En = weather_description
        CNC.Descricao_clima_Pt = tradutor.translate(str(weather_description))

        #A SEGUIR EXEMPLO DE UTILIZAÇÃO DESTA BIBLITECA:
        '''
        CNC()
        print(CNC.Noticia_Selecionada)
        print(CNC.Link_Selecionado)

        display(CNC.CincoMais)

        print("DOLAR AMERICANO:")
        print("D/H: ", CNC.USD_DataHora)
        print("1 U$ = R$", CNC.USD_Cotacao)
        print("Variação: ", CNC.USD_Variacao, "%")
        print("================================== \n")
        print("EURO: \n")
        print("D/H: ", CNC.EUR_DataHora)
        print("1 U$ = R$", CNC.EUR_Cotacao)
        print("Variação: ", CNC.EUR_Variacao, "%")
        print("================================== \n")
        print("YUAN: \n")
        print("D/H: ", CNC.CNY_DataHora)
        print("1 U$ = R$", CNC.CNY_Cotacao)
        print("Variação: ", CNC.CNY_Variacao, "%")

        print("Temperatura (ºC) = " +
              str(CNC.Temp_C) + "(" + str(CNC.Descricao_clima_En)+")" +
              "\n Temperatura (ºK) = " +
              str(CNC.Temp_K) +
              "\n Pressão Atmosférica (hPa) = " +
              str(CNC.Pressao) +
              "\n Umidade (%) = " +
              str(CNC.Umidade) +
              "\n Descrição = " +
              str(CNC.Descricao_clima_Pt) + "(" + str(CNC.Descricao_clima_En)+")")
        '''
