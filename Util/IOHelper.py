def getInput(default: str, prompt: str) -> str:
    #Get input from the user
    response = input(prompt)
    #Add a space for visibility
    print()
    #If the user didn't enter anything, use the default
    if len(response) == 0:
        response = default
    return response