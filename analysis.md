# Análisis del problema — StockPy Solutions

## Descripción del proyecto (en mis palabras)
StockPy Solutions es una PyME de 5 a 10 empleados que vende hardware, periféricos y
accesorios. Hoy controla su inventario con planillas de Excel desconectadas, papel y
comunicación verbal, lo que provoca ventas de productos sin stock, artículos duplicados
con nombres distintos y horas perdidas buscando información. Este sistema de consola en
Python centraliza el inventario en un único archivo CSV, permite registrar, consultar,
buscar, actualizar y eliminar productos, y valida los datos para evitar errores humanos.

## Problema principal
No existe una **fuente única y confiable** del stock disponible en tiempo real.

## Usuarios
Personal administrativo de la empresa (uso interno, sin autenticación en el MVP).

## Funcionalidades (acciones del usuario)
1. Registrar un producto nuevo (ID automático, nombre, precio, stock).
2. Consultar el inventario completo.
3. Buscar un producto por ID o por nombre.
4. Actualizar precio y/o stock.
5. Eliminar productos que ya no se comercializan.
6. Guardar automáticamente en CSV y cargarlo al iniciar.

## Modelo de datos — Producto

| Atributo | Tipo Python | Ejemplo            | Validación                 |
|----------|-------------|--------------------|----------------------------|
| id       | int         | 1                  | Único, autogenerado        |
| nombre   | str         | "Mouse Logitech"   | No vacío, máx. 100 chars   |
| precio   | float       | 29.99              | Mayor a 0                  |
| stock    | int         | 15                 | Mayor o igual a 0          |

## Preguntas que le haría al cliente
- ¿Se necesita manejar categorías o proveedores en una próxima versión?
- ¿Varias personas usarán el sistema al mismo tiempo?
- ¿En qué moneda se expresan los precios? ¿Se requieren impuestos?
- ¿Se debe registrar un historial de movimientos (entradas/salidas)?
- ¿Cómo se deben tratar dos productos con nombres casi iguales?

## Decisiones tomadas
- **Nombres únicos (sin distinguir mayúsculas ni espacios extra)** para atacar el
  problema de productos duplicados.
- **Guardado inmediato** tras cada cambio: si el programa se cierra inesperadamente,
  no se pierde información.
- **Validaciones en el modelo** (`Producto`) además de en la interfaz, para que ni un
  CSV editado a mano pueda introducir datos inválidos.
