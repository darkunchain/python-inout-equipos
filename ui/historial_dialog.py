from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
    QHBoxLayout,
)
from PySide6.QtCore import Qt


class HistorialDialog(QDialog):
    def __init__(self, elemento, movimientos, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Historial de movimientos")
        self.resize(650, 420)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Últimos 10 movimientos")
        titulo.setObjectName("dialogTitle")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        detalle = QLabel(
            f"{elemento['tipo_elemento']} | "
            f"{elemento['marca']} | "
            f"Serial: {elemento['serial']}"
        )
        detalle.setObjectName("dialogSubtitle")
        detalle.setAlignment(Qt.AlignCenter)
        layout.addWidget(detalle)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels([
            "Movimiento",
            "Fecha",
            "Observación",
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setAlternatingRowColors(True)

        layout.addWidget(self.tabla)

        self.cargar_movimientos(movimientos)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.setObjectName("dangerButton")
        self.btn_cerrar.setMinimumHeight(38)
        self.btn_cerrar.clicked.connect(self.close)

        buttons_layout.addWidget(self.btn_cerrar)
        layout.addLayout(buttons_layout)

    def cargar_movimientos(self, movimientos):
        self.tabla.setRowCount(0)

        if not movimientos:
            return

        self.tabla.setRowCount(len(movimientos))

        for row, movimiento in enumerate(movimientos):
            tipo = movimiento["tipo_movimiento"]

            if tipo == "INGRESO":
                texto_movimiento = "Entrada"
            elif tipo == "SALIDA":
                texto_movimiento = "Salida"
            else:
                texto_movimiento = tipo

            item_movimiento = QTableWidgetItem(texto_movimiento)
            item_movimiento.setTextAlignment(Qt.AlignCenter)

            item_fecha = QTableWidgetItem(movimiento["fecha_movimiento"])
            item_fecha.setTextAlignment(Qt.AlignCenter)

            observacion = movimiento["observacion"] or ""
            item_observacion = QTableWidgetItem(observacion)

            self.tabla.setItem(row, 0, item_movimiento)
            self.tabla.setItem(row, 1, item_fecha)
            self.tabla.setItem(row, 2, item_observacion)

        self.tabla.resizeRowsToContents()