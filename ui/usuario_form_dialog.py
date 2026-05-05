from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFormLayout,
    QGroupBox,
)
from PySide6.QtCore import Qt

from services.control_service import registrar_usuario_con_equipo


class UsuarioFormDialog(QDialog):
    def __init__(self, documento_inicial="", parent=None):
        super().__init__(parent)

        self.documento_registrado = None

        self.setWindowTitle("Registrar usuario y equipo")
        self.resize(600, 430)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        titulo = QLabel("Registrar usuario nuevo")
        titulo.setObjectName("dialogTitle")
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        subtitulo = QLabel("Complete los datos del usuario y del primer equipo.")
        subtitulo.setObjectName("dialogSubtitle")
        subtitulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitulo)

        grupo_usuario = QGroupBox("Datos del usuario")
        grupo_usuario.setObjectName("formGroup")
        usuario_layout = QFormLayout()
        grupo_usuario.setLayout(usuario_layout)

        self.documento_input = QLineEdit()
        self.documento_input.setPlaceholderText("Número de documento")
        self.documento_input.setText(documento_inicial)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")

        self.dependencia_input = QLineEdit()
        self.dependencia_input.setPlaceholderText("Dependencia - opcional")

        usuario_layout.addRow("Documento:", self.documento_input)
        usuario_layout.addRow("Nombre completo:", self.nombre_input)
        usuario_layout.addRow("Dependencia:", self.dependencia_input)

        main_layout.addWidget(grupo_usuario)

        grupo_equipo = QGroupBox("Datos del equipo o elemento")
        grupo_equipo.setObjectName("formGroup")
        equipo_layout = QFormLayout()
        grupo_equipo.setLayout(equipo_layout)

        self.tipo_input = QLineEdit()
        self.tipo_input.setPlaceholderText("Ejemplo: Portátil, Tablet, Respirador")

        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Ejemplo: HP, Lenovo, Samsung")

        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Serial del equipo")

        equipo_layout.addRow("Tipo de equipo:", self.tipo_input)
        equipo_layout.addRow("Marca:", self.marca_input)
        equipo_layout.addRow("Serial:", self.serial_input)

        main_layout.addWidget(grupo_equipo)

        botones_layout = QHBoxLayout()
        botones_layout.addStretch()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setObjectName("successButton")
        self.btn_guardar.setMinimumHeight(38)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("dangerButton")
        self.btn_cancelar.setMinimumHeight(38)
        self.btn_cancelar.clicked.connect(self.reject)

        botones_layout.addWidget(self.btn_guardar)
        botones_layout.addWidget(self.btn_cancelar)

        main_layout.addLayout(botones_layout)

    def guardar(self):
        documento = self.documento_input.text().strip()
        nombre_completo = self.nombre_input.text().strip()
        dependencia = self.dependencia_input.text().strip()
        tipo_elemento = self.tipo_input.text().strip()
        marca = self.marca_input.text().strip()
        serial = self.serial_input.text().strip()

        try:
            registrar_usuario_con_equipo(
                documento=documento,
                nombre_completo=nombre_completo,
                dependencia=dependencia,
                tipo_elemento=tipo_elemento,
                marca=marca,
                serial=serial,
            )

            self.documento_registrado = documento

            QMessageBox.information(
                self,
                "Registro exitoso",
                "El usuario y el equipo fueron registrados correctamente."
            )

            self.accept()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "No se pudo guardar",
                str(error)
            )