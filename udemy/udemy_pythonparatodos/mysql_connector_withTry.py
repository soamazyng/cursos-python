import mysql.connector
from mysql.connector import errorcode

try:
    conexao = mysql.connector.connect(user='', password='', host='', database='')
except mysql.connector.Error as erro:
    if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Usuário ou senha inválidos")
    elif erro.errno == errorcode.ER_BAD_DB_ERROR:
        print("Banco de dados não existe")
    else:
        print(erro)
else:
    conexao.close()

