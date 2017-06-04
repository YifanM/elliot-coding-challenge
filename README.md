## As part of my co-op application to Elliot for Fall 2017.

## yifan.ma@uwaterloo.ca

Program output on June 4 with sample calendar.csv file (program depends on current day so output may vary):

(actual)

2017-06-07 18:31:00 22:00:00


(debug, datetime.time is (hour, minute, ?second))

2017-06-04 [datetime.time(8, 0), datetime.time(9, 29, 59)]  
2017-06-05 [datetime.time(20, 30, 1), datetime.time(22, 0)]  
2017-06-06 [datetime.time(20, 0), datetime.time(22, 0)]  
2017-06-07 [datetime.time(8, 0), datetime.time(10, 34, 59)]  
2017-06-07 [datetime.time(11, 1), datetime.time(11, 29, 59)]  
2017-06-07 [datetime.time(11, 35, 1), datetime.time(12, 29, 59)]  
2017-06-07 [datetime.time(18, 31), datetime.time(22, 0)]  
2017-06-08 [datetime.time(8, 0), datetime.time(8, 59, 59)]

Explanation:

First csv entry removes most of June 4 and 5, first two debug lines show the remaining free time blocks on those days.  
June 6 csv entries remove free time near midnight, free time from 1:30pm to 2:30pm, and free time from midnight to 7:59pm. Next debug line shows the remaining block on June 6, 8:00pm to 10:00pm.  
June 7 csv entries remove small chunks of free time around 10am 11am and removes entire afternoon. Remaining blocks are the evening and portions of the morning.  
The next two csv entries take up almost all the time until one week later, June 11. The second last csv entry shows one small block left on June 8.  

The largest block is thus the actual output shown, the evening of June 7. It has the largest size, at a duration of about 3 and a half hours. The next largest block is in the morning on June 7 with a duration of about 2 and a half hours.
