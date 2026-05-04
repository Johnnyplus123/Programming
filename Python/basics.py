# print("Hello")

# A variable is a container that can be use to varible

# Naming convention

# Pascal naming convention
# Student_Total_Score = 40
# StudentTotalScore = 40

# Camel naming convention
# studentTotalScore = 40
# student_Total_Score = 40

# Snake naming convention
# studenttotalscore = 40
# studenttotalswcore = 40

# Correct naming convention
# student = "James"
# studen_ = 3
# Incorrect naming convention

# 1.Do not maie use of any python keyword or reserve word (e.g lis ,int ,str,set)
# 2.Do not seperate a name with an hyphen

# Data types 
# Premetive and non-premetive data types

# 1.Premetive
# string, float ,booalean. int

# a = "James"
# b = 3.0
# c = 13
# d = True


# type convertion

# How to confirm the data types u're woorking with using type()

# print(type(a))
# 2.non-premetive data types
# list turple dict set

# Comment and code documentation
# Types of comments
# 1. single line comment\
# e.g
# i am a devoleoper
# 2.Tripple or Multiple line comment
# e.g
# def add ():
#     """This isto show the calculation"""
#     a = 80
#     b = 70
    # return a+b

# 1. Arithmethic operators
# val1 = 12 
# val2 = 5

# print ("div", val1 / val2) 
# print ("add", val1 + val2)
# print ("mul", val1 * val2)
# print ("floor_div", val1 // val2)
# print ("mod", val1 % val2)
# print ("Expo", val1 ** val2)
# print ("sub", val1 - val2)

# input() os a python fucntion function use to cllect data


# val1 = int(input("Enter your value 1: "))
# val2 = int(input("Enter your value 2: "))

# print(val1  val2)

# 2.Assignment Operators (=,+=,-=)
# name ="John"
# val3 = 20
# val3 += 5 #val3=val3+5
# print (val3)

# name ="John"
# val3 = 20
# val3 -= 5 #val3=val3-5
# print (val3)

#3. Comparison Operators ()

# 4. Logical Operators(and,or,not)
# num1 = 20
# num2 = 30
# num3 = 20
# # Rule of and said both of the condition must be true in order for it to return true
# result = (num1 > num2) and (num3 < num2)

# for or atlest one condition must be true to return true
# result = (num1 > num2) or (num3 < num2)

# result = (num1 > num2) is not (num3 < num2)

# print (result)
# num = input("Enter a num: ")
# operator = input("Enter operator: ")
# num4 = input("Enter a num2: ")
# print(int(eval(f"{num} {operator} {num}")))


# 5. Membership Operators(in,not in)
# my_num = [10, 43, 6, 19, 34]
# if 20 in my_num:
#     print("Present")
# else:
#     print("Absent")


# if 20 not in my_num:
#     print("Absent")
# else:
#     print("Present")

# 6. Identity Operator(is)
# Is compate the memory location

# a = 30
# b = 30
# print(a is b)
# print(a.from_bytes)
# print(b.from_bytes)

# list1 = [1, 2, 3]
# list2 = [1, 2, 3]
# print(list1 is list2 )
# print(list1.append)
# print(list2.append)

# Creating and accessing string
# message = "I am a python developer"
# message2 = "nam"
# print(message)
# print(type(message))

# String indexing

# It is the process of getting the position of a particular character in a variable or in a string (any data type)
# print(message[7])
# print(message[15])
# print(message[-1]) from the back



# String slicing
# print(message[:10])
# print(message[5:])
# print(message[6:-10])
# print(message[::2])
# print(message[::-2])
# print(message2[::-1])


# Common Strings Methods
# message = "I am a python developer"
# print(message.upper()) #It change the string in the variable to uppercase and always put the open and close parentesys e.g .upper()
# print(message.capitalize()) to capitalise the first letter
# print(message.center(40))To put the with or shift it from the front to the center 
# print(message.count("e")) # Which displays how many times e appeared
# print(message.index("python")) To show the index of the number or the character place on it
# print(message.replace("python", "java")) what u wanna rplace will be the first while what u wanna replace it will will be the second



#Ten different methods

# # 1
# john = ( "I'm", "proud", "to", "be", "an", "hacker")
# john1 = " ".join(john)
# print (john1)
# # 2
# john = "I'm proud to be an hacker"
# john1 = john.replace("hacker", "cyber security expert").split(" ")
# print (john1)
# # print (john)




# practice the me = (2-2) * (3 + 4)
# and also string slicing



# print(50 / 8)

# print ((2-2) * (3 + 4))


# String formatting using percentage (%)
# fruit = "Apple"
# price = 500
# # "%s" is a placeholder for string 
# # "%d" is a placeholder for digit
# sentence = "The price of %s  is %d Naira"%(fruit,price)
# print(sentence)


# String formatting using .format()
# fruit = "Apple"
# price = 500
# # "{}" is a placeholder for them
# sentence = "The price of {}  is {} Naira".format(fruit,price)
# print(sentence)


# String formatting using (f-string)
# fruit = "Apple"
# price = 500
# # "{}" is a placeholder for them
# print (f"The price of {fruit} is {price} Naira")



# String concatination
# concatination is the process of joining 2 or more string together

# # concatination using f-strings
# Example 1
# message1 = "I am a python devoloper"
# message2 = "I study at sqi coled of ict"
# print (f"{message1}, {message2}")

# Example 2
# name = "John"
# department = "Cyber security"
# print (f"My name is {name} and i study {department}")

# Example 3
# name = "John"
# career = "Cyber Security"
# print (f"My name is {name} and am successful in my {career} carreer")


# concatination using +
# Example 1
# message1 = "I am a python devoloper"
# message2 = "I study at sqi coled of ict"
# print(message1+ " " +message2)

# Example 2
# name = "John"
# department = "Cyber security"
# print ("My name is "+name+" "+"and i study"+" "+department)

# Example 3
# name = "John"
# career = "Cyber Security"
# print ('My name is'+' '+name+' '+'and am a successful'+' '+career+' '+'expert')

# concatination using comma (,)
# Example 1
# name = "John"
# department = "Cyber security"
# print ('My name is', name, 'and i study', department,)

# # Example 2
# name = "John"
# career = "Cyber Security"
# school = "SQI College of ICT"
# print ('My name is', name, 'and am a', career, 'student at', school)

                            #  Control Flow
# Conditional statements
# Conditional statement are use for decision making in programming
# Example 1
# password = "john1234"
# user = input("Enter your password: ")
# if user == password:
#     print('Login successfully..')
# else:
#     print('Incorrect password..')

# Example 2
# age = 15 
# if age >= 23:
#     print("You are an adult")

# else:
#     print("You are still young")


# Example 3
# user_input = input("Enter the name of your fruit: ").capitalize()
# if user_input == "Apple":
#     print("This is my first choice.")

# elif user_input == "Banana":
#     print("This is my second choice.")

# elif user_input == "Pineapple":
#     print("Atleast I get something.")

# else:
#     print("I'm not buying anything.")


#  Boolean expression and logical operators
# age = 18
# nationality = "NG"

# if age>= 18 and nationality == "NG":
#     print("I'm eligible to vote")

# else:
#     print("Under age")


# Nested conditionals

# age = 18 
# nationality = input("Enter your country: ").capitalize()
# if nationality == "Nigeria":
#     print("U're an indegene")

#     if age>=18:

#         print("U're an indegene")

#     else:
#         print("U're Underage")

# else:
#     print("u're not an indegene")




# Assignment
# (75-100)=A
# (60 - 69) =B
# (50 - 59) = C
# (40 - 49) = D 
# (0 - 30) = Fail 


# student = int(input("Enter your grade: "))
# if 75<= student <= 100:
#     print("A")

# elif student>= 60:
#     print("B")

# elif student >=50:
#     print("C")

# elif student >=40:
#     print("D")

# elif student >=0:
#     print("Fail")

    #    Nested conditionnals
# if 75<= student <= 100:
#     # print("A")

#     if 75<= student <=100:
#         print("Excellent")

#     else:
#         print("Excellent")

# elif 60<= student <= 74:
#     # print("B")

#     if 60<= student <= 74:
#         print("Good")

#     else:
#         print("Good")

# elif 50<= student <= 59:

#     if 50<= student <= 59:
#         print("Pass")

#     else:
#         print("Pass")

# elif 40<= student <=49:

#     if 40<= student <=49:
#         print("Pass")

#     else:
#         print("Pass")

# elif 0<= student <=30:

#     if 0<= student <=30:
#         print("Try again")

#     # else:
#     #     print("Try again")

# else:
#     print("Invalid grade")

# Ternary (conditdionals) expression
# age = 18
# my_condition = "Adult" if age>=24 else "child"
# print(my_condition)

                                    #  Loops and Iteration

# For loops
# for loops and range()
# for i in range(1, 11):
#     print(i)


# for num in range(1, 1001):
#     print(num)

# basket = ['Apple', 'Orange', 'Mango', 'Pineapple', 'Cherry']
# # print(basket)
# for fruit in basket:
#     print(fruit,  end="\t")    # the end="/t" is in order for it to be on a straight line



# for fruit in range(len(basket)):
#     print(fruit)


# Loop control statements (break and continue)

# Loop contro using break
# Example 1 
# for list_fruits in basket:
#     if list_fruits == "Pineapple":
#         break
#     print(list_fruits)

# Example 2
# for a in range(1, 12):
#     if a ==7:
#         break
#     print(a)

# Loop control using continue

# Example 1
# for a in range(1, 12):
#     if a ==7:
#         continue
#     print(a)


# While loops
# Exanple  1
# x = 0
# while x<10:
    # print(x)
    # x+=1

# Example 2 Which is what the error in the handling would lool like
# x = 0
# count = 0
# while x<10:
#     count+=1
#     print(x)
#     print(count)

# Example 3 Which is for countdown
# x = 10
# while x>1:
#     x-=1
#     print(x)

# Loop control statements(break, continue)
# Using break
# x=0
# while x<10:
#     x+=1
#     if x==5:
#         break
#     print(x)


# Using Continue

# x=0
# while x<10:
#     x+=1
#     if x==5:
#         continue
#     print(x)


# Nested Loops
# Example 1
# for i in range(1, 5):
#     for x in range(1, 4):
#         print(i, x)

# Example 2
# j=0
# while j<4:
#     x=0
#     while x<3:
#         print(j, x)
#         x+=1
#         j+=1

# Assignment 
# Palindrome checker


#    Data Stuctures
# List is a python data types collection that it is in order, changable and accept any type of data type
# Creating and accessing elements
# How to create a list
# 1 Creating a list using square constructor
# my_list = []
# 2 Using list constructor
# my_list2 = list(())

# students_name = ['Ayo', 'Ayomide', 'Johnson', 'Shalom', 'John']
# print(students_name)
# List Methods (append , extend, insert, remove, clear)
# students_name.append("Aliyu")  # it serves only a single function which is to add to the last in a list
# print(students_name)
# students_name.clear()  # And it's single function what to cleat everything in a list
# print(students_name)
# print(students_name.count("Ayomide"))  It count how many times it appears in a list
# students_name.insert(3, 20)   # It almost similar toto append but you can specify the index which u want to add a thing to
# print(students_name)
# students_name.remove("Shalom")   To remove a particular element from a list
# print(students_name)
# students_name.sort() # which make it in ascending order
# print(students_name)
# print(students_name.__contains__("Shalom")) To check if it contains a particular element in a list



