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
    QHeaderView,
)
from PySide6.QtCore import Qt

from services.control_service import (
    buscar_usuario_con_elementos,
    registrar_ingreso,
    registrar_salida,
    obtener_ultimos_movimientos_elemento,
)

from ui.historial_dialog import HistorialDialog
from ui.usuario_form_dialog import UsuarioFormDialog
from ui.equipo_form_dialog import EquipoFormDialog
from ui.reportes_dialog import ReportesDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.usuario_actual = None

        self.setWindowTitle("Control de ingreso y salida de equipos")
        self.resize(1150, 700)

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
        self.documento_input.returnPressed.connect(self.buscar_usuario)

        self.buscar_button = QPushButton("Buscar")
        self.buscar_button.setObjectName("primaryButton")
        self.buscar_button.setMinimumHeight(38)
        self.buscar_button.clicked.connect(self.buscar_usuario)

        search_layout.addWidget(self.documento_input)
        search_layout.addWidget(self.buscar_button)

        main_layout.addLayout(search_layout)

        self.info_usuario = QLabel("Ingrese un número de documento para consultar.")
        self.info_usuario.setObjectName("userInfo")
        main_layout.addWidget(self.info_usuario)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "Tipo",
            "Marca",
            "Serial",
            "Estado",
            "Último movimiento",
            "Fecha",
            "Acciones",
        ])

        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.cellDoubleClicked.connect(self.mostrar_historial_elemento)

        main_layout.addWidget(self.tabla)

        bottom_layout = QHBoxLayout()

        self.btn_reportes = QPushButton("Reportes")
        self.btn_reportes.setObjectName("secondaryButton")
        self.btn_reportes.setMinimumHeight(42)
        self.btn_reportes.clicked.connect(self.abrir_reportes)

        self.btn_nuevo_elemento = QPushButton("Ingresar nuevo equipo")
        self.btn_nuevo_elemento.setObjectName("primaryButton")
        self.btn_nuevo_elemento.setMinimumHeight(42)
        self.btn_nuevo_elemento.setEnabled(False)
        self.btn_nuevo_elemento.clicked.connect(self.ingresar_nuevo_equipo)

        bottom_layout.addWidget(self.btn_reportes)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_nuevo_elemento)

        main_layout.addLayout(bottom_layout)

    def buscar_usuario(self):
        documento = self.documento_input.text().strip()

        if not documento:
            QMessageBox.warning(
                self,
                "Dato requerido",
                "Digite el número de documento."
            )
            return

        usuario = buscar_usuario_con_elementos(documento)

        if usuario is None:
            self.usuario_actual = None
            self.tabla.setRowCount(0)
            self.btn_nuevo_elemento.setEnabled(False)

            self.info_usuario.setText(
                f"No existe un usuario registrado con documento {documento}."
            )

            respuesta = QMessageBox.question(
                self,
                "Usuario no encontrado",
                "El usuario no existe.\n\n"
                "¿Desea registrar el usuario y su primer equipo?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                self.abrir_formulario_usuario_nuevo(documento)

            return

        self.usuario_actual = usuario

        self.info_usuario.setText(
            f"Usuario: {usuario['nombre_completo']} | "
            f"Documento: {usuario['documento']} | "
            f"Dependencia: {usuario['dependencia']}"
        )

        self.btn_nuevo_elemento.setEnabled(True)
        self.cargar_elementos(usuario["elementos"])

    def cargar_elementos(self, elementos):
        self.tabla.setRowCount(0)

        if not elementos:
            return

        self.tabla.setRowCount(len(elementos))

        for row, elemento in enumerate(elementos):
            tipo_item = QTableWidgetItem(elemento["tipo_elemento"])
            tipo_item.setData(Qt.UserRole, elemento)
            self.tabla.setItem(row, 0, tipo_item)
            self.tabla.setItem(row, 1, QTableWidgetItem(elemento["marca"]))
            self.tabla.setItem(row, 2, QTableWidgetItem(elemento["serial"]))

            estado_item = QTableWidgetItem(elemento["estado_actual"])
            estado_item.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(row, 3, estado_item)

            ultimo_movimiento = elemento["ultimo_movimiento"] or "Sin movimientos"
            fecha = elemento["fecha_ultimo_movimiento"] or "N/A"

            self.tabla.setItem(row, 4, QTableWidgetItem(ultimo_movimiento))
            self.tabla.setItem(row, 5, QTableWidgetItem(fecha))

            acciones_widget = self.crear_botones_accion(elemento)
            self.tabla.setCellWidget(row, 6, acciones_widget)

        self.tabla.resizeRowsToContents()

    def crear_botones_accion(self, elemento):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)
        widget.setLayout(layout)

        btn_ingresar = QPushButton("Ingresar")
        btn_ingresar.setObjectName("successButton")
        btn_ingresar.setMinimumHeight(32)

        btn_salir = QPushButton("Salir")
        btn_salir.setObjectName("dangerButton")
        btn_salir.setMinimumHeight(32)

        estado = elemento["estado_actual"]

        if estado == "FUERA":
            btn_ingresar.setEnabled(True)
            btn_salir.setEnabled(False)
        elif estado == "DENTRO":
            btn_ingresar.setEnabled(False)
            btn_salir.setEnabled(True)
        else:
            btn_ingresar.setEnabled(False)
            btn_salir.setEnabled(False)

        btn_ingresar.clicked.connect(
            lambda checked=False, e=elemento: self.confirmar_ingreso(e)
        )

        btn_salir.clicked.connect(
            lambda checked=False, e=elemento: self.confirmar_salida(e)
        )

        layout.addWidget(btn_ingresar)
        layout.addWidget(btn_salir)

        return widget

    def confirmar_ingreso(self, elemento):
        respuesta = QMessageBox.question(
            self,
            "Confirmar ingreso",
            f"¿Desea registrar el INGRESO del elemento?\n\n"
            f"Tipo: {elemento['tipo_elemento']}\n"
            f"Marca: {elemento['marca']}\n"
            f"Serial: {elemento['serial']}",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return

        try:
            registrar_ingreso(
                elemento_id=elemento["elemento_id"],
                usuario_id=self.usuario_actual["id"],
                observacion="Ingreso registrado desde la aplicación"
            )

            QMessageBox.information(
                self,
                "Ingreso registrado",
                "El ingreso fue registrado correctamente."
            )

            self.refrescar_usuario_actual()

        except ValueError as error:
            QMessageBox.warning(self, "No se pudo registrar el ingreso", str(error))

    def confirmar_salida(self, elemento):
        respuesta = QMessageBox.question(
            self,
            "Confirmar salida",
            f"¿Desea registrar la SALIDA del elemento?\n\n"
            f"Tipo: {elemento['tipo_elemento']}\n"
            f"Marca: {elemento['marca']}\n"
            f"Serial: {elemento['serial']}",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return

        try:
            registrar_salida(
                elemento_id=elemento["elemento_id"],
                usuario_id=self.usuario_actual["id"],
                observacion="Salida registrada desde la aplicación"
            )

            QMessageBox.information(
                self,
                "Salida registrada",
                "La salida fue registrada correctamente."
            )

            self.refrescar_usuario_actual()

        except ValueError as error:
            QMessageBox.warning(self, "No se pudo registrar la salida", str(error))

    def refrescar_usuario_actual(self):
        if self.usuario_actual is None:
            return

        documento = self.usuario_actual["documento"]
        usuario = buscar_usuario_con_elementos(documento)

        if usuario is None:
            self.usuario_actual = None
            self.tabla.setRowCount(0)
            self.btn_nuevo_elemento.setEnabled(False)
            return

        self.usuario_actual = usuario
        self.cargar_elementos(usuario["elementos"])

    def ingresar_nuevo_equipo(self):
        if self.usuario_actual is None:
            QMessageBox.warning(
                self,
                "Usuario requerido",
                "Primero debe buscar un usuario."
            )
            return

        dialog = EquipoFormDialog(
            usuario=self.usuario_actual,
            parent=self
        )

        resultado = dialog.exec()

        if resultado == EquipoFormDialog.Accepted and dialog.equipo_registrado:
            self.refrescar_usuario_actual()

    def mostrar_historial_elemento(self, row, column):
        item = self.tabla.item(row, 0)

        if item is None:
            return

        elemento = item.data(Qt.UserRole)

        if elemento is None:
            return

        movimientos = obtener_ultimos_movimientos_elemento(
            elemento_id=elemento["elemento_id"],
            limite=10
        )

        dialog = HistorialDialog(
            elemento=elemento,
            movimientos=movimientos,
            parent=self
        )
        dialog.exec()


    def abrir_formulario_usuario_nuevo(self, documento):
        dialog = UsuarioFormDialog(
            documento_inicial=documento,
            parent=self
        )

        resultado = dialog.exec()

        if resultado == UsuarioFormDialog.Accepted:
            documento_registrado = dialog.documento_registrado

            if documento_registrado:
                self.documento_input.setText(documento_registrado)
                self.buscar_usuario()

    def abrir_reportes(self):
        dialog = ReportesDialog(parent=self)
        dialog.exec()