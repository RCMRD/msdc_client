# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MsdcClient
                                 QGIS plugin
 MSDC QGIS Client Data Import and Export Tools
                              -------------------
        begin                : 2019-10-31
        git sha              : $Format:%H$
        copyright            : (C) 2019 by RCMRD
        email                : rcmrd@rcmrd.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import json
import psycopg2 as dbapi

from datetime import datetime
from osgeo import ogr, osr

def parse_geojson(plugin_dir, geofile, dbconfig):
    """
    Read geojson and extract data
    :param geofile:
    :return:
    """
    # parcel or non-parcel file
    if 'non_parcel' in os.path.basename(geofile):
        with open(geofile) as geojson:
            data = json.load(geojson)
            geom = data['geometry']
            attribute_fields = data['properties']
            parcel = ogr.CreateGeometryFromJson(str(geom))
            parcel_reprojected = reproject_utm(plugin_dir, parcel)
            upload_to_nonparcel(dbconfig, attribute_fields, parcel_reprojected.ExportToWkt())
            success_msg = os.path.basename(geofile) + ' ' + 'Imported successfully'
            return success_msg
    else:
        with open(geofile) as geojson:
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

                if (len(error_list) > 0):
                    error_msg = os.path.basename(geofile) + ' ' + ' '.join(map(str, error_list))
                    return error_msg
                else:
                    #pass
                    #geom = data['geometry']
                    parcel = ogr.CreateGeometryFromJson(str(geom))
                    parcel_reprojected, parcel_area, centroid_n, centroid_e = reproject_utm(plugin_dir, parcel)
                    #attribute_fields = data['properties']
                    upload_to_db(dbconfig, attribute_fields, parcel_reprojected.ExportToWkt(), parcel_area, centroid_n, centroid_e)
                    success_msg = os.path.basename(geofile) + ' ' + 'Imported successfully'
                    return success_msg


def reproject_utm(plugin_dir, feature):
    """
    Reproject polygon geometry to UTM (EPSG:20936)
    :param geom:
    :return:
    """
    districts = plugin_dir + '\\data\\' + 'mw_new_district_boundary.shp'
    # get projection from districts shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(districts)
    layer = dataset.GetLayer()
    target = layer.GetSpatialRef()

    # reproject
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(source, target)
    feature.Transform(transform)

    # compute centroid XY
    centroid_n = feature.Centroid().GetY()
    centroid_e = feature.Centroid().GetX()

    # compute area of parcel
    area = feature.GetArea()
    area_in_ha = area / 10000
    # specify precision
    if area_in_ha > 1:
        area_in_ha = round(area_in_ha, 3)
    else:
        area_in_ha = round(area_in_ha, 4)


    return feature, area_in_ha, centroid_n, centroid_e
    
def reproject_wgs(data_dir, feature):
    """
    Reproject to WGS84 coordinates
    :param feature:
    :return: reprojected feature
    """
    districts = data_dir + '\\data\\' + 'mw_new_district_boundary.shp'
    # get source projection
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(districts)
    layer = dataset.GetLayer()
    source = layer.GetSpatialRef()
    # target
    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)
    # reproject
    transform = osr.CoordinateTransformation(source, target)
    feature.Transform(transform)

    return feature

def get_upin_code(tlma, gvh, parcel_no, dbconfig):
    """
    Return UPIN given parcel tlma, gvh and parcel number
    :param tlma:
    :param gvh:
    :param parcel_no:
    :return:
    """
    # connect to existing database
    conn = dbapi.connect(host=dbconfig['host'], port=dbconfig['port'], database=dbconfig['database'],
                         user=dbconfig['user'], password=dbconfig['pass'])
    cur = conn.cursor()

    tlma = tlma.upper()

    # query ta/ward
    cur.execute("SELECT reg_code, dist_code, adm_code FROM tlmas WHERE ta_name = %s", (tlma,))
    tlma_record = cur.fetchone()
    # construct upin
    upin_code = str(tlma_record[0]) + '/' + str(tlma_record[1]) + '/' + str(tlma_record[2]) + '/' + gvh + '/' + str(parcel_no)

    # close communication
    cur.close()
    conn.close()

    return upin_code

def upload_to_db(dbconfig, data_fields, parcel_geom, parcel_area, centroid_n, centroid_e):
    """
    Upload attribute and geometry to database tables
    :param record:
    :return:
    """
    # connect to existing database
    #conn = dbapi.connect(host="localhost", port="5432", database="msdc", user="postgres", password="postgres")
    conn = dbapi.connect(host=dbconfig['host'], port=dbconfig['port'], database=dbconfig['database'], user=dbconfig['user'], password=dbconfig['pass'])
    cur = conn.cursor()

    dt = data_fields['forma_date']
    dt = datetime.strptime(dt, "%d_%m_%Y")

    dt_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    formb_parcels = data_fields['formb_parcels_number']
    if formb_parcels == "":
        formb_parcels = 0
    else:
        formb_parcels = int(formb_parcels),

    # construct full upin given tlma,gvh and parcel no.
    tlma_name = data_fields['tlma_name']
    gvh_name = data_fields['gvh_name']
    parcel_no = int(data_fields['key_upin'])
    upin_code = get_upin_code(tlma_name, gvh_name, parcel_no, dbconfig)

    # get applicant names to include in parcel
    applicant_names = []
    applicants_all = data_fields['applicant_TBL']
    for applicant in applicants_all:
        applicant_names.append(applicant['applicant_name'])

    applicant_names_txt = ','.join(map(str, applicant_names))
    # parcels table
    parcel_data_list = [
        int(data_fields['key_upin']),    # upin
        data_fields['formb_encumbrances'],    # encumberances
        data_fields['formb_encumbrances_type'],    # encumberance_type
        data_fields['formb_dispute'],    # dispute
        data_fields['formb_dispute_type'],    # dispute_type
        data_fields['formb_rights_evidence'],    # evidence_of_rights
        data_fields['formb_type_evidence'],    # evidence_type
        #int(data_fields['formb_parcels_number']),    # no_of_parcels_in_holdings
        formb_parcels, # no_of_parcels_in_holdings
        data_fields['formb_sheet_number'],    # field_sheet_number
        int(data_fields['teamno']),    # field_team_number
        data_fields['formb_additional_info'],    # additional_info
        data_fields['forma_applicant_particulars_corporate_registration'],    # registration_particulars
        data_fields['formb_ownership_type'],    # ownership_type
        parcel_area, # size_in_ha
        data_fields['forma_place'],    # place
        dt,    # date
        dt_now, # imported
        data_fields['gvh_name'],    # gvh
        data_fields['tlma_name'],   # tlma
        data_fields['district_name'],   # district
        data_fields['forma_purpose'],  # purpose
        data_fields['formb_land_use'],  # landuse
        data_fields['forma_applicant_registered_name'],  # registration name
        data_fields['forma_applicant_registered_address'],  # registration category
        data_fields['forma_applicant_category'],  # registration address
        data_fields['key_timestart'],  # time_start
        data_fields['key_timeend'],  # time_end
        applicant_names_txt,    # applicants
        upin_code, # upin_code
        centroid_n, # centroid_n
        centroid_e, # centroid_e
        parcel_geom  # geom
    ]

    # check existing upin
    _upin = int(data_fields['key_upin'])
    cur.execute("SELECT upin FROM parcels WHERE upin = %s", (_upin,))

    if len(cur.fetchall()) > 0:
        # delete upin
        cur.execute("DELETE FROM parcels WHERE upin = %s", (_upin,))
        cur.execute("DELETE FROM applicants WHERE parcel_upin = %s", (_upin,))
        cur.execute("DELETE FROM children WHERE parcel_upin = %s", (_upin,))
        cur.execute("DELETE FROM properties WHERE parcel_upin = %s", (_upin,))
        cur.execute("DELETE FROM guardians WHERE parcel_upin = %s", (_upin,))
        cur.execute("DELETE FROM holders WHERE parcel_upin = %s", (_upin,))
        cur.execute("DELETE FROM clcs WHERE parcel_upin = %s", (_upin,))


    cur.execute("INSERT INTO parcels (upin, encumberances, encumberance_type, dispute, dispute_type, \
                evidence_of_rights, evidence_type, no_of_parcels_in_holdings, field_sheet_number, \
                field_team_number, additional_info, registration_particulars, ownership_type, size_in_ha, place, date, imported, gvh, \
                tlma, district, purpose, landuse, registration_name, registration_category, registration_address, time_start, time_end, applicants, upin_code, centroid_n, centroid_e, geom) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s, 20936))",
                parcel_data_list)

    # applicants table
    applicants = data_fields['applicant_TBL']
    for applicant in applicants:
        if applicant['applicant_gender']:
            gender = applicant['applicant_gender']
        else:
            gender = ""

        applicant_fields = [
            applicant['key_upin'],  # parcel_upin
            applicant['applicant_name'],  # name
            applicant['applicant_id'],  # national_id
            applicant['applicant_marital_status'],  # marital_status
            applicant['applicant_address'],  # address
            applicant['applicant_signature'],  # signature
            applicant['applicant_nationality'],  # nationality
            applicant['applicant_photo'],  # photo
            applicant['applicant_id_photo'],   # id_photo
            applicant['applicant_joint'],  # joint
            applicant['key_index'],  # key_index
            applicant['key_grouped_index'],  # grouped_index
            gender, # gender
            upin_code,  # upin_code
            dt_now # imported
        ]

        cur.execute("INSERT INTO applicants (parcel_upin, name, national_id, marital_status, address, \
        signature, nationality, photo, id_photo, joint, key_index, grouped_index, gender, upin_code, imported) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", applicant_fields)

    # children table
    children = data_fields['children_TBL']
    for child in children:
        child_fields = [
            child['key_upin'],  # parcel_upin
            child['children_name'],  # name
            child['children_age'],  # age
            child['children_gender'],  # gender
            child['children_photo'],   # photo
            child['key_index'],
            child['key_grouped_index'],
            upin_code,  # upin_code
            dt_now  # imported
        ]

        cur.execute("INSERT INTO children (parcel_upin, name, age, gender, photo, key_index, grouped_index, upin_code, imported) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", child_fields)

    # properties table
    properties = data_fields['property_TBL']
    for property in properties:
        property_fields = [
            property['property_type'],   # type
            property['property_deed_number'],   # deed_number
            property['property_plot_number'],   # plot_number
            property['property_use'],   # land_use
            property['property_developed'],   # developed
            property['key_upin'],   # parcel_upin
            property['key_index'],
            property['key_grouped_index'],
            upin_code, # upin_code
            dt_now  # imported
        ]

        cur.execute("INSERT INTO properties (type, deed_number, plot_number, land_use, \
                    developed, parcel_upin, key_index, grouped_index, upin_code, imported) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", property_fields)

    # guardian table
    guardians = data_fields['guardian_TBL']
    for guardian in guardians:
        guardian_fields = [
            guardian['key_upin'],   # parcel_upin
            guardian['guardian_name'],   # name
            guardian['guardian_gender'], # gender
            guardian['guardian_id'],   # national_id
            guardian['guardian_address'],   # address
            guardian['guardian_signature'],   # signature
            guardian['guardian_photo'],   # photo
            guardian['guardian_id_photo'],   # id_photo
            guardian['key_index'],    # key_index
            guardian['key_grouped_index'],
            upin_code,  # upin_code
            dt_now  # imported
        ]

        cur.execute("INSERT INTO guardians (parcel_upin, name, gender, national_id, \
                    address, signature, photo, id_photo, key_index, grouped_index, upin_code, imported) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", guardian_fields)

    # holders table
    # holders table
    # holders = data_fields['customary_estate_TBL']
    # for holder in holders:
    #     holder_fields = [
    #         holder['key_upin'],     # parcel_upin
    #         holder['owner_name'],     # name
    #         holder['owner_gender'],     # gender
    #         holder['owner_id'],     # national_id
    #         holder['owner_marital_status'],     # marital_status
    #         holder['owner_signature'],     # signature
    #         holder['owner_photo'],     # photo
    #         holder['owner_id_photo'],     # id_photo
    #         holder['key_index'],
    #         holder['key_grouped_index']
    #     ]
    #
    #     cur.execute("INSERT INTO holders (parcel_upin, name, gender, national_id, marital_status, \
    #                 signature, photo, id_photo, key_index, grouped_index) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", holder_fields)

    # clc table
    clcs = data_fields['clc_TBL']
    for clc in clcs:
        clc_fields = [
            clc['key_upin'],    # parcel_upin
            clc['clc_name'],    # name
            clc['clc_gender'],    # gender
            clc['clc_id'],    # national_id
            clc['clc_marital_status'],    # marital_status
            clc['clc_signature'],    # signature
            clc['clc_photo'],    # photo
            clc['clc_id_photo'],     # id_photo
            clc['key_index'],
            clc['key_grouped_index'],
            upin_code,  # upin_code
            dt_now  # imported
        ]

        cur.execute("INSERT INTO clcs (parcel_upin, name, gender, national_id, marital_status, \
                    signature, photo, id_photo, key_index, grouped_index, upin_code, imported) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", clc_fields)


    # commit changes
    conn.commit()

    # close communication
    cur.close()
    conn.close()

def upload_to_nonparcel(dbconfig, data_fields, parcel_geom):
    """
    Upload attribute and geometry to non parcel table
    :param record:
    :return:
    """
    # connect to existing database
    #conn = dbapi.connect(host="localhost", port="5432", database="msdc", user="postgres", password="postgres")
    conn = dbapi.connect(host=dbconfig['host'], port=dbconfig['port'], database=dbconfig['database'], user=dbconfig['user'], password=dbconfig['pass'])
    cur = conn.cursor()

    dt = data_fields['feature_id']
    dt = dt[0:10]
    dt = datetime.strptime(dt, "%Y_%m_%d")
    #
    dt_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # non parcels table
    parcel_data_list = [
        dt,    # date
        dt_now,    # imported
        data_fields['feature_name'],    # feature_name
        data_fields['feature_id'],    # feature_id
        data_fields['district_name'],    # district_name
        data_fields['tlma_name'],    # tlma_name
        data_fields['gvh_name'],    # gvh_name
        int(data_fields['teamno']),    # teamno
        int(data_fields['formc_status']),    # formc_status
        int(data_fields['key_index']),    # key_index
        parcel_geom  # geom
    ]

    cur.execute("INSERT INTO non_parcels (date, imported, feature_name, feature_id, \
                district_name, tlma_name, gvh_name, teamno, formc_status, key_index, geom) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s, 20936))",
                parcel_data_list)

    # commit changes
    conn.commit()

    # close communication
    cur.close()
    conn.close()

def get_parcel_tables(data_dir, upin, dbconfig):
    # connect to existing database
    conn = dbapi.connect(host=dbconfig['host'], port=dbconfig['port'], database=dbconfig['database'],
                         user=dbconfig['user'], password=dbconfig['pass'])
    cur = conn.cursor()

    # query geometry
    cur.execute("SELECT ST_AsGeoJSON(geom) FROM parcels WHERE upin = %s", (upin,))
    parcel_geom = cur.fetchall()[0]
    parcel_geom = eval(parcel_geom[0])
    _parcel_geom = ogr.CreateGeometryFromJson(str(parcel_geom))
    parcel_geom_utm = reproject_wgs(data_dir, _parcel_geom)

    # query applicants
    cur.execute("SELECT * FROM applicants WHERE parcel_upin = %s", (upin,))
    applicants = []
    for row in cur.fetchall():
        applicant = {
            "key_upin": row[1],
            "applicant_name": row[2],
            "applicant_id": row[3],
            "applicant_marital_status": row[4],
            "applicant_address": row[5],
            "applicant_signature": row[6],
            "applicant_nationality": row[7],
            "applicant_photo": row[8],
            "applicant_id_photo": row[9],
            "applicant_joint": row[10],
            "key_index": row[11],
            "key_grouped_index": row[12]
        }
        applicants.append(applicant)

    # children
    cur.execute("SELECT * FROM applicants WHERE parcel_upin = %s", (upin,))
    children = []
    for row in cur.fetchall():
        child = {
            "key_upin": row[1],
            "children_name": row[2],    # name
            "children_age": row[3],     # age
            "children_gender": row[4],     # gender
            "children_photo": row[5],     # photo
            "key_index": row[6],     # key_index
            "key_grouped_index": row[7]     # grouped_index

        }
        children.append(child)

    # properties
    cur.execute("SELECT * FROM applicants WHERE parcel_upin = %s", (upin,))
    properties = []
    for row in cur.fetchall():
        property = {
            "property_type": row[1],  # type
            "property_deed_number": row[2],  # deed_number
            "property_plot_number": row[3],  # plot_number
            "property_use": row[4],  # land_use
            "property_developed": row[5],  # developed
            "key_upin": row[6],  # parcel_upin
            "key_index": row[7],  # key_index
            "key_grouped_index": row[8]  # grouped_index

        }
        properties.append(property)

    # guardians
    cur.execute("SELECT * FROM applicants WHERE parcel_upin = %s", (upin,))
    guardians = []
    for row in cur.fetchall():
        guardian = {
            "key_upin": row[1],  # parcel_upin
            "guardian_name": row[2],  #  name
            "guardian_gender": row[3],  #  gender
            "guardian_id": row[4],  #  national_id
            "guardian_address": row[5],  #  address
            "guardian_signature": row[6],  #  signature
            "guardian_photo": row[7],  #  photo
            "guardian_id_photo": row[8],  #  id_photo
            "key_index": row[9],  #  key_index
            "key_grouped_index": row[10]  # grouped_index

        }
        guardians.append(guardian)

    # holders
    cur.execute("SELECT * FROM applicants WHERE parcel_upin = %s", (upin,))
    holders = []
    for row in cur.fetchall():
        holder = {
            "key_upin": row[1],  # parcel_upin
            "owner_name": row[2],  # name
            "owner_gender": row[3],  # gender
            "owner_id": row[4],  # national_id
            "owner_marital_status": row[5],  # marital_status
            "owner_signature": row[6],  # signature
            "owner_photo": row[7],  # photo
            "owner_id_photo": row[8],  # id_photo
            "key_index": row[9],  # key_index
            "key_grouped_index": row[10]  # grouped_index
        }
        holders.append(holder)

    # clc
    cur.execute("SELECT * FROM applicants WHERE parcel_upin = %s", (upin,))
    clcs = []
    for row in cur.fetchall():
        clc = {
            "key_upin": row[1],  # parcel_upin
            "clc_name": row[2],  # name
            "clc_gender": row[3],  # gender
            "clc_id": row[4],  # national_id
            "clc_marital_status": row[5],  # marital_status
            "clc_signature": row[6],  # signature
            "clc_photo": row[7],  # photo
            "clc_id_photo": row[8],  # id_photo
            "key_index": row[9],  # key_index
            "key_grouped_index": row[10]  # grouped_index
        }
        clcs.append(clc)

    parcel_friends = {
        "parcel_geom": parcel_geom_utm,
        "applicants": applicants,
        "children": children,
        "properties": properties,
        "guardians": guardians,
        "holders": holders,
        "clcs": clcs
    }

    return parcel_friends


def get_export_file_name(export_folder, upin, team_no):
    """
    Generate export file name
    :param export_folder:
    :param upin:
    :param team_no:
    :return: _file_url
    """
    file_ext = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '_msdc.geojson'
    file_name = upin + '_' + team_no + '_' + file_ext

    _file_url = export_folder + '\\' + file_name

    return _file_url


def export_feature(data_dir, plugin_dir, feature, dbconfig):
    """
    Export selected feature
    :param data_dir:
    :param plugin_dir:
    :param feature:
    :param dbconfig:
    :return:
    """
    upin = feature['upin']
    #applicants, _geometry = get_parcel_tables(plugin_dir, upin, dbconfig)
    parcel_tables = get_parcel_tables(plugin_dir, upin, dbconfig)

    _geometry = parcel_tables['parcel_geom']
    _geometry = _geometry.ExportToJson()
    #_geometry = _geometry.replace("\\", "")
    #_geometry = json.dumps(_geometry)

    parcel_properties = {
        "forma_applicant_registered_name": feature['registration_name'],
        "forma_applicant_registered_address": feature['registration_address'],
        "forma_applicant_category": feature['registration_category'],
        "forma_date": "",
        "forma_applicant_particulars_corporate_registration": feature['registration_particulars'],
        "forma_parcel_number": str(feature['no_of_parcels_in_holdings']),
        "forma_place": str(feature['place']),
        "forma_purpose": str(feature['purpose']),
        "key_timestart": feature['time_start'],
        "key_timeend": feature['time_end'],
        "forma_size": str(feature['size_in_ha']),
        "key_upin": str(feature['upin']),
        "forma_status": "1",
        "key_index": "1",
        "district_name": str(feature['district']),
        "tlma_name": str(feature['tlma']),
        "gvh_name": str(feature['gvh']),
        "teamno": str(feature['field_team_number']),
        "formb_sheet_number": str(feature['field_sheet_number']),
        "formb_type_evidence": str(feature['evidence_type']),
        "formb_rights_evidence": str(feature['evidence_of_rights']),
        "formb_land_use": str(feature['landuse']),
        "formb_ownership_type": str(feature['ownership_type']),
        "formb_parcels_number": str(feature['no_of_parcels_in_holdings']),
        "formb_additional_info": str(feature['additional_info']),
        "formb_encumbrances": str(feature['encumberances']),
        "formb_encumbrances_type": str(feature['encumberance_type']),
        "formb_dispute": str(feature['dispute']),
        "formb_dispute_type": str(feature['dispute_type']),
        "formb_date": str(feature['date']),
        "formb_status": "1",
        "applicant_TBL": parcel_tables['applicants'],
        "children_TBL": parcel_tables['children'],
        "property_TBL": parcel_tables['properties'],
        "guardian_TBL": parcel_tables['guardians'],
        "customary_estate_TBL": parcel_tables['holders'],
        "clc_TBL": parcel_tables['clcs']
    }

    feature_dict = {
        "type":"Feature",
        "properties": parcel_properties,
        "geometry": eval(_geometry)
    }

    #file_url = data_dir + '\\exports.geojson'
    file_url = get_export_file_name(data_dir, str(feature['upin']), str(feature['field_team_number']))

    with open(file_url, 'w') as geojson:
        json.dump(feature_dict, geojson)

    return file_url


def add_to_canvas():
    """
    Add imported data to map canvas
    :return:
    """
    pass


if __name__ == '__main__':
    _plugin_dir = 'D:\msdc_client'
    sample = 'D:\Data\imports\\40000_4_2019_11_06_12_23_30_msdc.geojson'
    dbsettings = {
        "host": "localhost",
        "port": "5432",
        "database": "msdc",
        "user": "postgres",
        "pass": "postgres"
    }
    parse_geojson(_plugin_dir, sample, dbsettings)

