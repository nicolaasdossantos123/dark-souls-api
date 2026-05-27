import sqlite3

conexao = sqlite3.connect(
    "darksouls1.db",
    check_same_thread=False
)

cursor = conexao.cursor()