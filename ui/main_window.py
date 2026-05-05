from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control de ingreso y salida de equipos")
        self.resize(1000, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        title = QLabel("Control de ingreso y salida de equipos")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        search_layout = QHBoxLayout()

        self.documento_input = QLineEdit()
        self.documento_input.setPlaceholderText("Digite número de documento")
        self.documento_input.setMinimumHeight(38)

        self.buscar_button = QPushButton("Buscar")
        self.buscar_button.setMinimumHeight(38)
        self.buscar_button.clicked.connect(self.buscar_usuario)

        search_layout.addWidget(self.documento_input)
        search_layout.addWidget(self.buscar_button)

        main_layout.addLayout(search_layout)

        self.info_usuario = QLabel("Ingrese un número de documento para consultar.")
        self.info_usuario.setObjectName("userInfo")
        main_layout.addWidget(self.info_usuario)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Tipo",
            "Marca",
            "Serial",
            "Estado",
            "Último movimiento",
            "Fecha"
        ])
        main_layout.addWidget(self.tabla)

        buttons_layout = QHBoxLayout()

        self.btn_ingreso = QPushButton("Registrar ingreso")
        self.btn_salida = QPushButton("Registrar salida")
        self.btn_nuevo_elemento = QPushButton("Agregar nuevo elemento")
        self.btn_usuario = QPushButton("Registrar usuario")

        buttons_layout.addWidget(self.btn_ingreso)
        buttons_layout.addWidget(self.btn_salida)
        buttons_layout.addWidget(self.btn_nuevo_elemento)
        buttons_layout.addWidget(self.btn_usuario)

        main_layout.addLayout(buttons_layout)

    def buscar_usuario(self):
        documento = self.documento_input.text().strip()

        if not documento:
            QMessageBox.warning(
                self,
                "Dato requerido",
                "Digite el número de documento."
            )
            return

        # Por ahora solo probamos la pantalla.
        # Después conectamos esta acción con SQLite.
        self.info_usuario.setText(
            f"Buscando información para el documento: {documento}"
        )