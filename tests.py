import json
import psycopg2 as dbapi

import os
from datetime import datetime
#from osgeo import ogr, osr


def parse_geojson(plugin_dir, geofile, dbconfig):
    """
    Read geojson and extract data
    :param geofile:
    :return:
    """
    error_list = []
    with open(geofile) as geojson:
        data = json.load(geojson)
        try:
            geom = data['geometry']
        except:
            error_list.append("Missing parcel geometry")
        try:
            attribute_fields = data['properties']
        except:
            error_list.append("Missing parcel properties")
        try:
            key_upin = data['properties']['key_upin']
        except:
            error_list.append("Missing parcel attributes")

        if(len(error_list) > 0):
            error_msg = os.path.basename(geofile) + ' ' + ' '.join(map(str, error_list))
            result = 'Import unsuccessful'
            return result
        else:
            result = 'Import successful'
            return result
            #parcel = ogr.CreateGeometryFromJson(str(geom))
            #parcel_reprojected = reproject_utm(plugin_dir, parcel)
            #upload_to_db(dbconfig, attribute_fields, parcel_reprojected.ExportToWkt())





if __name__ == '__main__':
    _plugin_dir = 'F:\Blantyre\Errors'
    sample = 'F:\Blantyre\Errors\\10000_1_2020_08_11_17_04_53_msdc.geojson'
    dbsettings = {
        "host": "localhost",
        "port": "5432",
        "database": "msdc",
        "user": "postgres",
        "pass": "postgres"
    }
    result = parse_geojson(_plugin_dir, sample, dbsettings)
    print(result)