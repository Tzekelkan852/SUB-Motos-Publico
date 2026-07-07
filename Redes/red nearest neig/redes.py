import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

def exportar_red_dirigida_gephi(df, n_vecinos=4, archivo_nodos="nodos_dirigidos.csv", archivo_enlaces="enlaces_dirigidos.csv"):
    """
    Genera una red DIRIGIDA donde cada nodo tiene exactamente N enlaces salientes (Out-Degree),
    permitiendo ver qué motos son los 'hubs' o atractores del catálogo mediante el In-Degree.
    """
    datos = df.copy()
    datos = datos.rename(columns={
        "Vmax (km/h)": "Velocidad Maxima (km/h)",
        "Autonomia (Km)": "Autonomía (Km)"
    })
    
    variables_numericas = [   
        "C. Motor", "Potencia (HP)", "Torque (Nm)", 
        "Velocidad Maxima (km/h)", "Tanque (L)", "Autonomía (Km)"
    ]

    for col in variables_numericas:
        datos[col] = pd.to_numeric(datos[col], errors="coerce")
        datos[col] = datos[col].fillna(datos[col].median() if not datos[col].isna().all() else 0)

    # 1. Exportar Nodos
    nodos_df = datos[["Modelo", "Marca", "Tipo"]].copy()
    nodos_df = nodos_df.rename(columns={"Modelo": "Id"})
    nodos_df["Label"] = nodos_df["Id"]
    nodos_df = nodos_df.drop_duplicates(subset=["Id"])
    nodos_df.to_csv(archivo_nodos, index=False)
    print(f"✔️ Nodos guardados en: {archivo_nodos}")

    # 2. Procesamiento KNN para Enlaces
    scaler = StandardScaler()
    X = scaler.fit_transform(datos[variables_numericas])

    max_vecinos = min(n_vecinos, len(datos) - 1)
    nn = NearestNeighbors(n_neighbors=max_vecinos + 1)
    nn.fit(X)
    distancias, indices = nn.kneighbors(X)

    enlaces = []
    for i in range(len(datos)):
        moto_origen = datos.iloc[i]["Modelo"]
        
        for j in range(1, len(indices[i])):
            idx_destino = indices[i][j]
            moto_destino = datos.iloc[idx_destino]["Modelo"]
            distancia = distancias[i][j]
            similitud = 1 / (1 + distancia)
            
            enlaces.append({
                "Source": moto_origen,       # ID de origen (Gephi)
                "Target": moto_destino,      # ID de destino (Gephi)
                "Type": "Directed",          
                "Weight": round(similitud, 4),
                "Source_Label": moto_origen, 
                "Target_Label": moto_destino  
            })

    enlaces_df = pd.DataFrame(enlaces)
    enlaces_df.to_csv(archivo_enlaces, index=False)
    print(f"✔️ Enlaces dirigidos guardados en: {archivo_enlaces}")
    
    return nodos_df, enlaces_df

# ==========================================
# EJEMPLO DE FLUJO DE CARGA COMPLETO
# ==========================================
if __name__ == "__main__":
    # 1. Carga de tu base de datos real
    df_principal = pd.read_csv(r"C:\Users\PC\Desktop\Proyecto SUB\Motos.csv", encoding="cp1252")
    
    # 2. Correr la función configurada para buscar las 4 más similares
    exportar_red_dirigida_gephi(df_principal, n_vecinos=4)