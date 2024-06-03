import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import date
import pytz
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import plotly

datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
t = datetime_br.strftime('%d/%m/%Y %H:%M:%S')
data_atual = datetime_br.strftime('%d/%m/%Y')

# sqlria uma sqlonexão sqlom o bansqlo de dados SQLite3
connection = sqlite3.connect('Pesq.db')
sql = connection.cursor()

# sqlria a tabela 'Pesq' se ela não existir
sql.execute('''CREATE TABLE IF NOT EXISTS Pesq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    pesquisa TEXT,
    data DATE
)''')

def inicializarCRUDpesq():
    datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
    t = datetime_br.strftime('%d/%m/%Y %H:%M:%S')
    data_atual = datetime_br.strftime('%d/%m/%Y')

    # sqlria uma sqlonexão sqlom o bansqlo de dados SQLite3
    connection = sqlite3.connect('Pesq.db')
    sql = connection.cursor()

    # sqlria a tabela 'Pesq' se ela não existir
    sql.execute('''CREATE TABLE IF NOT EXISTS Pesq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        pesquisa TEXT,
        data DATE
    )''')
    return t, data_atual
    
# Adiciona um novo registro à tabela
def ADD_registro(USUARIO, PESQUISA, DATA):
    sql.execute('''INSERT INTO Pesq (usuario, pesquisa, data) VALUES (?, ?, ?)''',(USUARIO, PESQUISA, DATA))
    connection.commit()

# Exclui um registro da tabela
def DEL_registro(id):
    sql.execute('''DELETE FROM Pesq WHERE id = ?''', (id,))
    connection.commit()

# Exibe todos os registros da tabela
def MOSTRAR_registros():
    sql.execute('''SELECT * FROM Pesq''')
    registros = sql.fetchall()
    return registros

def Nuvem_de_Palavras(msg):
    stopwords = set(STOPWORDS)
    stopwords.update(["ao", "da", "de", "e", "E", "é", "É", "em", "Em", "meu", "nao", "não", "o", "ou", "os",  "para", "que", "Que", "ser", "só", "Te", "ter", "um", "você"])
    # gerar uma wordcloud
    wordcloud = WordCloud(stopwords=stopwords,
                          background_color="white",
                          width=1280, height=720).generate(msg)
    #resp = msg.replace("*", "")
    #resp = msg.replace("**", "")
    return wordcloud

def main():
    registros = MOSTRAR_registros()
    PESQ = ""
    if registros:
        #st.title("Nuvem de Palavras da Pesquisa")
        Titulo_Principal = '<p style="font-weight: bolder; color:#f55050; font-size: 44px;">Nuvem de Palavras da Pesquisa</p>'    
        st.markdown(Titulo_Principal, unsafe_allow_html=True)
        mystyle0 =   '''<style> p{text-align:center;}</style>'''
        st.markdown(mystyle0, unsafe_allow_html=True) 
        df = pd.DataFrame(registros, columns=['ID', 'USUARIO', 'TERMO_PESQUISADO', 'DATA'])        
        for i in range(len(df)):
            PESQ+=df['TERMO_PESQUISADO'][i] + " "

        NuvemPalavras = Nuvem_de_Palavras(PESQ)
        plt.imshow(NuvemPalavras);
        plt.imshow(NuvemPalavras, interpolation='bilinear')
        plt.axis("off")
        imagem = plt.show()
        NuvemPalavras.to_file("Nuvem_Palavras.png")
        st.pyplot(imagem) #Este método faz exibirt a nuvem de palavras
        st.set_option('deprecation.showPyplotGlobalUse', False)
        Nuvem = str(NuvemPalavras)  
        summary = df.dropna(subset=['TERMO_PESQUISADO'], axis=0)['TERMO_PESQUISADO']   
        all_summary = " ".join(s for s in summary)   
        wordlist = all_summary.split()
        wordfreq = []
        for w in wordlist:
            wordfreq.append(wordlist.count(w))
        
        #from collections import Counter
        #palavras = str(wordlist).replace('\n',' ').replace('\t','').split(' ')
        #contador = Counter(palavras)        
        #for i in contador.items():
        #    st.write(i)

        wordfreq = []
        for w in wordlist:
            wordfreq.append(wordlist.count(w))
        #chart_data = pd.DataFrame(wordfreq, wordlist)
        chart_data = pd.DataFrame({"Termos_Pesquisados": wordlist,"Freq_de_Ocorrência": wordfreq})
        st.bar_chart(chart_data, x = "Termos_Pesquisados", y = "Freq_de_Ocorrência", use_container_width=True)    
        
        with st.expander("Visualizar Detalhes"):
            st.dataframe(df)
            st.write(PESQ)        
    else:
        st.write('Não há registros no banco de dados.')
if __name__ == '__main__':
    main()