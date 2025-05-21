from flask import request, jsonify
import sqlite3
from marshmallow import ValidationError

from helpers.application import app
from helpers.database import getConnection
from helpers.logging import logger

from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema



@app.route("/")
def index():
    return jsonify({"versao": "0.0.1"}), 200


@app.get("/instituicoes")
def instituicoesResource():
    logger.info("Get - Instituições")
    try:
        instituicoesEnsino = []
        cursor = getConnection().cursor()
        cursor.execute('SELECT * FROM tb_instituicao')
        resultSet = cursor.fetchall()

        for row in resultSet:
            logger.info(row)
            instituicaoEnsino = InstituicaoEnsino(*row)
            instituicoesEnsino.append(instituicaoEnsino.toDict())

        return jsonify(instituicoesEnsino), 200

    except sqlite3.Error as e:
        logger.error(f"Erro ao buscar instituições: {e}")
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500


def validarInstituicao(content):
    isValido = True
    if len(content['no_entidade']) < 3 or content['no_entidade'].isdigit():
        isValido = False
    if not content['co_entidade'].isdigit():
        isValido = False
    if not content['qt_mat_bas'].isdigit():
        isValido = False
    return isValido


@app.post("/instituicoes")
def instituicaoInsercaoResource():
    logger.info("Post - Instituição")
    instituicaoSchema = InstituicaoEnsinoSchema()
    instituicaoData = request.get_json()

    try:
        instituicaoJson = instituicaoSchema.load(instituicaoData)

        if not validarInstituicao(instituicaoJson):
            logger.warning("Dados inválidos na validação manual.")
            return jsonify({"mensagem": "Dados inválidos."}), 400

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

        logger.info(f"Instituição inserida com ID: {id}")

        return jsonify(instituicaoEnsino.toDict()), 200

    except ValidationError as err:
        logger.error(f"Erro de validação: {err}")
        return jsonify(err.messages), 400
    except sqlite3.Error as e:
        logger.error(f"Erro no banco de dados: {e}")
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500


@app.route("/instituicoes/<int:id>", methods=["DELETE"])
def instituicaoRemocaoResource(id):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tb_instituicao WHERE id = ?', (id,))
        conn.commit()

        if cursor.rowcount == 0:
            logger.warning(f"Instituição com ID {id} não encontrada para remoção.")
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        logger.info(f"Instituição com ID {id} removida com sucesso.")
        return jsonify({"mensagem": "Instituição removida com sucesso."}), 200

    except sqlite3.Error as e:
        logger.error(f"Erro ao remover instituição: {e}")
        return jsonify({"mensagem": "Erro ao acessar o banco de dados."}), 500


@app.route("/instituicoes/<int:id>", methods=["PUT"])
def instituicaoAtualizacaoResource(id):
    logger.info(f"Put - Atualização de Instituição ID: {id}")
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
            logger.warning(f"Instituição com ID {id} não encontrada para atualização.")
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsino = InstituicaoEnsino(id, *values[:-1])
        logger.info(f"Instituição com ID {id} atualizada com sucesso.")

        return jsonify(instituicaoEnsino.toDict()), 200

    except ValidationError as err:
        logger.error(f"Erro de validação: {err}")
        return jsonify(err.messages), 400
    except sqlite3.Error as e:
        logger.error(f"Erro ao atualizar instituição: {e}")
        return jsonify({"mensagem": "Erro ao atualizar instituição."}), 500


@app.route("/instituicoes/<int:id>", methods=["GET"])
def instituicoesByIdResource(id):
    logger.info(f"Get - Instituição ID: {id}")
    try:
        cursor = getConnection().cursor()
        cursor.execute('SELECT * FROM tb_instituicao WHERE id = ?', (id,))
        row = cursor.fetchone()

        if not row:
            logger.warning(f"Instituição com ID {id} não encontrada.")
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsino = InstituicaoEnsino(*row)
        return jsonify(instituicaoEnsino.toDict()), 200

    except sqlite3.Error as e:
        logger.error(f"Erro ao buscar instituição: {e}")
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
