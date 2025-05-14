DROP TABLE IF EXISTS tb_instituicao;

CREATE TABLE tb_instituicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no_regiao TEXT NOT NULL,
    sg_uf TEXT NOT NULL,
    no_municipio TEXT NOT NULL,
    no_mesorregiao TEXT NOT NULL,
    no_microrregiao TEXT NOT NULL,
    co_entidade TEXT NOT NULL,
    qt_mat_bas TEXT NOT NULL,
    co_regiao TEXT NOT NULL,
    co_uf TEXT NOT NULL,
    co_municipio TEXT NOT NULL,
    co_microrregiao TEXT NOT NULL,
    co_mesorregiao TEXT NOT NULL
);
