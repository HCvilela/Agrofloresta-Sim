import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

# Classe principal da aplicação Kivy para simular o espaçamento em um sistema agroflorestal familiar
class AgroflorestaApp(App):
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

        # Botão para definir as culturas a partir da quantidade escolhida
        self.definir_culturas_button = Button(text="Definir Culturas")
        self.definir_culturas_button.bind(on_press=self.definir_culturas)
        self.layout.add_widget(self.definir_culturas_button)

        # Área de layout para adicionar os Spinners para escolher os tipos de culturas e tamanhos
        self.culturas_layout = BoxLayout(orientation='vertical', spacing=5)
        self.layout.add_widget(self.culturas_layout)

        # Botão para realizar a simulação
        self.simular_button = Button(text="Simular Espaçamento", disabled=True)
        self.simular_button.bind(on_press=self.simular)
        self.layout.add_widget(self.simular_button)

        # Área de saída para mostrar os resultados da simulação
        self.resultado_label = Label(text="Resultado da Simulação aparecerá aqui")
        self.layout.add_widget(self.resultado_label)

        return self.layout

    # Função para definir os Spinners de culturas e tamanhos com base na quantidade inserida pelo usuário
    def definir_culturas(self, instance):
        try:
            # Obtendo a quantidade de culturas escolhida pelo usuário
            self.quantidade_culturas = int(self.quantidade_culturas_input.text)

            # Limpando o layout de culturas antes de adicionar novos Spinners
            self.culturas_layout.clear_widgets()

            # Criando listas para armazenar os Spinners de culturas e tamanhos
            self.cultura_spinners = []
            self.tamanho_spinners = []

            # Adicionando Spinners para cada tipo de cultura e para o tamanho correspondente
            for i in range(self.quantidade_culturas):
                # Spinner para escolher o tipo de cultura
                spinner_label = Label(text=f"Selecione o tipo de cultura para a cultura {i+1}:")
                self.culturas_layout.add_widget(spinner_label)

                cultura_spinner = Spinner(
                    text='Selecione um tipo de cultura',
                    values=(
                        'Frutífera - Grande Porte', 'Frutífera - Médio Porte', 'Frutífera - Pequeno Porte',
                        'Rasteira', 'Frutas de Horta', 'Milho', 'Feijão', 'Mandioca', 'Café', 'Banana'
                    )
                )
                self.cultura_spinners.append(cultura_spinner)
                self.culturas_layout.add_widget(cultura_spinner)

                # Spinner para escolher o tamanho da cultura
                tamanho_label = Label(text=f"Selecione o tamanho para a cultura {i+1}:")
                self.culturas_layout.add_widget(tamanho_label)

                tamanho_spinner = Spinner(
                    text='Selecione um tamanho',
                    values=('Grande', 'Médio', 'Pequeno', 'Rasteira', 'Leira')
                )
                self.tamanho_spinners.append(tamanho_spinner)
                self.culturas_layout.add_widget(tamanho_spinner)

            # Habilitar o botão de simulação após definir as culturas e tamanhos
            self.simular_button.disabled = False

        except ValueError:
            # Tratamento de erro para entradas inválidas
            self.resultado_label.text = "Por favor, insira um valor numérico válido para a quantidade de culturas."

    # Função para calcular o espaçamento correto e realizar a simulação
    def simular(self, instance):
        try:
            # Obtendo os dados fornecidos pelo usuário
            tamanho_sistema = int(self.tamanho_sistema_input.text) * 10  # Escala de 10 m²
            quantidade_culturas = int(self.quantidade_culturas_input.text)

            # Lista para armazenar os tipos de cultura escolhidos e seus respectivos tamanhos
            tipos_culturas = []
            tamanhos_culturas = []

            # Validando a seleção dos tipos de cultura e seus tamanhos
            for i in range(self.quantidade_culturas):
                cultura_spinner = self.cultura_spinners[i]
                tamanho_spinner = self.tamanho_spinners[i]

                if cultura_spinner.text == "Selecione um tipo de cultura" or tamanho_spinner.text == "Selecione um tamanho":
                    self.resultado_label.text = "Por favor, selecione um tipo de cultura e um tamanho para cada cultura."
                    return

                tipos_culturas.append(cultura_spinner.text)
                tamanhos_culturas.append(tamanho_spinner.text)

            # Espaçamento ideal para cada tipo de cultura (apenas um exemplo simples)
            espacos_ideais = {
                'Grande': 5.0,  # 5 m entre plantas
                'Médio': 3.0,  # 3 m entre plantas
                'Pequeno': 2.0,  # 2 m entre plantas
                'Rasteira': 0.5,  # 50 cm entre plantas
                'Leira': 0.4  # 40 cm entre plantas
            }

            # Cálculo do espaçamento e do número máximo de plantas
            resultado_texto = f"Tamanho do sistema: {tamanho_sistema} m²\n"
            resultado_texto += f"Quantidade de culturas: {quantidade_culturas}\n\n"

            for i, (tipo_cultura, tamanho_cultura) in enumerate(zip(tipos_culturas, tamanhos_culturas)):
                espaco_planta = espacos_ideais.get(tamanho_cultura, 1.0)
                area_por_planta = espaco_planta ** 2
                num_maximo_plantas = tamanho_sistema / (quantidade_culturas * area_por_planta)

                resultado_texto += (
                    f"Cultura {i+1}: {tipo_cultura}\n"
                    f"Tamanho: {tamanho_cultura}\n"
                    f"Espaçamento ideal entre plantas: {espaco_planta} m\n"
                    f"Área necessária por planta: {area_por_planta:.2f} m²\n"
                    f"Número máximo de plantas desta cultura: {int(num_maximo_plantas)}\n\n"
                )

            # Exibindo o resultado na tela
            self.resultado_label.text = resultado_texto

        except ValueError:
            # Tratamento de erro para entradas inválidas
            self.resultado_label.text = "Por favor, insira valores numéricos válidos."

# Execução do aplicativo
if __name__ == "__main__":
    AgroflorestaApp().run()
