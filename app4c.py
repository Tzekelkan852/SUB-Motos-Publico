import streamlit as st
import pandas as pd
import os

# =========================
# CONFIGURACIÓN
# =========================

st.set_page_config(
    page_title="Catálogo de Motocicletas",
    layout="wide"
)
st.markdown("""
<style>

/* Fondo principal */
.stApp {
    background-color: #3D2740;
}

/* Texto general */
html, body, [class*="css"] {
    color: white;
}

/* Títulos */
h1, h2, h3 {
    color: #D94AA7 !important;
}

/* Expander */
.streamlit-expanderHeader {
    color: #D94AA7 !important;
    font-weight: bold;
}

/* Selectbox */
div[data-baseweb="select"] {
    color: white;
}

/* Labels */
label {
    color: white !important;
}

/* Texto dentro de expanders */
p {
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =========================
# CARGAR DATOS
# =========================

df = pd.read_csv("Motos.csv", encoding="cp1252")

df.columns = df.columns.str.strip()

# Correcciones de nombres
df = df.rename(columns={
    "A¤o": "Año",
    "Transmisi¢n": "Transmisión",
    "Autonomia (Km)": "Autonomía (Km)",
    "Vmax": "Velocidad Maxima"
})

#df["Modelo"] = df["Modelo"].astype(str).str.strip()

df["Modelo"] = (
    df["Modelo"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# =========================
# CATEGORÍAS
# =========================

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
        "Potencia",
        "Torque",
        "Velocidad Maxima",
        "Enfriam.",
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
        "Pesomax",
        "Prueba"
    ]
}

# =========================
# TÍTULO
# =========================

st.markdown(
    """
    <h1 style='color:#D94AA7;'>
        🏍️ Catálogo de Motocicletas
    </h1>
    """,
    unsafe_allow_html=True
)

# =========================
# MODO
# =========================

modo = st.radio(
    "Selecciona una opción",
    ["Ficha Técnica", "Comparar"]
)

# =========================
# SELECTOR
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

    ruta_imagen = os.path.join("img", f"{modelo}.jpg")

    if os.path.exists(ruta_imagen):

        st.image(ruta_imagen, use_container_width=True)

# =========================
# VIDEO 1
# =========================

    if "URL" in df.columns:

        video_url = str(fila["URL"]).strip()

        if video_url:

            st.subheader("🎥 Video de demostración")

            st.video(video_url)

# =========================
# VIDEO 2
# =========================

    if "URL2" in df.columns:

        if pd.notna(fila["URL2"]):

            video_url2 = str(fila["URL2"]).strip()

            if video_url2 != "":

                st.subheader("🎥 Video adicional")

                #st.write("DEBUG:", repr(video_url))

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
            "img",
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
            "img",
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

    st.dataframe(
        comparacion,
        use_container_width=True,
        hide_index=True
    )

