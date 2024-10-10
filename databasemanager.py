import pyodbc
import logging

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

    def execute_command(self, command, values=None):
        # Executa um comando SQL passado como parâmetro
        if not self.connection:
            logging.error("Erro: conexão não estabelecida.")
            return None

        try:
            with self.connection.cursor() as cursor:
                if values:
                    cursor.execute(command, values)
                else:
                    cursor.execute(command)
                self.connection.commit()
                logging.info(f"Comando executado com sucesso: {command}")
        except Exception as e:
            logging.error(f"Erro ao executar comando: {e}")
            self.connection.rollback()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logging.info("Conexão ao banco de dados fechada com sucesso.")

    
    def insert(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                logging.info("Dados inseridos com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao inserir dados: {e}")
            self.connection.rollback()

    def select(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logging.error(f"Erro ao selecionar dados: {e}")
            return None

    def update(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                logging.info("Dados atualizados com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao atualizar dados: {e}")
            self.connection.rollback()