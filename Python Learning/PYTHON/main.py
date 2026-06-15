from functools import reduce 
# f=open('myfile.txt','r')
# i=0
# # Read the file line by line
# while True:
#     i=i+1
#     line=f.readline()
#     if not line:
#         break
#     # Print the current line
#     m1=line.strip().split(",")[0]
#     m2=line.strip().split(",")[1]
#     m3=line.strip().split(",")[2]
#     print(f"Marks of student {i} in Maths is {m1}")
#     print(f"MArks of student {i} in Science is {m2}")
#     print(f"MArks of student {i} in English is {m3}")

# f=open('myfile2.txt','w+')
# f.write("Hello World\n")

# # f.seek(10)
# y=f.truncate(5)
# # x=f.tell()
# # print(x)
# print(y)
# f.seek(0)
# s = f.read()
# print(s)

# def addito(fx, value):
#     return 6 +  fx(value)

# cube = lambda x: x**3
# print(addito(cube,3))

# def cube(x):
#     return x**3

# l=[1,2,3,4,5]
# # new=list(map(cube,l))
# # print(new)

# def mysum(x,y):
#     return x+y

# s=reduce(mysum,l)
# print(s)

# class Person:
#     def __init__(Self):
#         print("hi I am Souvik in occupation ")
#     name="Souvik" 
#     occu="Student"
#     sal=10
#     def info(self):
#         print(f"Name is {self.name} and occupation is {self.occu}")

# a = Person()
# a.name="Roni"
# a.occu="Ganjawala"

# b= Person()

# a.info()
# b.info()

# print(a.name, a.occu)

# class Person():
#     def __init__(self, n, o):
#         print("I am in constructor")
#         self.name=n
#         self.occu=o

#     def info(self):
#         print(f"Name is {self.name} and occupation is {self.occu}")


# a= Person("Souvik", "Student")
# b= Person("Roni", "Ganjawala")

# a.info()
# b.info()

def greet(fx):
    def mfx():
        print("GM!")
        fx()
        print("Thanks")
    return mfx

@greet

def hello():
    print("Hello")

hello()
