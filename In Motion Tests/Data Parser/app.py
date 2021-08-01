import os
import json
import uuid
from geopy import distance

tower_location = (45.31829321111939, -75.75819861966221)

pickup_location = "/opt/data/"
drop_off_location = "/opt/dropoff/"

def getDistance(one,two):
    return round((distance.distance(one, two).km)*1000,3)

def nukeFile(path):
    os.remove(path)

def findFiles(path):
    return os.listdir("/opt/data")
def readFile(path,file):
    f = open(path+"/"+file, "r")
    data = json.loads(f.readline())
    f.close()
    return data
def replaceGPS(data):
    data["gps"] = {"mode": "3", "sat": "4", "lat": "45.270314", "lon": "-75.429543", "speed": "0"}
    return data
#print (getDistance(tower_location,test_location1))
#print (findFiles(pickup_location))
files = findFiles(pickup_location)
#{"mode": "3", "sat": "4", "lat": "0.0", "lon": "0.0", "speed": "0"}
#{'delay': '5.55', 'server': {'server': '172.21.30.10', 'port': '5000', 'name': 'Georges Home (VPN)'}, 'timestamp': '2021-07-20 23:32:24.534457', 
# 'sigalg': 'Dilithium2', 
# 'gps': {'mode': '3', 'sat': '4', 'lat': '45.270314', 'lon': '-75.429543', 'speed': '0'}}
csv_data = []
dilithium2 = []
dilithium3 = []
dilithium5 = []
rainbow1 = []
rainbow3 = []
rainbow5 = []
for file in files:
    data_from_file = readFile(pickup_location,file)
    #data_from_file = replaceGPS(data_from_file)
    #print (data_from_file)
    delay = data_from_file["delay"]
    server = data_from_file["server"]["name"]
    signature_algorithm = data_from_file["sigalg"]
    lat = data_from_file["gps"]["lat"]
    lon = data_from_file["gps"]["lon"]
    speed = data_from_file["gps"]["speed"]
    dist = getDistance(tower_location,(float(lat),float(lon)))
    tmp = ""+str(server)+","+str(signature_algorithm)+","+str(delay)+","+str(lat)+","+str(lon)+","+str(speed)+","+str(dist)
    #print (tmp)
    csv_data.append(tmp)
    if signature_algorithm == "Dilithium2":
        dilithium2.append(tmp)
    elif signature_algorithm == "Dilithium3":
        dilithium3.append(tmp)
    elif signature_algorithm == "Dilithium5":
        dilithium5.append(tmp)
    elif signature_algorithm == "Rainbow-I-Classic":
        rainbow1.append(tmp)
    elif signature_algorithm == "Rainbow-III-Classic":
        rainbow3.append(tmp)
    elif signature_algorithm == "Rainbow-V-Classic":
        rainbow5.append(tmp)
    #nukeFile(pickup_location+""+file)
#print (csv_data)
file_name = str(uuid.uuid4())
f = open(drop_off_location+file_name+"-overall.csv", "a")
f.write("Server Name,Signature Algorithm,Delay,Lat,Lon,Speed (kph),Distance (m)\n")
for i in csv_data:
    f.write(i+"\n")
f.close()

f = open(drop_off_location+file_name+"-dilithium2.csv", "a")
f.write("Server Name,Signature Algorithm,Delay,Lat,Lon,Speed (kph),Distance (m)\n")
for i in dilithium2:
    f.write(i+"\n")
f.close()

f = open(drop_off_location+file_name+"-dilithium3.csv", "a")
f.write("Server Name,Signature Algorithm,Delay,Lat,Lon,Speed (kph),Distance (m)\n")
for i in dilithium3:
    f.write(i+"\n")
f.close()

f = open(drop_off_location+file_name+"-dilithium5.csv", "a")
f.write("Server Name,Signature Algorithm,Delay,Lat,Lon,Speed (kph),Distance (m)\n")
for i in dilithium5:
    f.write(i+"\n")
f.close()

f = open(drop_off_location+file_name+"-rainbow1.csv", "a")
f.write("Server Name,Signature Algorithm,Delay,Lat,Lon,Speed (kph),Distance (m)\n")
for i in rainbow1:
    f.write(i+"\n")
f.close()

f = open(drop_off_location+file_name+"-rainbow3.csv", "a")
f.write("Server Name,Signature Algorithm,Delay,Lat,Lon,Speed (kph),Distance (m)\n")
for i in rainbow3:
    f.write(i+"\n")
f.close()

f = open(drop_off_location+file_name+"-rainbow5.csv", "a")
f.write("Server Name,Signature Algorithm,Delay,Lat,Lon,Speed (kph),Distance (m)\n")
for i in rainbow5:
    f.write(i+"\n")
f.close()