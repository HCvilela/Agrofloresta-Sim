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
            "Database=agroflorestasim;"
            "UID=root;"
            "PWD=123456;"
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

    # Funções de inserção (as mesmas que criamos anteriormente)

    def insert_cultura(self, nome_cultura, tipo_cultivo, atrai, proposito_cultivo, tamanho, ciclo, proposito_cultivo_id, tipo_cultivo_id, cultura_tratamento_id):
        command = """
            INSERT INTO Culturas (NomeCultura, Tipo_Cultivo, Atrai, PropositoCultivo, Tamanho, Ciclo, PropositoCultivo_idPropositoCultivo, TipoCultivo_idTipoCultivo, Cultura_Tratamento_idCultura_Tratamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (nome_cultura, tipo_cultivo, atrai, proposito_cultivo, tamanho, ciclo, proposito_cultivo_id, tipo_cultivo_id, cultura_tratamento_id)
        self.execute_command(command, values)

    def insert_culturas_caracteristicas(self, descricao, custo_semente, pragas, doencas, anomalia_fisiologica):
        command = """
            INSERT INTO Culturas_caracteristicas (Descricao, Custo_Semente, Pragas, Doencas, AnomaliaFisiologica)
            VALUES (?, ?, ?, ?, ?)
        """
        values = (descricao, custo_semente, pragas, doencas, anomalia_fisiologica)
        self.execute_command(command, values)

    def insert_cultura_tratamento(self, solo_preparado, tipos_solo, densidade_plantio, espacamento_sulcos, controle_daninhas, armazenamento, temperatura, armazenamento_refrig, irrigacao_necessaria, luminosidade, fertilidade_solo, fertilizantes, cultivares_certificadas):
        command = """
            INSERT INTO Cultura_Tratamento (SoloPreparado, `Tipos de solo`, DensidadePlantio_Cultura, Espacamento_Sulcos, controle_daninhas, Armazenamento, Temperatura, Armazenamento_Refrig, IrrigacaoNecessaria, luminosidade, FertilidadeSolo, Fertilizantes, `cultivares e certificadas`)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (solo_preparado, tipos_solo, densidade_plantio, espacamento_sulcos, controle_daninhas, armazenamento, temperatura, armazenamento_refrig, irrigacao_necessaria, luminosidade, fertilidade_solo, fertilizantes, cultivares_certificadas)
        self.execute_command(command, values)

    def insert_proposito_cultivo(self, descricao):
        command = """
            INSERT INTO PropositoCultivo (descricao)
            VALUES (?)
        """
        values = (descricao,)
        self.execute_command(command, values)

    def insert_tipo_cultivo(self, tipo_plantio, descricao):
        command = """
            INSERT INTO TipoCultivo (TIpo_Plantio, descricao)
            VALUES (?, ?)
        """
        values = (tipo_plantio, descricao)
        self.execute_command(command, values)

    def insert_requisitos(self, adubacao, temperatura, umidade, altitude, culturas_id):
        command = """
            INSERT INTO Requisitos (Adubacao, Temperatura, Umidade, Altitude, Culturas_idCulturas)
            VALUES (?, ?, ?, ?, ?)
        """
        values = (adubacao, temperatura, umidade, altitude, culturas_id)
        self.execute_command(command, values)

    def insert_sistemas_agricolas(self, sis_espacamento_plantas, sis_tempo, culturas_id):
        command = """
            INSERT INTO SistemasAgricolas (SisEspacamentoPlantas, Sis_Tempo, Culturas_idCulturas)
            VALUES (?, ?, ?)
        """
        values = (sis_espacamento_plantas, sis_tempo, culturas_id)
        self.execute_command(command, values)


# Função para ler o arquivo txt e preencher o banco de dados
def preencher_banco_dados_arquivo(arquivo_txt, db_manager):
    with open(arquivo_txt, 'r') as file:
        for linha in file:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue  # Ignorar linhas vazias ou de comentário

            dados = linha.split(";")
            tabela = dados[0]

            try:
                if tabela == "Culturas":
                    db_manager.insert_cultura(dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8], dados[9])
                elif tabela == "Culturas_caracteristicas":
                    db_manager.insert_culturas_caracteristicas(dados[1], dados[2], dados[3], dados[4], dados[5])
                elif tabela == "Cultura_Tratamento":
                    db_manager.insert_cultura_tratamento(dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8], dados[9], dados[10], dados[11], dados[12], dados[13])
                elif tabela == "PropositoCultivo":
                    db_manager.insert_proposito_cultivo(dados[1])
                elif tabela == "TipoCultivo":
                    db_manager.insert_tipo_cultivo(dados[1], dados[2])
                elif tabela == "Requisitos":
                    db_manager.insert_requisitos(dados[1], dados[2], dados[3], dados[4], dados[5])
                elif tabela == "SistemasAgricolas":
                    db_manager.insert_sistemas_agricolas(dados[1], dados[2], dados[3])
            except Exception as e:
                logging.error(f"Erro ao inserir dados da tabela {tabela}: {e}")


# Exemplo de uso
db_manager = DatabaseManager()
preencher_banco_dados_arquivo('preenchimento.txt', db_manager)
db_manager.close_connection()
