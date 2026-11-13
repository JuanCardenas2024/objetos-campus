from app.db.mariadb import get_connection

SEDES = [
    # Bogotá D.C.
    ("Bogotá D.C.", "Sede Principal Bogotá"),
    ("Bogotá D.C.", "Centro Usaquén"),
    ("Bogotá D.C.", "Centro Engativá"),
    ("Bogotá D.C.", "Centro Kennedy"),
    ("Bogotá D.C.", "Centro Ciudad Bolívar"),
    ("Bogotá D.C.", "Centro Santa Fe"),
    # Cundinamarca
    ("Cundinamarca", "Centro Regional Girardot"),
    ("Cundinamarca", "Centro Regional Madrid"),
    ("Cundinamarca", "Centro Regional Soacha"),
    ("Cundinamarca", "Centro Regional Zipaquirá"),
    # Valle del Cauca
    ("Valle del Cauca", "Sede Cali"),
    ("Valle del Cauca", "Sede Buga"),
    ("Valle del Cauca", "Sede Buenaventura"),
    # Otros departamentos
    ("Nariño", "Sede Pasto"),
    ("Risaralda", "Sede Pereira"),
    ("Bolívar", "Sede Cartagena"),
    ("Norte de Santander", "Centro Universitario Ocaña"),
    # Agregar aquí el resto de sedes y centros oficiales
]


def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for departamento, nombre in SEDES:
                cur.execute(
                    """INSERT INTO sedes (nombre, departamento) VALUES (%s, %s)
                       ON DUPLICATE KEY UPDATE departamento = VALUES(departamento)""",
                    (nombre, departamento),
                )
        print(f"{len(SEDES)} sedes cargadas.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()