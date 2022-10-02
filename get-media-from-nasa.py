import requests
from datetime import datetime
import calendar


url = "https://iswa.gsfc.nasa.gov/IswaSystemWebApp/hapi/data?id=NOAA_KP_P3H&parameters=KP_3H&time.min=2022-09-27T00:00:00.000Z&time.max=2022-09-28T23:00:00.000Z&format=json"

time_start = url.split("&")[2]
time_final = url.split("&")[3]

now = datetime.now()

year = now.year
month = now.month
day = now.day
hour = now.hour

back_year = now.year
back_month = now.month
back_day = day - 1 

if back_day == 0: ### Treatment - 1º day of month 
    if month == 1: ### Treatment - 1º day of year
        back_year = year - 1
        back_month = 12
    else:
        back_month = month - 1
    back_day = calendar.monthrange(back_year, back_month)[1]

### Treatment to modify the url
if month <= 10:
    back_month = '0' + str(back_month)
    if month != 10:
        month = '0' + str(month)
     
if day < 10:
    if day != 1:
        back_day = '0' + str(back_day)
    if day != 10:
        day = '0' + str(day)
        
time_start_out = time_start.split("2022")[0] + str(back_year) + '-' + str(back_month) + '-' + str(back_day) + 'T' + now.strftime("%H:%M:%S") + '.' + time_start.split(".")[-1]
        
time_final_out = time_final.split("2022")[0] + str(year) + '-' + str(month) + '-' + str(day) + 'T' + now.strftime("%H:%M:%S") + '.' + time_final.split(".")[-1]

url = url.split(time_start)[0] + time_start_out + '&' + time_final_out + url.split(time_final)[1]

r = requests.get(url)
dic = r.json()

sum = 0
count = 0
for i in dic.get("data"):
    count += 1
    sum += i[1]

med = sum / count
med_round = round(med)
str_med = str(med_round)

file_name = 'media.txt'
f = open(file_name, 'w+')
f.write(str_med)
f.close()