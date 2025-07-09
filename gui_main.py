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
    
def show_proficiency_button():
    
    def set_proficiency(rating):
        #store into the data
        data[index]["proficiency"] = rating
        
        #then write into the data.json
        with open("data.json", "w") as f:
            json.dump(data, f, indent = 4)
            
        #clear the star
        for widget in proficiency_frame.winfo_children():
            widget.destroy()
    
    #clean the old star
    for widget in proficiency_frame.winfo_children():
        widget.destroy()
        
    #build the star button
    for i in range(1, 6):
        #use canvas since in macOS, Button is not good                                      no frame(for look)
        question_button = tk.Canvas(proficiency_frame, width = 60, height = 60, bg = "grey21", highlightthickness = 0)
        question_button.pack(side = "left", padx = 3)
        
        question_button.create_text(30, 30, text = "?", font = ("Helvetica", 40), fill = "red")
        
        def on_click(event, rating = i):
            set_proficiency(rating)
            
        #<Button-1> is left mouse click
        question_button.bind("<Button-1>", on_click)

def next_word():
    global index
    global weight_list
    weight_list = []
    for i in range(len(data)):
        diff = data[i]["difficulty"] if data[i].get("difficulty") is not None else 3        #if the difficulty is None, the take 3
        pro = data[i]["proficiency"] if data[i].get("proficiency") is not None else 3
        for j in range(diff * (pro + 2)):
            weight_list.append(i)
        
    index = random.choice(weight_list)      
    word_label.config(text = data[index]["word"], font = ("Helvetica", 28), fg = "black", bg = "white")  #change the text of the word label
    meaning_label.config(text = "", font = ("Helvetica", 28), fg = "black", bg = "grey21")  #clear the meaning label
    example_label.config(text = "", font = ("Helvetica", 28), fg = "black", bg = "grey21")  #clear the example label
    
    
    #check if the difficulty has been set
    if not data[index].get("difficulty"):
        show_difficulty_button()
    else:
        for widget in difficulty_frame.winfo_children():
            widget.destroy()
    
    show_proficiency_button()
        
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
            "example" : example_entry.get(),
            "difficulty" : None,
            "proficiency" : None
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
        
#take the weight of the difficulty to decide which probaly will be the next word
weight_list = []
for i in range(len(data)):
    diff = data[i]["difficulty"] if data[i].get("difficulty") is not None else 3        #if the difficulty is None, the take 3
    pro = data[i]["proficiency"] if data[i].get("proficiency") is not None else 3
    for j in range(diff * (pro + 2)):
      weight_list.append(i)
      
index = random.choice(weight_list)

window = tk.Tk()                #build the window object
window.title("MyWordCoach")     #the window title
window.geometry("800x600")    #the window size
window.configure(bg = "grey21")


#add Label to show the word
word_label = tk.Label(window, text = data[index]["word"], font = ("Helvetica", 28), fg = "black", bg = "white")  #create a label with the word
word_label.place(relx = 0.5, y = 50, anchor = "center")      #relative x(0 ~ 1)  anchor is the object's point

#add the meaning label, and should be empty first
meaning_label = tk.Label(window, font = ("Helvetica", 28), fg = "black", bg = "grey21", wraplength = 750, justify = "left")  #create a nothing label for the meaning first
meaning_label.place(relx = 0.5, y = 150, anchor = "center")

#add the example label
example_label = tk.Label(window, font = ("Helvetica", 28), fg = "black", bg = "grey21", wraplength = 750)  #create a nothing label for the example first
example_label.place(relx = 0.5, y = 250, anchor = "center")


#add a frame for the difficulty button
difficulty_frame = tk.Frame(window, bg = "grey21")
difficulty_frame.place(relx = 0.5, y = 400, anchor = "center")

#add a frame for proficiency button
proficiency_frame = tk.Frame(window, bg = "grey21")
proficiency_frame.place(relx = 0.5, y = 450, anchor = "center")


#frame for the buttons
show_button_frame = tk.Frame(window, bg = "grey21")
show_button_frame.place(relx = 0.5, y = 500, anchor = "center")

#add the show_meaning button
show_meaning_buttin = tk.Button(show_button_frame, text = "Show Meaning", command = show_meaning, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the meaning
show_meaning_buttin.pack(side = "left")  

#add the meaning label, and should be empty first
show_example_buttin = tk.Button(show_button_frame, text = "Show Example", command = show_example, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the meaning
show_example_buttin.pack(side = "right")

#frame for next_word and add_word
word_button_frame = tk.Frame(window, bg = "grey21")
word_button_frame.place(relx = 0.5, y = 550, anchor = "center")

#add next_word button
next_word_button = tk.Button(word_button_frame, text = "Next Word", command = next_word, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the next word
next_word_button.pack(side = "left") 

add_word_button = tk.Button(word_button_frame, text = "Add Word", command = add_word, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to add a new word
add_word_button.pack(side = "right") 

if not data[index].get("difficulty"):
    show_difficulty_button()

show_proficiency_button()

window.mainloop()               #keep the window appearing