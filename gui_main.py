import tkinter as tk
import json
import random

def show_meaning():
    meaning_label.config(text = data[index]["meaning"], font = ("Helvetica", 28), fg = "black", bg = "white")     #change the text of the label
    
def show_example():
    example_label.config(text = data[index]["example"], font = ("Helvetica", 28), fg = "black", bg = "white")     #change the text of the label
    
def show_difficulty_button():
    
    def set_difficulty(rating):
        #store into the data
        data[index]["difficulty"] = rating
        
        #then write into the data.json
        with open("data.json", "w") as f:
            json.dump(data, f, indent = 4)
            
        #clear the star
        for widget in difficulty_frame.winfo_children():
            widget.destroy()
    
    #clean the old star
    for widget in difficulty_frame.winfo_children():
        widget.destroy()
        
    #build the star button
    for i in range(1, 6):
        #use canvas since in macOS, Button is not good                                      no frame(for look)
        star_button = tk.Canvas(difficulty_frame, width = 60, height = 60, bg = "grey21", highlightthickness = 0)
        star_button.pack(side = "left", padx = 3)
        
        star_button.create_text(30, 30, text = "*", font = ("Helvetica", 40), fill = "gold")
        
        def on_click(event, rating = i):
            set_difficulty(rating)
            
        #<Button-1> is left mouse click
        star_button.bind("<Button-1>", on_click)
    
        

def next_word():
    global index
    index = random.randint(0, len(data) - 1)        
    word_label.config(text = data[index]["word"], font = ("Helvetica", 28), fg = "black", bg = "white")  #change the text of the word label
    meaning_label.config(text = "", font = ("Helvetica", 28), fg = "black", bg = "grey21")  #clear the meaning label
    example_label.config(text = "", font = ("Helvetica", 28), fg = "black", bg = "grey21")  #clear the example label
    
    
    #check if the difficulty has been set
    if not data[index].get("difficulty"):
        show_difficulty_button()
    else:
        for widget in difficulty_frame.winfo_children():
            widget.destroy()
    
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
index = random.randint(0, len(data) - 1)

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




#add a frame for the difficulty button
difficulty_frame = tk.Frame(window, bg = "grey21")
difficulty_frame.pack(pady = 20)


#create a frame for the buttons
button_frame = tk.Frame(window)
button_frame.pack(pady = (100, 10))

#add the show_meaning button
show_meaning_buttin = tk.Button(button_frame, text = "Show Meaning", command = show_meaning, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the meaning
show_meaning_buttin.pack(side = "left")  

#add the meaning label, and should be empty first
show_example_buttin = tk.Button(button_frame, text = "Show Example", command = show_example, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the meaning
show_example_buttin.pack(side = "right")


#add next_word button
next_word_button = tk.Button(window, text = "Next Word", command = next_word, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the next word
next_word_button.pack()       

add_word_button = tk.Button(window, text = "Add Word", command = add_word, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to add a new word
add_word_button.pack()

if not data[index].get("difficulty"):
    show_difficulty_button()

window.mainloop()               #keep the window appearing