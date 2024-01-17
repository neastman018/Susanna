import datetime


def getTime():
    current_time = datetime.datetime.now()
    hour = str(current_time.hour)
    minute = str(current_time.minute)
    second = str(current_time.second)
    return hour + ":" + minute + ":" + second

    