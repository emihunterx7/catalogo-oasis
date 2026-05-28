import sqlite3
from supabase import create_client

# Configuración: Reemplaza con tus datos de Supabase
url = "https://hkuheednquclcnjdfcva.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhrdWhlZWRucXVjbGNuamRmY3ZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkxMjI1NzYsImV4cCI6MjA5NDY5ODU3Nn0.Pm2pU1NuSKDT0h87xxBo3hnm8TYLmINqvMWZkVsEGpA"
supabase = create_client(url, key)

def sincronizar_db():
    # 1. Obtener los datos de Supabase
    response = supabase.table("Productos").select("*").execute()
    data = response.data
    
    # 2. Conectar a tu archivo productos.db local
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    
    # 3. Limpiar la tabla actual para evitar duplicados o errores
    cursor.execute("DELETE FROM Productos")
    
    # 4. Insertar los nuevos datos traídos de Supabase
    for prod in data:
        cursor.execute("""
            INSERT INTO Productos (ProductoId, Nombre, Precio, Stock, CategoriaId) 
            VALUES (?, ?, ?, ?, ?)
        """, (prod['ProductoId'], prod['Nombre'], prod['Precio'], prod['Stock'], prod['CategoriaId']))
    
    conn.commit()
    conn.close()
    print("Base de datos local actualizada con éxito desde Supabase.")

if __name__ == "__main__":
    sincronizar_db()
