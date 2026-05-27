from fastapi import APIRouter
from database import cursor, conexao
import random
from schemas import (
    Persona,
    Boss,
    Armamento,
    Combate
)
from fastapi import HTTPException

router = APIRouter()


@router.post("/personagem")
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
        raise HTTPException(
            status_code=404,
            detail="Classe inválida"
        )
        
    cursor.execute(
        """
        INSERT INTO personagem
        (nome, classe, hp, stamina, forca)
        VALUES (?, ?, ?, ?, ?)
        """,
        (persona.nome, persona.classe, hp, stamina, forca)
    )
    conexao.commit()
    
    id_personagem = cursor.lastrowid

    return {
        "mensagem": "Personagem criado!",
        "id": id_personagem,
        "nome": persona.nome,
        "classe": persona.classe,
        "hp": hp,
        "stamina": stamina,
        "forca": forca
    }


@router.post("/armamento")
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
        raise HTTPException(
            status_code=404,
            detail="Armamento inválido"
        )

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


@router.post("/bosses")
def criar_boss(boss: Boss):
    
    if boss.nome.lower() == "artorias":

        vida = 890
        dano = 50
        regiao = "Oolacile Township"
        dificuldade = 9
        item_drop = "anel do lobo"

    elif boss.nome.lower() == "capra_demon":
        
        vida = 430
        dano = 23
        regiao = "Lower Undead Burg"
        dificuldade = 4
        item_drop = "machete do bom demonio"

    elif boss.nome.lower() == "gwyn":

        vida = 1000
        dano = 72
        regiao = "Kiln of the First Flame"
        dificuldade = 10
        item_drop = "alma de gwyn"

    else:
        raise HTTPException(
            status_code=404,
            detail="Boss inválido"
        )

    cursor.execute(
        """
        INSERT INTO bosses
        (nome, vida, dano, regiao, dificuldade,
         vivo_derrotado, item_drop)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            boss.nome,
            vida,
            dano,
            regiao,
            dificuldade,
            boss.vivo_derrotado,
            item_drop
        )
    )

    conexao.commit()

    id_boss = cursor.lastrowid

    return {
        "id": id_boss,
        "nome": boss.nome,
        "vida": vida,
        "dano": dano,
        "regiao": regiao,
        "dificuldade": dificuldade,
        "status": "Vivo" if boss.vivo_derrotado else "Derrotado",
        "item_drop": item_drop
    }
    
@router.delete("/personagem/{id}")
def deletar_personagem(id: int):
    cursor.execute(
        "DELETE FROM personagem WHERE id = ?",
        (id,)
    )
    conexao.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Personagem não encontrada"
        )
    
    return {
        "mensagem": "Personagem deletado!",
        "id": id
    }

@router.put("/personagem/{id}")
def atualizar_personagem(id: int, dados: Persona):

    cursor.execute(
        """
        UPDATE personagem
        SET nome = ?, classe = ?, level = ?
        WHERE id = ?
        """,
        (
            dados.nome,
            dados.classe,
            dados.level,
            id
        )
    )
    conexao.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Personagem não encontrado"
        )

    return {
        "mensagem": "Personagem atualizado!"
    }

@router.get("/personagem/{id}")
def buscar_personagem(id: int):

    cursor.execute(
        "SELECT * FROM personagem WHERE id = ?",
        (id,)
    )

    personagem = cursor.fetchone()

    if personagem is None:
        raise HTTPException(
    status_code=404,
    detail="Personagem não encontrado"
)

    return {
        "id": personagem[0],
        "nome": personagem[1],
        "classe": personagem[2],
        "hp": personagem[3],
        "stamina": personagem[4],
        "forca": personagem[5]
    }

@router.get("/bosses/{id}")
def buscar_boss(id: int):

    cursor.execute(
        "SELECT * FROM bosses WHERE id = ?",
        (id,)
    )

    boss = cursor.fetchone()

    if boss is None:
        raise HTTPException(
    status_code=404,
    detail="Boss inválido"
)

    return {

    "id": boss[0],
    "nome": boss[1],
    "vida": boss[2],
    "dano": boss[3],
    "dificuldade": boss[4],
    "regiao": boss[5],
    "status": "Vivo" if boss[6] else "Derrotado",
    "item_drop": boss[7]
}

@router.post("/combate")
def iniciar_combate(combate: Combate):
    
    log_combate = []

    cursor.execute(
        "SELECT * FROM personagem WHERE id = ?",
        (combate.personagem_id,)
    )

    personagem = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM bosses WHERE id = ?",
        (combate.boss_id,)
    )

    boss = cursor.fetchone()

    if personagem is None:
        raise HTTPException(
            status_code=404,
            detail="Personagem não encontrado"
        )

    if boss is None:
        raise HTTPException(
            status_code=404,
            detail="Boss não encontrado"
        )

    personagem_nome = personagem[1]
    personagem_hp = personagem[3]
    personagem_forca = personagem[5]

    boss_nome = boss[1]
    boss_vida = boss[2]
    boss_dano = boss[3]

    dano_personagem = (
        personagem_forca + random.randint(1,10)
    )

    dano_boss = (
        boss_dano + random.randint(1,10)
    )

    vida_restante_boss = (
        boss_vida - dano_personagem
    )

    vida_restante_personagem = (
        personagem_hp - dano_boss
    )

    while personagem_hp > 0 and boss_vida > 0:
        chance_esquiva_boss = random.randint(1,100)
        
        dano_personagem = (
            personagem_forca + random.randint(1,10)
        )
        
        boss_vida -= dano_personagem
        
        if chance_esquiva_boss <= 20:

            log_combate.append(
                f"{boss_nome} esquivou!"
            )

        else:

            dano_personagem = (
                personagem_forca +
                random.randint(1,10)
            )

        boss_vida -= dano_personagem
        personagem_hp -= dano_boss

    log_combate.append(
        f"{personagem_nome} causou "
        f"{dano_personagem} dano"
    )
        
    log_combate.append(
        f"{personagem_nome} causou "
        f"{dano_personagem} dano "
    )
    
    if boss_vida > 0:

        dano_boss = (
            boss_dano + random.randint(1,10)
    )

    personagem_hp -= dano_boss

    log_combate.append(
        f"{boss_nome} causou "
        f"{dano_boss} dano "
    )
    
    if personagem_hp > 0:
        vencedor = personagem_nome
        
    else:
        vencedor = boss_nome

    if vida_restante_boss <= 0:
        vencedor = personagem_nome

    elif vida_restante_personagem <= 0:
        vencedor = boss_nome

    return {

        "personagem": personagem_nome,
        "boss": boss_nome,

        "hp_final_personagem": personagem_hp,
        "hp_final_boss": boss_vida,

        "vencedor": vencedor,

        "log": log_combate
    }

