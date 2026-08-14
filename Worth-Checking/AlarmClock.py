import time as t
import datetime

print("******** This is an Alarm Clock ********\n")

print("Input a Deadline\nFormat = HH:MM:SS  AM/PM")
dateline = input("= ")

print("Current Time:\n")
while datetime.datetime.now().time().strftime("%I:%M:%S %p") != dateline:
    print(datetime.datetime.now().time().strftime("%I : %M : %S %p"))
    t.sleep(1)
print("Wakey Wakey")
