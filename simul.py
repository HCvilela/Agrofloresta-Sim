#class: Declaração de uma classe, neste caso, chamada AgroflorestaApp, que herda da classe App do Kivy.
#App: Classe pai, usada para criar uma aplicação.
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

# Classe principal da aplicação Kivy para simular o espaçamento em um sistema agroflorestal familiar
class AgroflorestaApp(App):
    #nome da função que cria a interface
    def build(self):
        # Layout principal da aplicação, organizado verticalmente
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Entrada para o tamanho do sistema (escala de 10 metros quadrados)
        self.layout.add_widget(Label(text="Tamanho do sistema (em múltiplos de 10 m²):"))
        self.tamanho_sistema_input = TextInput(hint_text="Digite um valor", multiline=False)
        self.layout.add_widget(self.tamanho_sistema_input)

        # Entrada para o número de culturas possíveis
        self.layout.add_widget(Label(text="Quantidade de culturas possíveis no sistema:"))
        self.quantidade_culturas_input = TextInput(hint_text="Digite um valor", multiline=False)
        self.layout.add_widget(self.quantidade_culturas_input)

        # Spinner para selecionar o tipo de cultura, com algumas opções pré-definidas
        self.layout.add_widget(Label(text="Selecione o tipo de cultura:"))
        self.tipo_cultura_spinner = Spinner(
            text='Selecione um tipo de cultura',
            values=('Milho', 'Feijão', 'Mandioca', 'Café', 'Banana')
        )
        self.layout.add_widget(self.tipo_cultura_spinner)

        # Botão para realizar a simulação
        self.simular_button = Button(text="Simular Espaçamento")
        self.simular_button.bind(on_press=self.simular)
        self.layout.add_widget(self.simular_button)

        # Área de saída para mostrar os resultados da simulação
        self.resultado_label = Label(text="Resultado da Simulação aparecerá aqui")
        self.layout.add_widget(self.resultado_label)

        return self.layout

    # Função para calcular o espaçamento correto e realizar a simulação
    def simular(self, instance):
        try:
            # Obtendo os dados fornecidos pelo usuário
            tamanho_sistema = int(self.tamanho_sistema_input.text) * 10  # Escala de 10 m²
            quantidade_culturas = int(self.quantidade_culturas_input.text)
            tipo_cultura = self.tipo_cultura_spinner.text

            # Validação para verificar se o usuário selecionou um tipo de cultura válido
            if tipo_cultura == "Selecione um tipo de cultura":
                self.resultado_label.text = "Por favor, selecione um tipo de cultura."
                return

            # Cálculo do espaçamento ideal com base em algumas regras definidas (apenas um exemplo simples)
            # Considera-se um espaçamento básico para diferentes tipos de culturas
            espacos_ideais = {
                'Milho': 0.6,  # 60 cm entre plantas
                'Feijão': 0.4,  # 40 cm entre plantas
                'Mandioca': 1.0,  # 1 m entre plantas
                'Café': 2.0,  # 2 m entre plantas
                'Banana': 3.0  # 3 m entre plantas
            }

            # Espaçamento baseado no tipo de cultura
            espaco_planta = espacos_ideais.get(tipo_cultura, 1.0)

            # Cálculo da área necessária para cada planta e do número máximo de plantas possíveis
            area_por_planta = espaco_planta ** 2  # Aproximando para simplificar como uma área quadrada ao redor da planta
            num_maximo_plantas = tamanho_sistema / area_por_planta

            # Mensagem de resultado da simulação
            resultado_texto = (
                f"Tamanho do sistema: {tamanho_sistema} m²\n"
                f"Tipo de Cultura: {tipo_cultura}\n"
                f"Espaçamento ideal entre plantas: {espaco_planta} m\n"
                f"Área necessária por planta: {area_por_planta:.2f} m²\n"
                f"Número máximo de plantas: {int(num_maximo_plantas)}"
            )

            # Exibindo o resultado na tela
            self.resultado_label.text = resultado_texto

        except ValueError:
            # Tratamento de erro para entradas inválidas
            self.resultado_label.text = "Por favor, insira valores numéricos válidos."

# Execução do aplicativo
if __name__ == "__main__":
    AgroflorestaApp().run()
