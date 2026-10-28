# tests/test_inventario.py
# Pruebas unitarias de las clases Producto e Inventario.
# Ejecutar desde la raíz del proyecto:  python -m unittest discover -s tests -v

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from producto import Producto  # noqa: E402
from inventario import Inventario, ProductoDuplicadoError  # noqa: E402


class TestProducto(unittest.TestCase):

    def test_crear_producto_valido(self):
        p = Producto(1, "  Mouse Logitech  ", 29.999, 15)
        self.assertEqual(p.nombre, "Mouse Logitech")
        self.assertEqual(p.precio, 30.0)
        self.assertEqual(p.stock, 15)

    def test_nombre_vacio_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto(1, "   ", 10, 1)

    def test_nombre_muy_largo_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto(1, "x" * 101, 10, 1)

    def test_precio_cero_o_negativo_lanza_error(self):
        for precio in (0, -5):
            with self.assertRaises(ValueError):
                Producto(1, "Teclado", precio, 1)

    def test_stock_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            Producto(1, "Teclado", 10, -1)

    def test_to_dict_y_from_dict(self):
        p = Producto(7, "Monitor", 149.9, 8)
        copia = Producto.from_dict(p.to_dict())
        self.assertEqual(copia.to_dict(), p.to_dict())


class TestInventario(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ruta = os.path.join(self.tmp.name, "data", "inventario.csv")
        self.inv = Inventario(archivo_csv=self.ruta)

    def tearDown(self):
        self.tmp.cleanup()

    def test_ids_unicos_y_autoincrementales(self):
        a = self.inv.agregar("Mouse", 10, 1)
        b = self.inv.agregar("Teclado", 20, 2)
        self.assertEqual((a.id, b.id), (1, 2))

    def test_no_permite_duplicados_por_nombre(self):
        self.inv.agregar("Mouse Logitech", 10, 1)
        with self.assertRaises(ProductoDuplicadoError):
            self.inv.agregar("mouse   LOGITECH", 12, 3)

    def test_datos_invalidos_no_consumen_id(self):
        with self.assertRaises(ValueError):
            self.inv.agregar("Malo", -1, 1)
        self.assertEqual(self.inv.agregar("Bueno", 1, 1).id, 1)

    def test_buscar_por_id_y_nombre(self):
        self.inv.agregar("Mouse Logitech", 10, 1)
        self.inv.agregar("Teclado HP", 20, 2)
        self.assertEqual(self.inv.buscar_por_id(2).nombre, "Teclado HP")
        self.assertIsNone(self.inv.buscar_por_id(99))
        self.assertEqual(len(self.inv.buscar_por_nombre("logi")), 1)

    def test_actualizar(self):
        self.inv.agregar("Mouse", 10, 1)
        self.assertTrue(self.inv.actualizar(1, precio=15.5))
        self.assertEqual(self.inv.buscar_por_id(1).precio, 15.5)
        self.assertEqual(self.inv.buscar_por_id(1).stock, 1)  # stock sin cambios
        self.assertFalse(self.inv.actualizar(99, stock=3))

    def test_eliminar(self):
        self.inv.agregar("Mouse", 10, 1)
        self.assertTrue(self.inv.eliminar(1))
        self.assertEqual(len(self.inv), 0)
        self.assertFalse(self.inv.eliminar(1))

    def test_valor_total(self):
        self.inv.agregar("Mouse", 10, 3)
        self.inv.agregar("Teclado", 2.5, 4)
        self.assertEqual(self.inv.valor_total(), 40.0)

    def test_persistencia_csv(self):
        self.inv.agregar("Mouse", 12.99, 25)
        self.inv.agregar("Teclado", 19.99, 15)
        self.assertTrue(self.inv.guardar_en_csv())

        nuevo = Inventario(archivo_csv=self.ruta)
        self.assertTrue(nuevo.cargar_desde_csv())
        self.assertEqual(len(nuevo), 2)
        # El contador de IDs continúa desde el mayor ID cargado
        self.assertEqual(nuevo.agregar("Monitor", 149.99, 8).id, 3)

    def test_cargar_sin_archivo_retorna_false(self):
        self.assertFalse(self.inv.cargar_desde_csv())

    def test_filas_corruptas_se_omiten(self):
        os.makedirs(os.path.dirname(self.ruta))
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write("id,nombre,precio,stock\n1,Mouse,10,5\n2,Malo,abc,1\n3,Teclado,20,2\n")
        self.inv.cargar_desde_csv()
        self.assertEqual([p.id for p in self.inv.listar()], [1, 3])


if __name__ == "__main__":
    unittest.main()
