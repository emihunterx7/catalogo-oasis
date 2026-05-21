import os
from supabase import create_client, Client

# Configuración de credenciales de Supabase
SUPABASE_URL = "TU_SUPABASE_URL"
SUPABASE_KEY = "TU_SUPABASE_ANON_KEY"

# Inicializamos el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def registrar_y_obtener_visitas(pagina_id="home"):
    """
    Incrementa el contador en Supabase mediante RPC y devuelve el total actualizado.
    """
    try:
        # 1. Llamamos a la función que creamos en Supabase para sumar 1 de forma segura
        supabase.rpc("incrementar_visitas", {"pagina_id": pagina_id}).execute()
        
        # 2. Traemos el valor que quedó guardado tras la actualización
        response = supabase.table("contador_visitas") \
                           .select("visitas") \
                           .eq("id", pagina_id) \
                           .single() \
                           .execute()
        
        if response.data:
            return response.data.get("visitas", 0)
        return 0
        
    except Exception as e:
        print(f"Error al conectar con el contador de Supabase: {e}")
        return None