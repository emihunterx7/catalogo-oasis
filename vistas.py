from flask import request

# Reemplazá este número por la IP real de tu casa (de cualesmiip.com):
IP_DE_MI_CASA = "181.44.XX.XX" 

def configurar_contador_visitas(app):
    """
    Registra en los logs de Render a los clientes que entran
    al catálogo, usando el encabezado correcto de Render.
    """
    @app.before_request
    def registrar_visita():
        if request.path == '/':
            # Modificamos esto para obligar a leer la IP externa real que pasa Render
            ip_visitante = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
            
            # Si no encuentra ninguna arriba, usa la básica por las dudas
            if not ip_visitante:
                ip_visitante = request.remote_addr
            
            # Si la IP es real, y no eres tú ni el localhost interno de Render
            if ip_visitante and ip_visitante != IP_DE_MI_CASA and ip_visitante != "127.0.0.1" and ip_visitante != "localhost":
                print(f"[VISITA_CLIENTE] - Nueva entrada desde la IP: {ip_visitante}", flush=True)
