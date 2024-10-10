import pyodbc
import logging
import os

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self):
        # Configurações da conexão
        self.data_connection = (
            "Driver={MariaDB ODBC 3.2 Driver};"  # Instalar esse driver no PC antes
            "Server=127.0.0.1;"
            "Database=AgroFlorestaSIM;"
            "UID=root;"
            "PWD=996550725;"
            "PORT=3306;"
        )
        self.connection = self.create_connection()  # Cria a conexão

    def create_connection(self):
        # Cria e retorna a conexão ao banco de dados
        try:
            conn = pyodbc.connect(self.data_connection)
            logging.info("Conexão ao banco de dados estabelecida com sucesso.")
            return conn
        except Exception as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logging.info("Conexão ao banco de dados fechada com sucesso.")

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
        except Exception as e:
            logging.error(f"Erro ao executar comando: {e}")
            connection.rollback()

    def load_data_from_sql_file(self, file_path):
        if not os.path.exists(file_path):
            logging.error(f"Arquivo não encontrado: {file_path}")
            return
        try:
            with open(file_path, 'r') as file:
                sql_command = ''
                for line in file:
                    line = line.strip()
                    if line.startswith('--') or not line:
                        continue
                    
                    sql_command += line + ' '
                    if line.endswith(';'):
                        logging.info(f"Executando comando SQL: {sql_command.strip()}")
                        self.execute_command(sql_command.strip())
                        sql_command = ''
        
            logging.info("Dados carregados com sucesso do arquivo SQL.")
        except Exception as e:
            logging.error(f"Erro ao carregar dados do arquivo: {e}")

class DataViewer:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def display_data(self, table_name):
        connection = self.db_manager.connection
        if not connection:
            logging.error("Erro: conexão não estabelecida.")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()

                # Exibir os dados recuperados
                if rows:
                    # Obtém os nomes das colunas
                    columns = [column[0] for column in cursor.description]
                    print(f"{' | '.join(columns)}")  # Exibe os nomes das colunas
                    print("-" * (len(columns) * 10))  # Linha separadora
                    for row in rows:
                        print(" | ".join(str(value) for value in row))
                else:
                    print(f"A tabela '{table_name}' está vazia.")
        except Exception as e:
            logging.error(f"Erro ao buscar dados da tabela {table_name}: {e}")

# Como usar
if __name__ == "__main__":
    db_manager = DatabaseManager()
    data_viewer = DataViewer(db_manager)

    #Podemos replicar vários desse para verificar várias tabelas
    # Exibir dados da tabela:
    data_viewer.display_data('Cultura_Tratamento')

    data_viewer.display_data('Culturas')

    db_manager.close_connection()
