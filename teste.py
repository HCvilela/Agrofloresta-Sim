# teste.py
from databasemanager import DatabaseManager  # Importa a classe DatabaseManager do arquivo onde ela está definida

def main():
    db_manager = DatabaseManager()  # Instancia a classe DatabaseManager

    # Exemplo de uso da tabela 'sua_tabela'. Altere conforme a sua necessidade.
    tabela = 'teste'

    # Testando inserção de dados
    try:
        insert_query = f"INSERT INTO {tabela} (id, testando) VALUES (2, 'teste python');"  # Substitua as colunas e valores
        db_manager.insert(insert_query)
        print("Dados inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

    # Testando seleção de dados
    try:
        select_query = f"SELECT * FROM {tabela};"
        results = db_manager.select(select_query)
        if results:
            print("Resultados da seleção:")
            for row in results:
                print(row)
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Erro ao selecionar dados: {e}")

    # Testando atualização de dados
    try:
        update_query = f"UPDATE {tabela} SET id = 3 WHERE testando = 'teste python';"  # Altere conforme necessário
        db_manager.update(update_query)
        print("Dados atualizados com sucesso.")
    except Exception as e:
        print(f"Erro ao atualizar dados: {e}")

    # # Testando exclusão de dados
    # try:
    #     delete_query = f"DELETE FROM {tabela} WHERE coluna1 = 'valor1';"  # Altere conforme necessário
    #     db_manager.delete(delete_query)
    #     print("Dados excluídos com sucesso.")
    # except Exception as e:
    #     print(f"Erro ao excluir dados: {e}")

if __name__ == "__main__":
    main()
