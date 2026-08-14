# Creates the "main" function, which is the main code the program will use.
def main():

    # A deliberate infinite loop
    while True:

        # Tries to run the code below
        try:
            n = int(input("Hello, I'm your very own counting bot! Which number do you want me to count to? :) "))
        
        # Code will not run if a ValueError is present, and instead will run the code below the "except" clause
        except ValueError:
            print("Please type an integer, or I won't be able to count for you. :(")
        
        # If the "except" clause isn't true, then break out of the loop and continue running the remaining code in the function
        else:
            break
    
    # Calls this function defined later in the code
    countup(n)

# Defines the function called from the "main" function
def countup(n):

    # Code that the function will perform

    # This "for" loop does the counting, with it listing all the numbers from 1 up to the user's input in the "main" function.
    for count in range(n):
        print(count + 1)

main()

# Thanks the user for using the bot
print("Thanks for using me! If you want to count with me again, you can run this code again.")