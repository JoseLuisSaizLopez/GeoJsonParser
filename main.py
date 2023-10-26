import SpainPolygonParser
import andalucia_reader_1


# [Value printers]
def print_locations(province_list):
    for prov_name, mun_dict in province_list.items():
        print(f"\n\n{prov_name}")
        print("________________________________________________________________________")
        for mun_name, location in mun_dict.items():
            print(f"{mun_name} -------> {location.properties.string}")
# [End of value printers]


if __name__ == '__main__':
    # locations = SpainPolygonParser.load_file("locationPoligons/georef-spain-municipio_public.geojson")
    # andalusia_provinces = locations["Andalucía"]
    #
    # for province_name, municipals in andalusia_provinces.items():
    #     for municipal_name, municipal in municipals.items():
    #         print(municipal.string['geometry'])
    #         SpainPolygonParser.export_data3(municipal)
    #         break
    #     break
    andalucia_reader_1.open_excel("samples/andalucia_data_test.xlsx")
