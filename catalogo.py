import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar las credenciales que guardaste en el .env
load_dotenv()

app = Flask(__name__)

# Configurar la conexión con Supabase usando tus variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    try:
        # 1. Traer todos los productos de Supabase ordenados alfabéticamente por nombre
        response = supabase.table("Productos").select("*").order("Nombre").execute()
        productos = response.data
        
        # 2. Extraer las categorías únicas de los productos para armar los botones de filtro
        Categorias = sorted(list(set([p['Categoria'] for p in Productos if p.get('Categoria')])))
        
    except Exception as e:
        print(f"Error al conectar o leer Supabase: {e}")
        Productos = []
        Categorias = []
        
    # 3. Renderizar la plantilla HTML pasándole los datos dinámicos
    return render_template('index.html', Productos=Productos, Categorias=Categorias)

if __name__ == '__main__':
    # Localmente va a correr en el puerto 5000 (http://127.0.0.1:5000)
    app.run(debug=True, port=5000)
