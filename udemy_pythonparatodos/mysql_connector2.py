from mysql.connector import connection

conexao = connection.MySQLConnection(user='', password='', host='', database='')

conexao.close()
