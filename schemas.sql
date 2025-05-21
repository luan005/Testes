PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS tb_instituicao;
DROP TABLE IF EXISTS tb_municipio;
DROP TABLE IF EXISTS tb_microrregiao;
DROP TABLE IF EXISTS tb_mesorregiao;
DROP TABLE IF EXISTS tb_uf;

CREATE TABLE tb_uf (
    id INTEGER PRIMARY KEY,
    sigla TEXT NOT NULL,
    nome TEXT NOT NULL,
    regiao_id INTEGER NOT NULL,
    regiao_nome TEXT NOT NULL
);

CREATE TABLE tb_mesorregiao (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    uf_id INTEGER NOT NULL,
    uf_nome TEXT NOT NULL,
    uf_sigla TEXT NOT NULL,
    regiao_id INTEGER NOT NULL,
    regiao_nome TEXT NOT NULL,
    regiao_sigla TEXT NOT NULL,
    FOREIGN KEY (uf_id) REFERENCES tb_uf(id)
);

CREATE TABLE tb_microrregiao (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    mesorregiao_id INTEGER NOT NULL,
    mesorregiao_nome TEXT NOT NULL,
    uf_id INTEGER NOT NULL,
    uf_nome TEXT NOT NULL,
    uf_sigla TEXT NOT NULL,
    regiao_id INTEGER NOT NULL,
    regiao_nome TEXT NOT NULL,
    regiao_sigla TEXT NOT NULL,
    FOREIGN KEY (mesorregiao_id) REFERENCES tb_mesorregiao(id),
    FOREIGN KEY (uf_id) REFERENCES tb_uf(id)
);

CREATE TABLE tb_municipio (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    microrregiao_id INTEGER NOT NULL,
    microrregiao_nome TEXT NOT NULL,
    mesorregiao_id INTEGER NOT NULL,
    mesorregiao_nome TEXT NOT NULL,
    uf_id INTEGER NOT NULL,
    uf_nome TEXT NOT NULL,
    uf_sigla TEXT NOT NULL,
    regiao_id INTEGER NOT NULL,
    regiao_nome TEXT NOT NULL,
    regiao_sigla TEXT NOT NULL,
    FOREIGN KEY (microrregiao_id) REFERENCES tb_microrregiao(id),
    FOREIGN KEY (mesorregiao_id) REFERENCES tb_mesorregiao(id),
    FOREIGN KEY (uf_id) REFERENCES tb_uf(id)
);

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
    co_municipio INTEGER NOT NULL,
    FOREIGN KEY (co_municipio) REFERENCES tb_municipio(id)
);
