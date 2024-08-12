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
    cursor.execute("select c.descricao as Categoria, mt.descricao as Motivo, nome, codigo, quantidade_minima, localizacao from medicamentos m join categorias c on m.id_categoria = c.id_categoria join motivos mt on m.id_motivo = mt.id_motivo")
    rows = cursor.fetchall()  # Obtemos todas as linhas da tabela

    cargos = []
    for row in rows:
        cargo = {
            "Categoria": row[0],
            "Motivo": row[1],
            "Nome": row[2],
            "Código": row[3],
            "Quantidade Minima": row[4],
            "Localização": row[5],
        }
        cargos.append(cargo)

    cursor.close()
    connection.close()
    return jsonify(cargos)  # Retorna a lista de cargos em formato JSON

# Ponto de entrada da aplicação
if __name__ == '__main__':
    app.run(debug=True)
