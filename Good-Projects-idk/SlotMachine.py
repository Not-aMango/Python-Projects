import random

symbols = "🍒🍌🍎"
output = []

print("*****************************************")
print("-------Welcome to GamblerX1069-------".center(42))


def gambler():
    bal = 100
    a = "y"
    amt = 0

    if  amt<=bal:
        while a.lower() == "y":
            print("\nCurrent balance: $", bal)
            amt = int(input("Enter your bet: $"))
            if amt>bal:
                print(f"Amount can't be greater than balance/try Again")
                amt = int(input("Enter your bet: $"))
            bal -= amt
            print("\nSpinning...")
            print("*************")
            output.append(random.choice(symbols))
            output.append(random.choice(symbols))
            output.append(random.choice(symbols))
            print(f"{output[0]} : {output[1]} : {output[2]}")
            print("*************")

            if output[0] == output[1] == output[2]:
                print("\nYay! you won")
                bal = bal + amt*5
            else:
                print("\nYou lost this round")
            output.clear()
            a = input("Do you want to play again? (y/n): ")
        else: quit()

    print("*************")





