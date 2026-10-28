# 📦 Sistema de Inventario — StockPy Solutions

Sistema de gestión de inventario por consola desarrollado en **Python** con
Programación Orientada a Objetos y persistencia en **CSV**.
Proyecto autogestionado que simula un encargo profesional real.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-unittest-green)
![Dependencias](https://img.shields.io/badge/dependencias-ninguna-lightgrey)

## Descripción
StockPy Solutions es una PyME que vende insumos tecnológicos y gestionaba su stock con
planillas desconectadas y papel. Esta aplicación reemplaza ese proceso manual con una
fuente única de verdad: un inventario digital que valida los datos, evita productos
duplicados y se guarda automáticamente.

## Funcionalidades
- ➕ Agregar productos con ID autoincremental, nombre, precio y stock
- 📋 Listar el inventario completo con su valor total
- 🔍 Buscar por ID o por nombre (coincidencia parcial, sin distinguir mayúsculas)
- ✏️ Actualizar precio y/o stock (Enter para mantener el valor actual)
- 🗑️ Eliminar productos con confirmación
- 💾 Persistencia automática en `data/inventario.csv` (se carga al iniciar)
- ✅ Validaciones: nombre no vacío y único, precio > 0, stock ≥ 0
- 🛡️ Tolerante a errores: entradas inválidas, filas corruptas en el CSV, Ctrl+C

## Tecnologías
- Python 3.10+
- Módulos estándar: `csv`, `os`, `typing`, `unittest` (sin dependencias externas)

## Cómo ejecutar
```bash
git clone https://github.com/ujeisson-alt/stockpy-inventario.git
cd stockpy-inventario
python main.py
```

### Ejemplo de uso
```
Sistema iniciado. 3 productos cargados.
========================================================================
   STOCKPY SOLUTIONS – INVENTARIO
========================================================================
  1. Agregar producto
  2. Listar todos los productos
  ...
Selecciona una opción: 2

-- Inventario (3 productos) --
ID:    1 | Mouse Logitech M170            | Precio: $    12.99 | Stock:    25
ID:    2 | Teclado HP USB                 | Precio: $    19.99 | Stock:    15
ID:    3 | Monitor 24 pulgadas            | Precio: $   149.99 | Stock:     8
Valor total del inventario: $1,824.52
```

## Pruebas
```bash
python -m unittest discover -s tests -v
```
Cubren validaciones del modelo, IDs autoincrementales, duplicados, búsqueda,
actualización, eliminación y persistencia CSV (incluyendo filas corruptas).

## Estructura del proyecto
```
stockpy-inventario/
├── main.py            # Menú principal (capa de presentación)
├── producto.py        # Clase Producto (modelo + validaciones de dominio)
├── inventario.py      # Clase Inventario (lógica de negocio + CSV)
├── utils.py           # Lectura y validación de entradas del usuario
├── data/
│   └── inventario.csv # Datos persistidos
├── tests/
│   └── test_inventario.py
├── analysis.md        # Análisis del problema
└── design.md          # Diseño del menú y flujos
```

## Decisiones de diseño
- **Arquitectura en capas**: la interfaz (`main.py`) nunca toca el CSV directamente.
- **Validación en dos niveles**: `utils.py` guía al usuario; `Producto` garantiza la integridad aunque el CSV se edite a mano.
- **Rutas absolutas al CSV** basadas en la ubicación del proyecto, para que funcione desde cualquier carpeta.

## Autor
**Jeisson Uribe** — [GitHub](https://github.com/ujeisson-alt) · [LinkedIn](https://linkedin.com/in/jeisson-uribe-qa-data)
