import serial
import xlrd
import xlwt
from xlrd import open_workbook
from tempfile import TemporaryFile
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np
from operator import sub

import xlwt
import time
wood=['744.69', '189.54', '379.00', '105.49', '240.07', '349.98', '116.78', '154.42', '100.73', '26.10', '60.51', '29.21', '356.61', '119.84', '42.73', '29.29', '60.03', '125.75']
metal=['5064.12', '1232.44', '2791.43', '492.85', '1928.96', '3140.74', '259.57', '343.37', '238.46', '114.69', '444.12', '99.31', '917.49', '987.93', '308.69', '218.82', '435.02', '1036.53']
plastic=['978.15', '277.82', '353.90', '121.92', '135.78', '138.18', '82.92', '115.10', '105.66', '57.35', '100.43', '47.71', '227.35', '193.83', '102.90', '56.86', '106.14', '218.59']
paper =['2080.42', '1071.46', '1482.24', '813.64', '1076.46', '1164.86', '446.52', '504.98', '286.16', '112.71', '197.73', '94.44', '1843.06', '449.15', '160.45', '99.07', '207.07', '381.94']
drywall=['1391.87', '497.65', '787.42', '402.06', '626.42', '730.94', '316.98', '361.11', '187.07', '58.93', '94.81', '52.58', '1194.47', '225.10', '78.48', '51.69', '107.88', '183.33']
concrete=['912.15', '307.24', '491.49', '269.77', '431.85', '511.40', '246.32', '289.18', '156.24', '49.04', '81.09', '43.81', '939.42', '183.41', '66.27', '42.21', '88.74', '156.30']






#ser.close()
ser = serial.Serial(
    port='COM8',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
material='wood'
Data=[]

if ser.isOpen():
    ser.flushInput()
    ser.flushOutput()
    
    while True:
        Data = ser.readline()
        Data=Data.decode("utf-8")
        Data=Data.split(',')
        del Data[-1]
        Datanp= np.asarray(Data, dtype=np.float32)
        woodnp=np.asarray(wood, dtype=np.float32)
        papernp=np.asarray(paper, dtype=np.float32)
        metalnp=np.asarray(metal, dtype=np.float32)
        plasticnp=np.asarray(plastic, dtype=np.float32)
        drywallnp=np.asarray(drywall, dtype=np.float32)
        concretenp=np.asarray(concrete, dtype=np.float32)
        
        #df = pd.DataFrame.from_dict({'material':material,'reading':Data})
        #dft=df.T
        #print(dft)
        diffwood= [a - b for a, b in zip(Datanp, woodnp)]#differnece B/W unknown and known material reading
        diffpaper= [c - d for c, d in zip(Datanp, papernp)]
        diffmetal= [e - f for e, f in zip(Datanp, metalnp)]
        diffplastic= [g - h for g, h in zip(Datanp, plasticnp)]
        diffdrywall= [g - h for g, h in zip(Datanp, drywallnp)]
        diffconcrete= [g - h for g, h in zip(Datanp, concretenp)]
        
        #sum of values in diffrence array
        sumofwood=sum(float(i) for i in diffwood)
        sumofpaper=sum(float(j) for j in diffpaper)
        sumofmetal=sum(float(k) for k in diffmetal )
        sumofplastic=sum(float(l) for l in diffplastic)
        sumofdrywall=sum(float(l) for l in diffdrywall)
        sumofconcrete=sum(float(l) for l in diffconcrete)
        #all the sums in single array
        
        diffsinarray=[abs(sumofwood),abs(sumofpaper),abs(sumofmetal),abs(sumofplastic),abs(sumofdrywall),abs(sumofconcrete)]
        min_value=min(diffsinarray)
        min_index=diffsinarray.index(min_value)
        fuzzwood=fuzz.ratio(Data, wood)
        fuzzpaper=fuzz.ratio(Data, paper)
        fuzzmetal=fuzz.ratio(Data, metal)
        fuzzplastic=fuzz.ratio(Data, plastic)
        fuzzdrywall=fuzz.ratio(Data, drywall)
        fuzzconcrete=fuzz.ratio(Data, concrete)
        
        
        results=[fuzzwood,fuzzpaper,fuzzmetal,fuzzplastic,fuzzdrywall,fuzzconcrete]
        max_value = max(results)
        max_index = results.index(max_value)
        #print(diffsinarray)
        #if min_index == max_index:
        if min_index == 0:
            print("looks like wood")
        elif min_index == 1:
                print("looks like paper")
        elif min_index == 2:
            print("looks like metal")
        elif min_index == 3:
            print ("looks like plastic")
        elif min_index == 4:
            print ("looks like drywall")
        elif min_index == 5:
            print("looks like concrete")
        #else:
         #  print("unknown")
            
            
        
        
            #print (results)
        #print((Data))
        #print(len(Data))
    
    
    

