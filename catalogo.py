from flask import Flask, render_template_string, request
import sqlite3
import os
import psycopg2 


app = Flask(__name__)

# --- CONFIGURACIÓN DE CONEXIÓN A SUPABASE ---
# Es recomendable usar una variable de entorno para no exponer la contraseña
# Si no la usas, reemplaza el texto con tu URL real.

DATABASE_URL = "postgresql://postgres:D*6hisi+67idKP.@db.hkuheednquclcnjdfcva.supabase.co:5432/postgres"

# 🚀 CONEXIÓN CON EL CONTADOR EN VIVO
from vistas import iniciar_contador_en_catalogo
iniciar_contador_en_catalogo(app)

# ==========================================
# CONFIGURACIÓN DE BANNER / NOVEDADES
# Podés cambiar los textos y links de imágenes acá abajo cuando quieras.
# ==========================================
BANNER_OFERTAS = [
    {
       "titulo": "🔥 ¡MAPLE HUEVO BLANCO $ 4800!",
        "descripcion": "ACEPTAMOS EFECTIVO Y TRANSFEENCIAS",
        "imagen": "https://raw.githubusercontent.com/emihunterx7/catalogo-oasis/11f042053004aa1188c218acd5a5ffc7c76805cc/oferta%20huevos.png",
        "badge": "OFERTA DE LA SEMANA"
    },
    {
        "titulo": "⚡ ",
        "descripcion": "",
        "imagen": "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=800&auto=format&fit=crop&q=60",
        "badge": ""
    },
    {
        "titulo": "📦 ",
        "descripcion": "",
        "imagen": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&auto=format&fit=crop&q=60",
        "badge": "INFO"
    }
]

import os

def encontrar_imagen_producto(producto_id):
    # Aseguramos la ruta absoluta a la carpeta de imágenes
    carpeta_imagenes = os.path.join(os.getcwd(), "static", "imagenes")
    extensiones = ['.jpg', '.jpeg', '.png', '.webp', '.PNG', '.JPG']

    if os.path.exists(carpeta_imagenes):
        for ext in extensiones:
            nombre_archivo = f"{producto_id}{ext}"
            ruta_completa = os.path.join(carpeta_imagenes, nombre_archivo)
            if os.path.exists(ruta_completa):
                # Retornamos la ruta relativa para el navegador
                return f"/static/imagenes/{nombre_archivo}"
    
    # Si no hay imagen, retornamos None para que el HTML muestre "Sin Foto"
    return None

# --- EN TU ARCHIVO app.py ---

# 1. PEGA EL MAPEO AQUÍ (fuera de las funciones, arriba de todo)
mapeo_cat = {
    "1": "GALLETITAS", "2": "LIMPIEZA", "3": "FARMACIA",
    "4": "KIOSCO", "5": "BEBIDAS", "6": "LIBRERIA", 
    "7": "JUGUETES Y FIGURAS", "8": "PAPELERIA"
}

# 2. REEMPLAZA TU FUNCIÓN VIEJA POR ESTA
def obtener_productos_con_categorias(busqueda=""):
    mapeo_cat = {
        "1": "GALLETITAS", "2": "LIMPIEZA", "3": "FARMACIA",
        "4": "KIOSCO", "5": "BEBIDAS", "6": "LIBRERIA", 
        "7": "JUGUETES Y FIGURAS", "8": "PAPELERIA"
    }

    try:
        conexion = psycopg2.connect(DATABASE_URL)
        cursor = conexion.cursor()
        
        consulta = "SELECT id, nombre, precio, stock, categoria, imagen FROM productos WHERE 1=1"
        parametros = []
        if busqueda:
            consulta += " AND nombre ILIKE %s"
            parametros.append(f"%{busqueda}%")
            
        cursor.execute(consulta, parametros)
        filas = cursor.fetchall() # Aquí se define 'filas'
        conexion.close()
    except Exception as e:
        print(f"Error en la base de datos: {e}")
        return [] # Retorna una lista vacía si falla, evitando que el programa se rompa

    # Procesamos solo si 'filas' fue definido correctamente
    productos_procesados = []
    for f in filas:
        p_id, nombre, precio, stock, cat_id, img_nombre = f
        nombre_cat = mapeo_cat.get(str(cat_id), "SIN CATEGORIA")
        
        # Usamos tu función que busca el archivo en el disco
        ruta_img = encontrar_imagen_producto(p_id) 
        
        productos_procesados.append((p_id, nombre, precio, stock, nombre_cat, ruta_img))
        
    return productos_procesados

# Interfaz Web Principal
PLANTILLA_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Librería Oasis - Catálogo</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background-color: #f4f6f9; 
            color: #333; 
            margin: 0; 
            padding: 20px; 
        }
        .container { max-width: 1100px; margin: 0 auto; padding-bottom: 80px; }
        h1 { text-align: center; color: #2c3e50; margin-bottom: 25px; font-size: 32px; }
        
        /* ESTILOS DEL BANNER ROTATIVO */
        .slider-contenedor {
            position: relative;
            max-width: 100%;
            height: 220px;
            margin: 0 auto 30px auto;
            overflow: hidden;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.06);
            background-color: #2c3e50;
        }
        .slider-wrapper {
            display: flex;
            width: 100%;
            height: 100%;
            transition: transform 0.5s ease-in-out;
        }
        .slide {
            min-width: 100%;
            height: 100%;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            box-sizing: border-box;
            background-size: cover;
            background-position: center;
        }
        .slide::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(90deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, rgba(0,0,0,0.1) 100%);
            z-index: 1;
        }
        .slide-contenido {
            position: relative;
            z-index: 2;
            color: white;
            padding: 20px 50px;
            max-width: 600px;
            text-align: left;
        }
        .slide-badge {
            background-color: #e74c3c;
            color: white;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: bold;
            border-radius: 4px;
            text-transform: uppercase;
            display: inline-block;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        .slide-titulo { font-size: 26px; font-weight: bold; margin: 0 0 8px 0; color: #ffffff; }
        .slide-desc { font-size: 15px; line-height: 1.4; color: #e2e8f0; margin: 0; }
        
        /* Flechas del banner */
        .slider-flecha {
            position: absolute; top: 50%; transform: translateY(-50%);
            background-color: rgba(255, 255, 255, 0.25); color: white;
            border: none; width: 40px; height: 40px; border-radius: 50%;
            font-size: 18px; font-weight: bold; cursor: pointer; z-index: 3;
            transition: background-color 0.2s; display: flex; align-items: center; justify-content: center;
        }
        .slider-flecha:hover { background-color: rgba(255, 255, 255, 0.45); }
        .flecha-izq { left: 10px; }
        .flecha-der { right: 10px; }

        /* Buscador */
        .buscador-contenedor { text-align: center; margin: 25px 0 35px 0; }
        .buscador-input {
            width: 100%; max-width: 500px; padding: 12px 20px; font-size: 16px;
            border: 2px solid #bdc3c7; border-radius: 25px; outline: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: border-color 0.2s;
        }
        .buscador-input:focus { border-color: #3498db; }

        /* Categorías y Grid */
        .seccion-categoria { margin-top: 30px; margin-bottom: 20px; }
        .titulo-categoria {
            font-size: 20px; color: #2c3e50; border-bottom: 3px solid #3498db;
            padding-bottom: 5px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;
        }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 25px; }
        
        .card { 
            background: white; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.04); 
            text-align: center; border: 1px solid #e1e8ed; overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s; display: flex; flex-direction: column;
            justify-content: space-between; padding-bottom: 15px; position: relative;
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.08); }
        .card.agotado { opacity: 0.75; }
        
        .img-contenedor {
            width: 100%; height: 180px; background-color: #fcfcfc;
            display: flex; align-items: center; justify-content: center;
            border-bottom: 1px solid #f0f0f0; overflow: hidden; position: relative;
        }
        .img-producto { max-width: 100%; max-height: 100%; object-fit: contain; padding: 10px; }

        .badge-agotado {
            position: absolute; top: 12px; left: 12px; background-color: #e74c3c;
            color: white; padding: 5px 12px; font-size: 12px; font-weight: bold;
            border-radius: 4px; text-transform: uppercase; box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }

        .info-contenedor { padding: 15px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .nombre { font-size: 15px; font-weight: bold; color: #34495e; margin-bottom: 10px; line-height: 1.4; height: 42px; overflow: hidden; }
        .precio { font-size: 24px; color: #27ae60; font-weight: bold; margin: 5px 0; }
        
        .stock-info { font-size: 13px; font-weight: bold; padding: 5px 12px; border-radius: 20px; display: inline-block; margin-bottom: 12px; }
        .stock-info.agotado-texto { color: #c0392b; background: #fdedec; }

        .selector-cantidad { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 12px; }
        .btn-modificar {
            background-color: #e2e8f0; color: #4a5568; border: none; width: 32px; height: 32px; font-size: 16px;
            font-weight: bold; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;
            user-select: none;
        }
        .btn-modificar:hover { background-color: #cbd5e1; }
        .input-cantidad { width: 40px; text-align: center; font-size: 16px; font-weight: bold; border: 1px solid #cbd5e1; border-radius: 6px; padding: 3px 0; outline: none; }

        .btn-carrito {
            background-color: #3498db; color: white; border: none; padding: 10px 15px;
            font-size: 14px; font-weight: bold; border-radius: 8px; cursor: pointer;
            transition: background-color 0.2s; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;
        }
        .btn-carrito:hover { background-color: #2980b9; }
        .btn-carrito:disabled { background-color: #bdc3c7; cursor: not-allowed; }

        /* Botón Verde Flotante */
        .carrito-flotante {
            position: fixed; bottom: 25px; right: 25px; background-color: #2ecc71;
            color: white; padding: 15px 25px; border-radius: 30px; font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); display: flex; align-items: center; gap: 10px;
            cursor: pointer; z-index: 999; transition: transform 0.2s;
        }
        .carrito-flotante:hover { transform: scale(1.05); background-color: #27ae60; }
        .contador-badge { background-color: white; color: #2ecc71; border-radius: 50%; padding: 2px 8px; font-size: 14px; }

        /* Modal Carrito */
        .modal-carrito {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center;
        }
        .modal-contenido {
            background: white; padding: 25px; border-radius: 15px; width: 90%; max-width: 500px;
            max-height: 85vh; overflow-y: auto; box-shadow: 0 5px 25px rgba(0,0,0,0.2);
            position: relative; display: flex; flex-direction: column;
        }
        .modal-cerrar { position: absolute; top: 15px; right: 20px; font-size: 24px; font-weight: bold; color: #7f8c8d; cursor: pointer; }
        .modal-titulo { font-size: 22px; color: #2c3e50; margin-bottom: 15px; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }
        
        .carrito-lista { margin-bottom: 20px; }
        .carrito-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f0f0f0; font-size: 15px; }
        .item-detalles { flex-grow: 1; text-align: left; padding-right: 10px; }
        .item-nombre { font-weight: bold; color: #34495e; }
        .item-subtotal { color: #27ae60; font-weight: bold; margin-top: 2px; }
        .item-acciones { display: flex; align-items: center; gap: 8px; }
        .btn-accion-carrito { background-color: #edf2f7; border: none; width: 26px; height: 26px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 14px; }
        .btn-eliminar-item { background-color: #ffeded; color: #e74c3c; font-size: 12px; padding: 6px 10px; border: none; border-radius: 4px; cursor: pointer; }

        /* CARTEL MERCADO PAGO */
        .cartel-mercado-pago {
            background-color: #009ee3; background-image: linear-gradient(135deg, #009ee3 0%, #1d5fae 100%);
            border-radius: 12px; padding: 20px; margin-bottom: 20px; text-align: center; color: white; box-shadow: 0 4px 12px rgba(0, 158, 227, 0.25);
        }
        .mp-encabezado { font-size: 15px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 6px; color: #e0f4ff; }
        .mp-caja-alias { background-color: rgba(255, 255, 255, 0.15); border: 2px dashed rgba(255, 255, 255, 0.4); border-radius: 8px; padding: 12px; margin-bottom: 10px; }
        .mp-label { font-size: 12px; color: #bde6ff; text-transform: uppercase; font-weight: bold; }
        .mp-valor-alias { font-size: 28px; font-weight: 800; letter-spacing: 0.5px; margin: 2px 0 6px 0; color: #ffffff; }
        .mp-titular { font-size: 14px; font-weight: 500; color: #ffffff; margin-top: 2px; }
        .btn-copiar-mp { background-color: #ffffff; color: #009ee3; border: none; border-radius: 6px; padding: 6px 14px; font-size: 12px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

        .carrito-total-seccion { font-size: 20px; font-weight: bold; color: #2c3e50; text-align: right; margin-top: 5px; margin-bottom: 15px; border-top: 2px solid #ecf0f1; padding-top: 12px; }
        .btn-enviar-wa { background-color: #25d366; color: white; border: none; padding: 14px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; }
        
        /* Ajustes Mobile Responsivo */
        @media (max-width: 600px) {
            .slider-contenedor { height: 180px; }
            .slide-contenido { padding: 15px 35px; }
            .slide-titulo { font-size: 20px; }
            .slide-desc { font-size: 13px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✨ Librería Oasis ✨</h1>
        
        <div class="slider-contenedor">
            <button class="slider-flecha flecha-izq" id="slide-ant">❮</button>
            <div class="slider-wrapper" id="slider-wrapper">
                {% for oferta in ofertas %}
                <div class="slide" style="background-image: url('{{ oferta.imagen }}');">
                    <div class="slide-contenido">
                        <span class="slide-badge">{{ oferta.badge }}</span>
                        <h2 class="slide-titulo">{{ oferta.titulo }}</h2>
                        <p class="slide-desc">{{ oferta.descripcion }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>
            <button class="slider-flecha flecha-der" id="slide-sig">❯</button>
        </div>

        <div class="buscador-contenedor">
            <input type="text" id="buscador" class="buscador-input" placeholder="Escribí para buscar productos..." autocomplete="off">
        </div>
        
        <div id="contenedor-catalogo">
            {{ html_productos_inicial|safe }}
        </div>
    </div>

    <div class="carrito-flotante" id="btn-abrir-carrito">
        🛒 Mi Carrito 
        <span class="contador-badge" id="contador-productos">0</span>
    </div>

    <div class="modal-carrito" id="modal-carrito">
        <div class="modal-contenido">
            <span class="modal-cerrar" id="btn-cerrar-carrito">&times;</span>
            <div class="modal-titulo">🛒 Tu Pedido</div>
            
            <div id="carrito-lista-contenedor" class="carrito-lista"></div>
            
            <div class="carrito-total-seccion">
                Total: <span id="carrito-total-valor">$0.00</span>
            </div>

            <div id="seccion-pago-mp" class="cartel-mercado-pago" style="display: none;">
                <div class="mp-encabezado">💙 Pagá con Mercado Pago</div>
                <div class="mp-caja-alias">
                    <div class="mp-label">Alias para transferir</div>
                    <div class="mp-valor-alias" id="mp-texto-alias">oasis.1</div>
                    <button type="button" class="btn-copiar-mp" id="btn-copiar-alias" onclick="copyAlias()">📋 Copiar Alias</button>
                </div>
                <div class="mp-titular"><strong>Titular:</strong> Emiliano Damian Coronel</div>
            </div>
            
            <button class="btn-enviar-wa" id="btn-enviar-whatsapp">💬 Enviar pedido por WhatsApp</button>
        </div>
    </div>

    <script>
        let carrito = {}; 

        // Lógica del Slider Automatizado y por Botones
        const wrapper = document.getElementById('slider-wrapper');
        const btnAnt = document.getElementById('slide-ant');
        const btnSig = document.getElementById('slide-sig');
        const totalSlides = {{ ofertas|length }};
        let indiceActual = 0;
        let intervaloSlider;

        function mostrarSlide(indice) {
            if (indice >= totalSlides) indiceActual = 0;
            else if (indice < 0) indiceActual = totalSlides - 1;
            else indiceActual = indice;
            
            wrapper.style.transform = `translateX(-${indiceActual * 100}%)`;
        }

        function iniciarAutoSlide() {
            intervaloSlider = setInterval(() => {
                mostrarSlide(indiceActual + 1);
            }, 4000); 
        }

        function reiniciarIntervalo() {
            clearInterval(intervaloSlider);
            iniciarAutoSlide();
        }

        btnSig.addEventListener('click', () => { mostrarSlide(indiceActual + 1); reiniciarIntervalo(); });
        btnAnt.addEventListener('click', () => { mostrarSlide(indiceActual - 1); reiniciarIntervalo(); });
        
        iniciarAutoSlide();

        // Código de Buscador, Carrito y WhatsApp
        const buscador = document.getElementById('buscador');
        const contenedor = document.getElementById('contenedor-catalogo');
        const modal = document.getElementById('modal-carrito');
        const btnAbrir = document.getElementById('btn-abrir-carrito');
        const btnCerrar = document.getElementById('btn-cerrar-carrito');
        const listaContenedor = document.getElementById('carrito-lista-contenedor');
        const totalValorHTML = document.getElementById('carrito-total-valor');
        const btnWhatsApp = document.getElementById('btn-enviar-whatsapp');
        const seccionMP = document.getElementById('seccion-pago-mp');

        const NUMERO_TELEFONO_NEGOCIO = "5491137887546"; 

        function copyAlias() {
            const aliasTexto = document.getElementById('mp-texto-alias').innerText;
            const botonCopiar = document.getElementById('btn-copiar-alias');
            navigator.clipboard.writeText(aliasTexto).then(() => {
                botonCopiar.innerHTML = "✅ ¡Alias Copiado!";
                botonCopiar.style.backgroundColor = "#e8f8f0";
                botonCopiar.style.color = "#2ecc71";
                setTimeout(() => {
                    botonCopiar.innerHTML = "📋 Copiar Alias";
                    botonCopiar.style.backgroundColor = "#ffffff";
                    botonCopiar.style.color = "#009ee3";
                }, 2000);
            });
        }

        buscador.addEventListener('input', function(e) {
            const textoBusqueda = e.target.value;
            fetch(`/?buscar_ajax=${encodeURIComponent(textoBusqueda)}`)
                .then(response => response.text())
                .then(html => { contenedor.innerHTML = html; });
        });

        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-sumar')) {
                const pId = e.target.getAttribute('data-id');
                const input = document.getElementById(`cant-${pId}`);
                const maxStock = parseInt(input.getAttribute('max'));
                let valorActual = parseInt(input.value);
                if (valorActual < maxStock) input.value = valorActual + 1;
            }
            if (e.target.classList.contains('btn-restar')) {
                const pId = e.target.getAttribute('data-id');
                const input = document.getElementById(`cant-${pId}`);
                let valorActual = parseInt(input.value);
                if (valorActual > 1) input.value = valorActual - 1;
            }
        });

        function cambiarCantidadCarrito(id, cambio) {
            if (!carrito[id]) return;
            let nuevaCantidad = carrito[id].cantidad + cambio;
            if (nuevaCantidad <= 0) { eliminarDelCarrito(id); return; }
            if (nuevaCantidad > carrito[id].stockMax) { alert("Disculpá, no quedan más unidades."); return; }
            carrito[id].cantidad = nuevaCantidad;
            actualizarInterfazCarrito();
        }

        function eliminarDelCarrito(id) { delete carrito[id]; actualizarInterfazCarrito(); }

        function agregarAlCarrito(id, nombre, precio, stockMax) {
            const input = document.getElementById(`cant-${id}`);
            const cantidadAAgregar = parseInt(input.value);
            if (carrito[id]) {
                let chequeoCantidad = carrito[id].cantidad + cantidadAAgregar;
                if (chequeoCantidad > stockMax) { alert("No podés agregar más unidades."); return; }
                carrito[id].cantidad = chequeoCantidad;
            } else {
                carrito[id] = { nombre: nombre, precio: parseFloat(precio), cantidad: cantidadAAgregar, stockMax: parseInt(stockMax) };
            }
            input.value = 1;
            actualizarInterfazCarrito();
        }

        function actualizarInterfazCarrito() {
            let totalItems = 0; let precioTotal = 0; let htmlContenido = "";
            for (let id in carrito) {
                let item = carrito[id]; totalItems += item.cantidad; let subtotal = item.precio * item.cantidad; precioTotal += subtotal;
                htmlContenido += `<div class="carrito-item"><div class="item-detalles"><div class="item-nombre">${item.nombre}</div><div class="item-subtotal">$${subtotal.toLocaleString('es-AR', {minimumFractionDigits: 2})}</div></div><div class="item-acciones"><button class="btn-accion-carrito" onclick="cambiarCantidadCarrito(${id}, -1)">−</button><span><strong>${item.cantidad}</strong></span><button class="btn-accion-carrito" onclick="cambiarCantidadCarrito(${id}, 1)">+</button><button class="btn-eliminar-item" onclick="eliminarDelCarrito(${id})">🗑️</button></div></div>`;
            }
            document.getElementById('contador-productos').innerText = totalItems;
            totalValorHTML.innerText = `$${precioTotal.toLocaleString('es-AR', {minimumFractionDigits: 2})}`;
            if (totalItems === 0) { listaContenedor.innerHTML = `<div class="carrito-vacio-texto">El carrito está vacío.</div>`; btnWhatsApp.style.display = "none"; seccionMP.style.display = "none"; }
            else { listaContenedor.innerHTML = htmlContenido; btnWhatsApp.style.display = "block"; seccionMP.style.display = "block"; }
        }

        btnAbrir.addEventListener('click', () => { modal.style.display = "flex"; });
        btnCerrar.addEventListener('click', () => { modal.style.display = "none"; });
        window.addEventListener('click', (e) => { if (e.target === modal) modal.style.display = "none"; });

        btnWhatsApp.addEventListener('click', () => {
            let textoPedido = "✨ *NUEVO PEDIDO DESDE EL CATÁLOGO* ✨\\n----------------------------------------\\n";
            let totalFinal = 0;
            for (let id in carrito) {
                let item = carrito[id]; let subtotal = item.precio * item.cantidad; totalFinal += subtotal;
                textoPedido += `• *${item.cantidad}x* ${item.nombre} -> _$${subtotal.toLocaleString('es-AR', {minimumFractionDigits: 2})}\\_\\n`;
            }
            textoPedido += "----------------------------------------\\n";
            textoPedido += `*TOTAL ESTIMADO:* $${totalFinal.toLocaleString('es-AR', {minimumFractionDigits: 2})}`;
            window.open(`https://wa.me/${NUMERO_TELEFONO_NEGOCIO}?text=${encodeURIComponent(textoPedido)}`, '_blank');
        });
    </script>
</body>
</html>
"""

# Bloque AJAX para recarga interactiva de productos (CORREGIDO EL NOMBRE VISIBLE)
PLANTILLA_PRODUCTOS_AJAX = """
{% if productos %}
    {% set categorias_procesadas = [] %}
    {% for p in productos %}
        {% set cat_actual = p[4] if p[4] else 'Sin Categoría' %}
        {% if cat_actual not in categorias_procesadas %}
            {% if categorias_procesadas.append(cat_actual) %}{% endif %}
            
            <div class="seccion-categoria">
                <div class="titulo-categoria">{{ cat_actual }}</div>
                <div class="grid">
                    {% for prod in productos %}
                        {% set prod_cat = prod[4] if prod[4] else 'Sin Categoría' %}
                        {% if prod_cat == cat_actual %}
                        
                        <div class="card {% if prod[3] <= 0 %}agotado{% endif %}">
                            <div class="img-contenedor">
                                {% if prod[3] <= 0 %}
                                    <div class="badge-agotado">Agotado</div>
                                {% endif %}
          
                   <!-- Cambia tu línea actual por esta -->
    <!-- Cambia la línea de la imagen por esta línea más limpia -->
    <img class="img-producto" src="{{ prod[5] }}" alt="{{ prod[1] }}">
                            </div>
                            <div class="info-contenedor">
                                <div class="nombre">{{ prod[1] }}</div>
                                <div>
                                    <div class="precio">${{ "{:,.2f}".format(prod[2]) }}</div>
                                    
                                    {% if prod[3] > 0 %}
                                        <div style="height: 12px;"></div> 
                                        <div class="selector-cantidad">
                                            <button type="button" class="btn-modificar btn-restar" data-id="{{ prod[0] }}">−</button>
                                            <input type="number" id="cant-{{ prod[0] }}" class="input-cantidad" value="1" min="1" max="{{ prod[3] }}" readonly>
                                            <button type="button" class="btn-modificar btn-sumar" data-id="{{ prod[0] }}">+</button>
                                        </div>
                                        <button class="btn-carrito" onclick="agregarAlCarrito({{ prod[0] }}, '{{ prod[1] }}', {{ prod[2] }}, {{ prod[3] }} )">
                                            ➕ Agregar al carrito
                                        </button>
                                    {% else %}
                                        <div class="stock-info agotado-texto">Sin stock disponible</div>
                                        <button class="btn-carrito" disabled>❌ Agotado</button>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        {% endif %}
                    {% endfor %}
                </div>
            </div>
        {% endif %}
    {% endfor %}
{% else %}
    <div class="sin-resultados">❌ No se encontraron productos que coincidan.</div>
{% endif %}
"""

@app.route('/')
def home():
    try:
        buscar_ajax = request.args.get('buscar_ajax', None)
        
        if buscar_ajax is not None:
            lista_productos = obtener_productos_con_categorias(buscar_ajax)
            return render_template_string(PLANTILLA_PRODUCTOS_AJAX, productos=lista_productos)
        
        lista_productos = obtener_productos_con_categorias("")
        html_productos_inicial = render_template_string(PLANTILLA_PRODUCTOS_AJAX, productos=lista_productos)
        
        return render_template_string(
            PLANTILLA_HTML, 
            ofertas=BANNER_OFERTAS, 
            html_productos_inicial=html_productos_inicial
        )
    except Exception as e:
        return f"<h3>Error al cargar el catálogo: {e}</h3>", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
