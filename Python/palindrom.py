user_input = input("Enter your palindrome: ")

if user_input == user_input[:: - 1]:
    print("correct palindrome")
else:
    print("incorrect palindrome")
