import re
import logging
import pyodbc
import os
from databasemanager import DatabaseManager

class DataManipulator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def execute_command(self, command, values=None):
        connection = self.db_manager.connection
        if not connection:
            logging.error("Erro: conexão não estabelecida.")
            return None

        try:
            with connection.cursor() as cursor:
                if values:
                    cursor.execute(command, values)
                else:
                    cursor.execute(command)
                connection.commit()
                logging.info(f"Comando executado com sucesso: {command}")
                print("Dados inseridos com sucesso no banco de dados.")
        except Exception as e:
            logging.error(f"Erro ao executar comando: {e}")
            print("Falha ao inserir dados no banco de dados.")
            connection.rollback()

    def load_data_from_sql_file(self, file_path):
        # Lê o arquivo SQL e executa os comandos INSERT
        if not os.path.exists(file_path):
            logging.error(f"Arquivo não encontrado: {file_path}")
            return
        try:
            with open(file_path, 'r') as file:
                sql_command = ''
                for line in file:
                    line = line.strip()
                    
                    # Ignora comentários e linhas vazias
                    if line.startswith('--') or not line:
                        continue
                    
                    # Concatena linhas até encontrar um ponto e vírgula
                    sql_command += line + ' '
                    if line.endswith(';'):
                        # Executa o comando SQL
                        logging.info(f"Executando comando SQL: {sql_command.strip()}")
                        self.execute_command(sql_command.strip())
                        
                        # Limpa o comando para o próximo ciclo
                        sql_command = ''
        
            logging.info("Dados carregados com sucesso do arquivo SQL.")
            print("Dados carregados com sucesso.")
        except FileNotFoundError:
            logging.error(f"Arquivo não encontrado: {file_path}")
            print(f"Arquivo não encontrado: {file_path}")
        except Exception as e:
            logging.error(f"Erro ao carregar dados do arquivo: {e}")
            print(f"Erro ao carregar dados do arquivo: {e}")

    def fetch_data_from_table(self, table_name):
        connection = self.db_manager.connection
        if not connection:
            logging.error("Erro: conexão não estabelecida.")
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                # Exibir os dados recuperados
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print(f"A tabela '{table_name}' está vazia.")
        except Exception as e:
            logging.error(f"Erro ao buscar dados da tabela {table_name}: {e}")

# Exemplo de uso
if __name__ == "__main__":
    db_manager = DatabaseManager()
    data_manipulator = DataManipulator(db_manager)
    file_path = '/home/alisson/Documentos/BackUp/AgroFloresta/Agrofloresta-Sim/preenchimento.txt'
    
    data_manipulator.load_data_from_sql_file(file_path)
    db_manager.close_connection()
