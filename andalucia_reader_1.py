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


def open_excel_by_province(filename):
    df = pd.read_excel(filename)
    municipios_gdf = gpd.read_file("locationPoligons/georef-spain-municipio_public.geojson", encoding='utf-8')

    # Crear un GeoDataFrame vacío para almacenar los municipios procesados
    provincias_andalusia = gpd.GeoDataFrame()

    # Debug para encontrar los nombres de los municipios de esa provincia
    ####################################################################################################################
    # municipios_cadiz = municipios_gdf[municipios_gdf["prov_name"] == "Granada"]

    # # Iterar sobre los municipios de Cádiz e imprimir sus nombres
    # for index, row in municipios_cadiz.iterrows():
    #     print(row["mun_name"])
    ####################################################################################################################

    # Nombre de la provincia que deseas seleccionar
    comunidad_deseada = "Andalucía"

    # Filtrar el GeoDataFrame para seleccionar una provincia específica
    comunidad_seleccionada = municipios_gdf[municipios_gdf["acom_name"] == comunidad_deseada]

    # Agrupar los municipios por provincia
    provincias_gdf = comunidad_seleccionada.dissolve(by="prov_name", as_index=False)

    # Accede a la lista de nombres de columnas
    columnas = provincias_gdf.columns

    # Imprime los nombres de las columnas
    print(columnas)

    # Iterar sobre las filas del archivo Excel
    for index, row in df.iterrows():
        # Obtener el mun_code de la fila actual
        prov_name = row["Provincia"]

        # Filtrar el GeoDataFrame para encontrar el municipio por mun_code
        provincia_seleccionada = provincias_gdf[provincias_gdf["prov_name"] == prov_name]

        # Verificar si se encontró el municipio
        if not provincia_seleccionada.empty:
            # Agregar el campo de consumo de agua al municipio
            provincia_seleccionada["emisiones_co2_toneladas_anuales"] = row["Emisiones de CO2 (toneladas anuales)"]
            provincia_seleccionada["consumo_agua_m3año"] = row["Consumo de agua (m3/año)"]
            provincia_seleccionada["recogida_envases_toneladas_anuales"] = row["Recogida de envases (toneladas anuales)"]
            provincia_seleccionada["recogida_papel_toneladas_anuales"] = row["Recogida de papel (toneladas anuales)"]
            provincia_seleccionada["recogida_vidrio_toneladas_anuales"] = row["Recogida de vidrio (toneladas anuales)"]

            # Agregar el municipio procesado al GeoDataFrame de Andalucía
            provincias_andalusia = pd.concat([provincias_andalusia, provincia_seleccionada], ignore_index=True)
        else:
            print(f"Cannot process --> {prov_name}")

    # Guardar el GeoDataFrame de Andalucía en un archivo GeoJSON
    provincias_andalusia.to_file("andalucia_test.geojson", driver="GeoJSON")
