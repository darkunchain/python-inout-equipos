from pathlib import Path
import sys


# Permite importar módulos del proyecto cuando se ejecuta desde /scripts
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))


from database.connection import get_connection
from database.schema import create_tables, drop_tables
from utils.time_utils import ahora_bogota


USUARIOS = [
    {
        "documento": "1001001001",
        "nombre_completo": "Carlos Andrés Ramírez",
        "dependencia": "Tecnología",
    },
    {
        "documento": "1001001002",
        "nombre_completo": "María Fernanda Gómez",
        "dependencia": "Talento Humano",
    },
    {
        "documento": "1001001003",
        "nombre_completo": "Julián Esteban Torres",
        "dependencia": "Financiera",
    },
    {
        "documento": "1001001004",
        "nombre_completo": "Laura Marcela Rojas",
        "dependencia": "Jurídica",
    },
    {
        "documento": "1001001005",
        "nombre_completo": "Andrés Felipe Cárdenas",
        "dependencia": "Administrativa",
    },
    {
        "documento": "1001001006",
        "nombre_completo": "Diana Carolina Vargas",
        "dependencia": "Planeación",
    },
    {
        "documento": "1001001007",
        "nombre_completo": "Santiago Mejía López",
        "dependencia": "Comunicaciones",
    },
    {
        "documento": "1001001008",
        "nombre_completo": "Paola Andrea Castro",
        "dependencia": "Contratación",
    },
    {
        "documento": "1001001009",
        "nombre_completo": "Miguel Ángel Herrera",
        "dependencia": "Archivo",
    },
    {
        "documento": "1001001010",
        "nombre_completo": "Natalia Fernanda Peña",
        "dependencia": "Atención al Ciudadano",
    },
]


ELEMENTOS = [
    # 14 portátiles
    {
        "documento_usuario": "1001001001",
        "tipo_elemento": "Portátil",
        "marca": "HP",
        "serial": "HP-LT-0001",
        "descripcion": "Portátil HP ProBook 440",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001001",
        "tipo_elemento": "Portátil",
        "marca": "Lenovo",
        "serial": "LEN-LT-0002",
        "descripcion": "Portátil Lenovo ThinkPad E14",
        "estado_actual": "FUERA",
    },
    {
        "documento_usuario": "1001001002",
        "tipo_elemento": "Portátil",
        "marca": "HP",
        "serial": "HP-LT-0003",
        "descripcion": "Portátil HP EliteBook",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001002",
        "tipo_elemento": "Portátil",
        "marca": "Mac",
        "serial": "MAC-LT-0004",
        "descripcion": "MacBook Air M1",
        "estado_actual": "FUERA",
    },
    {
        "documento_usuario": "1001001003",
        "tipo_elemento": "Portátil",
        "marca": "Lenovo",
        "serial": "LEN-LT-0005",
        "descripcion": "Portátil Lenovo ThinkPad T14",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001003",
        "tipo_elemento": "Portátil",
        "marca": "HP",
        "serial": "HP-LT-0006",
        "descripcion": "Portátil HP 240 G8",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001004",
        "tipo_elemento": "Portátil",
        "marca": "Mac",
        "serial": "MAC-LT-0007",
        "descripcion": "MacBook Pro 13",
        "estado_actual": "FUERA",
    },
    {
        "documento_usuario": "1001001005",
        "tipo_elemento": "Portátil",
        "marca": "Lenovo",
        "serial": "LEN-LT-0008",
        "descripcion": "Portátil Lenovo IdeaPad",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001005",
        "tipo_elemento": "Portátil",
        "marca": "HP",
        "serial": "HP-LT-0009",
        "descripcion": "Portátil HP Pavilion",
        "estado_actual": "FUERA",
    },
    {
        "documento_usuario": "1001001006",
        "tipo_elemento": "Portátil",
        "marca": "Lenovo",
        "serial": "LEN-LT-0010",
        "descripcion": "Portátil Lenovo V14",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001007",
        "tipo_elemento": "Portátil",
        "marca": "Mac",
        "serial": "MAC-LT-0011",
        "descripcion": "MacBook Air M2",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001008",
        "tipo_elemento": "Portátil",
        "marca": "HP",
        "serial": "HP-LT-0012",
        "descripcion": "Portátil HP ProBook 450",
        "estado_actual": "FUERA",
    },
    {
        "documento_usuario": "1001001009",
        "tipo_elemento": "Portátil",
        "marca": "Lenovo",
        "serial": "LEN-LT-0013",
        "descripcion": "Portátil Lenovo ThinkBook",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001010",
        "tipo_elemento": "Portátil",
        "marca": "HP",
        "serial": "HP-LT-0014",
        "descripcion": "Portátil HP 245 G9",
        "estado_actual": "DENTRO",
    },

    # 5 tablets
    {
        "documento_usuario": "1001001004",
        "tipo_elemento": "Tablet",
        "marca": "Samsung",
        "serial": "SAM-TB-0015",
        "descripcion": "Tablet Samsung Galaxy Tab A",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001006",
        "tipo_elemento": "Tablet",
        "marca": "iPad",
        "serial": "IPAD-TB-0016",
        "descripcion": "Apple iPad 9 generación",
        "estado_actual": "FUERA",
    },
    {
        "documento_usuario": "1001001007",
        "tipo_elemento": "Tablet",
        "marca": "Samsung",
        "serial": "SAM-TB-0017",
        "descripcion": "Tablet Samsung Galaxy Tab S6",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001008",
        "tipo_elemento": "Tablet",
        "marca": "iPad",
        "serial": "IPAD-TB-0018",
        "descripcion": "Apple iPad Mini",
        "estado_actual": "DENTRO",
    },
    {
        "documento_usuario": "1001001009",
        "tipo_elemento": "Tablet",
        "marca": "Samsung",
        "serial": "SAM-TB-0019",
        "descripcion": "Tablet Samsung Galaxy Tab S7",
        "estado_actual": "FUERA",
    },

    # 1 respirador
    {
        "documento_usuario": "1001001010",
        "tipo_elemento": "Respirador",
        "marca": "Philips",
        "serial": "RESP-0020",
        "descripcion": "Respirador portátil médico",
        "estado_actual": "DENTRO",
    },
]


def insertar_usuarios():
    with get_connection() as conn:
        cursor = conn.cursor()

        for usuario in USUARIOS:
            cursor.execute("""
                INSERT INTO usuarios (
                    documento,
                    nombre_completo,
                    dependencia
                )
                VALUES (?, ?, ?);
            """, (
                usuario["documento"],
                usuario["nombre_completo"],
                usuario["dependencia"],
            ))

        conn.commit()


def obtener_usuario_id_por_documento(documento):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE documento = ?;
        """, (documento,))

        usuario = cursor.fetchone()

        if usuario is None:
            raise ValueError(f"No existe usuario con documento {documento}")

        return usuario["id"]


def insertar_elementos_y_movimientos():
    with get_connection() as conn:
        cursor = conn.cursor()

        for elemento in ELEMENTOS:
            usuario_id = obtener_usuario_id_por_documento(
                elemento["documento_usuario"]
            )

            cursor.execute("""
                INSERT INTO elementos (
                    usuario_id,
                    tipo_elemento,
                    marca,
                    serial,
                    descripcion,
                    estado_actual
                )
                VALUES (?, ?, ?, ?, ?, ?);
            """, (
                usuario_id,
                elemento["tipo_elemento"],
                elemento["marca"],
                elemento["serial"],
                elemento["descripcion"],
                elemento["estado_actual"],
            ))

            elemento_id = cursor.lastrowid

            # Todo elemento inicia con un INGRESO.
            cursor.execute("""
                INSERT INTO movimientos (
                    usuario_id,
                    elemento_id,
                    tipo_movimiento,
                    fecha_movimiento,
                    observacion
                )
                VALUES (?, ?, 'INGRESO', ?, ?);
            """, (
                usuario_id,
                elemento_id,
                ahora_bogota(),
                "Movimiento inicial de prueba",
            ))

            # Si el estado final del elemento es FUERA,
            # agregamos también una SALIDA.
            if elemento["estado_actual"] == "FUERA":
                cursor.execute("""
                    INSERT INTO movimientos (
                        usuario_id,
                        elemento_id,
                        tipo_movimiento,
                        fecha_movimiento,
                        observacion
                    )
                    VALUES (?, ?, 'SALIDA', ?, ?);
                """, (
                    usuario_id,
                    elemento_id,
                    ahora_bogota(),
                    "Salida inicial de prueba",
                ))

        conn.commit()


def mostrar_resumen():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS total FROM usuarios;")
        total_usuarios = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM elementos;")
        total_elementos = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT tipo_elemento, COUNT(*) AS total
            FROM elementos
            GROUP BY tipo_elemento
            ORDER BY tipo_elemento;
        """)
        resumen_tipos = cursor.fetchall()

        cursor.execute("""
            SELECT estado_actual, COUNT(*) AS total
            FROM elementos
            GROUP BY estado_actual
            ORDER BY estado_actual;
        """)
        resumen_estados = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS total FROM movimientos;")
        total_movimientos = cursor.fetchone()["total"]

    print("\nBase de datos creada correctamente.")
    print("----------------------------------")
    print(f"Usuarios creados: {total_usuarios}")
    print(f"Elementos creados: {total_elementos}")
    print(f"Movimientos creados: {total_movimientos}")

    print("\nElementos por tipo:")
    for row in resumen_tipos:
        print(f"- {row['tipo_elemento']}: {row['total']}")

    print("\nElementos por estado:")
    for row in resumen_estados:
        print(f"- {row['estado_actual']}: {row['total']}")

    print()


def seed_database():
    print("Reiniciando base de datos de pruebas...")

    drop_tables()
    create_tables()
    insertar_usuarios()
    insertar_elementos_y_movimientos()
    mostrar_resumen()


if __name__ == "__main__":
    seed_database()