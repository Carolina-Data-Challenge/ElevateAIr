#The data will be processed here
#From the format of the CSV, the data will be put into an entries list
import csv
import math
import matplotlib.pyplot as plt

filename="data/CurrentUSAirData.csv"
filename2="data/SacramentoAirData.csv"
atl="data/AtlanticCityAirData.csv"
no2=[]
o3=[]
pm10=[]
pm25=[]
so2=[]
air_qualities=[]
latitude=[]
longitude=[]

def printEntries(entries):
    for entry in entries:
        print(entry)

def getPollutantIndex(pollutant):
    if pollutant=="no2": return 4
    elif pollutant=="o3": return 5
    elif pollutant=="pm10": return 6
    elif pollutant=="pm25": return 7
    elif pollutant=="so2": return 8

def getEntries(filename):
    current_row=2
    entries=[]

    with open(filename) as f:
        reader=csv.reader(f)
        header_row=next(reader)

        entry_number=1
        entry=next(reader)
        for row in reader:
            
            if row[0]!=entry[1]:
                if not(entry[4]==0 and entry[5]==0 and entry[6]==0 and entry[7]==0 and entry[8]==0):
                    entries.append(entry)
                entry=[]
                entry.append(entry_number) 
                entry.append(row[0]) #append the location
                entry.append(row[1]) #append the city
                entry.append(row[3]) #append the utc
                entry.append(0)
                entry.append(0)
                entry.append(0)
                entry.append(0)
                entry.append(0)
                entry.append(float(row[8])) #append the latitude
                entry.append(float(row[9])) #append the longitude
                
                entry_number+=1
            if float(row[6])>0:
                entry[getPollutantIndex(row[5])]=float(row[6])
            else:
                entry[getPollutantIndex(row[5])]=0
    return entries

def averageEntries(entries):
    
    delete=[]
    i=0
    while(i<len(entries)):
        j=i+1
        while(j<len(entries)):
            if entries[i][1]==entries[j][1]:
                entries[i][4]=(entries[i][4]+entries[j][4])/2
                entries[i][5]=(entries[i][5]+entries[j][5])/2
                entries[i][6]=(entries[i][6]+entries[j][6])/2
                entries[i][7]=(entries[i][7]+entries[j][7])/2
                entries[i][8]=(entries[i][8]+entries[j][8])/2
                delete.append(j)
            j+=i
        i+=1
    
    print(delete)
    return entries

def getAirQualityIndex(row,max_values):
    numberOfValues=0
    no2=row[4]/max_values['no2']
    o3=row[5]/max_values['o3']
    pm10=row[6]/max_values['pm10']
    pm25=row[7]/max_values['pm25']
    so2=row[8]/max_values['so2']
    for i in range(4,9):
        if row[i]>0: numberOfValues+=1
    return (no2+o3+pm10+pm25+so2)/numberOfValues
   
def getColor(AQI):
    if AQI<.1: return ""
    elif AQI<.2: return ""
    elif AQI<.3: return ""
    elif AQI<.4: return ""
    elif AQI<.6: return ""
    else: return ""

def plotCurrentUSAirQuality(good_air,moderate_air,bad_air,critical_air):
    g=plt.scatter(good_air[0],good_air[1],c='paleturquoise',s=.5)
    m=plt.scatter(moderate_air[0],moderate_air[1],c='skyblue',s=.5)
    b=plt.scatter(bad_air[0],bad_air[1],c='deepskyblue',s=.5)
    c=plt.scatter(critical_air[0],critical_air[1],c='blue',s=.5)
    plt.xlim(-130,-65)
    plt.title("Relative Air Qualities Across the Continental United States")
    plt.legend((g,m,b,c),("Relatively Good","Relatively Moderate","Relatively Bad","Relatively Critical"))
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

def getDistance(p1, p2):
    distance=math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
    #print(distance)
    return distance

def knn(entries, air_qualities, center, edge):
    good=0
    moderate=0
    bad=0
    critical=0
    for i in range(0, len(air_qualities)):
        p2=[entries[i][10],entries[i][9]]
        if ((getDistance(center,p2))<=(getDistance(center,edge))):
            if air_qualities[i]<.1: good+=1
            elif air_qualities[i]<.2: moderate+=1
            elif air_qualities[i]<.4: bad+=1
            else: critical+=1
    if good>=moderate and good>=moderate and good>=critical:
        return "RELATIVELY GOOD"
    elif moderate>=good and moderate>=bad and moderate>=critical:
        return "RELATIVELY MODERATE"
    elif bad>=good and bad>=moderate and bad>=critical:
        return "RELATIVELY BAD"
    else:
        return "RELATIVELY CRITICAL"

def plotCurrentUSAirQualityWithKnn(good_air,moderate_air,bad_air,critical_air,center,bound):
    g=plt.scatter(good_air[0],good_air[1],c='paleturquoise',s=.5)
    m=plt.scatter(moderate_air[0],moderate_air[1],c='skyblue',s=.5)
    b=plt.scatter(bad_air[0],bad_air[1],c='deepskyblue',s=.5)
    c=plt.scatter(critical_air[0],critical_air[1],c='blue',s=.5)
    plt.xlim(-130,-65)
    plt.title("Relative Air Qualities Across the Continental United States")
    plt.legend((g,m,b,c),("Relatively Good","Relatively Moderate","Relatively Bad","Relatively Critical"))
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.Circle((center[0], center[1]), getDistance(center,bound),fill=False)
    plt.show()    

def plotCityLineGraph(air_qualities):
    plt.plot(air_qualities)
    plt.title("Air Qualities [2015-Current]")
    plt.xlabel("Entry #")
    plt.ylabel("Relative Air Quality")

    plt.show()

#Get the entries
entries=getEntries(filename)
del entries[0]

#Put them into lists
for i in range(0,len(entries)):
    no2.append(entries[i][getPollutantIndex('no2')])
    o3.append(entries[i][getPollutantIndex('o3')])
    pm10.append(entries[i][getPollutantIndex('pm10')])
    pm25.append(entries[i][getPollutantIndex('pm25')])
    so2.append(entries[i][getPollutantIndex('so2')])
    latitude.append(entries[i][9])
    longitude.append(entries[i][10])

max_values={
    "no2":max(no2),
    "o3":max(o3),
    "pm10":max(pm10),
    "pm25":max(pm25),
    "so2":max(so2)
}

for entry in entries:
    air_qualities.append(getAirQualityIndex(entry,max_values))
    
#Analysis
good_air=[[],[]]
moderate_air=[[],[]]
bad_air=[[],[]]
critical_air=[[],[]]

for i in range(0, len(air_qualities)):
    if air_qualities[i]<.1:
        good_air[0].append(longitude[i])
        good_air[1].append(latitude[i])
    elif air_qualities[i]<.2:
        moderate_air[0].append(longitude[i])
        moderate_air[1].append(latitude[i])
    elif air_qualities[i]<.4:
        bad_air[0].append(longitude[i])
        bad_air[1].append(latitude[i])
    else:
        critical_air[0].append(longitude[i])
        critical_air[1].append(latitude[i])

#plotCurrentUSAirQuality(good_air,moderate_air,bad_air,critical_air)
nyc=[-74.0060,40.7128]
outer_bound=[-80,40]
quality=knn(entries,air_qualities,nyc,outer_bound)
print("The quality at ["+str(nyc[0])+", "+str(nyc[1])+"] is likely "+quality)

#plotCurrentUSAirQualityWithKnn(good_air,moderate_air,bad_air,critical_air,nyc,outer_bound)

entries=getEntries(filename2)
del entries[0]

for i in range(0,len(entries)):
    no2.append(entries[i][getPollutantIndex('no2')])
    o3.append(entries[i][getPollutantIndex('o3')])
    pm10.append(entries[i][getPollutantIndex('pm10')])
    pm25.append(entries[i][getPollutantIndex('pm25')])
    so2.append(entries[i][getPollutantIndex('so2')])
    latitude.append(entries[i][9])
    longitude.append(entries[i][10])

max_values={
    "no2":max(no2),
    "o3":max(o3),
    "pm10":max(pm10),
    "pm25":max(pm25),
    "so2":max(so2)
}

for entry in entries:
    air_qualities.append(getAirQualityIndex(entry,max_values))

#plotCityLineGraph(air_qualities)

#Atlantic city

entries=getEntries(atl)
del entries[0]

for i in range(0,len(entries)):
    no2.append(entries[i][getPollutantIndex('no2')])
    o3.append(entries[i][getPollutantIndex('o3')])
    pm10.append(entries[i][getPollutantIndex('pm10')])
    pm25.append(entries[i][getPollutantIndex('pm25')])
    so2.append(entries[i][getPollutantIndex('so2')])
    latitude.append(entries[i][9])
    longitude.append(entries[i][10])

max_values={
    "no2":max(no2),
    "o3":max(o3),
    "pm10":max(pm10),
    "pm25":max(pm25),
    "so2":max(so2)
}

for entry in entries:
    air_qualities.append(getAirQualityIndex(entry,max_values))

plotCityLineGraph(air_qualities)