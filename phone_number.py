import phonenumbers
from phonenumbers import geocoder
import folium

ch_number = phonenumbers.parse("+916380351620")
print(geocoder.description_for_number(ch_number, "en"))
yournumber = geocoder.description_for_number(ch_number, "en")
from phonenumbers import carrier
service_provider = phonenumbers.parse("+916380351620")
print(carrier.name_for_number(service_provider, "en"))

from opencage.geocoder import OpenCageGeocode
Key="15c81528a4a14d7cb9934ff90f9a1e13"
geoc = OpenCageGeocode(Key)
quury = str(yournumber)
result = geoc.geocode(quury)
print(result[0]['geometry']['lat'], result[0]['geometry']['lng'])

lat = result[0]['geometry']['lat']
lng = result[0]['geometry']['lng']

myMap = folium.Map(location=[lat,lng],zoom_start=9)
folium.Marker([lat,lng],popup=yournumber).add_to((myMap))

myMap.save("test.html")