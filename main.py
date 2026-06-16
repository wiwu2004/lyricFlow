
import sys
from PyQt6.QtWidgets import QApplication
from ui import JanelaArrastavel

app = QApplication(sys.argv)

janela = JanelaArrastavel()
janela.move(600, 800)
janela.show()

sys.exit(app.exec())
