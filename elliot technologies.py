#Suppose we have a CSV file with calendar events.  This file has the following format:
#user id, begin time, end time
#...

#For example, the file may be 
#100, 2017-04-03 13:30:00, 2017-04-03 14:30:00
#101, 2017-04-15 00:00:00, 2017-04-15 23:59:59

#The times listed in the file are times when each user is busy, in the format above.
#A single user may have several events listed and some events may overlap.
#Write a program to read the CSV file (called calendar.csv) and find the longest block of time in a single day that's free for all the users to meet.
#Only look for meetings between 8AM and 10PM, on days up to one week from the date the program is run.

import csv
from datetime import date, datetime, timedelta, time
from collections import defaultdict

CONST_START_OF_DAY = time(8, 0, 0)
CONST_END_OF_DAY = time(22, 0, 0)
currDate = datetime.now().date()
freeTime = defaultdict(list)

#Assumptions

#time at which program is run is not a factor in determining free time in the current day
#an event's end time will always be greater than or equal to its start time
#an event may be longer than one day
#output format is: day startTime endTime
#if there is a tie for the largest free time block, output the soonest one

def adjustTime(startTime, endTime): #only adjusts single out-of-bounds, double out-of-bounds should not be passed to this
    return [max(startTime, CONST_START_OF_DAY), min(endTime, CONST_END_OF_DAY)]

def stringToDate(dateString):
    return date(*map(int, dateString.split("-")))

def stringToTime(timeString):
    return time(*map(int, timeString.split(":")))

def dayInRange(dayDate):
    return currDate <= dayDate and currDate + timedelta(days=7) >= currDate

def timeInRange(dayTime):
    return dayTime >= CONST_START_OF_DAY and dayTime <= CONST_END_OF_DAY

def timeToDateTime(date, time):
    return datetime.combine(date, time)

def applyEvent(key, times):
    currentFreeTime = freeTime[key]
    startTime, endTime = times
    newFreeTime = []
    for block in currentFreeTime:
        if startTime <= block[0] and endTime >= block[1]:
            continue
        elif startTime < block[0] and endTime < block[0]:
            newFreeTime.append(block)
        elif startTime > block[1] and endTime > block[1]:
            newFreeTime.append(block)
        elif startTime > block[0] and endTime < block[1]:
            newFreeTime.append([block[0], (timeToDateTime(key, startTime) - timedelta(seconds=1)).time()])
            newFreeTime.append([(timeToDateTime(key, endTime) + timedelta(seconds=1)).time(), block[1]])
        elif startTime <= block[0]: #endTime is block[0] <= endTime < block[1] at this point
            newFreeTime.append([(timeToDateTime(key, endTime) + timedelta(seconds=1)).time(), block[1]])
        elif endTime >= block[1]: #startTime is block[0] < startTime <= block[1] at this point
            newFreeTime.append([block[0], (timeToDateTime(key, startTime) - timedelta(seconds=1)).time()])
    freeTime[key] = newFreeTime
    
def updateFreeTime(row):
    startString = row[1].strip().split()
    endString = row[2].strip().split()
    startDay, endDay = list(map(stringToDate, [startString[0], endString[0]]))
    startTime, endTime = list(map(stringToTime, [startString[1], endString[1]]))
    if startDay == endDay:
        if dayInRange(startDay) and (timeInRange(startTime) or timeInRange(endTime)):
            applyEvent(startDay, adjustTime(startTime, endTime))
    else:
        if startTime <= CONST_END_OF_DAY and dayInRange(startDay):
            applyEvent(startDay, adjustTime(startTime, CONST_END_OF_DAY))
        if endTime >= CONST_START_OF_DAY and dayInRange(endDay):
            applyEvent(endDay, adjustTime(CONST_START_OF_DAY, endTime))
        for i in range(1, (endDay-startDay).days):
            middleDay = (startDay + timedelta(days=i))
            if (dayInRange(middleDay)):
                applyEvent(middleDay, [CONST_START_OF_DAY, CONST_END_OF_DAY])

def printLargestFreeTime():
    largestDuration = time(0, 0, 0)
    output = [currDate, CONST_START_OF_DAY, CONST_START_OF_DAY]
    for i in range(7):
        key = currDate + timedelta(days=i)
        for block in freeTime[key]:
            #print(key, block) #for testing
            duration = (datetime.min + (timeToDateTime(key, block[1]) - timeToDateTime(key, block[0]))).time()
            if duration > largestDuration:
                largestDuration = duration
                output = key, block[0], block[1]
    print(output[0], output[1], output[2])

def main():
    for i in range(7):
        freeTime[currDate + timedelta(days=i)].append([CONST_START_OF_DAY, CONST_END_OF_DAY])

    with open("calendar.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            updateFreeTime(row)

    printLargestFreeTime()

main()
