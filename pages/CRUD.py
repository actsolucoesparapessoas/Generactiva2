import sqlite3
import streamlit as st
import pandas as pd
import random  # necessário para utilizar o módulo random
from Send2MaillMSK import Send2Mail

# Cria uma conexão com o banco de dados SQLite3
conn = sqlite3.connect('User.db')
c = conn.cursor()

# Cria a tabela 'User' se ela não existir
c.execute('''CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    mail TEXT,
    senha int,
    keyGEMINI TEXT,
    keyOPENAI TEXT,
    situacao TEXT
)''')

# Adiciona um novo registro à tabela
def add_registro(NOME, MAIL, SENHA, ChaveGEMINI, ChaveOPENAI, SITUACAO):
    c.execute('''INSERT INTO User (nome, mail, senha, keyGEMINI, keyOPENAI, situacao) VALUES (?, ?, ?, ?, ?, ?)''',
              (NOME, MAIL, SENHA, ChaveGEMINI, ChaveOPENAI, SITUACAO))
    conn.commit()

# Exclui um registro da tabela
def del_registro(id):
    c.execute('''DELETE FROM User WHERE id = ?''', (id,))
    conn.commit()

# Exibe todos os registros da tabela
def mostrar_registros():
    c.execute('''SELECT * FROM User''')
    registros = c.fetchall()
    return registros

def gerar_senha():
    random.seed()
    sorteio = random.sample(range(10), k=5)
    senha = str(sorteio[0])+str(sorteio[1])+str(sorteio[2])+str(sorteio[3])+str(sorteio[4])
    return senha

# Interface do usuário do Streamlit
st.title('User')

# Formulário para adicionar um novo registro
with st.form('add_registro'):
    NOME = st.text_input('Nome Completo:')
    MAIL = st.text_input('e-mail:')
    st.info("Enviaremos para seu e-mail a sua senha gerada; necessária para acessos Generactiva!")
    ChaveGEMINI = st.text_input('API KEY GEMINI:')
    ChaveOPENAI = st.text_input('API KEY OPENAI:')
    SITUACAO = st.selectbox('Situação:', ('Ativo', 'Inativo'))
    submitted = st.form_submit_button('Adicionar')
    if submitted:
        PSWD = gerar_senha()
        add_registro(NOME, MAIL, PSWD, ChaveGEMINI, ChaveOPENAI, SITUACAO)
        st.write(Send2Mail("massaki.igarashi@gmail.com", MAIL, "Bem vindo(a) à Generactiva, sua Multi Assistente! A seguir sua senha de acesso, guarde-a!", "Para acessar a plataforma digite este e-mail cadastrado mais a senha de acesso: " + PSWD))
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
    df = pd.DataFrame(registros, columns=['ID', 'NOME', 'MAIL', 'SENHA', 'CHAVE_GEMINI', 'CHAVE_OPENAI', 'SITUACAO'])
    st.dataframe(df)
else:
    st.write('Não há registros no banco de dados.')