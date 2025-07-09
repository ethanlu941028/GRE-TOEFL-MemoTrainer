import tkinter as tk
import json
import os

def show_meaning():
    meaning_label.config(text = data[index]["meaning"], font = ("Helvetica", 28), fg = "black", bg = "white")     #change the text of the label
    
def show_example():
    example_label.config(text = data[index]["example"], font = ("Helvetica", 28), fg = "black", bg = "white")     #change the text of the label

def next_word():
    global index
    index+=1
    if(index >= len(data)):
        index = 0
    word_label.config(text = data[index]["word"], font = ("Helvetica", 28), fg = "black", bg = "white")  #change the text of the word label
    meaning_label.config(text = "", font = ("Helvetica", 28), fg = "black", bg = "grey21")  #clear the meaning label
    example_label.config(text = "", font = ("Helvetica", 28), fg = "black", bg = "grey21")  #clear the example label
    
def add_word():
    
    global data
    #build a new window for input new word
    popup = tk.Tk()
    popup.title = ("AddNewWord")
    popup.geometry("400x300")
    
    #word, meaning, example label
    tk.Label(popup, text = "Word: ", font = ("Helvetica", 20)).pack()
    word_entry = tk.Entry(popup, font = ("Helvetica", 20))
    word_entry.pack()
    
    tk.Label(popup, text = "Meaning: " , font = ("Helvetica", 20)).pack()
    meaning_entry = tk.Entry(popup, font = ("Helvetica", 20))
    meaning_entry.pack()
    
    tk.Label(popup, text = "Example: ", font = ("Helvetica", 20)).pack()
    example_entry = tk.Entry(popup, font = ("Helvetica", 20))
    example_entry.pack()
    
    def save_new_word():
        new_entry = {
            "word" : word_entry.get(),
            "meaning" :  meaning_entry.get(),
            "example" : example_entry.get()
        }
        
        data.append(new_entry)
        
        with open("data.json", "w") as f:
            json.dump(data, f, indent = 4)
        
        popup.destroy()
        
    save_word_button = tk.Button(popup, text = "Save Word", command = save_new_word, font = ("Helvetica", 20))
    save_word_button.pack()
        

#main
with open("data.json", "r") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        data = []
index = 0

window = tk.Tk()                #build the window object
window.title("MyWordCoach")     #the window title
window.geometry("800x600")    #the window size
window.configure(bg = "grey21")


#add Label to show the word
word_label = tk.Label(window, text = data[index]["word"], font = ("Helvetica", 28), fg = "black", bg = "white")  #create a label with the word
word_label.pack(pady = 20)      #add the label to the window and set the padding

#add the meaning label, and should be empty first
meaning_label = tk.Label(window, font = ("Helvetica", 28), fg = "black", bg = "grey21")  #create a nothing label for the meaning first
meaning_label.pack(pady = 30)   

#add the example label
example_label = tk.Label(window, font = ("Helvetica", 28), fg = "black", bg = "grey21")  #create a nothing label for the example first
example_label.pack(pady = 30)




#create a frame for the buttons
button_frame = tk.Frame(window)
button_frame.pack(pady = (200, 10))

#add the show_meaning button
show_meaning_buttin = tk.Button(button_frame, text = "Show Meaning", command = show_meaning, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the meaning
show_meaning_buttin.pack(side = "left")  

#add the meaning label, and should be empty first
show_example_buttin = tk.Button(button_frame, text = "Show Example", command = show_example, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the meaning
show_example_buttin.pack(side = "right")


#add next_word button
next_word_button = tk.Button(window, text = "Next Word", command = next_word, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the next word
next_word_button.pack()       #add the button to the window

add_word_button = tk.Button(window, text = "Add Word", command = add_word, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to add a new word
add_word_button.pack()

window.mainloop()               #keep the window appearing