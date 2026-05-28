import sqlite3
import os
from supabase import create_client

# 1. Usamos variables de entorno para mayor seguridad (ya no pegues tu clave aquí)
url = os.environ.get("https://hkuheednquclcnjdfcva.supabase.co")
key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhrdWhlZWRucXVjbGNuamRmY3ZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkxMjI1NzYsImV4cCI6MjA5NDY5ODU3Nn0.Pm2pU1NuSKDT0h87xxBo3hnm8TYLmINqvMWZkVsEGpA")
supabase = create_client(url, key)

def sincronizar_db():
    # Obtener datos
    response = supabase.table("Productos").select("*").execute()
    data = response.data
    
    # Conectar y actualizar localmente
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos")
    
    datos_a_insertar = [(p['ProductoId'], p['Nombre'], p['Precio'], p['Stock'], p['CategoriaId']) for p in data]
    cursor.executemany("INSERT INTO Productos VALUES (?, ?, ?, ?, ?)", datos_a_insertar)
    
    conn.commit()
    conn.close()
    print("Base de datos local actualizada.")

if __name__ == "__main__":
    sincronizar_db()
