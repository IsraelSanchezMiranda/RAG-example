"""Genera db/02_datos.sql con datos ficticios y reproducibles (semilla fija).

Uso:  python datos/generar_datos.py
Todos los nombres, RFC, correos y teléfonos son inventados.
"""
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2026)

SUCURSALES = [("Sucursal León", "León"), ("Sucursal Querétaro", "Querétaro"),
              ("Sucursal Aguascalientes", "Aguascalientes"), ("Sucursal Irapuato", "Irapuato")]

PROVEEDORES = [
    ("Aceros y Tornillería Valquiria", "AVT120304AB1", "León", "Ramiro Ibarra"),
    ("Pinturas Arcoíris del Centro", "PAC110815CD2", "Querétaro", "Lucía Montes"),
    ("Eléctrica Fénix Industrial", "EFI090212EF3", "Guadalajara", "Octavio Zárate"),
    ("Hidráulica Manantial", "HMA100630GH4", "Irapuato", "Berenice Cuevas"),
    ("Herramientas Titán", "HTI130118IJ5", "Celaya", "Gustavo Peña"),
    ("Maderas y Tableros El Roble", "MTR080925KL6", "Aguascalientes", "Dolores Quiroz"),
]

# (sku, nombre, categoria, indice_proveedor, precio, costo)
PRODUCTOS = [
    ("TOR-001", "Tornillo hexagonal 1/4 x 1 pulg (caja 100)", "Tornillería", 0, 85, 52),
    ("TOR-002", "Tornillo hexagonal 3/8 x 2 pulg (caja 100)", "Tornillería", 0, 140, 88),
    ("TOR-003", "Tuerca hexagonal 1/4 (caja 100)", "Tornillería", 0, 60, 35),
    ("TOR-004", "Rondana plana 1/4 (caja 200)", "Tornillería", 0, 48, 27),
    ("TOR-005", "Pija para madera 8 x 1-1/2 (caja 100)", "Tornillería", 0, 72, 41),
    ("TOR-006", "Varilla roscada 3/8 x 1 m", "Tornillería", 0, 95, 60),
    ("TOR-007", "Ancla expansiva 3/8 (caja 25)", "Tornillería", 0, 130, 82),
    ("TOR-008", "Perno de carro 5/16 x 3 (caja 50)", "Tornillería", 0, 110, 68),
    ("PIN-001", "Pintura vinílica blanca 19 L", "Pinturas", 1, 1250, 820),
    ("PIN-002", "Pintura vinílica blanca 4 L", "Pinturas", 1, 340, 215),
    ("PIN-003", "Esmalte negro mate 1 L", "Pinturas", 1, 210, 130),
    ("PIN-004", "Impermeabilizante rojo 19 L", "Pinturas", 1, 1480, 990),
    ("PIN-005", "Thinner estándar 4 L", "Pinturas", 1, 160, 98),
    ("PIN-006", "Sellador acrílico 19 L", "Pinturas", 1, 980, 640),
    ("PIN-007", "Brocha de cerda 4 pulg", "Pinturas", 1, 55, 28),
    ("PIN-008", "Rodillo de felpa 9 pulg", "Pinturas", 1, 65, 34),
    ("ELE-001", "Cable THW calibre 12 (rollo 100 m)", "Eléctrico", 2, 980, 690),
    ("ELE-002", "Cable THW calibre 14 (rollo 100 m)", "Eléctrico", 2, 720, 500),
    ("ELE-003", "Interruptor sencillo", "Eléctrico", 2, 38, 20),
    ("ELE-004", "Contacto doble polarizado", "Eléctrico", 2, 45, 24),
    ("ELE-005", "Pastilla termomagnética 20 A", "Eléctrico", 2, 120, 72),
    ("ELE-006", "Cinta aislante negra (pieza)", "Eléctrico", 2, 22, 11),
    ("ELE-007", "Foco LED 9 W (caja 10)", "Eléctrico", 2, 260, 165),
    ("HID-001", "Tubo PVC hidráulico 1/2 pulg x 6 m", "Plomería", 3, 78, 48),
    ("HID-002", "Tubo PVC hidráulico 3/4 pulg x 6 m", "Plomería", 3, 112, 70),
    ("HID-003", "Codo PVC 1/2 pulg (bolsa 20)", "Plomería", 3, 90, 54),
    ("HID-004", "Válvula de esfera 1/2 pulg", "Plomería", 3, 95, 58),
    ("HID-005", "Llave mezcladora para lavabo", "Plomería", 3, 420, 270),
    ("HID-006", "Tinaco 1100 L", "Plomería", 3, 2350, 1650),
    ("HID-007", "Cinta teflón (caja 20)", "Plomería", 3, 80, 45),
    ("HID-008", "Bomba periférica 1/2 HP", "Plomería", 3, 1280, 890),
    ("HER-001", "Martillo de uña 16 oz", "Herramientas", 4, 160, 98),
    ("HER-002", "Juego de desarmadores (6 piezas)", "Herramientas", 4, 190, 115),
    ("HER-003", "Taladro percutor 1/2 pulg", "Herramientas", 4, 1450, 980),
    ("HER-004", "Disco de corte para metal 4-1/2 pulg", "Herramientas", 4, 28, 14),
    ("HER-005", "Flexómetro 5 m", "Herramientas", 4, 75, 40),
    ("HER-006", "Nivel de burbuja 24 pulg", "Herramientas", 4, 130, 78),
    ("HER-007", "Guantes de carnaza (par)", "Herramientas", 4, 55, 30),
    ("MAD-001", "Triplay de pino 12 mm (hoja)", "Maderas", 5, 560, 380),
    ("MAD-002", "Triplay de pino 6 mm (hoja)", "Maderas", 5, 340, 225),
    ("MAD-003", "Tablero MDF 15 mm (hoja)", "Maderas", 5, 610, 420),
    ("MAD-004", "Polín de pino 2x4 x 2.44 m", "Maderas", 5, 135, 85),
    ("MAD-005", "Barrote de pino 1x2 x 2.44 m", "Maderas", 5, 48, 28),
    ("MAD-006", "Duela de pino (m²)", "Maderas", 5, 310, 205),
]

NOMBRES = ["Alejandro", "María", "José", "Guadalupe", "Luis", "Fernanda", "Carlos", "Daniela",
           "Miguel", "Paola", "Jorge", "Ximena", "Ricardo", "Valeria", "Héctor", "Andrea"]
APELLIDOS = ["Hernández", "García", "Martínez", "López", "Ramírez", "Torres", "Flores", "Vargas",
             "Mendoza", "Cortés", "Salazar", "Ortega", "Navarro", "Rangel", "Aguilar", "Luna"]
EMPRESAS = ["Constructora", "Ferretería", "Remodelaciones", "Casas", "Inmobiliaria", "Instalaciones",
            "Herrería", "Carpintería", "Servicios", "Materiales"]
SUFIJOS = ["del Valle", "San Miguel", "Los Pinos", "Altavista", "El Cedro", "La Joya", "Monarca",
           "Cumbres", "Real", "Guanajuato", "Bajío", "Centenario"]
CIUDADES = ["León", "Querétaro", "Aguascalientes", "Irapuato", "Celaya", "Silao", "San Miguel de Allende"]
PAGOS = ["efectivo", "tarjeta", "transferencia", "crédito"]


def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def main():
    out = []
    w = out.append
    w("-- GENERADO por datos/generar_datos.py (semilla 2026). No editar a mano.")
    for i, (n, c) in enumerate(SUCURSALES, 1):
        w(f"INSERT INTO sucursales (id, nombre, ciudad) VALUES ({i}, {q(n)}, {q(c)});")
    for i, (n, rfc, c, ct) in enumerate(PROVEEDORES, 1):
        w(f"INSERT INTO proveedores (id, nombre, rfc, ciudad, contacto) VALUES ({i}, {q(n)}, {q(rfc)}, {q(c)}, {q(ct)});")
    for i, (sku, n, cat, p, pr, co) in enumerate(PRODUCTOS, 1):
        w(f"INSERT INTO productos (id, sku, nombre, categoria, proveedor_id, precio_unitario, costo_unitario) "
          f"VALUES ({i}, {q(sku)}, {q(n)}, {q(cat)}, {p + 1}, {pr}, {co});")

    clientes = []
    for i in range(1, 121):
        if i % 3 == 0:
            nombre = f"{random.choice(EMPRESAS)} {random.choice(SUFIJOS)}"
            tipo = "empresa"
            limite = random.choice([50000, 80000, 120000, 200000])
        else:
            nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"
            tipo = "persona"
            limite = random.choice([0, 5000, 10000, 20000])
        ciudad = random.choice(CIUDADES)
        email = f"cliente{i:03d}@correo-ficticio.example"
        tel = "477" + "".join(str(random.randint(0, 9)) for _ in range(7))
        alta = date(2023, 1, 1) + timedelta(days=random.randint(0, 900))
        clientes.append(i)
        w(f"INSERT INTO clientes (id, nombre, tipo, ciudad, email, telefono, fecha_alta, limite_credito) "
          f"VALUES ({i}, {q(nombre)}, {q(tipo)}, {q(ciudad)}, {q(email)}, {q(tel)}, '{alta}', {limite});")

    inicio, fin = date(2025, 1, 1), date(2026, 10, 31)
    dias = (fin - inicio).days
    did = 0
    for vid in range(1, 1801):
        f = inicio + timedelta(days=random.randint(0, dias))
        w(f"INSERT INTO ventas (id, fecha, cliente_id, sucursal_id, metodo_pago) VALUES "
          f"({vid}, '{f}', {random.choice(clientes)}, {random.randint(1, 4)}, {q(random.choice(PAGOS))});")
        for _ in range(random.randint(1, 4)):
            did += 1
            pid = random.randint(1, len(PRODUCTOS))
            precio = PRODUCTOS[pid - 1][4]
            w(f"INSERT INTO detalle_venta (id, venta_id, producto_id, cantidad, precio_unitario) "
              f"VALUES ({did}, {vid}, {pid}, {random.randint(1, 12)}, {precio});")

    for pid in range(1, len(PRODUCTOS) + 1):
        for sid in range(1, 5):
            w(f"INSERT INTO inventario (producto_id, sucursal_id, existencias) "
              f"VALUES ({pid}, {sid}, {random.choice([0, 0, 4, 12, 25, 40, 80, 150])});")

    for t in ("sucursales", "proveedores", "productos", "clientes", "ventas", "detalle_venta"):
        w(f"SELECT setval(pg_get_serial_sequence('{t}', 'id'), (SELECT MAX(id) FROM {t}));")

    destino = Path(__file__).resolve().parent.parent / "db" / "02_datos.sql"
    destino.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Escrito {destino} ({len(out)} líneas)")


if __name__ == "__main__":
    main()
