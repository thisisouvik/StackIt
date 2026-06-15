# fibbonacci series
# def fibb(n):
#     if n==0:
#         return 0
#     elif (n==1):
#         return 1
#     else:
#         return fibb(n-1) + fibb(n-2)
# print(fibb(6))

#set
# a=input("Enter a number:")
# print(f"Multiplication table of {a} is : ")

# for i in range(1,11):
#     print(f"{int(a)} x {i} = {int(a)*i}")

a = input("Enter a number:")

if a == "quit":
    print("You have entered quit")
else:
    a = int(a)
    if a < 5 or a > 9:
        raise ValueError("value should be between 5 and 9")