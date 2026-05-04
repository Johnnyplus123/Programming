passwd = input("Enter your password for check: ")

if len(passwd)<10:
    print("Password must not be less than 10")

elif passwd == passwd.isupper() and passwd == len(passwd)<10:
    print("Must include Capital letter")



# elif passwd.capitalize ==0:
#     print("Weak ")