# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 15:05:44 2015

@author: Admin
"""
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import sqlite3
import numpy as np


# Open a connection to the database file
con = sqlite3.connect('renewable.db')
# Read sqlite query results into a pandas DataFrame
dfLocation = pd.read_sql_query("SELECT * from location", con)
dfPorts = pd.read_sql_query("SELECT * from ports", con)
#close the connection fetching data from DB
con.close()


# Assign radius of the earth to R in order to find distance between 2 locations given their geographic spots
R = 6373.0
#Initialising the lists that stores choosen port latitude and longitude
avgDistance=[]
portLong = []
portLat = []
# i iteration for each location j iteration for each port 
for i in range(0,dfLocation.shape[0]):
    portDistance=[]
    long1 = radians(dfLocation.iloc[i][0])
    lat1 = radians(dfLocation.iloc[i][1])
    for j in range(0,dfPorts.shape[0]):         
        long2 = radians(dfPorts.iloc[j][0])
        lat2 = radians(dfPorts.iloc[j][1])
        dlong = long2 - long1
        dlat = lat2 - lat1
        #Find the distance given latitude and longitude values    
        temp1 = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
        temp1 = 2 * atan2(sqrt(temp1), sqrt(1 - temp1))
        distance = R * temp1
        #Append  to locationDistance list in order to find shortest at end of all possible combinations
        portDistance.append(distance)
    minPortDistance = np.min(portDistance)
    #Select the port with minimum distance
    selectedPort = portDistance.index(minPortDistance)
    #Get their corresponding latitude and longitude values
    portLong.append(dfPorts.iloc[selectedPort][0])
    portLat.append(dfPorts.iloc[selectedPort][1])
    print "Location ",i+1," Corresponding nearest port is ", selectedPort+1
    #print "\nThe shoretest distance from the selected location and the port is ",np.min(portDistance)," at port with latitude ", ," and latitude ",
# l iteration for each location k iteration for every other locations
for l in range(0,dfLocation.shape[0]):
    locationDistance=[] 
    long1 = radians(dfLocation.iloc[l][0])
    lat1 = radians(dfLocation.iloc[l][1])    
    for k in range(0,dfLocation.shape[0]):
        if(i<>k):  # i==j gives distance 0 so ignore it.            
            long2 = radians(dfLocation.iloc[k][0])
            lat2 = radians(dfLocation.iloc[k][1])
            dlong = long2 - long1
            dlat = lat2 - lat1
            #Find the distance with given latitude and longitude values
            temp1 = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
            temp1 = 2 * atan2(sqrt(temp1), sqrt(1 - temp1))
            distance = R * temp1
            #Append  to locationDistance list in order to find averageDistance at end of all possible combinations
            locationDistance.append(distance)
            #avg.append(distance)
    #Attach the corresponding port and its distance at the end
    long3 = radians(portLong[l])
    lat3 = radians(portLat[l])
    dlong = long3 - long1
    dlat = lat3 - lat1
    #Find the distance with given latitude and longitude values
    temp1 = sin(dlat / 2)**2 + cos(lat1) * cos(lat3) * sin(dlong / 2)**2
    temp1 = 2 * atan2(sqrt(temp1), sqrt(1 - temp1))
    distance = R * temp1
    locationDistance.append(distance)
    print " Mean distance between location ",l+1,"and all other locations and selected port is ",np.mean(locationDistance)        
    avgDistance.append(np.mean(locationDistance))
#Pick the location with shortest average distance.
selectedLocation = avgDistance.index(np.min(avgDistance))
print "\nThe minimum average distance is ",np.min(avgDistance)," at location ",selectedLocation+1," with longitude ",dfLocation.iloc[selectedLocation][0], " and latitude ",dfLocation.iloc[selectedLocation][1]



