from database.connection import get_connection


def buscar_usuario_con_elementos(documento: str):
    """
    Busca un usuario por documento y retorna sus datos con los elementos asociados.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                documento,
                nombre_completo,
                dependencia
            FROM usuarios
            WHERE documento = ?;
        """, (documento,))

        usuario = cursor.fetchone()

        if usuario is None:
            return None

        cursor.execute("""
            SELECT
                e.id AS elemento_id,
                e.tipo_elemento,
                e.marca,
                e.serial,
                e.descripcion,
                e.estado_actual,
                m.tipo_movimiento AS ultimo_movimiento,
                m.fecha_movimiento AS fecha_ultimo_movimiento
            FROM elementos e
            LEFT JOIN movimientos m
                ON m.id = (
                    SELECT id
                    FROM movimientos
                    WHERE elemento_id = e.id
                    ORDER BY fecha_movimiento DESC, id DESC
                    LIMIT 1
                )
            WHERE e.usuario_id = ?
            ORDER BY e.tipo_elemento, e.marca, e.serial;
        """, (usuario["id"],))

        elementos = cursor.fetchall()

        return {
            "id": usuario["id"],
            "documento": usuario["documento"],
            "nombre_completo": usuario["nombre_completo"],
            "dependencia": usuario["dependencia"],
            "elementos": [dict(elemento) for elemento in elementos],
        }


def registrar_ingreso(elemento_id: int, usuario_id: int, observacion: str = ""):
    """
    Registra ingreso de un elemento.
    Solo permite ingreso si el elemento está FUERA.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                usuario_id,
                estado_actual
            FROM elementos
            WHERE id = ?;
        """, (elemento_id,))

        elemento = cursor.fetchone()

        if elemento is None:
            raise ValueError("El elemento no existe.")

        if elemento["usuario_id"] != usuario_id:
            raise ValueError("Este elemento no pertenece al usuario consultado.")

        if elemento["estado_actual"] != "FUERA":
            raise ValueError("El elemento no puede ingresar porque no se encuentra registrado como FUERA.")

        cursor.execute("""
            INSERT INTO movimientos (
                usuario_id,
                elemento_id,
                tipo_movimiento,
                observacion
            )
            VALUES (?, ?, 'INGRESO', ?);
        """, (usuario_id, elemento_id, observacion))

        cursor.execute("""
            UPDATE elementos
            SET estado_actual = 'DENTRO'
            WHERE id = ?;
        """, (elemento_id,))

        conn.commit()


def registrar_salida(elemento_id: int, usuario_id: int, observacion: str = ""):
    """
    Registra salida de un elemento.
    Solo permite salida si el elemento está DENTRO.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                usuario_id,
                estado_actual
            FROM elementos
            WHERE id = ?;
        """, (elemento_id,))

        elemento = cursor.fetchone()

        if elemento is None:
            raise ValueError("El elemento no existe.")

        if elemento["usuario_id"] != usuario_id:
            raise ValueError("Este elemento no pertenece al usuario consultado.")

        if elemento["estado_actual"] != "DENTRO":
            raise ValueError("El elemento no puede salir porque no se encuentra registrado como DENTRO.")

        cursor.execute("""
            INSERT INTO movimientos (
                usuario_id,
                elemento_id,
                tipo_movimiento,
                observacion
            )
            VALUES (?, ?, 'SALIDA', ?);
        """, (usuario_id, elemento_id, observacion))

        cursor.execute("""
            UPDATE elementos
            SET estado_actual = 'FUERA'
            WHERE id = ?;
        """, (elemento_id,))

        conn.commit()


def obtener_ultimos_movimientos_elemento(elemento_id: int, limite: int = 10):
    """
    Retorna los últimos movimientos de un elemento.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                m.tipo_movimiento,
                m.fecha_movimiento,
                m.observacion
            FROM movimientos m
            WHERE m.elemento_id = ?
            ORDER BY m.fecha_movimiento DESC, m.id DESC
            LIMIT ?;
        """, (elemento_id, limite))

        movimientos = cursor.fetchall()

        return [dict(movimiento) for movimiento in movimientos]
    

def registrar_usuario_con_equipo(
    documento: str,
    nombre_completo: str,
    dependencia: str,
    tipo_elemento: str,
    marca: str,
    serial: str,
):
    """
    Registra un usuario nuevo junto con su primer equipo.
    El equipo queda automáticamente en estado DENTRO
    y se registra su primer movimiento como INGRESO.
    """

    documento = documento.strip()
    nombre_completo = nombre_completo.strip()
    dependencia = dependencia.strip()
    tipo_elemento = tipo_elemento.strip()
    marca = marca.strip()
    serial = serial.strip()

    if not documento:
        raise ValueError("El documento de identidad es obligatorio.")

    if not nombre_completo:
        raise ValueError("El nombre completo es obligatorio.")

    if not tipo_elemento:
        raise ValueError("El tipo de equipo o elemento es obligatorio.")

    if not marca:
        raise ValueError("La marca del equipo es obligatoria.")

    if not serial:
        raise ValueError("El serial del equipo es obligatorio.")

    if not dependencia:
        dependencia = "Sin información de dependencia"

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE documento = ?;
        """, (documento,))

        usuario_existente = cursor.fetchone()

        if usuario_existente is not None:
            raise ValueError("Ya existe un usuario registrado con este documento.")

        cursor.execute("""
            SELECT id
            FROM elementos
            WHERE serial = ?;
        """, (serial,))

        serial_existente = cursor.fetchone()

        if serial_existente is not None:
            raise ValueError("Ya existe un equipo registrado con este serial.")

        cursor.execute("""
            INSERT INTO usuarios (
                documento,
                nombre_completo,
                dependencia
            )
            VALUES (?, ?, ?);
        """, (
            documento,
            nombre_completo,
            dependencia,
        ))

        usuario_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO elementos (
                usuario_id,
                tipo_elemento,
                marca,
                serial,
                descripcion,
                estado_actual
            )
            VALUES (?, ?, ?, ?, ?, 'DENTRO');
        """, (
            usuario_id,
            tipo_elemento,
            marca,
            serial,
            "Equipo registrado junto con usuario nuevo",
        ))

        elemento_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO movimientos (
                usuario_id,
                elemento_id,
                tipo_movimiento,
                observacion
            )
            VALUES (?, ?, 'INGRESO', ?);
        """, (
            usuario_id,
            elemento_id,
            "Ingreso inicial al registrar usuario nuevo",
        ))

        conn.commit()

        return usuario_id