import pandas as pd
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')


def open_excel(filename):
    df = pd.read_excel(filename)
    municipios_gdf = gpd.read_file("locationPoligons/georef-spain-municipio_public.geojson", encoding='utf-8')

    # Crear un GeoDataFrame vacío para almacenar los municipios procesados
    municipios_andalusia = gpd.GeoDataFrame()

    # Debug para encontrar los nombres de los municipios de esa provincia
    ####################################################################################################################
    # municipios_cadiz = municipios_gdf[municipios_gdf["prov_name"] == "Granada"]

    # # Iterar sobre los municipios de Cádiz e imprimir sus nombres
    # for index, row in municipios_cadiz.iterrows():
    #     print(row["mun_name"])
    ####################################################################################################################

    # Iterar sobre las filas del archivo Excel
    for index, row in df.iterrows():
        # Obtener el mun_code de la fila actual
        mun_name = row["Municipio"]

        # Filtrar el GeoDataFrame para encontrar el municipio por mun_code
        municipio_seleccionado = municipios_gdf[municipios_gdf["mun_name"] == mun_name]

        # Verificar si se encontró el municipio
        if not municipio_seleccionado.empty:
            # Agregar el campo de consumo de agua al municipio
            municipio_seleccionado["consumo_agua_m3año"] = row["Consumo de agua (m3/año)"]

            # Agregar el municipio procesado al GeoDataFrame de Andalucía
            municipios_andalusia = pd.concat([municipios_andalusia, municipio_seleccionado], ignore_index=True)
        else:
            print(f"Cannot process --> {mun_name}")

    # Guardar el GeoDataFrame de Andalucía en un archivo GeoJSON
    municipios_andalusia.to_file("andalucia_test.geojson", driver="GeoJSON")



