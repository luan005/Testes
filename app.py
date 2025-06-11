from flask import jsonify
import sqlite3

from helpers.application import app, api
from helpers.database import getConnection
from helpers.logging import logger
from helpers.CORS import cors

from resources.InstituicaoResource import InstituicoesResource, InstituicaoResource
from resources.IndexResource import IndexResource

# Inicializa CORS
cors.init_app(app)

# Define recursos RESTful
api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicaoResource, '/instituicoes/<int:id>')
