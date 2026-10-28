# producto.py
# Clase que representa un producto del inventario de StockPy Solutions.

MAX_LARGO_NOMBRE = 100


class Producto:
    """
    Representa un producto en el inventario.

    Atributos:
        id (int): Identificador único del producto (autogenerado).
        nombre (str): Nombre descriptivo del producto (no vacío, máx. 100 caracteres).
        precio (float): Precio unitario en moneda local (mayor a 0).
        stock (int): Cantidad disponible en inventario (mayor o igual a 0).
    """

    def __init__(self, id: int, nombre: str, precio: float, stock: int):
        self.id = id
        self.nombre = self._validar_nombre(nombre)
        self.precio = self._validar_precio(precio)
        self.stock = self._validar_stock(stock)

    # ------------------------------------------------------------------
    # Validaciones de dominio: garantizan que nunca exista un producto
    # con datos inválidos, sin importar desde dónde se cree (menú o CSV).
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        nombre = str(nombre).strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if len(nombre) > MAX_LARGO_NOMBRE:
            raise ValueError(f"El nombre no puede superar {MAX_LARGO_NOMBRE} caracteres.")
        return nombre

    @staticmethod
    def _validar_precio(precio: float) -> float:
        precio = round(float(precio), 2)
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        return precio

    @staticmethod
    def _validar_stock(stock: int) -> int:
        stock = int(stock)
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        return stock

    def __str__(self) -> str:
        return (f"ID: {self.id:>4} | {self.nombre:<30} | "
                f"Precio: ${self.precio:>9.2f} | Stock: {self.stock:>5}")

    def __repr__(self) -> str:
        return f"Producto(id={self.id}, nombre={self.nombre!r}, precio={self.precio}, stock={self.stock})"

    def to_dict(self) -> dict:
        """Convierte el producto a diccionario (útil para guardar en CSV)."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": f"{self.precio:.2f}",
            "stock": self.stock,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Producto":
        """Crea un Producto a partir de una fila del CSV."""
        return cls(
            id=int(datos["id"]),
            nombre=datos["nombre"],
            precio=float(datos["precio"]),
            stock=int(datos["stock"]),
        )

    def actualizar(self, nuevo_precio: float = None, nuevo_stock: int = None) -> None:
        """Actualiza precio y/o stock del producto (aplicando las validaciones)."""
        if nuevo_precio is not None:
            self.precio = self._validar_precio(nuevo_precio)
        if nuevo_stock is not None:
            self.stock = self._validar_stock(nuevo_stock)
