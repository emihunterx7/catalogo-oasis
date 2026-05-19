from flask import request

# ⚠️ REEMPLAZÁ ESTE NÚMERO POR LA IP REAL DE TU WI-FI:
IP_DE_MI_CASA = "181.44.XX.XX" 

def configurar_contador_visitas(app):
    """
    Registra en los logs de Render a los clientes que entran
    al catálogo, ignorando las visitas de tu casa.
    """
    @app.before_request
    def registrar_visita():
        # Solo miramos cuando entran a la página principal '/'
        if request.path == '/':
            # Render nos pasa la IP del cliente en este encabezado
            ip_visitante = request.headers.get('X-Forwarded-For', request.remote_addr)
            
            # Si hay una IP y NO es la de tu casa ni la prueba local, se registra
            if ip_visitante and ip_visitante != IP_DE_MI_CASA and ip_visitante != "127.0.0.1":
                print(f"[VISITA_CLIENTE] - Nueva entrada desde la IP: {ip_visitante}", flush=True)