"""
Script that averages the entropy, relative entropy, and gini coefficient as a function of item "age". 
The "age" of an item is defined as the number of calendar months since the first month in which it was tagged.
"""

import sys 
sys.path.append('../bin') 
from dbSetup import *


cursor=db.cursor()
cursor.execute("DROP TABLE IF EXISTS full_table;") 


cursor.execute("CREATE TABLE full_table (age mediumint(8), ent FLOAT, rel_ent FLOAT, gini FLOAT, \
    index(age)) ENGINE=innodb DEFAULT CHARSET=latin1;") 
     
closeDBConnection(cursor) 

cursor=db.cursor()
cursorSS=dbSS.cursor()
cursorSS.execute("select * from ent_table order by item_id, month;")

###
#Sorts ent_table into a dictionary, adding data for months with no tags.
###

dic={}
for row in cursorSS:
    
    #if there is a new id, create a new key w/ val = a list where the zero index is the age
    if row[0] not in dic:
        dic[row[0]] = [-1]
        y= row[1].year
        m= row[1].month
    
    #fills in data if an item hasn't been tagged in that month
    while y!= row[1].year or m!= row[1].month:
        m+=1
        if m == 13:
            y+=1
            m=1    
        
        #I didn't really nead to put in a value for age but did in case there was a need to know the highest age of a particular item
        dic[row[0]][0] += 1   #bump the age up 
        dic[row[0]].append(dic[row[0]][-1])
    
    #append new list to value with age and data
    m+=1
    if m == 13:
        y+=1
        m=1
    dic[row[0]][0] += 1
    dic[row[0]].append([dic[row[0]][0], row[2], row[3], row[4]])
        

###
#Takes the dictionary made above and averages the values based on the age.
#While also inserting the averages into the table.
###
age = 0
for x in range(100): #100 represents the max possible age. Should be slightly less but not sure the exact number. 
    age += 1
    ent = 0
    rel_ent = 0
    gini = 0
    count = 0   
    
    #adds all values for a certain age
    for i in dic:
        
        #skips an item if it's too young
        if len(dic[i]) > age:
            ent += dic[i][age][1]
            rel_ent += dic[i][age][2]
            gini += dic[i][age][3]
            count +=1
    
    #a check for edge cases, then takes the average of each value
    if count > 0:
        ent = ent / count
        rel_ent = rel_ent / count
        gini = gini / count       
    cursor.execute("insert ignore into full_table (age, ent, rel_ent, gini) values (%s,%s,%s,%s)",(age - 1,ent,rel_ent,gini))
    db.commit()


closeDBConnection(cursor)	 
closeDBConnection(cursorSS)