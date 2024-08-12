from flask import Flask, jsonify
import getpass
import oracledb

app = Flask(__name__)

# Configurações do banco de dados
dsn = "oracle.fiap.com.br:1521/orcl"

# Função para obter a conexão com o banco de dados
def get_db_connection():
    user = input("Insira o nome de usuário (rm00000): ")
    pw = getpass.getpass("Insira a senha: ")
    connection = oracledb.connect(user=user, password=pw, dsn=dsn)
    return connection

# Rota para obter todos os cargos
@app.route('/cargos', methods=['GET'])
def get_cargos():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM cargos")
    rows = cursor.fetchall()  # Obtemos todas as linhas da tabela

    # Transformar os resultados em um formato de lista de dicionários
    cargos = []
    for row in rows:
        cargo = {
            "id": row[0],  # Substitua pelos nomes reais das colunas
            "nome": row[1],  # Substitua pelos nomes reais das colunas
            # Adicione outros campos conforme necessário
        }
        cargos.append(cargo)

    cursor.close()
    connection.close()
    return jsonify(cargos)  # Retorna a lista de cargos em formato JSON

# Ponto de entrada da aplicação
if __name__ == '__main__':
    app.run(debug=True)
