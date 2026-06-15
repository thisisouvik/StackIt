import random

point = 0
while True:
    user=input("Enter your choice Snake/Water/Gun/Exit :")
    if user=="Exit":
        print("Thanks for playing")
        print("Your total points are",point)
        break
    if user=="Snake":
        print("You chose Snake")
    elif user=="Water":
        print("You chose Water")
    elif user=="Gun":
        print("You chose Gun")
    else:
        print("Invalid choice! Please try again.")
        continue


    snake,water,gun=1,2,3
    cmp=random.randint(1,3)
    point=0

    if cmp==1:
        print("Computer choosed Snake")
        if user=="Snake":
            print("Game is Draw")
            print("No points")
        elif user=="Water":
            print("You lose")
            print("No points")
        elif user=="Gun":
            print("You win")
            point+=1
            print("You got a point")
    elif cmp==2:
        print("Computer choosed Water")
        if user=="Snake":
            print("You win")
            print("You got a point")
            point+=1
        elif user=="Water":
            print("Game is Draw")
            print("No points")
        elif user=="Gun":
            print("You lose")
            print("No points")
    elif cmp==3:
        print("Computer choosed Gun")
        if user=="Snake":
            print("You lose")
            print("No points")
        elif user=="Water":
            print("You win")
            print("You got a point")
            point+=1
        elif user=="Gun":
            print("Game is Draw")
            print("No points")
        print("Your total points are",point)
   


