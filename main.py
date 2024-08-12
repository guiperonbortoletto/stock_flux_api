from flask import Flask, jsonify
from flask_cors import CORS  # Adicione esta linha
import oracledb
import json

app = Flask(__name__)
CORS(app)  # Adicione esta linha para permitir CORS
# Função para carregar credenciais a partir de um arquivo JSON
def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)

# Função para obter a conexão com o banco de dados
def get_db_connection():
    credentials = load_credentials()
    connection = oracledb.connect(user=credentials['user'], password=credentials['password'], dsn=credentials['dsn'])
    return connection

# Rota para obter todos os medicamentos
@app.route('/get_medicamentos', methods=['GET'])
def get_cargos():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT c.descricao AS Categoria, mt.descricao AS Motivo, nome, codigo, quantidade_minima, localizacao, s.descricao AS Status "
                   "FROM rm93069.medicamentos m "
                   "JOIN rm93069.categorias c ON m.id_categoria = c.id_categoria "
                   "JOIN rm93069.motivos mt ON m.id_motivo = mt.id_motivo "
                   "JOIN rm93069.status_medicamento sm ON m.id_medicamento = sm.id_medicamento "
                   "JOIN rm93069.status s ON sm.id_status = s.id_status")
    rows = cursor.fetchall()

    cargos = []
    for row in rows:
        cargo = {
            "Categoria": row[0],
            "Motivo": row[1],
            "Nome": row[2],
            "Código": row[3],
            "Quantidade Minima": row[4],
            "Localização": row[5],
            "Status": row[6],
        }
        cargos.append(cargo)

    cursor.close()
    connection.close()
    return jsonify(cargos)

# Ponto de entrada da aplicação
if __name__ == '__main__':
    app.run(debug=True)
