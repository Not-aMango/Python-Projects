import time

print("This is a Timer".center(40))
hr = int(input("Enter number of hours : "))
mins = int(input("Enter number of minutes : "))
secs = int(input("Enter number of seconds : "))

t = hr * 3600 + mins * 60 + secs
print("\n","Timer".center(40))
for i in range(t, 0, -1):
    if hr >= 60 or mins >= 60 or secs >= 60:
        print("Invalid Input".center(40))
        break
    secs = i % 60
    mins = (i // 60) % 60
    hr = (((i // 60)) // 60) % 60
    print(f"{hr:02} : {mins:02} : {secs:02}".center(40))
    time.sleep(1)
