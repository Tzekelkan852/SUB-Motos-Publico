import pandas as pd
import numpy as np
import os

def crear_csv_red_marcas(ruta_motos_csv=r"C:\Users\PC\Desktop\Proyecto SUB\Motos.csv", 
                         ruta_enlaces_motos=r"C:\Users\PC\Desktop\Proyecto SUB\Redes\red nearest neig\enlaces_dirigidos.csv"):
    
    # 1. Verificar que existan los archivos necesarios
    if not os.path.exists(ruta_motos_csv):
        print(f"Error: No se encontró el archivo base '{ruta_motos_csv}'")
        return
    if not os.path.exists(ruta_enlaces_motos):
        print(f"Error: Se requiere el archivo de similitudes '{ruta_enlaces_motos}' para mapear la competencia.")
        return

    # 2. Cargar los archivos de datos (Agregado el encoding compatible con tu archivo)
    df_motos = pd.read_csv(ruta_motos_csv, encoding="cp1252")
    df_enlaces_motos = pd.read_csv(ruta_enlaces_motos)

    # 3. Crear un diccionario de mapeo: Modelo -> Marca
    # Usamos las columnas 'Modelo' y 'Marca' de tu archivo Motos.csv
    dict_marcas = pd.Series(df_motos['Marca'].values, index=df_motos['Modelo']).to_dict()

    # 4. Mapear los enlaces de motos individuales a sus respectivas marcas empresariales
    df_enlaces_motos["Marca_Source"] = df_enlaces_motos["Source"].map(dict_marcas)
    df_enlaces_motos["Marca_Target"] = df_enlaces_motos["Target"].map(dict_marcas)

    # Eliminar posibles filas con datos nulos si algún modelo no se mapeó correctamente
    df_competencia = df_enlaces_motos.dropna(subset=["Marca_Source", "Marca_Target"]).copy()

    # Filtrar auto-competencia: quitar cuando una marca conecta con modelos de sí misma
    df_competencia = df_competencia[df_competencia["Marca_Source"] != df_competencia["Marca_Target"]]

    # 5. Agrupar pares de marcas sin importar el orden (Grafo No Dirigido / Undirected)
    # Ordenamos alfabéticamente cada par de marcas por fila para consolidar Bajaj->Italika e Italika->Bajaj en una sola cuenta
    marcas_ordenadas = np.sort(df_competencia[["Marca_Source", "Marca_Target"]].values, axis=1)
    df_competencia["Source_Marca"] = marcas_ordenadas[:, 0]
    df_competencia["Target_Marca"] = marcas_ordenadas[:, 1]

    # 6. Calcular el peso (Weight) contando cuántas conexiones de modelos similares existen
    df_enlaces_marcas = df_competencia.groupby(["Source_Marca", "Target_Marca"]).size().reset_index(name="Weight")
    df_enlaces_marcas.columns = ["Source", "Target", "Weight"]
    df_enlaces_marcas["Type"] = "Undirected"

    # 7. GENERAR ARCHIVO DE NODOS (Lista única de marcas y su grado de competencia)
    todas_las_marcas = pd.concat([df_enlaces_marcas["Source"], df_enlaces_marcas["Target"]]).unique()
    
    conteo_source = df_enlaces_marcas["Source"].value_counts()
    conteo_target = df_enlaces_marcas["Target"].value_counts()
    
    lista_nodos_marcas = []
    for marca in todas_las_marcas:
        # Grado es con cuántas marcas distintas compite directamente en el mercado
        grado_mercado = conteo_source.get(marca, 0) + conteo_target.get(marca, 0)
        lista_nodos_marcas.append({
            "Id": marca,
            "Label": marca,
            "Grado_Competencia": int(grado_mercado)
        })
        
    df_nodos_marcas = pd.DataFrame(lista_nodos_marcas)

    # 8. Exportar los archivos finales listos para usar en la misma carpeta de ejecución
    df_nodos_marcas.to_csv("nodos_marcas.csv", index=False)
    df_enlaces_marcas.to_csv("enlaces_marcas.csv", index=False)
    
    print("¡Procesamiento completo!")
    print(f"-> Creado 'nodos_marcas.csv' con {len(df_nodos_marcas)} marcas.")
    print(f"-> Creado 'enlaces_marcas.csv' con {len(df_enlaces_marcas)} aristas de competencia.")

# Ejecutar el generador
crear_csv_red_marcas()