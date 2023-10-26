import geojson
import geopandas as gpd
from geojson import Polygon, MultiPolygon


# [Data class definition]
class SpainLocationPolygon:
    def __init__(self, features):
        self.properties = SpainLocationPolygon.Properties(features['properties'])
        self.geometry = features['geometry']
        self.string = features

    class Properties:
        def __init__(self, property_list):
            self.acom_code = property_list["acom_code"]
            self.acom_name = property_list["acom_name"]
            self.prov_code = property_list["prov_code"]
            self.prov_name = property_list["prov_name"]
            self.mun_area_code = property_list["mun_area_code"]
            self.mun_code = property_list["mun_code"]
            self.mun_name = property_list["mun_name"]
            self.mun_name_local = property_list["mun_name_local"]
            self.mun_type = property_list["mun_type"]
            self.year = property_list["year"]
            self.string = property_list
# [End of data class definition]


# [Load Spain file]
def load_file(path):
    spain_locations = {}
    with open(path) as file:
        data = geojson.load(file)
    features = data['features']
    for feature in features:
        #print(feature["properties"])
        # Create properties
        location = SpainLocationPolygon(feature)
        acom_name = location.properties.acom_name
        mun_name = location.properties.mun_name
        prov_name = location.properties.prov_name
        if acom_name not in spain_locations:
            spain_locations[acom_name] = {}
        if prov_name not in spain_locations[acom_name]:
            spain_locations[acom_name][prov_name] = {}
        spain_locations[acom_name][prov_name][mun_name] = location
    return spain_locations
# [End of load Spain file]


# [Province geometry sum functions]
def __get_province_polygon(municipal_list):
    municipal_polygons = []
    for municipal, location in municipal_list.items():
        municipal_polygons.append(Polygon(location.geometry["coordinates"]))
    provincia_total = MultiPolygon(municipal_polygons)
    #print(provincia_total)
    return provincia_total
# [End of province geometry sum functions]


def get_community_data(province_data_list, group_by_province):
    community_data = {}
    if group_by_province:
        for prov_name, mun_dict in province_data_list.items():
            # print(f"\n{prov_name}")
            # print("________________________________________________________________________")
            province_polygon = __get_province_polygon(mun_dict)
            community_data[prov_name] = province_polygon
    return community_data


# [Data export to GeoJSON]
def export_data(community_data):

    # Supongamos que tienes una estructura de datos que almacena las coordenadas por provincia.
    #comunidad_data = {
    #    "Provincia1": [  # Datos de la provincia 1
    #        [[x1, y1], [x2, y2], ...],  # Polígono 1 de la provincia 1
    #        [[x3, y3], [x4, y4], ...],  # Polígono 2 de la provincia 1
    #        # ...
    #    ],
    #    "Provincia2": [  # Datos de la provincia 2
    #        [[x5, y5], [x6, y6], ...],  # Polígono 1 de la provincia 2
    #        # ...
    #    ],
    #    # ...
    #}

    # Crear una característica de GeoJSON para cada provincia
    features = []

    for provincia, coordenadas in community_data.items():
        # print(f"\n\n{provincia}\n_____________________________________________________________________________")
        # print(len(coordenadas))
        feature = geojson.Feature(
            properties={"provincia": provincia},
            geometry=MultiPolygon(coordenadas)
        )
        features.append(feature)

    # Crear una colección de características GeoJSON
    feature_collection = geojson.FeatureCollection(features)

    # Escribir el GeoJSON en un archivo
    with open('comunidad.geojson', 'w', encoding='utf-8') as f:
        geojson.dump(feature_collection, f, ensure_ascii=False)


def export_data2(data):

    features = []
    feature = geojson.Feature(
        properties={"nombre": "Andalucía"},
        geometry=data.string['geometry']
    )
    features.append(feature)

    # Crear una colección de características GeoJSON
    feature_collection = geojson.FeatureCollection(features)

    # Escribir el GeoJSON en un archivo
    with open('comunidad.geojson', 'w', encoding='utf-8') as f:
        geojson.dump(feature_collection, f, ensure_ascii=False)

    return


def export_data3(data):
    # Cargar los datos GeoJSON con los municipios
    municipios_gdf = gpd.read_file("locationPoligons/georef-spain-municipio_public.geojson")

    # Nombre de la provincia que deseas seleccionar
    comunidad_deseada = "Andalucía"

    # Filtrar el GeoDataFrame para seleccionar una provincia específica
    provincia_seleccionada = municipios_gdf[municipios_gdf["acom_name"] == comunidad_deseada]

    # Agrupar los municipios por provincia
    provincias_gdf = provincia_seleccionada.dissolve(by="prov_name")

    # Guardar el GeoDataFrame de provincias en un archivo GeoJSON
    provincias_gdf.to_file("provincias.geojson", driver="GeoJSON")
# [End of data export to GeoJSON]
