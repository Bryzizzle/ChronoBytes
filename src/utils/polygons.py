import xml.etree.ElementTree as ET
import math
from shapely.geometry import Point, Polygon

from api.yelp import YelpBusiness


def get_polygon_coordinates(xml_string: str) -> list[tuple[float, float]]:
    # takes in xml, spits out coordinates

    # parse xml, # lat long order

    # tree = ET.parse('test.xml')
    # root = tree.getroot()
    root = ET.fromstring(xml_string)

    # print(root.attrib), find posList
    dataNode = root
    while (1):
        if root.tag == "{http://www.opengis.net/gml}posList":
            dataNode = root
            break
        for child in root:
            root = child

    # parse values
    polygon_coordinates = []

    s_vals = (dataNode.text).split()
    for i in range(0, len(s_vals), 2):
        lat = s_vals[i]
        long = s_vals[i + 1]
        # print([long, lat])
        polygon_coordinates.append(tuple((float(lat), float(long))))

    return polygon_coordinates


def furthest_distance(center_coordinates, polygon_coordinates):
    # find longest distance in list
    maxCoordinate = []
    maxD = 0
    for lat, long in polygon_coordinates:
        lat1 = math.radians(center_coordinates[0])
        lat2 = math.radians(lat)
        long1 = math.radians(center_coordinates[1])
        long2 = math.radians(long)
        # calc dist
        # acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*6371
        step1 = (math.sin(lat1) * math.sin(lat2)) + (math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1))
        step2 = math.acos(step1) * 6371

        if step2 > maxD:
            maxD = max(step2, maxD)
            maxCoordinate = [lat, long]

    # print(maxD) # max distance in km
    # print(maxCoordinate)
    return maxD

    # yelp api stuff, 
    # yelp returns list of stuff
    # return list of restaurants / locations that fit in the polygon

    # taking in list of structs


def in_polygon(places_list: list[YelpBusiness], polygon_coordinates: list[tuple[float, float]]) -> list[YelpBusiness]:
    # good places, list of structs
    ret = []

    # parse places list
    for place in places_list:
        # check if the place is in polygon
        lat = place.coord_lat
        long = place.coord_long

        point = Point(lat, long)
        poly = Polygon(polygon_coordinates)

        if point.within(poly):
            ret.append(place)

    return ret

    # point in polygon
    # https://kodu.ut.ee/~kmoch/geopython2021/L3/point-in-polygon.html

# def main():

#     xml_string = '<Inrix docType="GetDriveTimePolygons" copyright="Copyright INRIX Inc." versionNumber="23.0" createdDate="2023-11-12T00:55:15Z" statusId="0" statusText="" responseId="375b392c-2e12-49bf-985e-36fa2efb9398"><Polygons><DriveTime duration="30"><Polygon xmlns="http://www.opengis.net/gml"><exterior><LinearRing><posList>37.8079676628113 -122.44247674942 37.806658744812 -122.435846328735 37.8071093559265 -122.427778244019 37.8075814247131 -122.420761585236 37.8083109855652 -122.410826683044 37.8066158294678 -122.405977249146 37.803955078125 -122.401685714722 37.7954578399658 -122.394089698792 37.8081178665161 -122.367224693298 37.7872395515442 -122.384626865387 37.7835702896118 -122.388296127319 37.7736568450928 -122.381880283356 37.7697730064392 -122.383511066437 37.7599239349365 -122.382202148438 37.7516198158264 -122.38050699234 37.7459764480591 -122.381772994995 37.737672328949 -122.379133701324 37.7335953712463 -122.382287979126 37.7161073684692 -122.384412288666 37.7111506462097 -122.386450767517 37.6781058311462 -122.388253211975 37.6612186431885 -122.395849227905 37.6340961456299 -122.408766746521 37.6293110847473 -122.432219982147 37.6320147514343 -122.436769008636 37.6430869102478 -122.45726108551 37.6264786720276 -122.488095760345 37.677698135376 -122.490992546082 37.6960873603821 -122.494511604309 37.7078461647034 -122.498159408569 37.7217292785645 -122.501270771027 37.7302050590515 -122.506506443024 37.737865447998 -122.506463527679 37.7452898025513 -122.507450580597 37.7527141571045 -122.508437633514 37.7640223503113 -122.510454654694 37.7712750434875 -122.511162757874 37.7764248847961 -122.511677742004 37.7827119827271 -122.511312961578 37.7840852737427 -122.504403591156 37.7864027023315 -122.492172718048 37.7894282341003 -122.486035823822 37.7942776679993 -122.480413913727 37.8018522262573 -122.477130889893 37.8095126152039 -122.47740983963 37.9031753540039 -122.518243789673 37.9055786132813 -122.515454292297 37.8029894828796 -122.455372810364 37.8070449829102 -122.447519302368 37.8079676628113 -122.44247674942</posList></LinearRing></exterior></Polygon></DriveTime></Polygons></Inrix> '
#     polygon = get_polygon_coordinates(xml_string)

#     center = [37.770315, -122.446527]

#     d = furthest_distance(center, polygon)

#     lst = in_polygon()

# if __name__ == "__main__":
#     main()
