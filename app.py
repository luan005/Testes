from flask import Flask, request, jsonify, g
import sqlite3
from marshmallow import ValidationError

from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema

DATABASE = 'censoescolar.db'

app = Flask(__name__)


def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return jsonify({"versao": "0.0.1"}), 200


@app.get("/instituicoes")
def instituicoesResource():
    try:
        instituicoesEnsino = []
        cursor = getConnection().cursor()
        cursor.execute('SELECT * FROM tb_instituicao')
        resultSet = cursor.fetchall()

        for row in resultSet:
            instituicaoEnsino = InstituicaoEnsino(*row)
            instituicoesEnsino.append(instituicaoEnsino.toDict())

        return jsonify(instituicoesEnsino), 200

    except sqlite3.Error:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500


@app.post("/instituicoes")
def instituicaoInsercaoResource():
    instituicaoSchema = InstituicaoEnsinoSchema()
    instituicaoData = request.get_json()

    try:
        instituicaoJson = instituicaoSchema.load(instituicaoData)

        values = (
            instituicaoJson['no_regiao'], instituicaoJson['sg_uf'], instituicaoJson['no_municipio'],
            instituicaoJson['no_mesorregiao'], instituicaoJson['no_microrregiao'], instituicaoJson['co_entidade'],
            instituicaoJson['qt_mat_bas'], instituicaoJson['co_regiao'], instituicaoJson['co_uf'],
            instituicaoJson['co_municipio'], instituicaoJson['co_microrregiao'], instituicaoJson['co_mesorregiao']
        )

        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tb_instituicao (
                no_regiao, sg_uf, no_municipio, no_mesorregiao, no_microrregiao,
                co_entidade, qt_mat_bas, co_regiao, co_uf, co_municipio, co_microrregiao, co_mesorregiao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)
        conn.commit()

        id = cursor.lastrowid
        instituicaoEnsino = InstituicaoEnsino(id, *values)

        return jsonify(instituicaoEnsino.toDict()), 200

    except ValidationError as err:
        return jsonify(err.messages), 400
    except sqlite3.Error:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500


@app.route("/instituicoes/<int:id>", methods=["DELETE"])
def instituicaoRemocaoResource(id):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tb_instituicao WHERE id = ?', (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        return jsonify({"mensagem": "Instituição removida com sucesso."}), 200

    except sqlite3.Error:
        return jsonify({"mensagem": "Erro ao acessar o banco de dados."}), 500


@app.route("/instituicoes/<int:id>", methods=["PUT"])
def instituicaoAtualizacaoResource(id):
    instituicaoSchema = InstituicaoEnsinoSchema()
    instituicaoData = request.get_json()

    try:
        instituicaoJson = instituicaoSchema.load(instituicaoData)

        values = (
            instituicaoJson['no_regiao'], instituicaoJson['sg_uf'], instituicaoJson['no_municipio'],
            instituicaoJson['no_mesorregiao'], instituicaoJson['no_microrregiao'], instituicaoJson['co_entidade'],
            instituicaoJson['qt_mat_bas'], instituicaoJson['co_regiao'], instituicaoJson['co_uf'],
            instituicaoJson['co_municipio'], instituicaoJson['co_microrregiao'], instituicaoJson['co_mesorregiao'], id
        )

        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tb_instituicao SET
                no_regiao = ?, sg_uf = ?, no_municipio = ?, no_mesorregiao = ?, no_microrregiao = ?,
                co_entidade = ?, qt_mat_bas = ?, co_regiao = ?, co_uf = ?, co_municipio = ?,
                co_microrregiao = ?, co_mesorregiao = ?
            WHERE id = ?''', values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsino = InstituicaoEnsino(id, *values[:-1])
        return jsonify(instituicaoEnsino.toDict()), 200

    except ValidationError as err:
        return jsonify(err.messages), 400
    except sqlite3.Error:
        return jsonify({"mensagem": "Erro ao atualizar instituição."}), 500


@app.route("/instituicoes/<int:id>", methods=["GET"])
def instituicoesByIdResource(id):
    try:
        cursor = getConnection().cursor()
        cursor.execute('SELECT * FROM tb_instituicao WHERE id = ?', (id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsino = InstituicaoEnsino(*row)
        return jsonify(instituicaoEnsino.toDict()), 200

    except sqlite3.Error:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500


if __name__ == '__main__':
    app.run(debug=True)
