import os
from flask import request, g
from supabase import create_client, Client

# 1. CREDENCIALES DE SUPABASE
SUPABASE_URL = "https://hkuheednquclcnjdfcva.supabase.co"
SUPABASE_KEY = "ACÁ_PEGÁS_TU_CLAVE_PUBLISHABLE_LARGA"  # <-- Tu clave real de siempre

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. INYECTOR AUTOMÁTICO
def iniciar_contador_en_catalogo(app):
    
    @app.before_request
    def procesar_visita():
        if request.path == "/":
            try:
                # Sumamos la visita en Supabase
                supabase.rpc("incrementar_visitas", {"pagina_id": "home"}).execute()
                
                # Traemos el total actualizado
                response = supabase.table("contador_visitas") \
                                   .select("visitas") \
                                   .eq("id", "home") \
                                   .single() \
                                   .execute()
                
                if response.data:
                    g.visitas_total = str(response.data.get('visitas', 0))
                else:
                    g.visitas_total = "---"
            except Exception as e:
                print(f"Error en contador Supabase: {e}")
                g.visitas_total = "---"

    # Modificamos la respuesta final de la página para pegarle el HTML aparte sin tocar catalogo.py
    @app.after_request
    def inyectar_html_contador(response):
        # Solo modificamos si la página cargó bien y es el Home HTML
        if response.status_code == 200 and response.mimetype == "text/html" and request.path == "/":
            try:
                # Buscamos la ruta del archivo contador.html
                ruta_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contador.html")
                
                if os.path.exists(ruta_html):
                    with open(ruta_html, "r", encoding="utf-8") as f:
                        html_contador = f.read()
                    
                    # Reemplazamos la variable del HTML por el número real de visitas
                    numero_visitas = getattr(g, 'visitas_total', "---")
                    html_contador = html_contador.replace("{{ visitas }}", f"Visitas: {numero_visitas}")
                    
                    # Obtenemos el texto original de tu catálogo
                    data_original = response.get_data(as_text=True)
                    
                    # Le pegamos nuestro cartelito justo antes de que termine el cuerpo de la página
                    if "</body>" in data_original:
                        nueva_data = data_original.replace("</body>", f"{html_contador}\n</body>")
                    else:
                        nueva_data = data_original + html_contador
                    
                    response.set_data(nueva_data)
            except Exception as e:
                print(f"No se pudo inyectar el HTML del contador: {e}")
        return response