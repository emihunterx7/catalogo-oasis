import sqlite3
import psycopg2

# 1. DATOS DE CONEXIÓN
URL_SUPABASE = "postgresql://postgres:D*6hisi+67idKP.@db.hkuheednquclcnjdfcva.supabase.co:5432/postgres"
ARCHIVO_SQLITE = r"C:\Users\emiliano\Desktop\CATALOGO\productos.db"

try:
    print("🔌 Conectando a las bases de datos...")
    conn_local = sqlite3.connect(ARCHIVO_SQLITE)
    cursor_local = conn_local.cursor()

    conn_cloud = psycopg2.connect(URL_SUPABASE)
    cursor_cloud = conn_cloud.cursor()

    # 2. MIGRAR CATEGORIAS (Esta ya anduvo bien, la dejamos igual por seguridad)
    print("📦 Migrando categorías...")
    cursor_local.execute('SELECT "CategoriaId", "Nombre" FROM "Categorias";')
    categorias = cursor_local.fetchall()
    
    for cat in categorias:
        cursor_cloud.execute("""
            INSERT INTO "Categorias" ("id", "Nombre") 
            VALUES (%s, %s)
            ON CONFLICT ("id") DO NOTHING;
        """, (cat[0], cat[1]))

    # 3. MIGRAR PRODUCTOS (Usamos "ProductoId" que es como la tenés en Supabase)
    print("🛍️ Migrando productos...")
    cursor_local.execute('SELECT "ProductoId", "Nombre", "Precio", "Stock", "CategoriaId" FROM "Productos";')
    productos = cursor_local.fetchall()
    
    for prod in productos:
        cursor_cloud.execute("""
            INSERT INTO "Productos" ("ProductoId", "Nombre", "Precio", "Stock", "CategoriaId") 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT ("ProductoId") DO NOTHING;
        """, (prod[0], prod[1], float(prod[2]), prod[3], prod[4]))

    # Guardamos definitivamente los cambios en internet
    conn_cloud.commit()
    print("\n✅ ¡MIGRACIÓN COMPLETADA CON ÉXITO! Tus productos ya están en internet.")

except Exception as e:
    print(f"\n❌ Hubo un error durante la migración: {e}")

finally:
    if conn_local: conn_local.close()
    if conn_cloud: conn_cloud.close()