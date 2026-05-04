# while True:
#  ussd_value = input("Enter USSD code: ")

#  if ussd_value.startswith("*") and ussd_value.endswith("#"):
#  print(
#  "Welcome to MyNetwork\n"
#  "1. Buy Airtime\n"
#  "2. Buy Data\n"
#  "3. Check Balance\n"
#  "4. Customer Care"
#  )

#  choice = input("Enter your choice: ")
#  # Airtime recharge
#  if choice == "1":
#  print(
#  "1. Self Recharge\n"
#  "2. Recharge Others\n"
#  "3. Recharge from Bank\n"
#  "4. Back to Main Menu"
#  )
#  # while True:
#  choice = input("Enter your choice: ")
#  if choice == "1":
#  amount = input("Enter amount to recharge: ")
#  print(f"Recharging {amount} to your account...")
#  print(f"Your recharge of {amount} was succesful")
#  break

#  elif choice == "2":
#  phone_number = input("Enter your phone number: ")

#  if len(phone_number) != 11 or not phone_number.isdigit():
#  print("Invalid phone number")

#  else:
#  amount = input("Enter amount to recharge: ")
#  print(f"Recharging {amount} to your {phone_number}...")
#  print(f"Your recharge of {amount} to {phone_number} was succesful")

#  elif choice == "2":
#  print(
#  "1. Daily Data\n"
#  "2. Weekly Data\n"
#  "3. Monthly Data\n"
#  "4. Back to Main Menu"
#  )
#  elif choice == "3":
#  print("Your balance is $10")

#  elif choice == "4":
#  print("Connecting to Customer Care...")

#  else:

#  print("Invalid choice. Please try again.")

#  while True:

#  choice = input("Enter your choice: ")

ussd_value = input("Enter your ussd code: ")

if ussd_value.startswith('*') and ussd_value.endswith('#'):
    print(
    "Welcome to MyNetwork\n"
    "1. Buy Airtime\n"
    "2. Buy Data\n"
    "3. Check Balance\n"
    "4. Customer Care"
    )

    choice = input("Enter your choice: ")

    if choice == "1":
        print("1. Self\n"
        "2. Others\n"
        "3. Quick Recharge\n"
        "4. Borrow Airtime")

        choice = input("Enter your choice: ")
        amount = input("Enter your amount: ")
        print(f"Your recharge of {amount} was successful...")

    elif choice == "2":
        choice = input("Enter your choice: ")
        user = input("Enter your phone number: ")
        amount = input("Enter your amount: ")
        print(user)

    else:
        print("Not available")

else:
    print("Invalid code: ")

        # # else:
        # # print("Invalid ussd code..")

        # # ========== OPTION 1: BUY AIRTIME ==========

        # if choice == "1":

        #  print(
        #  "1. Self\n"
        #  "2. Others\n"
        #  "3. Quick Recharge\n"
        #  "4. Borrow Airtime"
        #  )

        #  if choice == "1":
        #  choice = input("Enter your choice: ")
        #  amount = input("Enter amount to recharge: ")

        #  if amount and int(amount) > 0:
        #  print(f"Your recharge of {amount} was being process")
        #  # print(f"Your recharge of {amount} to {phone_number} is succesful")

        #  elif choice == "2":

        #  phone_number = input("Enter your phone number: ")
        #  if phone_number !=11:
        #  print("Invalid phone number")
        #  amount = input("Enter amount to recharge: ")
        #  if len(phone_number)!=11 or not phone_number.isdigit():

        #  print("Invalid Number")
        #  else:
        #  print("Your recharge of {amount} to {phone_number} was being
        # processed ...")
        #  print("Your recharge of {amount} to {phone_number} was successfull
        # ...")

        #  elif choice == "3":
        #  print("")

        # # ========== OPTION 2: BUY DATA ==========
        # elif choice == "2":
        #  print(
        #  )

        # # ========== OPTION 3: CHECK BALANCE ==========

        # elif choice == "3":
        #  print()

        # # ========== OPTION 4: CUSTOMER CARE ==========

        # elif choice == "4":
        #  print()

        # # ========== OPTION 5: INVALID CODE ==========

        # else:
        #  print("Invalid choice")
        #  break
