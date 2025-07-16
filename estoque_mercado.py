import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()


def get_connection() :
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )
        if connection.is_connected():
            print("Conectado ao banco de dados")
            return connection
    except Error as e:
        print("Erro ao conectar ao MySQL", e)
        return None
    
def inserir_produto(name: str, price: float, quantity: int):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, price, quantity))
        conn.commit()

        novo_id = cursor.lastrowid
        print(f"Produto cadastrado! ID gerado:{novo_id}")
    except Error as e:
        print("Erro ao inserir:", e)
    finally:
        cursor.close()
        conn.close()

def listar_todos():
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, quantity FROM products")
        rows = cursor.fetchall()
        if not rows:
            print("Nenhum cadastro")
        else:
            print("Lista de produtos!")
            for r in rows:
                print(f"ID {r[0]:>3} | {r[1]:<20} | R$ {r[2]:>7.2f} | Qtde: {r[3]}")
    except Error as e:
        print("Erro ao buscar:", e)
    finally:
        cursor.close()
        conn.close()

def consultar_por_id(prod_id: int):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, price, quantity FROM products WHERE id = %s", (prod_id,)
        )
        row = cursor.fetchone()
        if row:
            print(f"Produto encontrado!\n"
                  f"ID:{row[0]}\n Nome: {row[1]}\n Preço: R$ {row[2]:.2f}\n Quantidade : {row[3]}")
        else:
            print("Nenhum produto com esse ID.")
    except Error as e:
        print("Erro na consulta:")
    finally:
        cursor.close()
        conn.close()

def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Consultar produto por ID")
        print("2 - Listar TODOS os produtos")
        print("3 - Cadastrar novo produto")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                pid = int(input("Digite o ID do produto:"). strip())
                consultar_por_id(pid)
            except ValueError:
                print("Id invalido")
        elif opcao == "2":
            listar_todos()
        elif opcao == "3":
            nome = input("Nome do produto: ").strip()
            try:
                preco = float(input("Preço (ex: 12.50): ").replace(",", "."))
                qtd = int(input("Quantidade: "))
                inserir_produto(nome, preco, qtd)
            except ValueError:
                print(" Preço ou quantidade inválidos!")
        elif opcao == "4":
            print("...")
            break
        else:
            print(" Opção inválida.")

if __name__ == "__main__":
    menu()