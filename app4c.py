#region IMPORTACIONES
###################################################################################################################################################################
###################################################################################################################################################################


# IMPORTACIONES

# En esta sección se cargan todas las librerías que utilizará
# la aplicación web.

# - Streamlit: Construcción de la interfaz gráfica, es nuetro Jupyter o Spyder por así decirlo, nuestra plataforma de trabajo.
# - Pandas: Lectura y manipulación de la base de datos en nuestro caso el CSV construido.
# - os: Manejo de archivos y rutas (imágenes, carpetas, etc.).
# - Matplotlib: Creación de gráficas, específicamente el gráfico de radar.
# - NumPy: Operaciones matemáticas.
# - Scikit-Learn: Para recomendar motocicletas similares mediante K-Nearest Neighbors, transformando características en vectores
# entre los cuales se pueden medir distancias.


import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
###################################################################################################################################################################
###################################################################################################################################################################
# endregion

#region  CONFIGURACIÓN DE LA APLICACIÓN Y CONSTANTES
###################################################################################################################################################################
###################################################################################################################################################################


st.set_page_config(
    page_title="Catálogo Inteligente de Motos",
    layout="wide",
    page_icon="🏍️"
)

#CONSTANTES
CARPETA_IMAGENES = "resultado"

###################################################################################################################################################################
###################################################################################################################################################################
#endregion

#region  ENCABEZADO DE LA APLICACIÓN
###################################################################################################################################################################
###################################################################################################################################################################


# Construye la parte superior de la interfaz:
# - Título.
# - Descripción, el st.caption.
# - Métricas principales, como lo son los modelos disponibles, si está operativo el módulo de las comparaciones, marcas y guía


st.title("🏍️ Catálogo Inteligente de Motocicletas")

st.caption(
    "Consulta, comparación y recomendación de motocicletas para apoyar la toma de decisiones."
)

st.divider()

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Modelos",
        value="17",
        delta="🟡 En crecimiento",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="Marcas",
        value="4"
    )

with col3:
    st.metric(
        label="Comparador",
        value="Activo",
        delta="🟢 Funcional",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="Guía",
        value="Activo",
        delta="🟢 Funcional",
        delta_color="normal"
    )

st.divider()
###################################################################################################################################################################
###################################################################################################################################################################
#endregion

#region  ESTILOS CSS
###################################################################################################################################################################
###################################################################################################################################################################

# Define la apariencia visual de toda la aplicación:
# - Colores
# - Tipografías
# - Expanders
# - Tarjetas
# - Componentes personalizados


st.markdown("""
<style>

/* Fondo principal */
.stApp {
    background-color: #3D2740;
    color: white;
}

h1, h2, h3 {
    color: #D94AA7 !important;
}

.streamlit-expanderHeader {
    color: #D94AA7 !important;
    font-weight: bold;
}

div[data-baseweb="select"],
label {
    color: white !important;
}

/* TARJETAS */
.tarjeta-moto {
    background: #533658;
    border: 2px solid #D94AA7;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,.35);
    transition: .25s;
}

.tarjeta-moto:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,.45);
}

.tarjeta-titulo {
    color: #D94AA7;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
}

.tarjeta-info b {
    color: #F7B7E5;
}

</style>
            

""", unsafe_allow_html=True)
###################################################################################################################################################################
###################################################################################################################################################################
#endregion

#region CARGA DE DATOS Y PREPARACION DELOS MISMOS
###################################################################################################################################################################
###################################################################################################################################################################

df = pd.read_csv("Motos.csv", encoding="cp1252") #codificación de windows en español, como utf-8 y latini 
df.columns = df.columns.str.strip() #limpieza de los nombres de las columnas como espacios invisibles.

# Correcciones de nombres
df = df.rename(columns={
    "A¤o": "Año",
    "Transmisi¢n": "Transmisión",
    "Autonomia (Km)": "Autonomía (Km)",
    "Vmax (km/h)": "Velocidad Maxima (km/h)",
    "Pesomax (kg)": "Peso Máximo Soportado (kg)",
    "Enfriam.": "Enfriamiento"
})

#Limpiamos la columna modelo
df["Modelo"] = (
    df["Modelo"]
    .fillna("")
    .astype(str)
    .str.strip()
)

###################################################################################################################################################################
###################################################################################################################################################################
#endregion

#region FUNCIONES
###################################################################################################################################################################
###################################################################################################################################################################
def motos_similares(df, modelo, n=5):
    
    #Se definen las variables importantes, estas variables vas a ser las responsables directas de la comparación
    #y recomendacion de motos "similares" a la seleccionada por el cliente y que el asesor puede 
    #consultar en busqueda de mayores opciones. Estas son elegidas por su sencilla cuatificación.
    #Cada moto tendrá su propio conjunto de valores númericos como una huella de identidad.
    variables = [   
        "C. Motor",
        "Potencia (HP)",
        "Torque (Nm)",
        "Velocidad Maxima (km/h)",
        "Tanque (L)",
        "Autonomía (Km)"
    ]

    datos = df.copy() #copiamos el df para no modificar el original

    for col in variables:

        #convertimos texto en numero
        datos[col] = pd.to_numeric(
            datos[col],
            errors="coerce"
        )
        #conveirte errores en Nan y los rellena con la mediana
        datos[col] = datos[col].fillna(
            datos[col].median()
        )

    #Esto es una normalización de los datos
    scaler = StandardScaler()
    X = scaler.fit_transform(
        datos[variables]
    )

    #con los datos normalizados busca los vecinos más cercanos en este espacio matemático construido con
    #las "huellas digitales" de cada moto
    nn = NearestNeighbors(
        n_neighbors=n + 1 #el n+1 es porque se incluye así misma como su propio vecino
    )
    nn.fit(X)

    #Ahora encontramos la moto seleccionada y su posición en este espacio
    indice = datos[
        datos["Modelo"] == modelo
    ].index[0]
    posicion = datos.index.get_loc(indice)

    #esta instrucción mide las distancias para encontrar las más cercanas
    distancias, indices = nn.kneighbors(
        [X[posicion]]
    )

    #excluyes la original
    similares = datos.iloc[
        indices[0][1:]#    indices[0][0] es la misma moto
    ]

    return similares #devuelve el df con motos similares
###################################################################################################################################################################
###################################################################################################################################################################
#endregion

#region CATEGORIAS
###################################################################################################################################################################
###################################################################################################################################################################

#Se trata de los rubros principales bajo los cuales vamos a identificar las motos, estos definen la ficha técnica pero no solo se limitan a esto, pues también
#permiten cambiar el nombre de las columnas por uno más adecuado para el entendimiento del lector, o corregir algunos errores de la base de datos.

categorias = {

    "Información General": [
        "Marca",
        "Modelo",
        "Tipo",
        "Año"
    ],

    "Motor y Rendimiento": [
        "C. Motor",
        "Cilindros",
        "Potencia (HP)",
        "Torque (Nm)",
        "Velocidad Maxima (km/h)",
        "Enfriamiento",
        "Transmisión"
    ],

    "Consumo y Autonomía": [
        "Tanque (L)",
        "Consumo (km/L)",
        "Autonomía (Km)"
    ],

    "Frenos y Arranque": [
        "F. Delantero",
        "F. Trasero",
        "Arranque"
    ],

    "Capacidad": [
        "Peso Máximo Soportado (kg)",
        "Prueba"
    ]
}
###################################################################################################################################################################
###################################################################################################################################################################
#endregion
# =========================
# MODO
# =========================

modo = st.radio(
    "Selecciona una opción",
    ["Ficha Técnica", "Comparar", "Guía del Vendedor", "Acerca del proyecto"]
)

# =========================
# SELECTOR PRIMER MODO FICHA
# =========================

if modo == "Ficha Técnica":

    modelo = st.selectbox(
        "Selecciona un modelo",
        sorted(df["Modelo"].unique())
    )

# =========================
# BUSCAR MOTO
# =========================

    resultado = df[df["Modelo"] == modelo]

    if resultado.empty:

        st.error("Modelo no encontrado")
        st.stop()

    fila = resultado.iloc[0]

# =========================
# IMAGEN
# =========================

    ruta_imagen = os.path.join(CARPETA_IMAGENES, f"{modelo}.jpg")

    if os.path.exists(ruta_imagen):

        st.image(ruta_imagen, use_container_width=True)

# =========================
# VIDEO 1
# =========================

    if "URL" in df.columns:

        if pd.notna(fila["URL"]):

            video_url = str(fila["URL"]).strip()

            if (
                video_url != ""
                and video_url.lower() != "nan"
            ):

                st.subheader("🎥 Video de demostración")

                st.video(video_url)

# =========================
# VIDEO 2
# =========================

    if "URL2" in df.columns:

        if pd.notna(fila["URL2"]):

            video_url2 = str(fila["URL2"]).strip()

            if (
                video_url2 != ""
                and video_url2.lower() != "nan"
            ):

                st.subheader("🎥 Video adicional")

                st.video(video_url2)


# =========================
# FICHA TÉCNICA
# =========================

    st.header("📋 Ficha Técnica")


    for categoria, columnas in categorias.items():

        with st.expander(categoria, expanded=True):

            for columna in columnas:

                if columna in fila.index:

                    valor = fila[columna]

                    if pd.notna(valor) and str(valor).strip() != "":

                        st.markdown(
                            f"""
                            <span style='color:white'>
                                <b>{columna}:</b> {valor}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

    # ====================================================================================================PRUEBA


# =========================
# MOTOS SIMILARES
# =========================

    st.header("🤝 También te puede interesar")

    similares = motos_similares(
        df,
        modelo,
        n=4
    )

    # Crear una columna por cada recomendación
    columnas = st.columns(len(similares))

    for col, (_, moto) in zip(columnas, similares.iterrows()):

        modelo_sim = str(moto["Modelo"]).strip()

        ruta_img = os.path.join(CARPETA_IMAGENES, f"{modelo_sim}.jpg")

        with col:

            if os.path.exists(ruta_img):

                st.image(
                    ruta_img,
                    use_container_width=True
                )

            st.markdown(f"""
            <div class="tarjeta-moto">

            <div class="tarjeta-titulo">
            🏍️ {modelo_sim}
            </div>

            <div class="tarjeta-texto">

            <b>Marca:</b> {moto['Marca']}<br>

            <b>Motor:</b> {moto['C. Motor']} cc<br>

            <b>Potencia:</b> {moto['Potencia (HP)']} HP<br>

            <b>Torque:</b> {moto['Torque (Nm)']} Nm

            </div>

            </div>
            """, unsafe_allow_html=True)
    
    #    ====================================================================================================

elif modo == "Comparar":

    #modelos = sorted(df["Modelo"].unique())
    modelos = sorted(
        [
            m
            for m in df["Modelo"]
            .fillna("")
            .astype(str)
            .str.strip()
            .unique()
            if m
        ]
    )

    modelo1 = st.selectbox(
        "Moto 1",
        modelos,
        key="moto1"
    )

    modelo2 = st.selectbox(
        "Moto 2",
        modelos,
        key="moto2"
    )

    fila1 = df[df["Modelo"] == modelo1].iloc[0]

    fila2 = df[df["Modelo"] == modelo2].iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(modelo1)

        ruta1 = os.path.join(
            CARPETA_IMAGENES,
            f"{modelo1}.jpg"
        )

        if os.path.exists(ruta1):

            st.image(
                ruta1,
                use_container_width=True
            )

    with col2:

        st.subheader(modelo2)

        ruta2 = os.path.join(
            CARPETA_IMAGENES,
            f"{modelo2}.jpg"
        )

        if os.path.exists(ruta2):

            st.image(
                ruta2,
                use_container_width=True
            )

    st.header("⚖️ Comparación")

    filas = []

    for categoria, columnas in categorias.items():

        for columna in columnas:

            if columna in df.columns:

                filas.append({

                    "Característica": columna,

                    modelo1: fila1[columna],

                    modelo2: fila2[columna]

                })

    comparacion = pd.DataFrame(filas)


    max_hp = df["Potencia (HP)"].max() #normalizamos todos los resultado de HP de manera consistente

    st.dataframe(
        comparacion,
        use_container_width=True,
        hide_index=True
    )

    st.header("📊 Comparación Visual")
    
    
    metricas = [
        "Potencia (HP)",
        "Torque (Nm)",
        "Velocidad Maxima (km/h)",
        "Consumo (km/L)",
        "Autonomía (Km)",
        "Peso Máximo Soportado (kg)"
    ]

    #normalizamos################################

    valores1 = []
    valores2 = []

    for metrica in metricas:

        maximo = pd.to_numeric(
            df[metrica],
            errors="coerce"
        ).max()

        v1 = pd.to_numeric(
            fila1[metrica],
            errors="coerce"
        )

        v2 = pd.to_numeric(
            fila2[metrica],
            errors="coerce"
        )

        valores1.append(v1 / maximo)
        valores2.append(v2 / maximo)

    N = len(metricas) #creamos el radar############

    angulos = np.linspace(
        0,
        2 * np.pi,
        N,
        endpoint=False
    ).tolist()

    valores1 += valores1[:1]
    valores2 += valores2[:1]

    angulos += angulos[:1]

    fig, ax = plt.subplots(
        figsize=(8,8),
        subplot_kw=dict(polar=True)
    )

    # =========================
    # MOTO 1 (VERDE)
    # =========================

    ax.plot(
        angulos,
        valores1,
        linewidth=3,
        color="limegreen",
        label=modelo1
    )

    ax.fill(
        angulos,
        valores1,
        color="limegreen",
        alpha=0.35
    )

    # =========================
    # MOTO 2 (ROJO)
    # =========================

    ax.plot(
        angulos,
        valores2,
        linewidth=3,
        color="red",
        label=modelo2
    )

    ax.fill(
        angulos,
        valores2,
        color="red",
        alpha=0.35
    )

    # =========================
    # ETIQUETAS
    # =========================

    ax.set_xticks(angulos[:-1])

    ax.set_xticklabels(
        [
            "HP",
            "Torque",
            "V. Máx",
            "Consumo",
            "Autonomía",
            "Carga"
        ],
        fontsize=14,      # tamaño letra
        fontweight="bold"
    )

    # =========================
    # ESCALA
    # =========================

    ax.set_ylim(0, 1)

    # tamaño de números radiales
    ax.tick_params(
        axis='y',
        labelsize=12
    )

    # =========================
    # TÍTULO
    # =========================

    ax.set_title(
        "Comparación de Desempeño",
        fontsize=18,
        fontweight="bold",
        pad=30
    )

    # =========================
    # LEYENDA
    # =========================

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.10),
        fontsize=12
    )

    ax.grid(
        color="gray",
        alpha=0.3
    )

    st.pyplot(fig)


################## TERCER MODO #####################

elif modo == "Guía del Vendedor":

    st.header("🎓 Guía del Vendedor")

    with st.expander("¿Qué es la potencia?"):

        st.write("""
        La potencia indica la capacidad del motor para realizar
        trabajo en un determinado tiempo.

        En las motocicletas suele expresarse en Caballos de Fuerza
        (HP).

        Una mayor potencia generalmente significa:

        • Mejor aceleración.
        • Mayor velocidad máxima.
        • Mejor desempeño en carretera.

        Mientras el torque representa la fuerza de empuje,
        la potencia representa qué tan rápido puede utilizarse
        esa fuerza.

        Una forma sencilla de explicarlo a un cliente es:

        "El torque ayuda a arrancar y subir pendientes;
        la potencia ayuda a alcanzar y mantener velocidades altas."
        """)

    with st.expander("¿Qué son los caballos de fuerza (HP)?"):

        st.write("""
        Los HP (Horse Power) indican la potencia del motor.

        La potencia representa qué tan rápido puede realizar trabajo
        el motor.

        Un mayor número de HP generalmente significa:

        • Mejor aceleración.
        • Mayor velocidad máxima.
        • Mejor desempeño en carretera.

        Es una de las especificaciones más importantes para
        comparar motocicletas.
        """)

    with st.expander("¿Por qué la potencia se alcanza a ciertas RPM?"):

        st.write("""
        El motor no produce su máxima potencia todo el tiempo.

        Por ejemplo:

        24 HP @ 8,000 RPM

        significa que el motor entrega 24 HP cuando gira
        a 8,000 revoluciones por minuto.

        Antes o después de ese punto la potencia suele ser menor.

        Esto ayuda a entender cómo se comporta la moto
        durante la conducción.
        """)

    with st.expander("¿Qué es el torque?"):

        st.write("""
        El torque es la fuerza de empuje que genera el motor.

        Un torque elevado ayuda en:

        • Arranques rápidos.
        • Subidas.
        • Llevar pasajero o carga.
        • Recuperaciones de velocidad.

        Mientras la potencia ayuda a alcanzar velocidad,
        el torque ayuda a mover la motocicleta con fuerza.
        """)

    with st.expander("¿Por qué el torque y la potencia tienen RPM diferentes?"):

        st.write("""
        Es normal que una motocicleta alcance su torque máximo
        antes que su potencia máxima.

        El torque suele aparecer a RPM medias.

        La potencia continúa aumentando mientras el motor
        sigue girando más rápido.

        Por eso una ficha técnica puede mostrar:

        • Torque máximo a 6,500 RPM
        • Potencia máxima a 8,000 RPM

        Esto no significa que exista un error,
        sino que el motor entrega características distintas
        según el régimen de giro.
        """)

    with st.expander("¿Qué es la cilindrada (C. Motor)?"):

        st.write("""
        La cilindrada es el volumen total de los cilindros del motor,
        normalmente expresado en centímetros cúbicos (cc).

        En general:

        • Más cilindrada = más potencia y velocidad.
        • Menos cilindrada = mejor consumo de combustible.

        Ejemplo:
        Una moto de 125 cc suele enfocarse en economía,
        mientras que una de 250 cc ofrece mejor desempeño.
        """)

    with st.expander("¿Qué son los cilindros?"):

        st.write("""
        Los cilindros son las cámaras donde ocurre la combustión.

        Una moto con más cilindros suele tener:

        • Funcionamiento más suave.
        • Mayor potencia.
        • Mejor desempeño a altas RPM.

        Sin embargo, también puede consumir más combustible
        y requerir mayor mantenimiento.
        """)

    with st.expander("¿Qué es la velocidad máxima (Vmax)?"):

        st.write("""
        Es la mayor velocidad que la motocicleta puede alcanzar
        en condiciones ideales.

        La velocidad real puede variar dependiendo de:

        • Peso del conductor.
        • Pendientes.
        • Viento.
        • Estado de la carretera.

        Debe tomarse como una referencia comparativa.
        """)

    with st.expander("¿Qué significa el enfriamiento?"):

        st.write("""
        El sistema de enfriamiento evita que el motor
        se sobrecaliente.

        Tipos comunes:

        • Aire
        • Aceite
        • Líquido

        Los sistemas por líquido suelen controlar mejor
        la temperatura en trayectos largos y uso intensivo.
        """)

    with st.expander("¿Qué es la transmisión?"):

        st.write("""
        La transmisión envía la potencia del motor
        hacia la rueda trasera.

        Tipos comunes:

        • Manual
        • Semiautomática
        • Automática

        La elección depende del estilo de conducción
        y experiencia del usuario.
        """)

    with st.expander("¿Qué significa el consumo (km/L) o rendimiento?"):

        st.write("""
        Indica cuántos kilómetros puede recorrer la motocicleta
        con un litro de combustible.

        Un número más alto significa mejor rendimiento
        y menor gasto de gasolina.

        Ejemplo:

        40 km/L consume más combustible que una moto
        que alcanza 55 km/L.
        """)

    with st.expander("¿Qué es la autonomía?"):

        st.write("""
        La autonomía es la distancia aproximada que puede
        recorrer la motocicleta con un tanque lleno.

        Se calcula considerando:

        • Capacidad del tanque.
        • Consumo de combustible.

        Una mayor autonomía permite realizar recorridos
        más largos sin necesidad de repostar.
        """)

    with st.expander("¿Qué tipos de frenos existen?"):

        st.write("""
        Los frenos permiten reducir la velocidad
        o detener la motocicleta.

        Los más comunes son:

        • Disco
        • Tambor

        Generalmente los frenos de disco ofrecen
        mejor capacidad de frenado y disipación de calor.
        """)

    with st.expander("¿Qué sistemas de arranque existen?"):

        st.write("""
        El arranque es el método utilizado para encender
        la motocicleta.

        Los más comunes son:

        • Eléctrico
        • Pedal (kick)
        • Combinado

        El arranque eléctrico suele ser el más cómodo
        para el usuario.
        """)

################################# CUARTO MODO, ACERCA DEL PROYECTO Y DEL AUTOR, MEDIOS DE CONTACTO ######################################

elif modo == "Acerca del proyecto":

    st.title("🏍️ Catálogo Inteligente de Motocicletas")
    st.markdown("### Presentación ejecutiva del sistema")
    st.divider()

    # ---------------- PROBLEMA + PROYECTO ----------------
    st.markdown("## 🧭 Descripción del proyecto")

    st.markdown("""
    Plataforma desarrollada para facilitar la consulta, comparación y análisis de motocicletas dentro del catálogo de la empresa.

    El objetivo es mejorar la toma de decisiones tanto para asesores de venta como para clientes,
    centralizando información técnica y permitiendo explorar alternativas de forma rápida e intuitiva.
    """)

    st.divider()

    # ---------------- OBJETIVOS ----------------
    st.markdown("## 🎯 Objetivos del sistema")

    st.markdown("""
    - Centralizar la información técnica de motocicletas.
    - Facilitar la comparación entre modelos.
    - Agilizar la atención al cliente en piso de venta.
    - Reducir el tiempo de búsqueda de especificaciones.
    - Servir como base para futuras herramientas de análisis y recomendación.
    """)

    st.divider()

    # ---------------- FUNCIONALIDADES ----------------
    st.markdown("## ⚙️ Funcionalidades actuales")

    st.markdown("""
    - ✅ Consulta de especificaciones técnicas por modelo
    - ✅ Filtros por marca, cilindrada y tipo
    - ✅ Comparador de motocicletas lado a lado
    - ✅ Sistema de recomendación basado en similitud
    - ✅ Visualización estructurada de catálogo
    """)

    st.divider()

    # ---------------- IMPACTO ----------------
    st.markdown("## 📊 Impacto esperado")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Tiempo de consulta", "-70%")

    with col2:
        st.metric("Comparación", "Más rápida")

    with col3:
        st.metric("Experiencia cliente", "Mejorada")

    st.divider()

    # ---------------- ROADMAP ----------------
    st.markdown("## 🚀 Roadmap")

    st.markdown("""
    - 🧠 Recomendación más avanzada (modelo predictivo)
    - 📊 Integración con datos de ventas reales
    - 🔗 Conexión con inventario en tiempo real
    - 📱 Migración a aplicación móvil
    - 📈 Dashboard de análisis para gerencia
    """)

    st.divider()

    # ---------------- ARQUITECTURA ----------------
    st.markdown("## ⚙️ Arquitectura del sistema")

    st.code("""
CSV / Base de datos
      ↓
Pandas (procesamiento)
      ↓
Streamlit (interfaz actual)
      ↓
Futuro: FastAPI + App móvil
""")

    st.divider()

    # ---------------- DESARROLLADOR ----------------
    st.markdown("## 👨‍💻 Desarrollador")

    st.markdown("""
    **Giovanni Jefté Aguilar Carmona**  
    Licenciado en Física - Facultad de Ciencias, UNAM

    ### Intereses principales:
    - Ciencia de datos
    - Sistemas complejos
    - Programación aplicada
    - Análisis de información

    Este proyecto forma parte de una iniciativa de desarrollo de herramientas internas orientadas
    a la optimización de procesos de consulta y decisión.
    """)

    st.divider()

    # ---------------- CV ----------------
    st.markdown("## 📄 Currículum Vitae")

    with open("CV_Aguilar Carmona Giovanni Jefté.pdf", "rb") as file:
        st.download_button(
            label="📄 Descargar CV",
            data=file,
            file_name="CV_Giovanni_Aguilar.pdf",
            mime="application/pdf"
        )

    st.divider()

    # ---------------- CONTACTO ----------------
    st.markdown("## 📬 Contacto")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.link_button("📧 Correo (Institucional)", "mailto:gjaguilarc@suburbia.com.mx")

    with col2:
        st.link_button("📧 Correo", "mailto:gj.aguilar852@gmail.com")

    with col3:
        st.link_button("💻 GitHub", "https://github.com/Tzekelkan852")




############ FIRMA DEL CATALOGO ##########################

st.divider()

st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 13px;'>
        🏍️ Catálogo Inteligente de Motocicletas<br>
        Desarrollado por <b>Giovanni J. Aguilar</b> · UNAM<br>
        Proyecto interno de análisis y optimización de catálogo
    </div>
    """,
    unsafe_allow_html=True
)