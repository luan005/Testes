from marshmallow import Schema, fields, validate

class InstituicaoEnsino:
    def __init__(self, id, no_regiao, sg_uf, no_municipio, no_mesorregiao, no_microrregiao,
                 co_entidade, qt_mat_bas, co_regiao, co_uf, co_municipio, co_microrregiao, co_mesorregiao):
        self.id = id
        self.no_regiao = no_regiao
        self.sg_uf = sg_uf
        self.no_municipio = no_municipio
        self.no_mesorregiao = no_mesorregiao
        self.no_microrregiao = no_microrregiao
        self.co_entidade = co_entidade
        self.qt_mat_bas = qt_mat_bas
        self.co_regiao = co_regiao
        self.co_uf = co_uf
        self.co_municipio = co_municipio
        self.co_microrregiao = co_microrregiao
        self.co_mesorregiao = co_mesorregiao

    def toDict(self):
        return {
            "id": self.id,
            "no_regiao": self.no_regiao,
            "sg_uf": self.sg_uf,
            "no_municipio": self.no_municipio,
            "no_mesorregiao": self.no_mesorregiao,
            "no_microrregiao": self.no_microrregiao,
            "co_entidade": self.co_entidade,
            "qt_mat_bas": self.qt_mat_bas,
            "co_regiao": self.co_regiao,
            "co_uf": self.co_uf,
            "co_municipio": self.co_municipio,
            "co_microrregiao": self.co_microrregiao,
            "co_mesorregiao": self.co_mesorregiao
        }
    
class InstituicaoEnsinoSchema(Schema):
    no_regiao = fields.Str(required=True, validate=validate.Length(min=1))
    sg_uf = fields.Str(required=True, validate=validate.Length(equal=2))
    no_municipio = fields.Str(required=True, validate=validate.Length(min=1))
    no_mesorregiao = fields.Str(required=True, validate=validate.Length(min=1))
    no_microrregiao = fields.Str(required=True, validate=validate.Length(min=1))
    co_entidade = fields.Str(required=True, validate=validate.Regexp(r'^[0-9]+$'))
    qt_mat_bas = fields.Str(required=True, validate=validate.Regexp(r'^[0-9]+$'))
    co_regiao = fields.Str(required=True, validate=validate.Regexp(r'^[0-9]+$'))
    co_uf = fields.Str(required=True, validate=validate.Regexp(r'^[0-9]+$'))
    co_municipio = fields.Str(required=True, validate=validate.Regexp(r'^[0-9]+$'))
    co_microrregiao = fields.Str(required=True, validate=validate.Regexp(r'^[0-9]+$'))
    co_mesorregiao = fields.Str(required=True, validate=validate.Regexp(r'^[0-9]+$'))

