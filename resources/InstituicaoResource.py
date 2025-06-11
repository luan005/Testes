from flask import request
from flask_restful import Resource
import sqlite3
from marshmallow import ValidationError

from helpers.database import getConnection
from helpers.logging import logger
from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema

def validarInstituicao(content):
    try:
        logger.info("Validando dados da instituição: %s", content)
        int(str(content.get('co_entidade', '')).strip())
        int(str(content.get('qt_mat_bas', '')).strip())
        return True
    except (ValueError, TypeError) as e:
        logger.warning("Erro na validação: %s", e)
        return False

class InstituicoesResource(Resource):
    def get(self):
        logger.info("Get - Instituições")
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            offset = (page - 1) * per_page

            logger.info("Paginação - Página: %d, Por página: %d", page, per_page)

            cursor = getConnection().cursor()

            cursor.execute('SELECT COUNT(*) FROM tb_instituicao')
            total = cursor.fetchone()[0]

            cursor.execute('''
                SELECT * FROM tb_instituicao
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            resultSet = cursor.fetchall()

            logger.info("Instituições encontradas: %d", len(resultSet))

            instituicoesEnsino = [
                InstituicaoEnsino(*row).toDict() for row in resultSet
            ]

            return {
                "total": total,
                "page": page,
                "per_page": per_page,
                "instituicoes": instituicoesEnsino
            }, 200

        except Exception as e:
            logger.error(f"Erro ao paginar instituições: {e}")
            return {"mensagem": "Erro ao acessar dados"}, 500

    def post(self):
        logger.info("Post - Instituição")
        instituicaoSchema = InstituicaoEnsinoSchema()
        instituicaoData = request.get_json()
        logger.info("Dados recebidos: %s", instituicaoData)

        try:
            instituicaoJson = instituicaoSchema.load(instituicaoData)
            logger.info("Dados validados: %s", instituicaoJson)

            if not validarInstituicao(instituicaoJson):
                logger.warning("Dados inválidos na validação manual.")
                return {"mensagem": "Dados inválidos."}, 400

            values = (
                instituicaoJson['no_regiao'], instituicaoJson['sg_uf'], instituicaoJson['no_municipio'],
                instituicaoJson['no_mesorregiao'], instituicaoJson['no_microrregiao'], str(instituicaoJson['co_entidade']),
                str(instituicaoJson['qt_mat_bas']), instituicaoJson['co_regiao'], instituicaoJson['co_uf'],
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
            logger.info("Instituição inserida com ID: %d", id)

            instituicaoEnsino = InstituicaoEnsino(id, *values)

            return instituicaoEnsino.toDict(), 200

        except ValidationError as err:
            logger.error(f"Erro de validação: {err}")
            return err.messages, 400
        except sqlite3.Error as e:
            logger.error(f"Erro no banco de dados: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500
        except Exception as e:
            logger.error(f"Erro inesperado ao inserir instituição: {e}")
            return {"mensagem": "Erro inesperado no servidor."}, 500

class InstituicaoResource(Resource):
    def get(self, id):
        logger.info(f"Get - Instituição ID: {id}")
        try:
            cursor = getConnection().cursor()
            cursor.execute('SELECT * FROM tb_instituicao WHERE id = ?', (id,))
            row = cursor.fetchone()

            if not row:
                logger.warning(f"Instituição com ID {id} não encontrada.")
                return {"mensagem": "Instituição não encontrada."}, 404

            logger.info("Instituição encontrada: %s", row)
            instituicaoEnsino = InstituicaoEnsino(*row)
            return instituicaoEnsino.toDict(), 200

        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar instituição: {e}")
            return {"mensagem": "Problema com o banco de dados."}, 500

    def delete(self, id):
        logger.info(f"Delete - Instituição ID: {id}")
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tb_instituicao WHERE id = ?', (id,))
            conn.commit()

            if cursor.rowcount == 0:
                logger.warning(f"Instituição com ID {id} não encontrada para remoção.")
                return {"mensagem": "Instituição não encontrada."}, 404

            logger.info(f"Instituição com ID {id} removida com sucesso.")
            return {"mensagem": "Instituição removida com sucesso."}, 200

        except sqlite3.Error as e:
            logger.error(f"Erro ao remover instituição: {e}")
            return {"mensagem": "Erro ao acessar o banco de dados."}, 500

    def put(self, id):
        logger.info(f"Put - Atualização de Instituição ID: {id}")
        instituicaoSchema = InstituicaoEnsinoSchema()
        instituicaoData = request.get_json()
        logger.info("Dados recebidos para atualização: %s", instituicaoData)

        try:
            instituicaoJson = instituicaoSchema.load(instituicaoData)
            logger.info("Dados validados para atualização: %s", instituicaoJson)

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
                return {"mensagem": "Instituição não encontrada."}, 404

            logger.info(f"Instituição com ID {id} atualizada com sucesso.")
            instituicaoEnsino = InstituicaoEnsino(id, *values[:-1])
            return instituicaoEnsino.toDict(), 200

        except ValidationError as err:
            logger.error(f"Erro de validação: {err}")
            return err.messages, 400
        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar instituição: {e}")
            return {"mensagem": "Erro ao atualizar instituição."}, 500
