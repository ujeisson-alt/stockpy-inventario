# inventario.py
# Clase gestora que maneja la colección de productos y su persistencia en CSV.

import csv
import os
from typing import List, Optional

from producto import Producto

# Ruta por defecto del CSV, relativa a la carpeta del proyecto
# (así funciona sin importar desde qué carpeta se ejecute el programa).
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CSV = os.path.join(DIRECTORIO_BASE, "data", "inventario.csv")
CAMPOS_CSV = ["id", "nombre", "precio", "stock"]


class ProductoDuplicadoError(ValueError):
    """Se lanza al intentar registrar un producto cuyo nombre ya existe."""


class Inventario:
    """Gestiona la colección de productos de StockPy Solutions."""

    def __init__(self, archivo_csv: str = ARCHIVO_CSV):
        self.archivo_csv = archivo_csv
        self._productos: List[Producto] = []  # lista interna
        self._ultimo_id: int = 0              # contador de IDs

    # ------------------------------------------------------------------
    # Operaciones CRUD
    # ------------------------------------------------------------------
    def _generar_id(self) -> int:
        """Genera un nuevo ID único autoincremental."""
        self._ultimo_id += 1
        return self._ultimo_id

    def existe_nombre(self, nombre: str, excluir_id: Optional[int] = None) -> bool:
        """Indica si ya hay un producto con ese nombre (ignora mayúsculas y espacios)."""
        clave = " ".join(nombre.lower().split())
        return any(
            " ".join(p.nombre.lower().split()) == clave and p.id != excluir_id
            for p in self._productos
        )

    def agregar(self, nombre: str, precio: float, stock: int) -> Producto:
        """Crea y agrega un nuevo producto. Evita duplicados por nombre."""
        if self.existe_nombre(nombre):
            raise ProductoDuplicadoError(f"Ya existe un producto llamado '{nombre.strip()}'.")
        # Se valida creando el objeto ANTES de consumir un ID nuevo.
        producto = Producto(self._ultimo_id + 1, nombre, precio, stock)
        self._generar_id()
        self._productos.append(producto)
        return producto

    def listar(self) -> List[Producto]:
        """Retorna una copia de todos los productos, ordenados por ID."""
        return sorted(self._productos, key=lambda p: p.id)

    def buscar_por_id(self, id: int) -> Optional[Producto]:
        """Busca un producto por su ID. Retorna None si no existe."""
        for producto in self._productos:
            if producto.id == id:
                return producto
        return None

    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        """Busca productos cuyo nombre contenga el término (insensible a mayúsculas)."""
        termino_lower = termino.strip().lower()
        return [p for p in self._productos if termino_lower in p.nombre.lower()]

    def actualizar(self, id: int, precio: float = None, stock: int = None) -> bool:
        """Actualiza un producto por ID. Retorna True si lo encontró."""
        producto = self.buscar_por_id(id)
        if producto:
            producto.actualizar(precio, stock)
            return True
        return False

    def eliminar(self, id: int) -> bool:
        """Elimina un producto por ID. Retorna True si lo encontró."""
        producto = self.buscar_por_id(id)
        if producto:
            self._productos.remove(producto)
            return True
        return False

    def valor_total(self) -> float:
        """Valor total del inventario (precio x stock de cada producto)."""
        return round(sum(p.precio * p.stock for p in self._productos), 2)

    def __len__(self) -> int:
        return len(self._productos)

    # ------------------------------------------------------------------
    # Persistencia en CSV
    # ------------------------------------------------------------------
    def cargar_desde_csv(self) -> bool:
        """Carga productos desde el archivo CSV al iniciar el programa.

        Las filas con datos corruptos se omiten (y se informan) en lugar
        de detener la carga completa.
        """
        if not os.path.exists(self.archivo_csv):
            return False  # No hay archivo todavía, es normal en el primer uso
        try:
            with open(self.archivo_csv, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for numero_fila, fila in enumerate(reader, start=2):
                    try:
                        producto = Producto.from_dict(fila)
                    except (ValueError, KeyError, TypeError) as e:
                        print(f"Aviso: fila {numero_fila} del CSV omitida ({e}).")
                        continue
                    if self.buscar_por_id(producto.id):
                        print(f"Aviso: ID {producto.id} repetido en el CSV, fila {numero_fila} omitida.")
                        continue
                    self._productos.append(producto)
                    # Mantener el contador de IDs sincronizado con el mayor ID existente
                    self._ultimo_id = max(self._ultimo_id, producto.id)
            return True
        except OSError as e:
            print(f"Error al cargar datos: {e}")
            return False

    def guardar_en_csv(self) -> bool:
        """Guarda todos los productos en el archivo CSV (sobrescribe)."""
        try:
            os.makedirs(os.path.dirname(self.archivo_csv) or ".", exist_ok=True)
            with open(self.archivo_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
                writer.writeheader()
                for producto in self.listar():
                    writer.writerow(producto.to_dict())
            return True
        except OSError as e:
            print(f"Error al guardar datos: {e}")
            return False
