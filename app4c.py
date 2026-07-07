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
        value="26",
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
    #ALGORITMO Nearest Neighbors.
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

###################################################################################################################################################################
###################################################################################################################################################################
#MODO

#Pieza angular del codigo, es donde nacen los cuatro modos
modo = st.radio(
    "Selecciona una opción",
    ["Ficha Técnica", "Comparar", "Guía del Vendedor", "Acerca del proyecto", "Red"]
)

###################################################################################################################################################################
###################################################################################################################################################################

#region MODO 1 FICHA Y SUGERENCIA
###################################################################################################################################################################
###################################################################################################################################################################

#region FICHA TECNICA

# Muestra un menú desplegable con todos los modelos disponibles en el catálogo para que el vendedor o usuario
# seleccione la motocicleta que desea consultar.

if modo == "Ficha Técnica": #aqui comienza la primera anidación de todo este segmento, así mismo cabe resaltar, que sería mucho más sencillo
                            #definir un montón de funciones en este bloque y el siguiente para tener un resultado más limpio, pero eso es
                            #únicamente tema de optimización, por ahora esto basta.
    modelo = st.selectbox(
        "Selecciona un modelo",
        sorted(df["Modelo"].unique())  #Elimina modelos repetidos, en nuestra base de datos esto no ocurre, pues la he creado a mano, 
                                        #identificando ademas cada modelo con su año, pero para el futuro podría ser útil.
    )

# ==================================================
# BUSCAR MOTO

# Busca en el df la fila correspondiente al modelo seleccionado.
    resultado = df[df["Modelo"] == modelo]

    if resultado.empty:

        st.error("Modelo no encontrado") #si no se encuentra ningún registro detiene la ejecución
        st.stop()

    fila = resultado.iloc[0] # Extrae la fila encontrada para facilitar el acceso a cada característica.

# =========================
# IMAGEN

    # Construye automáticamente la ruta donde debería encontrarse la imagen de la motocicleta.
    ruta_imagen = os.path.join(CARPETA_IMAGENES, f"{modelo}.jpg")

    if os.path.exists(ruta_imagen): # Solo muestra la imagen si el archivo existe.
        st.image(ruta_imagen, use_container_width=True)

# =========================
# VIDEO 1

# Si existe la columna URL y contiene un enlace válido, muestra el video principal de la motocicleta y secundario respectivamente.

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

# Con lo anterior definido, construímos por fín la ficha técnica
# Recorre las categorías definidas al inicio del programa y organiza la información en expanders para facilitar la lectura.

    st.header("📋 Ficha Técnica")


    for categoria, columnas in categorias.items():

        with st.expander(categoria, expanded=True): # Para cada categoría se muestran únicamente las
                                                    # columnas que existan y cuyo valor no esté vacío.
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
#endregion
###################################################################################################################################################################
###################################################################################################################################################################

#region SUGERENCIA DE MOTO
# ===========================================================================
# MOTOS SIMILARES
# =========================

# Utiliza el sistema de recomendación basado en Machine Learning para sugerir motocicletas con características similares a la
# seleccionada por el usuario. Usando la función ya explicada, que genera un espacio matemático similar a un vector y calcula
# las distancias.

    st.header("🤝 También te puede interesar")

    similares = motos_similares(
        df,
        modelo,
        n=4
    )

# Crea una columna por cada motocicleta recomendada para mostrarlas horizontalmente en forma de tarjetas.
    columnas = st.columns(len(similares))

    for col, (_, moto) in zip(columnas, similares.iterrows()):# Recorre simultáneamente las columnas creadas y cada una de las motocicletas recomendadas.
    # En este caso iterrows devuelve dos valores "indice, fila" por eso el (_, moto) porque desechamos el índice, de nada nos sirve ahora.

        modelo_sim = str(moto["Modelo"]).strip()# Obtiene el nombre del modelo y elimina posibles espacios sobrantes para construir 
    # correctamente la ruta de la imagen.

        ruta_img = os.path.join(CARPETA_IMAGENES, f"{modelo_sim}.jpg") #Busca la imagen

        with col: # Todo el contenido generado dentro de este bloque aparecerá en la columna asignada a la motocicleta actual.

            if os.path.exists(ruta_img): # Si existe, se muestra

                st.image(
                    ruta_img,
                    use_container_width=True
                )

            # Genera una tarjeta utilizando HTML y CSS personalizado para mostrar de forma compacta la información más
            # relevante de cada motocicleta recomendada. 
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
#endregion
###################################################################################################################################################################
###################################################################################################################################################################
    
#endregion


#region MODO 2 COMPARACION TEXTUAL Y GRÁFICA
###################################################################################################################################################################
###################################################################################################################################################################

#region Textual

# Se ejecuta cuando el usuario selecciona el modo "Comparar", permitiendo analizar dos motocicletas lado a lado, inspirado
# en las típicas páginas que comparan entre procesadores de computadoras resaltando caracterísitcas frente a otras.
elif modo == "Comparar":

    # Obtiene todos los modelos disponibles del catálogo, elimina posibles valores vacíos o duplicados y los ordena alfabéticamente.
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

    #Creamos dos selectores independientes
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

    # Localiza dentro del DataFrame la información correspondiente a cada uno de los modelos seleccionados.
    fila1 = df[df["Modelo"] == modelo1].iloc[0]

    fila2 = df[df["Modelo"] == modelo2].iloc[0]

    col1, col2 = st.columns(2) # Divide la pantalla en dos columnas para mostrar visualmente ambas motocicletas una junto a la otra.


    with col1: #primera moto

        st.subheader(modelo1)

        ruta1 = os.path.join(
            CARPETA_IMAGENES,
            f"{modelo1}.jpg"
        )

        if os.path.exists(ruta1): #si esxiste imagen (que procuro sea así) se muestra

            st.image(
                ruta1,
                use_container_width=True
            )

    with col2: #moto2

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
    ###############################################################################################################################
    ###############################################################################################################################    
        
    # Inicia la construcción de la tabla comparativa, donde se mostrarán las especificaciones técnicas de ambas motocicletas.
    st.header("⚖️ Comparación")

    filas = []
    # Recorre cada categoría definida previamente y extrae las características correspondientes para construir la comparación.
    for categoria, columnas in categorias.items():

        for columna in columnas:

            if columna in df.columns:

                filas.append({ # Cada característica se almacena como un diccionario, donde la primera columna indica el nombre de la
                               # especificación y las siguientes contienen los valores de ambas motocicletas.
                    "Característica": columna,

                    modelo1: fila1[columna],

                    modelo2: fila2[columna]

                })

    comparacion = pd.DataFrame(filas) #Convierte la lista de diccionarios en un df para facilitar su procesamiento.
    
    # Muestra la tabla comparativa ocupando todo el ancho disponible y ocultando el índice del df.
    st.dataframe(
        comparacion,
        use_container_width=True,
        hide_index=True
    )
#endregion
###################################################################################################################################################################
###################################################################################################################################################################

#region  COMPARACIÓN VISUAL (GRÁFICA DE RADAR)

# Genera una gráfica de radar para comparar de forma visual las principales características de ambas motocicletas.

    max_hp = df["Potencia (HP)"].max() #normalizamos todos los resultado de HP de manera consistente

    st.header("📊 Comparación Visual")
    
    # Define las variables numéricas que se utilizarán para construir el radar. Cada una representará un eje de la gráfica.
    metricas = [
        "Potencia (HP)",
        "Torque (Nm)",
        "Velocidad Maxima (km/h)",
        "Consumo (km/L)",
        "Autonomía (Km)",
        "Peso Máximo Soportado (kg)"
    ]
    # ====================================================================================================
    # NORMALIZACIÓN DE DATOS (Paréntesis muy necesario sobra la normalización a uno)
    # =================================================================================================

    # Cada métrica posee unidades y escalas diferentes, Por ejemplo:
    #
    # Potencia:        20 - 40 HP
    # Velocidad:      100 - 180 km/h
    # Autonomía:      250 - 700 km
    #
    # Si se compararan directamente, las variables con valores más grandes dominarían la gráfica.
    #
    # Para evitarlo, cada valor se divide entre el máximo existente dentro del catálogo, obteniendo valores
    # entre 0 y 1. Las normalizaciones a la unidad son tipicas dentro de las matemáticas, la normalización
    # más cotidiana de esto es manejar así las probabilidades, simplemente se escalan a un interválo.


    valores1 = []# Almacenarán los valores normalizados de ambas motos.
    valores2 = []

    for metrica in metricas:# Recorre cada una de las métricas seleccionadas y calcula su valor normalizado para ambas motos.
        # Obtiene el mayor valor registrado en el catálogo para la métrica actual. Servirá como referencia
        # para normalizar los datos. Todo para obtener una mejor visulización.
        maximo = pd.to_numeric(
            df[metrica],
            errors="coerce"
        ).max()
        #convierte a tipo numerico 
        v1 = pd.to_numeric(
            fila1[metrica],
            errors="coerce"
        )

        v2 = pd.to_numeric(
            fila2[metrica],
            errors="coerce"
        )

        valores1.append(v1 / maximo)#Normalización
        valores2.append(v2 / maximo)

    # =========================
    # CONSTRUCCIÓN DEL RADAR
    # =========================

    # Determina el número de ejes que tendrá la gráfica, uno por cada métrica dada.
    N = len(metricas)
    # Calcula la posición angular de cada eje dentro del círculo.
    angulos = np.linspace(
        0,
        2 * np.pi,
        N,
        endpoint=False
    ).tolist()

    # Para cerrar correctamente el polígono del radar, se vuelve a agregar el primer valor al final de cada lista.
    # De otro modo no se cierra.
    valores1 += valores1[:1]
    valores2 += valores2[:1]

    angulos += angulos[:1]

    #Creamo una figura polar, ya que usamos radianes para las posiciones angulares.
    fig, ax = plt.subplots(
        figsize=(8,8),
        subplot_kw=dict(polar=True)
    )

    # MOTO 1 (VERDE) contorno y área
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
    # MOTO 2 (ROJO)
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

    # ETIQUETAS
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


    # ESCALA (Entre cero y uno), aqui se encuentra la gran ventaja de la normalizacion.
    ax.set_ylim(0, 1)

    # tamaño de números radiales
    ax.tick_params(
        axis='y',
        labelsize=12
    )

    # =========================
    # TÍTULO
    ax.set_title(
        "Comparación de Desempeño",
        fontsize=18,
        fontweight="bold",
        pad=30
    )

    # LEYENDA
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
#endregion
###################################################################################################################################################################
###################################################################################################################################################################

#endregion


#region MODO 3 GUIA DEL VENDEDOR
###################################################################################################################################################################
###################################################################################################################################################################

elif modo == "Guía del Vendedor":

    st.header("🎓 Guía del Vendedor")

    with st.expander("🏍️ ¿Qué tipos de motocicletas existen y qué las diferencia?"):
        st.write("""
        Clasificar las motocicletas ayuda al vendedor a identificar rápidamente qué tipo de usuario es el cliente y ofrecerle el modelo ideal. Aquí están los segmentos principales:

        * **Urbanas / Street (Trabajo):** Motos de baja cilindrada (100cc a 250cc), ligeras y muy ágiles. Su enfoque principal es la economía de combustible y la durabilidad en el tráfico diario. Tienen una posición de manejo erguida y cómoda.
          * *Ideal para:* Repartidores, estudiantes y personas que buscan su primer vehículo para ir al trabajo.

        * **Scooters y Maxi-Scooters:**
          Motos automáticas (transmisión CVT) donde los pies van apoyados en una plataforma interna en lugar de estribos laterales. Suelen tener espacio de carga debajo del asiento. Las *Maxi-Scooters* tienen motores más grandes (300cc+) para salir a carretera.
          * *Ideal para:* Quienes buscan máxima comodidad, facilidad de manejo (sin cambios) y protección contra salpicaduras en ciudad.

        * **Deportivas (Sport):**
          Inspiradas en las motos de carreras. Tienen carenados aerodinámicos (plásticos que cubren el motor) y manubrios bajos que obligan al piloto a inclinarse hacia adelante. Priorizan la velocidad máxima, el paso por curva y la aceleración alta.
          * *Ideal para:* Amantes de la velocidad, la adrenalina y quienes planean rodar en circuitos o autopistas los fines de semana.

        * **Doble Propósito (Dual Sport / Adventure):**
          Motos diseñadas para funcionar tanto en asfalto como en caminos de tierra, arena o empedrados. Tienen suspensiones muy altas y suaves para absorber baches, llantas con tacos (gajos) y una posición de manejo alta que da mucha visibilidad.
          * *Ideal para:* Ciudades con muchos baches/topes, o aventureros que quieren explorar rutas de terracería y viajar sin preocuparse por el estado del camino.

        * **Chopper / Custom / Cruiser:**
          Motos de estilo clásico, inspiradas en el diseño americano tradicional. Tienen asientos bajos, manubrios altos o retrasados, y descansapiés adelantados que permiten una postura de manejo muy relajada ("estilo sillón"). Suelen priorizar el torque sobre la velocidad de punta.
          * *Ideal para:* Conductores que buscan comodidad en carretera, un estilo rebelde/clásico y disfrutan pasear los fines de semana a ritmos tranquilos.

        * **Touring / Viajeras:**
          Verdaderos "autos de dos ruedas". Son motocicletas grandes, pesadas, con motores potentes, enormes parabrisas, maletas rígidas integradas y asientos ultra cómodos (tanto para piloto como pasajero). Suelen incluir tecnología avanzada como reversa, calefacción y pantallas de navegación.
          * *Ideal para:* Viajeros de largas distancias que pasan horas o días enteros en autopista.

        **Tip de venta rápida:** *Si el cliente busca ahorrar ➡️ **Urbana o Scooter**.*
        *Si el cliente se queja de los baches o viaja a pueblos ➡️ **Doble Propósito**.*
        *Si el cliente busca estilo y viajar los domingos ➡️ **Cruiser/Chopper**.*
        """)

    with st.expander("¿Qué es la potencia?"):
        st.write("""
        La potencia indica la capacidad del motor para realizar trabajo en un determinado tiempo. 
        En las motocicletas suele expresarse en Caballos de Fuerza (HP).

        Una mayor potencia generalmente significa:
        * Mejor aceleración a altas revoluciones.
        * Mayor velocidad máxima.
        * Mejor desempeño en carretera y rebases.

        Mientras el torque representa la fuerza de empuje, la potencia representa qué tan rápido puede utilizarse esa fuerza.

        **Forma sencilla de explicarlo a un cliente:**
        *"El torque ayuda a arrancar, cargar peso y subir pendientes; la potencia ayuda a alcanzar y mantener velocidades altas."*
        """)

    with st.expander("¿Qué son los caballos de fuerza (HP)?"):
        st.write("""
        Los HP (*Horse Power*) son la unidad de medida de la potencia del motor. Representan la rapidez con la que el motor puede entregar su fuerza.

        Un mayor número de HP generalmente se traduce en una velocidad final más alta y una aceleración sostenida en autopista. Es una de las especificaciones clave para comparar el rendimiento entre motocicletas de la misma cilindrada.
        """)

    with st.expander("¿Por qué la potencia se alcanza a ciertas RPM?"):
        st.write("""
        El motor no produce su máxima potencia en todo momento; necesita girar a cierta velocidad para alcanzar su punto óptimo.

        Por ejemplo: **24 HP @ 8,000 RPM** significa que el motor entrega sus 24 caballos completos justo cuando el tacómetro marca 8,000 revoluciones por minuto. Antes de llegar a ese punto, o si se sobrepasa, la potencia disponible será menor.
        """)

    with st.expander("¿Qué es el torque?"):
        st.write("""
        El torque (o par motor) es la fuerza de torsión o empuje puro que genera el motor. Es lo que sientes como "patada" al acelerar.

        Un torque elevado o a bajas RPM ayuda en:
        * Arranques rápidos desde cero.
        * Subir pendientes pronunciadas sin perder fuerza.
        * Llevar pasajero o carga pesada sin que el motor se fatigue.
        """)

    with st.expander("¿Por qué el torque y la potencia tienen RPM diferentes?"):
        st.write("""
        Es el comportamiento natural de un motor de combustión. El torque máximo (la fuerza) suele alcanzarse a RPM medias, mientras que la potencia máxima (la velocidad para usar esa fuerza) se logra a RPM más altas, cuando el motor gira más rápido.

        Por eso una ficha técnica muestra, por ejemplo:
        * **Torque máximo:** 6,500 RPM
        * **Potencia máxima:** 8,000 RPM

        Esto describe la curva de rendimiento de la moto y ayuda al vendedor a saber en qué momento el motor responderá con más fuerza o con más velocidad.
        """)

    with st.expander("¿Qué es la cilindrada (C. Motor)?"):
        st.write("""
        La cilindrada es el volumen útil total de los cilindros del motor, expresado en centímetros cúbicos (cc). 

        A grandes rasgos:
        * **Mayor cilindrada:** Mayor capacidad de admisión de mezcla, lo que suele derivar en más potencia y torque, pero incrementa el consumo.
        * **Menor cilindrada:** Motores más compactos, ideales para entornos urbanos debido a su alta economía de combustible.
        """)

    with st.expander("¿Qué son los cilindros y cómo influye su número?"):
        st.write("""
        El cilindro es la cavidad donde se mueve el pistón y ocurre la combustión. Las motocicletas pueden tener uno (monocilíndricas), dos (bicilíndricas) o más cilindros.

        * **Un solo cilindro:** Entrega mucho torque a bajas revoluciones, es económico y fácil de mantener, pero genera más vibraciones.
        * **Más cilindros (2 o 4):** Entregan una marcha mucho más suave, menos vibraciones y mayor potencia a altas RPM, ideal para viajes largos o altas velocidades.
        """)

    with st.expander("¿Qué es la velocidad máxima (Vmax)?"):
        st.write("""
        Es la velocidad límite que la motocicleta puede alcanzar bajo condiciones de laboratorio o pistas ideales (sin viento en contra, piso plano y piloto con peso estándar).

        En el mundo real, la velocidad máxima variará según el peso del conductor, los acompañantes, las pendientes del camino y la altitud sobre el nivel del mar. Debe usarse únicamente como una referencia comparativa.
        """)

    with st.expander("¿Qué diferencias hay en los sistemas de enfriamiento?"):
        st.write("""
        El sistema de enfriamiento disipa el calor extremo del motor para evitar daños:

        * **Por Aire:** Simple, económico y libre de mantenimiento. Depende del movimiento de la moto para enfriarse. Ideal para ciudad y bajas cilindradas.
        * **Por Aceite:** Utiliza el mismo lubricante del motor pasándolo por un radiador. Ofrece mejor control térmico que el aire puro.
        * **Líquido (Refrigerante):** Utiliza un radiador y líquido anticongelante. Es el más eficiente; mantiene el motor a una temperatura óptima constante, ideal para trayectos largos, tráfico pesado o altas prestaciones.
        """)

    with st.expander("¿Qué tipos de transmisión existen?"):
        st.write("""
        La transmisión gestiona la potencia del motor y la envía a la rueda trasera:

        * **Manual (Con embrague/clutch):** El piloto controla los cambios de marcha manualmente. Ofrece el máximo control del motor.
        * **Semiautomática:** Permite cambiar de marchas con el pie pero no requiere palanca de embrague (común en motos de trabajo o tipo *Underbone*).
        * **Automática (CVT):** No existen los cambios de marcha. Solo se acelera y frena (característico de las *Scooters*). Ideal para máxima comodidad urbana.
        """)

    with st.expander("¿Qué significa el rendimiento de combustible (km/L)?"):
        st.write("""
        Indica la distancia promedio que la motocicleta puede recorrer por cada litro de gasolina consumido. **Un número más alto significa mayor eficiencia y ahorro.**

        Por ejemplo: Una motocicleta con rendimiento de **55 km/L** es mucho más ahorradora y eficiente que una que rinde **40 km/L**.
        """)

    with st.expander("¿Qué es la autonomía?"):
        st.write("""
        Es la distancia total estimada que la motocicleta puede recorrer con un solo tanque lleno de combustible antes de quedarse vacía. 

        Se calcula multiplicando la capacidad del tanque (en litros) por el rendimiento promedio (km/L). Una alta autonomía es crucial para usuarios que viajan en carretera o quieren visitar la gasolinera con menos frecuencia.
        """)

    with st.expander("¿Qué diferencias hay entre los tipos de frenos?"):
        st.write("""
        * **Frenos de Tambor:** Sistema mecánico más antiguo y económico. Tiende a perder eficiencia bajo uso muy intenso debido a la acumulación de calor.
        * **Frenos de Disco:** Sistema hidráulico expuesto al aire. Ofrece una respuesta de frenado mucho más rápida, precisa y con excelente disipación de calor.
        """)

    with st.expander("¿Qué es el sistema de frenos ABS y por qué es importante?"):
        st.write("""
        El ABS (*Anti-lock Braking System*) es un sistema electrónico de seguridad que evita que las ruedas se bloqueen o se amarren durante una frenada de emergencia.

        * **Beneficio clave:** Si el cliente frena a fondo sobre pavimento mojado, arena o aceite, el sistema modula la presión del freno automáticamente para evitar que la moto derrape, permitiendo mantener el control del manillar. Es un argumento de venta masivo en seguridad.
        """)

    with st.expander("¿Qué diferencia hay entre un motor a carburador y uno de inyección electrónica (FI)?"):
        st.write("""
        Describe cómo entra el combustible al motor:

        * **Carburador:** Sistema mecánico tradicional. Es económico de reparar, pero es sensible a los cambios de altitud y clima (puede costar trabajo encender la moto en mañanas frías).
        * **Inyección Electrónica (Fuel Injection - FI):** Una computadora dosifica la gasolina con precisión exacta. Ofrece un encendido inmediato, optimiza el consumo de combustible, genera menos emisiones y no requiere ajustes si viajas de la costa a zonas altas.
        """)

    with st.expander("¿Qué diferencias hay entre transmisión por cadena, banda y cardán?"):
        st.write("""
        Es el componente final que mueve la rueda trasera:

        * **Cadena:** El más común y eficiente transmitiendo energía, pero requiere lubricación y ajuste cada 500-1,000 km.
        * **Banda:** Muy silenciosa y suave. No requiere lubricación (no ensucia) y se usa casi siempre en *Scooters* o motos tipo *Cruiser*.
        * **Cardán:** Un eje rígido de acero (como en los autos). Es extremadamente durable y prácticamente libre de mantenimiento, reservado para motos de viaje de alta cilindrada.
        """)

    with st.expander("¿Qué son los modos de manejo o mapas de motor?"):
        st.write("""
        Es una tecnología electrónica que permite modificar el comportamiento de la motocicleta con solo presionar un botón.

        Ejemplos comunes para explicar a un cliente:
        * **Modo Urban/Rain:** Suaviza la entrega de potencia para evitar que la llanta trasera patine en superficies resbaladizas.
        * **Modo Sport:** Libera toda la potencia y aceleración de forma inmediata para un manejo más entusiasta.
        """)

    with st.expander("¿Por qué es importante fijarse en la altura del asiento al suelo?"):
        st.write("""
        Generalmente medida en milímetros (ej. 790 mm), define la distancia desde la parte más baja del asiento hasta el piso.

        Es un dato crítico de ergonomía para el vendedor: ayuda a perfilar si el cliente (especialmente primerizos o personas de baja estatura) podrá plantar ambos pies firmemente en el suelo al detenerse en un semáforo, dándole mayor confianza y seguridad física.
        """)

    with st.expander("¿Qué significa que las llantas sean Sellomatic (Tubeless o sin cámara)?"):
        st.write("""
        A diferencia de las llantas tradicionales con cámara interna (comunes en rines de rayos), las *Tubeless* sellan directamente contra el rin de aleación.

        * **Ventaja comercial:** Si un clavo perfora la llanta, el aire se pierde de manera muy lenta, permitiendo al conductor rodar varios kilómetros de forma segura hasta una vulcanizadora en lugar de sufrir una ponchadura instantánea y peligrosa.
        """)

    with st.expander("¿Qué sistemas de arranque existen?"):
        st.write("""
        * **Eléctrico:** Enciende el motor presionando un botón en el manillar mediante el uso de la batería. Es el método estándar por comodidad.
        * **De Pedal (Kickstart):** Requiere una patada física en una palanca mecánica. Es una excelente opción de respaldo si la batería se descarga.
        """)




###################################################################################################################################################################
###################################################################################################################################################################
#endregion

#region MODO 4 ACERCA DEL PROYECTO Y DEL AUTOR, MEDIOS DE CONTACTO

elif modo == "Acerca del proyecto":

    st.title("🏍️ Catálogo Inteligente de Motocicletas")
    st.markdown("## Presentación del sistema")
    st.divider()

    # ---------------- PROBLEMA + PROYECTO ----------------
    st.markdown("##  Descripción del proyecto")

    st.markdown("""
    Plataforma desarrollada para facilitar la consulta, comparación y análisis de motocicletas pertenecientes al catálogo de la empresa. 
                Su propósito va más allá de mostrar y comparar fichas técnicas: busca servir como una herramienta de apoyo para el asesor de ventas, 
                proporcionando explicaciones claras sobre los principales conceptos presentes en las especificaciones de cada motocicleta. Además de
                apoyar mostrando material audiovisual para que el cliente pueda conocer un producto que podría no estar disponible directamente en
                piso de venta.
    
    Además de centralizar la información técnica, la aplicación incorpora una guía interactiva que explica, en un lenguaje sencillo, términos como potencia, 
                caballos de fuerza (HP), torque, revoluciones por minuto (RPM), autonomía y otros conceptos que suelen generar dudas tanto en asesores como 
                en clientes. De esta manera, la plataforma no solo facilita la consulta de información, sino que también contribuye al aprendizaje continuo 
                del personal.

    La idea de este proyecto surge a partir de la experiencia de un asesor de experiencia al cliente en sus primeras etapas de formación. 
                Durante ese proceso se identificaron dos desafíos principales. El primero fue la necesidad de adaptarse rápidamente a un gran volumen de 
                información técnica y comprender conceptos provenientes de áreas como la física y la mecánica. El segundo fue reconocer que la seguridad y 
                el dominio del producto durante una asesoría generan mayor confianza en el cliente, favoreciendo una comunicación más clara y una mejor 
                toma de decisiones al momento de la compra. Así, centralizando información técnica y permitiendo explorar alternativas de forma rápida e 
                intuitiva se lanza la propuesta de este proyecto que pretende llegar a TODOS los asesores experiencia cliente que desen brindar 
                la mejor atención a los clientes.
                
    Este proyecto no pretende ser una mera exhibición "bruta" de capacidades técnicas, sino que es un proyecto que busca resolver
                problemáticas específicas de la manera más sencilla posible a la que un asesor pueda acceder sin instalar ninguna 
                aplicación, ¡solo guardando un link!
    """)

    st.divider()

    # ---------------- OBJETIVOS ----------------
    st.markdown("## Objetivos del sistema")

    st.markdown("""
    - Centralizar la información técnica de motocicletas.
    - Facilitar la comparación entre modelos.
    - Agilizar la atención al cliente en piso de venta.
    - Reducir el tiempo de búsqueda de especificaciones.
    - Servir como base para futuras herramientas de análisis y recomendación.
    """)

    st.divider()

    # ---------------- FUNCIONALIDADES ----------------
    st.markdown("## Funcionalidades actuales")

    st.markdown("""
    - ✅ Consulta de especificaciones técnicas por modelo (ficha técnica).
    - ✅ Exhibición directa de los productos por medio del uso de materiales audio visuales (videos).
    - ✅ Comparador de motocicletas lado a lado (textual y visual).
    - ✅ Sistema de recomendación basado en similitud.
    - ✅ Visualización estructurada de catálogo (esquema de cuatro modos).
    - ✅ Guía de consulta a modo de capacitación "a la mano".
    """)

    st.divider()



    # ---------------- ROADMAP ----------------
    st.markdown("## 🚀 Roadmap")

    st.markdown("""
                
    - 🛍️ Integración de nuevas categorías de mercancías: La arquitectura modular del sistema facilita su escalabilidad, permitiendo reutilizar 
    la plataforma con diferentes bases de datos e incorporar nuevas categorías de productos, como colchones, telefonía, línea blanca u otras mercancías 
    comercializadas por la empresa que requieren especial atención a sus especificaciones.
            
    - 📊 Integración con datos de ventas reales: La plataforma podría conectarse con la información histórica de ventas de la 
    empresa para identificar tendencias, conocer cuáles son los modelos con mayor demanda y analizar el comportamiento de los clientes. 
    Esto permitiría generar reportes estadísticos que apoyen la toma de decisiones comerciales si es el caso.
                
    - 🔗 Conexión con inventario en tiempo real: Una futura integración con el sistema de inventario permitiría mostrar únicamente las motocicletas 
    disponibles en cada sucursal, consultar existencias en tiempo real e incluso indicar cuándo un modelo está próximo a agotarse o cuándo se 
    espera un nuevo ingreso.
                
    - 📱 Migración a aplicación móvil: Si bien el espiritu del proyecto es disponibilidad sin mayores requerimientos, es de conocimiento general
    que no todos los asesores cuentan con una red o acceso competente a ella. Aunque actualmente la plataforma funciona como una aplicación web desarrollada 
    con Streamlit, una evolución natural del proyecto sería convertirla en una aplicación móvil para Android e iOS. Esto con la intención de facilitar su uso 
    directamente desde el piso de ventas, reduciendo los requisitos de dos a uno (smartphone + conexión a internet), permitiendo a los asesores consultar 
    información desde un teléfono sin más requerimientos..
    """)

    st.divider()

    # ---------------- ARQUITECTURA ----------------
    st.markdown("## ⚙️ Arquitectura del sistema")

    st.code("""
                        Usuario
                        │
                        ▼
    ┌─────────────────────────────────────┐
    │      PRESENTACIÓN (Streamlit)        │
    │ Interfaz gráfica de la aplicación    │
    └─────────────────────────────────────┘
                        │
                        ▼
    ┌─────────────────────────────────────┐
    │        LÓGICA DE NEGOCIO            │
    │ • Consulta de fichas técnicas       │
    │ • Comparador de motocicletas        │
    │ • Sistema de recomendación          │
    │ • Guía interactiva para el asesor   │
    └─────────────────────────────────────┘
                        │
                        ▼
    ┌─────────────────────────────────────┐
    │   PROCESAMIENTO DE DATOS            │
    │ Pandas • NumPy • scikit-learn       │
    └─────────────────────────────────────┘
                        │
                        ▼
    ┌─────────────────────────────────────┐
    │       ALMACENAMIENTO                │
    │ CSV • Imágenes • Videos             │
    └─────────────────────────────────────┘

    ═══════════════════════════════════════════

        ☁️ Alojado en Streamlit Community Cloud
                (SCC)

    ═══════════════════════════════════════════
    """)

    st.divider()

    # ---------------- DESARROLLADOR ----------------
    st.markdown("## 👨‍💻 Desarrollador")

    st.markdown("""
    **Giovanni Jefté Aguilar Carmona.**  
    Licenciado en Física - Facultad de Ciencias, UNAM.

    ### Competencias principales:
    - Física y matemáticas.
    - Ciencia de datos.
    - Sistemas complejos (redes).
    - Programación aplicada Python, R y Ruby.
    - Análisis e interpretación de información.
    - Dominio de paquetería M. Office. y terminal Linux con enfoque en distribuciones basadas en Debian.

    Este proyecto forma parte de una iniciativa de desarrollo de herramientas internas orientadas
    a la optimización de procesos de consulta y decisión para colaboradores.
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

    col1, col2 , col3= st.columns(3)

    with col1:
        st.markdown("""
    **📧 Correo institucional**

    gjaguilarc@suburbia.com.mx
    """)

    with col2:
        st.markdown("""
    **📧 Correo personal**

    gj.aguilar852@gmail.com
    """)
    with col3:
        st.link_button("💻 GitHub", "https://github.com/Tzekelkan852")

###################################################################################################################################################################
###################################################################################################################################################################
#endregion

#region MODO 5 PRUEBA NETWORKS
elif modo == "Red":
    st.title("🌐 Módulo de Ciencia de Redes y Grafos")
    st.write("Analiza la estructura del catálogo automotriz a través de modelos topológicos relacionales.")

    # Estructura de pestañas actualizada para incorporar la red de marcas
    tab1, tab2= st.tabs([
        "🔗 Red de Similitud KNN (Física)", 
        "🏢 Red de Competencia entre Marcas"
    ])

    # ==========================================
    # PESTAÑA 1: RED DE SIMILITUD KNN
    # ==========================================
    with tab1:
        st.header("Red Dirigida $K$-Nearest Neighbors ($K$-NN) de Similitud Técnica")
        
        with st.expander("📖 Glosario Técnico e Interpretación del Grafo", expanded=True):
            st.markdown("""
            ### ¿Qué es esta red?
            Es un modelo topológico donde cada **nodo** representa una motocicleta y cada **enlace dirigido (flecha)** representa una relación de 
            proximidad matemática. Está basada en el algoritmo **$K$-Nearest Neighbors ($K$-NN)**, el cual mapea cada vehículo en un espacio 
            multidimensional utilizando sus variables numéricas clave (*cilindrada, potencia, torque, velocidad máxima, tanque y autonomía*). 
            En términos prácticos, es el algoritmo subyacente que se utiliza para generar y mostrar las "motos sugeridas".

            ### ¿Para qué sirve en el negocio?
            Permite al asesor o analista identificar **alternativas directas de sustitución de producto**. Si un cliente busca un modelo específico 
            pero no hay inventario, o si desea explorar una opción similar, la red revela de inmediato cuáles son sus competidores más cercanos en 
            rendimiento real, yendo más allá de las etiquetas comerciales de las marcas.

            ### ¿Cómo se interpreta el grafo y sus atributos visuales?
            En esta red, las conexiones se ponderan mediante un factor de **peso** (con valores entre 0 y 1), el cual es directamente proporcional a la **similitud**:
            
            * **El grosor y tamaño de la flecha (Similitud):** El ancho de cada línea es directamente proporcional al peso de la conexión. Una flecha 
            notablemente más gruesa indica una menor distancia euclidiana en el espacio de características, es decir, que ambos modelos son técnicamente muy 
            idénticos en rendimiento y prestaciones.
            * **Grado de entrada:** Es la cantidad de flechas que recibe una motocicleta. Representa cuántas otras motos del catálogo 
            consideran a este modelo como uno de sus "vecinos más cercanos" y más similares.
            * **El gradiente de color:** Los enlaces y nodos se tiñen según su grado de conexión:
                * **Tonos fríos (Azul/Gris):** Modelos periféricos. Cuentan con especificaciones muy únicas o extremas; por lo tanto, casi ninguna 
                otra moto se les asemeja.
                * **Tonos cálidos (Rojo grisáceo/Rojo vivo):** Modelos **atractores**. Son motocicletas con configuraciones técnicas estándar y 
                equilibradas. Al representar el "promedio óptimo" del mercado, múltiples modelos apuntan hacia ellas, convirtiéndolas en los pilares 
                relacionales del catálogo.
            """)

        st.markdown("---")

        ruta_mapa_png = "Redes/redimg/nearest-neig.png" 

        if os.path.exists(ruta_mapa_png):
            col_info, col_descarga = st.columns([3, 1])
            with col_info:
                st.info("💡 **Tip de exploración:** Haz clic en las flechas de la esquina de la imagen para expandir a **Pantalla Completa** y leer cómodamente las etiquetas de cada motocicleta.")
            
            with col_descarga:
                with open(ruta_mapa_png, "rb") as file:
                    st.download_button(
                        label="📥 Descargar Mapa HD",
                        data=file,
                        file_name="nearest-neig.png",
                        mime="image/png",
                        use_container_width=True
                    )
            
            with st.container(border=True):
                st.image(
                    ruta_mapa_png, 
                    caption="Mapeo de Mercado: Directed K-NN Similarity Network (Gephi Layout)",
                    use_container_width=True
                )
        else:
            st.error("No se encontró el archivo visual en la ruta especificada.")
            st.info(f"Verifica que el archivo exista en: `{ruta_mapa_png}`")

    # ==========================================
    # PESTAÑA 2: RED DE COMPETENCIA ENTRE MARCAS (NUEVA)
    # ==========================================
    with tab2:
        st.header("Red No Dirigida de Competencia y Rivalidad de Mercado")
        
        with st.expander("📖 Glosario Técnico e Interpretación del Grafo de Marcas", expanded=True):
            st.markdown("""
            ### ¿Qué es esta red?
            Es un modelo de abstracción macro donde los **nodos representan las marcas del mercado** y las **aristas (líneas)** representan una relación de competencia 
            directa. Una conexión significa que ambas empresas ofrecen productos con características técnicas muy similares que se disputan los mismos clientes 
            del catálogo. Basado en el modelo K-nn utilizado para las recomendaciones de modelos similares.
            
            ### ¿Para qué sirve en el negocio?
            Permite realizar **análisis de inteligencia competitiva de forma visual**. Ayuda a los directores y analistas a identificar de inmediato qué 
            marcas son rivales frontales en ingeniería, cuáles operan de forma aislada en nichos específicos, y dónde se concentran los clústeres de oferta del 
            mercado automotriz.

            ### ¿Cómo se interpretan los atributos visuales de esta red?
            A diferencia de la red de similitus, este grafo es **no dirigido**, ya que la rivalidad comercial es mutua:
            
            * **El grosor del enlace (Intensidad de Competencia):** Representa el **número total de modelos similares** que 
            cruzan las fronteras de ambas marcas. Un enlace notablemente grueso (por ejemplo, entre *Bajaj* y *Suzuki*) denota que tienen catálogos altamente 
            superpuestos y compiten directamente en múltiples segmentos.
            * **Grado de competencia (Degree):** Es la cantidad de rivales comerciales distintos con los que una marca se conecta directamente en el grafo. 
            Por ejemplo, entre *Veloci* y *Suzuki* no existe enlace alguno, esto quiere decir mínima competencia ya que bajo nuestro modelo K-nn jamás aparecerá
            recomendada una *Veloci* al visualizar una *Suzuki* y viceversa. 

            """)

        st.markdown("---")

        # Ruta sugerida para tu exportación de Gephi de la red de marcas
        ruta_mapa_marcas = "Redes/redimg/competencia.png"

        if os.path.exists(ruta_mapa_marcas):
            col_info_m, col_descarga_m = st.columns([3, 1])
            with col_info_m:
                st.info("💡 **Tip de exploración:** Expande el mapa a **Pantalla Completa** para analizar la densidad de los enlaces gruesos y ver qué marcas actúan como los núcleos o 'hubs' competitivos de tu catálogo.")
            
            with col_descarga_m:
                with open(ruta_mapa_marcas, "rb") as file:
                    st.download_button(
                        label="📥 Descargar Mapa de Marcas",
                        data=file,
                        file_name="competencia-marcas.png",
                        mime="image/png",
                        use_container_width=True
                    )
            
            with st.container(border=True):
                st.image(
                    ruta_mapa_marcas, 
                    caption="Estructura de Competencia Industrial: Corporate Rivalry Network (Gephi Layout)",
                    use_container_width=True
                )
        else:
            st.error("No se encontró el plano visual de la red de marcas en la ruta especificada.")
            st.info(f"Para visualizar este mapa, expórtalo desde Gephi como PNG con el nombre `competencia-marcas.png` y guárdalo en:\n`{ruta_mapa_marcas}`")


#endregion

#region FIRMA DEL CATALOGO ##########################

###################################################################################################################################################################

###################################################################################################################################################################

st.divider()

# Firma (Texto centrado)
st.markdown("""
<div style='text-align:center;
            color:#BFBFBF;
            font-size:13px;
            padding-top:15px;
            margin-bottom:15px;'>

🏍️ <b>Catálogo Inteligente de Motocicletas</b><br>

Desarrollado por <b>Giovanni J. Aguilar</b> · Facultad de Ciencias · UNAM<br>

Proyecto de desarrollo de software con técnicas de análisis de datos y recomendación basada en similitud.

</div>
""", unsafe_allow_html=True)

# QR centrado usando columnas balanceadas
col1, col2, col3 = st.columns([1.5, 1, 1.5])

with col2:
    st.image("qr-code.png", width=350)
    # Leyenda en negrita y centrada justo bajo el QR
    st.markdown("""
    <div style='text-align:center; 
                color:#BFBFBF; 
                font-size:34px; 
                margin-top:-10px;'>
        <b>¡Compártelo!</b>
    </div>
    """, unsafe_allow_html=True)

#endregion