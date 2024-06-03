import sqlite3
import streamlit as st
import pandas as pd
import datetime
from datetime import datetime
from datetime import date, time
import pytz
import time

import random  # necessário para utilizar o módulo random
from Send2MaillMSK import Send2Mail

# Cria uma conexão com o banco de dados SQLite3
conn = sqlite3.connect('Atualizacao_Processos.db')
c = conn.cursor()

# Cria a tabela 'Processos' se ela não existir
c.execute('''CREATE TABLE IF NOT EXISTS Processos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Codigo TEXT,
    Cliente TEXT,
    Responsavel TEXT,
    Atualizacao TEXT,
    DataAtualizacao DATE,
    HoraAtualizacao TEXT,
    Situacao TEXT
)''')

# Adiciona um novo registro à tabela
def add_registro(CODIGO, CLIENTE, RESPONSAVEL, ATUALIZACAO, DATA, HORA, SITUACAO):
    c.execute('''INSERT INTO Processos (Codigo, Cliente, Responsavel, Atualizacao, DataAtualizacao, HoraAtualizacao, Situacao) VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (CODIGO, CLIENTE, RESPONSAVEL, ATUALIZACAO, DATA, HORA, SITUACAO))
    conn.commit()

# Exclui um registro da tabela
def del_registro(id):
    c.execute('''DELETE FROM Processos WHERE id = ?''', (id,))
    conn.commit()

# Exibe todos os registros da tabela
def mostrar_registros():
    c.execute('''SELECT * FROM Processos''')
    registros = c.fetchall()
    return registros

datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
t = datetime_br.strftime('%d/%m/%Y %H:%M:%S')
data_atual = datetime_br.strftime('%d/%m/%Y')
hora_atual = datetime_br.strftime('%H:%M:%S')


# Interface do usuário do Streamlit
st.title('Atualização de Processos')

# Formulário para adicionar um novo registro
with st.form('add_registro'):
    #CODIGO, CLIENTE, RESPONSAVEL, ATUALIZACAO, DATA, SITUACAO
    CODIGO = st.text_input('Código do Processo:')
    CLIENTE = st.text_input('Cliente:')
    RESPONSAVEL = st.text_input('Responsável interno pelo processo:')
    ATUALIZACAO = st.text_area('Digite atualizações do processo:')
    DATA = st.date_input("Data da atualização", date(datetime_br.year, datetime_br.month, datetime_br.day))
    HORA = st.text_input("Selecione horário", hora_atual)
    SITUACAO = st.selectbox('Situação:', ('Ativo', 'Inativo'))
    submitted = st.form_submit_button('Adicionar')
    if submitted:
        add_registro(CODIGO, CLIENTE, RESPONSAVEL, ATUALIZACAO, DATA, HORA, SITUACAO)
        #st.write(Send2Mail("massaki.igarashi@gmail.com", MAIL, "Bem vindo(a) à Generactiva, sua Multi Assistente! A seguir sua senha de acesso, guarde-a!", "Para acessar a plataforma digite este e-mail cadastrado mais a senha de acesso: " + PSWD))
        #st.divider()
        st.success('Registro adicionado com sucesso!')

# Botão para excluir um registro
with st.form('del_registro'):
    id = st.number_input('ID do registro a ser excluído:', min_value=1)
    submitted = st.form_submit_button('Excluir')
    if submitted:
        del_registro(id)
        st.success('Registro excluído com sucesso!')

# Exibe todos os registros
st.write('Registros:')
registros = mostrar_registros()
if registros:
#CODIGO, CLIENTE, RESPONSAVEL, ATUALIZACAO, DATA, HORA, SITUACAO
    df = pd.DataFrame(registros, columns=['ID', 'CODIGO', 'CLIENTE', 'RESPONSAVEL', 'ATUALIZACAO', 'DATA', 'HORA', 'SITUACAO'])
    st.dataframe(df)
else:
    st.write('Não há registros no banco de dados.')