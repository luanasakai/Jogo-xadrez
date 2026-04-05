import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt
from UI.ui_tabuleiro import Ui_MainWindow
import pecas as pc

class Tabuleiro(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.carregar_pecas()
        self.btn_Confirmar.clicked.connect(self.ao_confirmar)

    def svg_para_icone(self, caminho: str, tamanho: int) -> QIcon:
        renderer = QSvgRenderer(caminho)
        pixmap = QPixmap(tamanho, tamanho)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def carregar_pecas(self):
        TAMANHO = 65
        # Limpa todos os botões primeiro
        for linha in ["1","2","3","4","5","6","7","8"]:
            for col in ["A","B","C","D","E","F","G","H"]:
                btn = getattr(self, f"btn_{col}{linha}")
                btn.setIcon(QIcon())

        # Coloca as peças conforme o estado atual
        for casa, peca in pc.Pecas.estado.items():
            btn = getattr(self, f"btn_{casa}")
            icone = self.svg_para_icone(pc.Pecas.caminho_svg(peca), TAMANHO)
            btn.setIcon(icone)
            btn.setIconSize(QSize(TAMANHO, TAMANHO))

    def ao_confirmar(self):
        pass  # lógica futura

app = QApplication(sys.argv)
janela = Tabuleiro()
janela.show()
sys.exit(app.exec())