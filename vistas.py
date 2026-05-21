import os
from flask import request, g
from supabase import create_client, Client

# =========================================================
# 1. CONFIGURACIÓN DE CREDENCIALES DE SUPABASE
# =========================================================
SUPABASE_URL = "https://hkuheednquclcnjdfcva.supabase.co"
SUPABASE_KEY = "ACÁ_PEGÁS_TU_CLAVE_PUBLISHABLE_LARGA"  # <-- Tu clave de siempre

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================================================
# 2. FUNCIÓN PARA INYECTAR LAS VISITAS EN TU CATÁLOGO
# =========================================================
def iniciar_contador_en_catalogo(app):
    """
    Se conecta a tu app de Flask y maneja las visitas de forma automática
    sin que tengas que escribir código adentro de catalogo.py
    """
    
    # Esto se ejecuta automáticamente CADA VEZ que alguien entra a la web
    @app.before_request
    def procesar_visita():
        # Solo contamos si entran a la página principal "/"
        if request.path == "/":
            try:
                # Sumamos 1 en Supabase
                supabase.rpc("incrementar_visitas", {"pagina_id": "home"}).execute()
                
                # Traemos el total actualizado
                response = supabase.table("contador_visitas") \
                                   .select("visitas") \
                                   .eq("id", "home") \
                                   .single() \
                                   .execute()
                
                if response.data:
                    g.visitas_total = f"Visitas: {response.data.get('visitas', 0)}"
                else:
                    g.visitas_total = "Visitas: ---"
            except Exception as e:
                print(f"Error en contador Supabase: {e}")
                g.visitas_total = "Visitas: ---"

    # Esto hace que la variable 'visitas' esté disponible en TODO tu HTML automáticamente
    @app.context_processor
    def inyectar_variable_html():
        return dict(visitas=getattr(g, 'visitas_total', "Visitas: ---"))