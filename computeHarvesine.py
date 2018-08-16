from math import radians, cos, sin, asin, sqrt, inf



def funHaversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    #print("lon1: " + str(lon1) + " lat1: " + str(lat1) + " lon2: " + str(lon2) + " lat2: " + str(lat2) )

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371* c * 1000
    # print(" dist: " + str(km))
    return m


lat1 = 42.457806
lon1 = -72.581505
lat2 = 42.36241
lon2 = -72.48823

lat3 = 42.390926
lon3 = -72.525154

dist1 = funHaversine(lon1, lat1, lon2, lat2)
dist2 = funHaversine(lon1, lat1, lon3, lat3)
dist3 = funHaversine(lon2, lat2, lon3, lat3)

# print(str(dist1) + " " + str(dist2) + " " + str(dist3))

