# Asks for the user's name
name = input("Hello there, stranger, what's your name? ")

# Defines "main" function
def main():
    hello(name)

# Defines the function "hello(name)" found in the "main" function
def hello(name):
    print(f"It is very nice to meet you, {name}.")

# Calls the newly defined "main" function, which runs the code above.
main()

# Defines a function called "checkin".
def checkin():
    answer = input(f"How's everything going so far, {name}? ")
    respond(answer)

# Defines the function "respond(answer)" found in the "checkin" function
def respond(answer):
    if "good" in answer:
        print(f"I'm very glad to hear that, {name}!")
    
    elif "bad" in answer:
        print(f"I'm very sorry to hear that, {name}. :()")
    
    else:
        print(f"That's okay {name}! It was very nice to meet you.")

# Calls the newly defined "checkin" function, which runs after the "main" function is complete.
checkin()