# main.py
# Punto de entrada del Sistema de Inventario de StockPy Solutions.

from inventario import Inventario, ProductoDuplicadoError
from utils import leer_entero, leer_flotante, leer_texto, confirmar, mostrar_separador

inv = Inventario()


def mostrar_menu() -> None:
    """Muestra el menú principal."""
    mostrar_separador("=")
    print("   STOCKPY SOLUTIONS – INVENTARIO")
    mostrar_separador("=")
    print("  1. Agregar producto")
    print("  2. Listar todos los productos")
    print("  3. Buscar producto")
    print("  4. Actualizar producto")
    print("  5. Eliminar producto")
    print("  6. Salir")
    mostrar_separador("-")


def guardar() -> None:
    """Guarda en CSV e informa si hubo un problema."""
    if not inv.guardar_en_csv():
        print("⚠ No se pudieron guardar los cambios en el archivo.")


def agregar_producto() -> None:
    print("\n-- Agregar Producto --")
    nombre = leer_texto("Nombre del producto: ")
    if inv.existe_nombre(nombre):
        print(f"✗ Ya existe un producto llamado '{nombre}'. Usa 'Actualizar' para modificarlo.")
        return
    precio = leer_flotante("Precio unitario: $")
    stock = leer_entero("Stock inicial: ", minimo=0)
    try:
        prod = inv.agregar(nombre, precio, stock)
    except (ProductoDuplicadoError, ValueError) as e:
        print(f"✗ {e}")
        return
    guardar()
    print(f"\n✓ Producto agregado con ID {prod.id}")


def listar_productos() -> None:
    productos = inv.listar()
    if not productos:
        print("\nEl inventario está vacío.")
        return
    print(f"\n-- Inventario ({len(productos)} productos) --")
    mostrar_separador()
    for p in productos:
        print(p)
    mostrar_separador()
    print(f"Valor total del inventario: ${inv.valor_total():,.2f}")


def buscar_producto() -> None:
    print("\n-- Buscar Producto --")
    print("  1. Buscar por ID")
    print("  2. Buscar por nombre")
    opcion = leer_entero("Selecciona: ", minimo=1, maximo=2)
    if opcion == 1:
        id_ = leer_entero("ID del producto: ", minimo=1)
        p = inv.buscar_por_id(id_)
        print(p if p else "Producto no encontrado.")
    else:
        termino = leer_texto("Término de búsqueda: ")
        resultados = inv.buscar_por_nombre(termino)
        if resultados:
            for p in resultados:
                print(p)
        else:
            print("No se encontraron productos.")


def actualizar_producto() -> None:
    if len(inv) == 0:
        print("\nEl inventario está vacío.")
        return
    listar_productos()
    id_ = leer_entero("\nID del producto a actualizar: ", minimo=1)
    p = inv.buscar_por_id(id_)
    if not p:
        print("Producto no encontrado.")
        return
    print(f"Editando: {p}")
    print("(Presiona Enter para mantener el valor actual)")
    nuevo_precio = leer_flotante(f"Nuevo precio (actual ${p.precio:.2f}): ", permitir_vacio=True)
    nuevo_stock = leer_entero(f"Nuevo stock (actual {p.stock}): ", minimo=0, permitir_vacio=True)
    if nuevo_precio is None and nuevo_stock is None:
        print("Sin cambios.")
        return
    inv.actualizar(id_, nuevo_precio, nuevo_stock)
    guardar()
    print("\n✓ Producto actualizado.")


def eliminar_producto() -> None:
    if len(inv) == 0:
        print("\nEl inventario está vacío.")
        return
    listar_productos()
    id_ = leer_entero("\nID del producto a eliminar: ", minimo=1)
    p = inv.buscar_por_id(id_)
    if not p:
        print("Producto no encontrado.")
        return
    print(f"Vas a eliminar: {p}")
    if confirmar("¿Confirmas la eliminación?"):
        inv.eliminar(id_)
        guardar()
        print("\n✓ Producto eliminado.")
    else:
        print("Operación cancelada.")


ACCIONES = {
    1: agregar_producto,
    2: listar_productos,
    3: buscar_producto,
    4: actualizar_producto,
    5: eliminar_producto,
}


def main() -> None:
    inv.cargar_desde_csv()
    print(f"Sistema iniciado. {len(inv)} productos cargados.")
    try:
        while True:
            mostrar_menu()
            opcion = leer_entero("Selecciona una opción: ", minimo=1, maximo=6)
            if opcion == 6:
                print("¡Hasta pronto!")
                break
            ACCIONES[opcion]()
            input("\nPresiona Enter para continuar...")
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D: salida limpia, los datos ya están guardados
        print("\n\nPrograma interrumpido. Los datos ya estaban guardados. ¡Hasta pronto!")


if __name__ == "__main__":
    main()
