# -*- coding: utf-8 -*-

# Interface e integração com operações

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import RECLASS_NDVI_FINAL
import mask_res
import graficos

class Ui_biomassa(object):
    def setupUi(self, biomassa):
        biomassa.setObjectName("biomassa")
        biomassa.resize(811, 641)
        
        self.botao = QtWidgets.QDialogButtonBox(biomassa)
        self.botao.setGeometry(QtCore.QRect(620, 46, 161, 32))
        self.botao.setOrientation(QtCore.Qt.Horizontal)
        self.botao.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.botao.setObjectName("botao")
        
        self.caminho_pasta = QtWidgets.QLineEdit(biomassa)
        self.caminho_pasta.setGeometry(QtCore.QRect(110, 20, 671, 21))
        self.caminho_pasta.setObjectName("caminho_pasta")
        
        self.nome_shp = QtWidgets.QLineEdit(biomassa)
        self.nome_shp.setGeometry(QtCore.QRect(110, 50, 491, 21))
        self.nome_shp.setObjectName("nome_shp")
        
        self.label = QtWidgets.QLabel(biomassa)
        self.label.setGeometry(QtCore.QRect(30, 20, 61, 20))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(biomassa)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 91, 20))
        self.label_2.setObjectName("label_2")
        
        self.grafico_tabela = QtWidgets.QGraphicsView(biomassa)
        self.grafico_tabela.setGeometry(QtCore.QRect(30, 90, 751, 521))
        self.grafico_tabela.setObjectName("grafico_tabela")

        # Configurar o Canvas do Matplotlib dentro do QGraphicsView
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(self.canvas)
        self.grafico_tabela.setScene(self.scene)

        self.retranslateUi(biomassa)
        self.botao.accepted.connect(self.executar_operacao)  # Conectar o botão de "Ok" à operação
        self.botao.rejected.connect(biomassa.reject)
        QtCore.QMetaObject.connectSlotsByName(biomassa)

    def retranslateUi(self, biomassa):
        _translate = QtCore.QCoreApplication.translate
        biomassa.setWindowTitle(_translate("biomassa", "BIOMASSA"))
        self.caminho_pasta.setText(_translate("biomassa", "X:/Sigmagis/VERTICAIS/COLABORADORES/Luan_Faria/MODELOS_QGIS/MODELO/CAMPO FURLAN/"))
        self.nome_shp.setText(_translate("biomassa", "BASE_TALHOES_NDVI_EXEMPLO.shp"))
        self.label.setText(_translate("biomassa", "CAMINHO"))
        self.label_2.setText(_translate("biomassa", "NOME DO SHP"))

    def executar_operacao(self):
        # Obter os valores dos campos da interface
        raiz = self.caminho_pasta.text()
        shp = self.nome_shp.text()
        ervas = ''  # Pode adicionar mais inputs na interface para configurar este valor, se necessário
        upscale_factor = 4  # Fixo no código original, mas pode ser ajustado conforme necessidade

        # Chamar as operações do segundo código
        try:
            #mask_res.extract(raiz, shp, upscale_factor)
            #RECLASS_NDVI_FINAL.reclass(raiz, shp, ervas)
            self.plotar_grafico_pizza()  # Chamar função para plotar o gráfico de pizza
            print("Operações concluídas com sucesso!")
        except Exception as e:
            print(f"Erro durante a execução: {e}")

    def plotar_grafico_pizza(self):
        # Limpar o gráfico atual
        self.figure.clear()

        # Criar novo subplot para o gráfico de pizza
        ax = self.figure.add_subplot(111)

        try:
            # Modifique a função pizza para aceitar 'ax' como argumento e plote no eixo fornecido
            graficos.pizza(ax=ax)  
        except AttributeError:
            # Caso contrário, plote um gráfico de exemplo
            data = [30, 20, 50]
            labels = ["Categoria A", "Categoria B", "Categoria C"]
            ax.pie(data, labels=labels, autopct='%1.1f%%')

        # Atualizar o canvas
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    biomassa = QtWidgets.QDialog()
    ui = Ui_biomassa()
    ui.setupUi(biomassa)
    biomassa.show()
    sys.exit(app.exec_())
