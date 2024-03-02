from collections import namedtuple
import ast
import json
import sqlite3

# This script queries the Apple Photos database and returns a GeoJSON blob
# which represents all points of interest collected. The source of truth is the
# Apple Photos db.
#
# First, obtain the photos.db
# dogsheep-photos apple-photos photos.db
#
# Then, ensure the album names which contain relevant photos are referenced.
# The script will iterate through all specified albums and return a single
# GeoJSON file. This represents all points of interest collected.
ALBUM_NAMES = [
    'benches outer peninsula',
    'benches northend',
    'benches dartmouth',
    'benches peninsula',
]

RowData = namedtuple('RowData', [
    'sha256',
    'uuid',
    'burst_uuid',
    'filename',
    'original_filename',
    'description',
    'date',
    'date_modified',
    'title',
    'keywords',
    'albums',
    'persons',
    'path',
    'ismissing',
    'hasadjustments',
    'external_edit',
    'favorite',
    'hidden',
    'latitude',
    'longitude',
    'path_edited',
    'shared',
    'isphoto',
    'ismovie',
    'uti',
    'burst',
    'live_photo',
    'path_live_photo',
    'iscloudasset',
    'incloud',
    'portrait',
    'screenshot',
    'slow_mo',
    'time_lapse',
    'hdr',
    'selfie',
    'panorama',
    'has_raw',
    'uti_raw',
    'path_raw',
    'place_street',
    'place_sub_locality',
    'place_city',
    'place_sub_administrative_area',
    'place_state_province',
    'place_postal_code',
    'place_country',
    'place_iso_country_code',
])
def query_database(db_file):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        feature_collection = {
            "type": "FeatureCollection",
        }

        features = []
        # Perform a query for each album
        for album_name in ALBUM_NAMES:
            # Perform the query
            query = """SELECT * FROM apple_photos WHERE albums = '["{}"]'""".format(album_name)
            cursor.execute(query)

            for row in cursor.fetchall():
                f = create_feature(RowData(*row))
                if f is None:
                    continue
                features.append(f)

        feature_collection["features"] = features
        geojson_blob = json.dumps(feature_collection, indent=2)
        print(geojson_blob)


    except sqlite3.Error as e:
        print("Error while querying the database:", e)
    finally:
        # Close the connection
        if conn:
            conn.close()

def create_feature(row: RowData): 
    keywords = ast.literal_eval(row.keywords)

    # Only concerned with photos which are tagged with a type.
    x = True
    for kw in keywords:
        if kw.startswith("type:"):
            x = False
    if x:
        return None

    properties = {}

    for kw in keywords:
        if kw.startswith("size"):
            properties["Size"] = kw.split(":")[1]
        if kw.startswith("type"):
            p = kw.split(":")[1]
            properties["Type"] = p.title()

    # Map the various keywords to the appropriate properties.
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row.longitude, row.latitude]
        },
        "properties": properties,
    }

if __name__ == "__main__":
    database_file = "photos.db"
    query_database(database_file)
