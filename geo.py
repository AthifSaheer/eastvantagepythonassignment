# # Import the required library
# from geopy.geocoders import Nominatim
# import geopy.distance as GeoDistance
# import asyncio

# # Initialize Nominatim API
# geolocator = Nominatim(user_agent="MyApp")

# async def lag_log(place):
#     return await geolocator.geocode(place)

# # location = asyncio.run(lag_log(place))

# # print("The latitude is: ", delhi.latitude)
# # print("The longitude is: ", delhi.longitude)

# # coords_1 = (11.3033733, 76.33758118764645)
# # coords_2 = (11.3724262, 75.7826701)
# # print(distance.geodesic(coords_1, coords_2).km)

# places_latlog = [("28.5355", "77.3910"), ("12.9716", "77.5946")]

# def matchedplaces(place, distance):
#     location = asyncio.run(lag_log(place))
#     location_lag_log = (location.latitude, location.longitude)

#     km_l = []
#     for plc in places_latlog:
#         location2_lag_log = plc[0], plc[1]
#         km = GeoDistance.geodesic(location_lag_log, location2_lag_log).km
#         km_l.append(km)

#     return km_l

# kms = matchedplaces("Delhi", 10)
# print("kilometers: ", kms)