from database.connection import get_connection


def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento TEXT NOT NULL UNIQUE,
            nombre_completo TEXT NOT NULL,
            dependencia TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS elementos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tipo_elemento TEXT NOT NULL,
            marca TEXT NOT NULL,
            serial TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            estado_actual TEXT NOT NULL CHECK(estado_actual IN ('DENTRO', 'FUERA')),
            fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            elemento_id INTEGER NOT NULL,
            tipo_movimiento TEXT NOT NULL CHECK(tipo_movimiento IN ('INGRESO', 'SALIDA')),
            fecha_movimiento TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            observacion TEXT,

            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (elemento_id) REFERENCES elementos(id)
        );
        """)

        conn.commit()