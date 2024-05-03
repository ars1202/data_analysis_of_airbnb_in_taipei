import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
plt.rc('font', family='Microsoft JhengHei')

def pie_func(c,d):
  t = int(round(c/100.*sum(d))) 
  return f'{c:.2f}%\n( {t} )' 

connection = mysql.connector.connect(host='HOST',
                                    port='PORT',
                                    user='USER_NAME',
                                    password='PASSWORD',
                                    database='DATABASE_NAME')
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) AS 'total_host' FROM `taipei`;")
total = cursor.fetchall()[0][0]

#Question 1
#只統計前十名，剩下的都會統計成others
cursor.execute("SELECT `neighbourhood_cleansed`,COUNT(`neighbourhood_cleansed`) AS 'location' FROM `taipei` WHERE `neighbourhood_cleansed` IS NOT NULL GROUP BY `neighbourhood_cleansed` ORDER BY `location` DESC;")
location = cursor.fetchall() #
limit = 9
tmp = location[:limit]
tmp.append(("Others",sum(i[1] for i in location[limit:])))
#print(tmp)

plt.figure(figsize=(12,8))
plt.title('total room:'+str(total))
plt.pie([i[1] for i in tmp],
        labels=[i[0] for i in tmp],
        autopct=lambda x:pie_func(x,[i[1] for i in tmp]),
        labeldistance=1.05,
        pctdistance=0.9
        )
plt.show()
del tmp

#Question 2
cursor.execute("SELECT t.`room_type`,COUNT(t.`room_type`) AS 'taipei',r.`rome` AS 'rome',san.`san_francisco` AS 'san_francisco' FROM `taipei` t INNER JOIN (SELECT `room_type`,COUNT(`room_type`) AS 'rome' FROM `rome` GROUP by `room_type`) r ON r.`room_type`=t.`room_type` INNER JOIN (SELECT `room_type`,COUNT(`room_type`) AS 'san_francisco' FROM `san francisco` GROUP by `room_type`) san ON san.`room_type`=t.`room_type` GROUP BY t.`room_type`;")
tmp = cursor.fetchall()
room = []
for j in range(1,len(tmp)):
  room.append([i[j] for i in tmp])
#print(room)
room_type = ['entire home','private room','hotel','shared room']
cities = ['taipei','rome','san francisco']


for i in range(len(room)):
  bar = plt.bar(room_type,[round(room[i][j]*100/sum(room[i]),1) for j in range(len(room[i]))],width=0.5,color=['r','g','b','y'])
  plt.bar_label(bar,label_type='edge')
  plt.ylabel('%')
  plt.title(cities[i])
  plt.savefig(cities[i]+'.png')
  plt.show()

#Question 3
#計算出的價格為當地貨幣，因此要匯率轉換(日圓*0.21、澳幣*21.6、泰銖0.88)
cursor.execute("SELECT t.`room_type`,ROUND(AVG(REPLACE(REPLACE(t.`price`,'$',''),',','')),1) AS 'taipei',j.`tokyo` AS 'tokyo',s.`sydney` AS 'sydney',b.`bangkok` AS 'bangkok' FROM `taipei` t INNER JOIN (SELECT `room_type`,ROUND(AVG(REPLACE(REPLACE(`price`,'$',''),',',''))*0.21,1) AS 'tokyo' FROM `tokyo` WHERE `number_of_reviews`>5 GROUP BY `room_type`) j ON j.`room_type`=t.`room_type` INNER JOIN (SELECT `room_type`,ROUND(AVG(REPLACE(REPLACE(`price`,'$',''),',',''))*21.6,1) AS 'sydney' FROM `sydney` WHERE `number_of_reviews`>5 GROUP BY `room_type`) s ON s.`room_type`=t.`room_type` INNER JOIN (SELECT `room_type`,ROUND(AVG(REPLACE(REPLACE(`price`,'$',''),',',''))*0.88,1) AS 'bangkok' FROM `bangkok` WHERE `number_of_reviews`>5 GROUP BY `room_type`) b ON b.`room_type`=t.`room_type` WHERE `number_of_reviews`>5 GROUP BY `room_type`;")
tmp = cursor.fetchall()
cities = ['taipei','tokyo','sydney','bangkok']
price = list(zip(*tmp))
print(price)
_, ax = plt.subplots(figsize=(12,8),layout='constrained')
plt.rcParams.update({'font.size': 10})

x = np.arange(len(price[0]))
width = 0.2
mul=0

for i in price[1:]:
  offset = width*mul
  pic = ax.bar(x+offset,i,width,label=cities[mul])
  ax.bar_label(pic,padding=3)
  mul+=1
ax.set_ylabel('價格$')
ax.set_title('avg price')
ax.set_xticks(x+width,[i[0] for i in tmp])
ax.legend(loc='best')
plt.savefig('avg_price.png')
plt.show()

cursor.close()
#connection.commit()
connection.close() 