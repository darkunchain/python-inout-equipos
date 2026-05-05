from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PySide6.QtCore import Qt

from services.control_service import (
    obtener_equipos_que_salieron_hoy,
    obtener_equipos_que_entraron_hoy,
)


class ReportesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Reportes")
        self.resize(1050, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        titulo = QLabel("Módulo de reportes")
        titulo.setObjectName("dialogTitle")
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        subtitulo = QLabel("Seleccione un reporte para visualizar la información.")
        subtitulo.setObjectName("dialogSubtitle")
        subtitulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitulo)

        botones_layout = QHBoxLayout()

        self.btn_salieron_hoy = QPushButton("Equipos que salieron hoy")
        self.btn_salieron_hoy.setObjectName("dangerButton")
        self.btn_salieron_hoy.setMinimumHeight(40)
        self.btn_salieron_hoy.clicked.connect(self.cargar_salidas_hoy)

        self.btn_entraron_hoy = QPushButton("Equipos que entraron hoy")
        self.btn_entraron_hoy.setObjectName("successButton")
        self.btn_entraron_hoy.setMinimumHeight(40)
        self.btn_entraron_hoy.clicked.connect(self.cargar_entradas_hoy)

        botones_layout.addWidget(self.btn_salieron_hoy)
        botones_layout.addWidget(self.btn_entraron_hoy)

        main_layout.addLayout(botones_layout)

        self.titulo_reporte = QLabel("Seleccione un reporte.")
        self.titulo_reporte.setObjectName("reportTitle")
        self.titulo_reporte.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.titulo_reporte)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "Equipo",
            "Marca",
            "Serial",
            "Usuario",
            "Documento",
            "Dependencia",
            "Fecha y hora",
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setAlternatingRowColors(True)

        main_layout.addWidget(self.tabla)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.setObjectName("dangerButton")
        self.btn_cerrar.setMinimumHeight(38)
        self.btn_cerrar.clicked.connect(self.close)

        bottom_layout.addWidget(self.btn_cerrar)
        main_layout.addLayout(bottom_layout)

    def cargar_salidas_hoy(self):
        datos = obtener_equipos_que_salieron_hoy()
        self.titulo_reporte.setText("Equipos que salieron hoy")
        self.cargar_tabla(datos)

    def cargar_entradas_hoy(self):
        datos = obtener_equipos_que_entraron_hoy()
        self.titulo_reporte.setText("Equipos que entraron hoy")
        self.cargar_tabla(datos)

    def cargar_tabla(self, datos):
        self.tabla.setRowCount(0)

        if not datos:
            QMessageBox.information(
                self,
                "Sin datos",
                "No se encontraron registros para este reporte."
            )
            return

        self.tabla.setRowCount(len(datos))

        for row, item in enumerate(datos):
            equipo = QTableWidgetItem(item["tipo_elemento"])
            marca = QTableWidgetItem(item["marca"])
            serial = QTableWidgetItem(item["serial"])
            usuario = QTableWidgetItem(item["nombre_completo"])
            documento = QTableWidgetItem(item["documento"])
            dependencia = QTableWidgetItem(item["dependencia"])
            fecha = QTableWidgetItem(item["fecha_movimiento"])

            equipo.setTextAlignment(Qt.AlignCenter)
            marca.setTextAlignment(Qt.AlignCenter)
            serial.setTextAlignment(Qt.AlignCenter)
            documento.setTextAlignment(Qt.AlignCenter)
            fecha.setTextAlignment(Qt.AlignCenter)

            self.tabla.setItem(row, 0, equipo)
            self.tabla.setItem(row, 1, marca)
            self.tabla.setItem(row, 2, serial)
            self.tabla.setItem(row, 3, usuario)
            self.tabla.setItem(row, 4, documento)
            self.tabla.setItem(row, 5, dependencia)
            self.tabla.setItem(row, 6, fecha)

        self.tabla.resizeRowsToContents()