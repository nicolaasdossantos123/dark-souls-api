from database import cursor, conexao

cursor.execute("""
CREATE TABLE IF NOT EXISTS personagem (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,
    classe TEXT,
    hp INTEGER,
    level INTEGER,
    stamina INTEGER,
    forca INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,
    tipo_arma TEXT,
    peso INTEGER,
    durabilidade INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bosses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,
    vida INTEGER,
    dano INTEGER,
    dificuldade INTEGER,
    regiao TEXT,
    vivo_derrotado INTEGER,
    item_drop TEXT
)
""")
conexao.commit()