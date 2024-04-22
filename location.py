import math
from pymongo import MongoClient

class RTreeNode:
    def __init__(self, bounding_box, data=None):
        self.bounding_box = bounding_box
        self.data = data
        self.children = []

class GeoLocationDict:
    def __init__(self, latitude, longitude, name):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name

def calculate_bounding_box(latitude, longitude, distance):
    earth_radius = 6371.0
    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)
    delta = distance / earth_radius
    min_lat = math.degrees(lat1 - delta)
    max_lat = math.degrees(lat1 + delta)
    delta_lon = math.asin(math.sin(delta) / math.cos(lat1))
    min_lon = math.degrees(lon1 - delta_lon)
    max_lon = math.degrees(lon1 + delta_lon)
    min_lon = max(min_lon, -180.0)
    max_lon = min(max_lon, 180.0)
    return [(min_lon, min_lat), (max_lon, max_lat)]

def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    return distance

def range_query(node, search_area, target_lat, target_lon, results):
    if node is None:
        return
    if intersects(node.bounding_box, search_area):
        if isinstance(node.data, GeoLocationDict):
            distance = calculate_distance(target_lat, target_lon, node.data.latitude, node.data.longitude)
            results.append((node.data, distance))
        for child in node.children:
            range_query(child, search_area, target_lat, target_lon, results)

def intersects(box1, box2):
    x1_min, y1_min = box1[0]
    x1_max, y1_max = box1[1]
    x2_min, y2_min = box2[0]
    x2_max, y2_max = box2[1]
    return not (x1_max < x2_min or x1_min > x2_max or y1_max < y2_min or y1_min > y2_max)

def perform_location_query(latitude, longitude):
    client = MongoClient("mongodb+srv://20z342:cBwPEGWx2iMWCUyE@cluster0.xdefz6l.mongodb.net/")
    dbName = "complaints"
    collectionName = "user_locations"
    collection = client[dbName][collectionName]
    locations_data = locations_data = collection.find({}, {"latitude": 1, "longitude": 1, "_id": 1})

    root = RTreeNode([(-180, -90), (180, 90)])
    erode_bounding_box = calculate_bounding_box(latitude, longitude, 3)
    results = []
    for location_data in locations_data:
        lat = location_data["latitude"]
        lon = location_data["longitude"]
        _id = location_data["_id"]
        location_node = RTreeNode([(lon, lat), (lon, lat)], GeoLocationDict(lat, lon, _id))
        root.children.append(location_node)
    range_query(root, erode_bounding_box, latitude, longitude, results)
    ans = []
    images = []
    for result, distance in results:
        result_id = result.name
        document = collection.find_one({"_id": result_id}, {"complaint": 1, "_id": 0, "imageUrl" : 1})
        ans.append(document['complaint'])
        if document['imageUrl'] != "":
            images.append(document['imageUrl'])

    dic = {}
    dic["complaints"] = ans
    dic["urls"] = images
    return dic

# Example usage:
# latitude = 11.3410
# longitude = 77.7172
# locations_data = collection.find({}, {"latitude": 1, "longitude": 1, "_id": 1})
# results = perform_location_query(latitude, longitude)
# print(results)