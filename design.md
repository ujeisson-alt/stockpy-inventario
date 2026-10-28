# Diseño funcional — StockPy Solutions

## Menú principal
```
========================================================================
   STOCKPY SOLUTIONS – INVENTARIO
========================================================================
  1. Agregar producto
  2. Listar todos los productos
  3. Buscar producto
  4. Actualizar producto
  5. Eliminar producto
  6. Salir
------------------------------------------------------------------------
Selecciona una opción:
```

## Flujos de navegación

### 1. Agregar producto
1. El usuario selecciona la opción 1.
2. El sistema pide el nombre (no vacío, máx. 100 caracteres).
3. Si el nombre ya existe → muestra error y vuelve al menú.
4. El sistema pide el precio (> 0) y el stock inicial (≥ 0); repite la pregunta si el dato es inválido.
5. Guarda el producto en memoria y en el CSV.
6. Muestra confirmación con el ID asignado y vuelve al menú.

### 3. Buscar producto
1. El usuario elige buscar por ID o por nombre.
2. Por ID → muestra el producto o "Producto no encontrado".
3. Por nombre → muestra todas las coincidencias parciales (sin distinguir mayúsculas) o "No se encontraron productos".

### 4. Actualizar producto
1. Se muestra el listado y se pide el ID.
2. Si no existe → "Producto no encontrado" y vuelve al menú.
3. Se pide nuevo precio y nuevo stock (Enter = mantener el valor actual).
4. Se guarda en CSV y se confirma.

### 5. Eliminar producto
1. Se muestra el listado y se pide el ID.
2. Si existe, se muestra el producto y se pide confirmación (s/n).
3. Si confirma → se elimina, se guarda el CSV y se confirma; si no → "Operación cancelada".

## Arquitectura en capas
```
main.py          → Presentación (menú, entradas y mensajes)
utils.py         → Validación de entradas del usuario
inventario.py    → Lógica de negocio + persistencia CSV
producto.py      → Modelo de dominio
data/inventario.csv → Almacenamiento
```
