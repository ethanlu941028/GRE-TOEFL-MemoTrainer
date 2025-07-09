import os
import json

while True:
    
    operation = str(input("Enter the operation: "))

    if(operation == "input"):
        with open("data.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            
        word = input ("Enter the word:")
        meaning = input("Enter the meaning:")
        example = input("Enter the example:")

        new_data = {"word": word, "meaning": meaning, "example": example}

        data.append(new_data)
            
        with open ("data.json", "w") as f:
            json.dump(data, f, indent=4)

    elif(operation == "read"):
        with open("data.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        for i in range(len(data)):
            print("[", i+1, "]", data[i]["word"], "-", data[i]["meaning"], "-", data[i]["example"])
                    
    elif(operation == quit):
        break
    