import sqlite3
import psycopg2

# 1. DATOS DE CONEXIÓN
URL_SUPABASE = "postgresql://postgres:D*6hisi+67idKP.@db.hkuheednquclcnjdfcva.supabase.co:5432/postgres"
ARCHIVO_SQLITE = r"C:\Users\EMI\Desktop\GestionGratis_v1.6.2.0\Productos.db"

try:
    print("🔌 Conectando a las bases de datos...")
    conn_local = sqlite3.connect(ARCHIVO_SQLITE)
    cursor_local = conn_local.cursor()

    conn_cloud = psycopg2.connect(URL_SUPABASE)
    cursor_cloud = conn_cloud.cursor()

    # 2. MIGRAR CATEGORIAS (Esta ya anduvo bien, la dejamos igual por seguridad)
    print("📦 Migrando categorías...")
    cursor_local.execute('SELECT "categoriaId", "nombre" FROM "categorias";')
    categorias = cursor_local.fetchall()
    
    for cat in categorias:
        cursor_cloud.execute("""
            INSERT INTO "categorias" ("id", "nombre") 
            VALUES (%s, %s)
            ON CONFLICT ("id") DO NOTHING;
        """, (cat[0], cat[1]))

    # 3. MIGRAR PRODUCTOS (Usamos "ProductoId" que es como la tenés en Supabase)
    # 3. MIGRAR PRODUCTOS
    print("🛍️ Migrando productos...")
    # SQLITE: Aquí mantenemos los nombres de tu base local
    cursor_local.execute('SELECT "ProductoId", "Nombre", "Precio", "Stock", "CategoriaId" FROM "Productos";')
    productos = cursor_local.fetchall()
    
    for prod in productos:
        # SUPABASE: Aquí usamos los nombres EXACTOS de tu panel (id, nombre, precio, stock, categoria)
        cursor_cloud.execute("""
            INSERT INTO productos (id, nombre, precio, stock, categoria) 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (prod[0], prod[1], float(prod[2]), prod[3], prod[4]))

    # Guardamos definitivamente los cambios en internet
    conn_cloud.commit()
    print("\n✅ ¡MIGRACIÓN COMPLETADA CON ÉXITO! Tus productos ya están en internet.")

except Exception as e:
    print(f"\n❌ Hubo un error durante la migración: {e}")

finally:
    if conn_local: conn_local.close()
    if conn_cloud: conn_cloud.close()