
import time
import threading
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import Qt, QPoint, QTimer
from lrc_service import calcular_estado, buscar_lrc_api
from spotify_service import get_musica_atual


class JanelaArrastavel(QWidget):
    def __init__(self):
        super().__init__()
        self._arrastando = False
        self._offset = QPoint()

        self.linhas = []
        self.indice_atual = 0
        self.musica_atual = None
        self.carregando = False

        
        self.tempo_spotify = 0
        self.tempo_local = 0
        self.contador_sync = 0

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
        """)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.resize(900, 150)
        self.label.resize(900, 150)

        self._mostrar_carregando()

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.atualizar)
        self.timer.start()

    def _mostrar_carregando(self):
        self.label.setText('<span style="color:gray; font-size:20px">Identificando música...</span>')

    def _buscar_lrc_async(self, artista, nome, identificador):
        linhas = buscar_lrc_api(artista, nome)
        # só aplica se a música não mudou enquanto carregava
        if self.musica_atual == identificador:
            self.linhas = linhas
            self.indice_atual = 0
            self.carregando = False

    def atualizar(self):
        self.contador_sync += 1

        if self.contador_sync >= 40 or self.musica_atual is None:
            self.contador_sync = 0
            musica = get_musica_atual()

            if not musica:
                self._mostrar_carregando()
                return

            identificador = f"{musica['nome']} - {musica['artista']}"

            if identificador != self.musica_atual:
                print(f"Nova música detectada: {identificador}")
                self.musica_atual = identificador
                self.linhas = []
                self.indice_atual = 0
                self.carregando = True
                self._mostrar_carregando()

                # busca o LRC em thread separada para não travar a UI
                t = threading.Thread(
                    target=self._buscar_lrc_async,
                    args=(musica["artista"], musica["nome"], identificador),
                    daemon=True
                )
                t.start()

            self.tempo_spotify = musica["tempo"]
            self.tempo_local = time.time()

        if not self.musica_atual or self.carregando or not self.linhas:
            return

        tempo_atual = self.tempo_spotify + (time.time() - self.tempo_local)

        while (self.indice_atual + 1 < len(self.linhas) and
               self.linhas[self.indice_atual + 1][0] <= tempo_atual):
            self.indice_atual += 1

        self.indice_atual, passada, futura, proxima = calcular_estado(
            self.linhas, self.indice_atual, tempo_atual
        )

        self.label.setText(
            f'<span style="color:white">{passada}</span>'
            f'<span style="color:gray">{futura}</span>'
            f'<br><span style="color:gray; font-size:18px">{proxima}</span>'
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._arrastando = True
            self._offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._arrastando:
            self.move(event.globalPosition().toPoint() - self._offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._arrastando = False
