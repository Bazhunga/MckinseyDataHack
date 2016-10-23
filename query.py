import urllib2

start = "110 Charles St,Toronto ON"
destination = "51 Mountainash Road,Brampton ON|25 Woodbine Downs Blvd,Etobicoke,ON"

start = start.replace(" ", "+")
destination = destination.replace(" ", "+") 
response = urllib2.urlopen('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=' + start + '&destinations=' + destination)
json_result = response.read()
print(json_result)