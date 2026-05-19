import sqlite3
from pydantic import BaseModel
from fastapi import FastAPI

conexao = sqlite3.connect("darksouls1.db", check_same_thread=False)
cursor = conexao.cursor()

app = FastAPI()

class Persona(BaseModel):
    nome: str
    classe: str

class Boss(BaseModel):
    nome: str
    vivo_derrotado: bool

class Armamento(BaseModel):
    tipo_arma: str


cursor.execute("""
CREATE TABLE IF NOT EXISTS personagem (
    nome TEXT,
    classe TEXT,
    hp INTEGER,
    stamina INTEGER,
    forca INTEGER
)
""")
conexao.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario (
    nome TEXT,
    tipo_arma TEXT,
    peso INTEGER,
    durabilidade INTEGER
)
""")
conexao.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bosses (
    nome TEXT,
    vida INTEGER,
    dano INTEGER,
    regiao TEXT,
    dificuldade INTEGER,
    vivo_derrotado INTEGER,
    item_drop TEXT
)
""")
conexao.commit()


@app.get("/classes")
def classes_disponiveis():
    return [
        "guerreiro",
        "mago",
        "ladrao",
        "clerigo",
        "arqueiro"
    ]


@app.post("/personagem")
def criar_personagem(persona: Persona):

    if persona.classe.lower() == "guerreiro":
        hp = 125
        stamina = 40
        forca = 11

    elif persona.classe.lower() == "mago":
        hp = 80
        stamina = 20
        forca = 8

    elif persona.classe.lower() == "ladrao":
        hp = 70
        stamina = 55
        forca = 9

    elif persona.classe.lower() == "clerigo":
        hp = 90
        stamina = 60
        forca = 6

    elif persona.classe.lower() == "arqueiro":
        hp = 100
        stamina = 30
        forca = 10

    else:
        return {"erro": "Classe inválida"}

    cursor.execute(
        """
        INSERT INTO personagem
        (nome, classe, hp, stamina, forca)
        VALUES (?, ?, ?, ?, ?)
        """,
        (persona.nome, persona.classe, hp, stamina, forca)
    )
    conexao.commit()

    return {
        "mensagem": "Personagem criado!",
        "nome": persona.nome,
        "classe": persona.classe,
        "hp": hp,
        "stamina": stamina,
        "forca": forca
    }


@app.post("/armamento")
def escolher_armamento(armamento: Armamento):

    if armamento.tipo_arma.lower() == "espada":

        nome = "espada_longa"
        peso = 4
        durabilidade = 100

    elif armamento.tipo_arma.lower() == "adaga":

        nome = "faca_do_bandido"
        peso = 1.2
        durabilidade = 80

    else:
        return {"erro": "Armamento inválido"}

    cursor.execute(
        """
        INSERT INTO inventario
        (nome, tipo_arma, peso, durabilidade)
        VALUES (?, ?, ?, ?)
        """,
        (nome, armamento.tipo_arma, peso, durabilidade)
    )
    conexao.commit()

    return {
        "tipo_arma": armamento.tipo_arma,
        "nome": nome,
        "peso": peso,
        "durabilidade": durabilidade
    }


@app.post("/bosses")
def criar_boss(boss: Boss):

    cursor.execute(
        "INSERT INTO bosses (nome, vivo_derrotado) VALUES (?, ?)",
        (boss.nome, boss.vivo_derrotado)
    )
    conexao.commit()

    if boss.nome.lower() == "artorias":
        return {
            "nome": "artorias",
            "vida": 890,
            "dano": 50,
            "regiao": "Oolacile Township",
            "dificuldade": 9,
            "status": "Vivo" if boss.vivo_derrotado else "Derrotado",
            "item_drop": "anel do lobo"
        }

    elif boss.nome.lower() == "capra_demon":
        return {
            "nome": "capra_demon",
            "vida": 430,
            "dano": 23,
            "regiao": "Lower Undead Burg",
            "dificuldade": 4,
            "status": "Vivo" if boss.vivo_derrotado else "Derrotado",
            "item_drop": "machete do bom demonio"
        }

    elif boss.nome.lower() == "gwyn":
        return {
            "nome": "gwyn",
            "vida": 1000,
            "dano": 72,
            "regiao": "Kiln of the First Flame",
            "dificuldade": 10,
            "status": "Vivo" if boss.vivo_derrotado else "Derrotado",
            "item_drop": "alma de gwyn"
        }

    else:
        return {"erro": "Boss inválido"}


@app.get("/listar_personagem")
def listar_personagem(
    nome=None,
    forca=None,
    hp=None,
    classe=None,
    stamina=None,
    limit: int = 5,
    offset: int = 0
):

    resultado = []
    parametros = []

    query = "SELECT * FROM personagem WHERE 1=1"

    if nome:
        query += " AND nome LIKE ?"
        parametros.append(f"%{nome}%")

    if forca is not None:
        query += " AND forca = ?"
        parametros.append(forca)

    if hp is not None:
        query += " AND hp = ?"
        parametros.append(hp)

    if stamina is not None:
        query += " AND stamina = ?"
        parametros.append(stamina)

    if classe is not None:
        query += " AND classe LIKE ?"
        parametros.append(f"%{classe}%")

    query += " LIMIT ? OFFSET ?"

    parametros.append(limit)
    parametros.append(offset)

    cursor.execute(query, parametros)

    dados = cursor.fetchall()

    for t in dados:
        resultado.append({
            "nome": t[0],
            "classe": t[1],
            "hp": t[2],
            "stamina": t[3],
            "forca": t[4]
        })

    return {
        "total": len(resultado),
        "dados": resultado
    }


@app.get("/listar_bosses")
def listar_bosses(
    nome=None,
    vida=None,
    dano=None,
    regiao=None,
    dificuldade=None,
    vivo_derrotado=None,
    item_drop=None,
    limit: int = 5,
    offset: int = 0
):

    resultado = []
    parametros = []

    query = "SELECT * FROM bosses WHERE 1=1"

    if nome:
        query += " AND nome LIKE ?"
        parametros.append(f"%{nome}%")

    if vida is not None:
        query += " AND vida = ?"
        parametros.append(vida)

    if dano is not None:
        query += " AND dano = ?"
        parametros.append(dano)

    if regiao is not None:
        query += " AND regiao LIKE ?"
        parametros.append(f"%{regiao}%")

    if dificuldade is not None:
        query += " AND dificuldade = ?"
        parametros.append(dificuldade)

    if vivo_derrotado is not None:
        query += " AND vivo_derrotado = ?"
        parametros.append(vivo_derrotado)

    if item_drop is not None:
        query += " AND item_drop LIKE ?"
        parametros.append(f"%{item_drop}%")

    query += " LIMIT ? OFFSET ?"

    parametros.append(limit)
    parametros.append(offset)

    cursor.execute(query, parametros)

    dados = cursor.fetchall()

    for t in dados:
        resultado.append({
            "nome": t[0],
            "vida": t[1],
            "dano": t[2],
            "regiao": t[3],
            "dificuldade": t[4],
            "vivo_derrotado": t[5],
            "item_drop": t[6]
        })

    return {
        "total": len(resultado),
        "dados": resultado
    }