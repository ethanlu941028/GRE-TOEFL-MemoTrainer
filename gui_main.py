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
    popup1 = tk.Tk()
    popup1.title = ("AddNewWord")
    popup1.geometry("400x300")
    
    #word, meaning, example label
    tk.Label(popup1, text = "Word: ", font = ("Helvetica", 20)).pack()
    word_entry = tk.Entry(popup1, font = ("Helvetica", 20))
    word_entry.pack()
    
    tk.Label(popup1, text = "Meaning: " , font = ("Helvetica", 20)).pack()
    meaning_entry = tk.Entry(popup1, font = ("Helvetica", 20))
    meaning_entry.pack()
    
    tk.Label(popup1, text = "Example: ", font = ("Helvetica", 20)).pack()
    example_entry = tk.Entry(popup1, font = ("Helvetica", 20))
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
        
        popup1.destroy()
        
    save_word_button = tk.Button(popup1, text = "Save Word", command = save_new_word, font = ("Helvetica", 20))
    save_word_button.pack()
       
       
def show_help():
    
    help_window = tk.Tk()
    help_window.title("HelpWindow")
    help_window.geometry("400x600")
    help_window.configure(bg = "grey21")
    help_window.rowconfigure(0, weight = 1)
    help_window.columnconfigure(0, weight = 1)
    
    help_main_frame = tk.Frame(help_window, bg = "grey21")
    help_main_frame.grid(row = 0, column = 0, sticky = "nsew")
    help_main_frame.columnconfigure(0, weight = 1)
    help_main_frame.rowconfigure(3, weight = 1)
    help_main_frame.rowconfigure(4, weight = 1)
    help_main_frame.rowconfigure(5, weight = 1)
    help_main_frame.rowconfigure(6, weight = 1)
    
    
    help_word_label = tk.Label(help_main_frame, text = "Word", font = ("Helvetica", 28), fg = "white", bg = "grey21")
    help_word_label.grid(row = 0, column = 0, pady = (20, 0))
    
    help_meaning_label = tk.Label(help_main_frame, text = "Meaning of the Word", font = ("Helvetica", 28), fg = "white", bg = "grey21")
    help_meaning_label.grid(row = 1, column = 0, pady = (5, 10))
    
    help_example_label = tk.Label(help_main_frame, text = "Example of the Word", font = ("Helvetica", 28), fg = "white", bg = "grey21")
    help_example_label.grid(row = 2, column = 0, pady = (5, 10))
    
    help_difficulty_label = tk.Label(help_main_frame, text = "Rate the difficulty of the word you think", font = ("Helvetica", 28), fg = "white", bg = "grey21", wraplength = 350)
    help_difficulty_label.grid(row = 3, column = 0, pady = (40, 0))
    
    help_proficiency_label = tk.Label(help_main_frame, text = "Rate the proficiency of the word you remember this time", font = ("Helvetica", 28), fg = "white", bg = "grey21", wraplength = 350)
    help_proficiency_label.grid(row = 4, column = 0, pady = (40, 0))
    
    show_frame = tk.Frame(help_main_frame, bg = "grey21")
    show_frame.grid(row = 5, column = 0, pady = (40, 0))
    
    help_show_meaning_label = tk.Label(show_frame, text = "Press to look the meaning of the word", font = ("Helvetica", 16), fg = "white", bg = "grey21", wraplength = 150)
    help_show_meaning_label.pack(side = "left", padx = 10)
    
    help_show_example_label = tk.Label(show_frame, text = "Press to look the example of the word", font = ("Helvetica", 16), fg = "white", bg = "grey21", wraplength = 150)
    help_show_example_label.pack(side = "right", padx = 10)
    
    add_next_frame = tk.Frame(help_main_frame, bg = "grey21")
    add_next_frame.grid(row = 6, column = 0, pady = (40, 0))
    
    help_next_word = tk.Label(add_next_frame, text = "Press then get to the next word", font = ("Helvetica", 16), fg = "white", bg = "grey21", wraplength = 150)
    help_next_word.pack(side = "left", padx = 10)
    
    help_add_word = tk.Label(add_next_frame, text = "Press the button then you can add word", font = ("Helvetica", 16), fg = "white", bg = "grey21", wraplength = 150)
    help_add_word.pack(side = "right", padx = 10)

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
window.rowconfigure(0, weight = 1)          #the thing inside row 0 can adjust the distance averagely, relatively
window.columnconfigure(0, weight = 1)       #the thing inside column  0 can adjust the distance avegrely, relatively

main_frame = tk.Frame(window, bg = "grey21")
main_frame.grid(row = 0, column = 0, sticky = "nsew")           #expand the main_frame in the window
main_frame.rowconfigure(0, weight = 1)
main_frame.rowconfigure(1, weight = 1, minsize = 100)           #the object inside row 1 can adjust the distance averagely, relatively
main_frame.rowconfigure(2, weight = 1, minsize = 100)           #the object inside row 2 can adjust the distance avegrely, relatively
main_frame.columnconfigure(0, weight = 1)



#press help_button, it will show every objects' function
help_button = tk.Button(main_frame, text = "@", command = show_help, font = ("Helvetica", 20), fg = "white", bg = "grey21", highlightthickness = 0, borderwidth = 0)
help_button.grid(row = 0, column = 0, sticky = "e", padx = (0, 30))

word_label = tk.Label(main_frame, text = data[index]["word"], font = ("Helvetica", 28), fg = "black", bg = "white")  #create a label with the word
word_label.grid(row = 1, column = 0, sticky = "n")


#meaning_frame to contain meaning_label (cause the label may change line)
meaning_frame = tk.Frame(main_frame, bg = "grey21")
meaning_frame.grid(row = 2, column = 0, pady = (10, 10), sticky = "nsew")
meaning_frame.columnconfigure(0, weight = 1)
meaning_frame.grid_propagate(False)          #don't let the inside object change the height of frame

meaning_label = tk.Label(meaning_frame, font = ("Helvetica", 28), fg = "black", bg = "grey21", wraplength = 750, justify = "left")  #create a nothing label for the meaning first
meaning_label.grid(row = 0, column = 0)


#example_frame to contain example_label (cause the label may change line)
example_frame = tk.Frame(main_frame, bg = "grey21")
example_frame.grid(row = 3, column = 0, pady = (10, 10), sticky = "nsew")
example_frame.columnconfigure(0, weight = 1)
example_frame.grid_propagate(False)          #don't let the label change the height of frame

example_label = tk.Label(example_frame, font = ("Helvetica", 28), fg = "black", bg = "grey21", wraplength = 750)  #create a nothing label for the example first
example_label.grid(row = 0, column = 0)


#add a frame for the difficulty button
difficulty_frame = tk.Frame(main_frame, bg = "grey21")
difficulty_frame.grid(row = 4, column = 0, pady = (10, 0))

#add a frame for proficiency button
proficiency_frame = tk.Frame(main_frame, bg = "grey21")
proficiency_frame.grid(row = 5, column = 0, pady = (5, 10))


#frame for the buttons
show_button_frame = tk.Frame(main_frame, bg = "grey21")
show_button_frame.grid(row = 6, column = 0, pady = 10)

#add the show_meaning button
show_meaning_buttin = tk.Button(show_button_frame, text = "Show Meaning", command = show_meaning, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the meaning
show_meaning_buttin.pack(side = "left", padx = 10)  

#add the meaning label, and should be empty first
show_example_buttin = tk.Button(show_button_frame, text = "Show Example", command = show_example, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the meaning
show_example_buttin.pack(side = "right", padx = 10)

#frame for next_word and add_word
word_button_frame = tk.Frame(main_frame, bg = "grey21")
word_button_frame.grid(row = 7, column = 0, pady = 10)

#add next_word button
next_word_button = tk.Button(word_button_frame, text = "Next Word", command = next_word, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to show the next word
next_word_button.pack(side = "left", padx = 10) 

add_word_button = tk.Button(word_button_frame, text = "Add Word", command = add_word, font = ("Helvetica", 20), fg = "black", bg = "white")  #create a button to add a new word
add_word_button.pack(side = "right", padx = 10) 

if not data[index].get("difficulty"):
    show_difficulty_button()

show_proficiency_button()

window.mainloop()               #keep the window appearing