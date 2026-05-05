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

from services.control_service import registrar_equipo_a_usuario


class EquipoFormDialog(QDialog):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)

        self.usuario = usuario
        self.equipo_registrado = False

        self.setWindowTitle("Ingresar nuevo equipo")
        self.resize(560, 340)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        titulo = QLabel("Ingresar nuevo equipo")
        titulo.setObjectName("dialogTitle")
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        usuario_label = QLabel(
            f"Usuario: {usuario['nombre_completo']} | "
            f"Documento: {usuario['documento']}"
        )
        usuario_label.setObjectName("dialogSubtitle")
        usuario_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(usuario_label)

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

        nota = QLabel(
            "Nota: el equipo quedará registrado automáticamente como DENTRO."
        )
        nota.setObjectName("dialogNote")
        nota.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(nota)

        botones_layout = QHBoxLayout()
        botones_layout.addStretch()

        self.btn_guardar = QPushButton("Guardar equipo")
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
        tipo_elemento = self.tipo_input.text().strip()
        marca = self.marca_input.text().strip()
        serial = self.serial_input.text().strip()

        try:
            registrar_equipo_a_usuario(
                usuario_id=self.usuario["id"],
                tipo_elemento=tipo_elemento,
                marca=marca,
                serial=serial,
            )

            self.equipo_registrado = True

            QMessageBox.information(
                self,
                "Equipo registrado",
                "El nuevo equipo fue registrado correctamente."
            )

            self.accept()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "No se pudo guardar",
                str(error)
            )