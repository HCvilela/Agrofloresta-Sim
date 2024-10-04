import pyodbc #instalar via terminal
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self):
        # Configurações da conexão
        self.data_connection = (
            "Driver={MariaDB ODBC 3.2 Driver};" #Instalar esse driver no pc antes
            "Server=127.0.0.1;"
            "Database=agroflorestasim;"
            "UID=root;"
            "PWD=123456;"
            "PORT=3306;"
        )
        self.connection = self.create_connection()  # Cria a conexão

    def create_connection(self):
        # Cria e retorna a conexão ao banco de dados
        try:
            conn = pyodbc.connect(self.data_connection)  # Estabelece a conexão
            logging.info("Conexão ao banco de dados estabelecida com sucesso.")
            return conn
        except Exception as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None  # Retorna None se a conexão falhar

    def execute_command(self, command):
        # Executa um comando SQL passado como parâmetro
        if not self.connection:
            logging.error("Erro: conexão não estabelecida.")
            return None  # Verifica se a conexão foi criada

        sqlreturn = None  # Inicializa a variável para armazenar resultados
        try:
            with self.connection.cursor() as cursor:  # Usa um gerenciador de contexto para o cursor
                cursor.execute(command)  # Executa o comando
                if command.strip().lower().startswith("select"):
                    sqlreturn = cursor.fetchall()  # Obtém resultados para comandos SELECT
                    return sqlreturn  # Retorna resultados diretamente
                else:
                    self.connection.commit()  # Comita a transação se não for um SELECT
                logging.info("Comando executado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao executar o comando: {e}")
        return sqlreturn  # Retorna os resultados

    def select(self, query):
        # Método específico para executar comandos SELECT
        return self.execute_command(query)

    def insert(self, query):
        # Método específico para executar comandos INSERT
        return self.execute_command(query)

    def update(self, query):
        # Método específico para executar comandos UPDATE
        return self.execute_command(query)

    def delete(self, query):
        # Método específico para executar comandos DELETE
        return self.execute_command(query)

# Exemplo de uso
if __name__ == "__main__":
    db_manager = DatabaseManager()  # Instancia a classe DatabaseManager

    # Exemplo de uso de métodos
    select_query = "SELECT * FROM teste;"  # Substitua 'sua_tabela' pelo nome da tabela
    results = db_manager.select(select_query)  # Executa um comando SELECT

    if results:  # Verifica se há resultados
        for row in results:
            logging.info(row)  # Imprime os resultados armazenados
