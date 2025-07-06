import json
import os


if os.path.exists("data.json"):
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