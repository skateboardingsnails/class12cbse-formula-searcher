

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector as msc
from dotenv import load_dotenv
import os

load_dotenv()

msco = msc.connect(
   host=os.getenv("DB_HOST"),
   user=os.getenv("DB_USER"),
   password=os.getenv("DB_PASSWORD"),
   database=os.getenv("DB_NAME")
)
if msco.is_connected():
   cursor = msco.cursor()

# -----------------------------------------------------------
# MAIN WINDOW
# -----------------------------------------------------------
window = Tk()
window.geometry("900x400")
window.title("Friday-03 Homework Helper")

# -----------------------------------------------------------
# BACKGROUND IMAGE SETUP (adjust path)
# -----------------------------------------------------------
bg_path = "fridaybg.png"
bg_original = Image.open(bg_path)

canvas = Canvas(window, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

bg_tk = ImageTk.PhotoImage(bg_original)
bg_item = canvas.create_image(0, 0, image=bg_tk, anchor="nw")

def resize_bg(event):
   new_w, new_h = event.width, event.height
   resized = bg_original.resize((new_w, new_h), Image.Resampling.LANCZOS)
   new_bg = ImageTk.PhotoImage(resized)
   canvas.itemconfig(bg_item, image=new_bg)
   canvas.image = new_bg  # keep reference alive

window.bind("<Configure>", resize_bg)

# Helper to place widgets on canvas
def place(widget, x, y):
   canvas.create_window(x, y, window=widget)

# -----------------------------------------------------------
# CLEAR + RESET FUNCTIONS
# -----------------------------------------------------------
def clear_widgets():
   """Remove all widgets from canvas except the background."""
   for item in canvas.find_all():
       if item != bg_item:
           canvas.delete(item)

# -----------------------------------------------------------
# SCROLLING DISPLAY (used for showing results)
# -----------------------------------------------------------
def show_scrolling_result(result_text, back_command):
   """
   Clear the screen, show a scrollable Text area with result_text,
   and a Back button that calls back_command (restores the previous input screen).
   """
   clear_widgets()

   frame = Frame(window, bg='floral white')
   text_area = Text(frame, wrap=WORD, font=('Arial', 14), bg='floral white', width=60, height=10)
   scroll_y = ttk.Scrollbar(frame, orient=VERTICAL, command=text_area.yview)
   text_area.config(yscrollcommand=scroll_y.set)

   # Insert result and lock the text widget
   text_area.insert(END, result_text if result_text else "No results found.")
   text_area.config(state=DISABLED)

   text_area.pack(side=LEFT, fill=BOTH, expand=True)
   scroll_y.pack(side=RIGHT, fill=Y)

   place(frame, 450, 220)

   # Back button returns to the search screen (the provided back_command)
   back_btn = Button(window, text="Back", command=back_command, font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   place(back_btn, 140, 340)

# -----------------------------------------------------------
# NAME SCREEN
# -----------------------------------------------------------
def show_name_screen():
   clear_widgets()

   fridaym1 = Label(window, text='Welcome user. What is your name?',
                    bg='#362016', fg='floral white', font=('Arial', 26))
   entry = Entry(window, font=('Ink Free', 30))

   def submit_name():
       name = entry.get().strip()
       words = name.split()
       cleaned = " ".join(
           [w for w in words if w.lower() not in
            ["hello", "hi", "good", "morning", "evening", "greetings", "i", "am", "my", "name", "is"]]
       )
       msg = f"Hello {cleaned}!\nI am Friday-03, your personal homework helper for grade 12.\nIt's nice to meet you!"
       greeting = Label(window, text=msg, bg='floral white', font=('Brush Script MT', 25))
       clear_widgets()
       place(greeting, 450, 180)
       place(next_btn, 780, 340)

   def delete_text():
       entry.delete(0, END)

   def backspace_text():
       entry.delete(len(entry.get()) - 1, END)

   submit_btn = Button(window, text='Submit', command=submit_name,
                       font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   delete_btn = Button(window, text='Delete', command=delete_text,
                       font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   backspace_btn = Button(window, text='Backspace', command=backspace_text,
                          font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')

   place(fridaym1, 450, 100)
   place(entry, 450, 180)
   place(submit_btn, 740, 180)
   place(delete_btn, 830, 180)
   place(backspace_btn, 940, 180)

# -----------------------------------------------------------
# SUBJECT MENU
# -----------------------------------------------------------
def step2():
   clear_widgets()

   msg2 = Label(window, text='I provide the following services:', font=('Arial', 30), bg='floral white')
   place(msg2, 450, 80)

   math_btn = Button(window, text='Mathematics', height=3, width=20,
                     command=maths, font=("Arial", 16, "bold"),
                     bg='#d8e5f0', fg='BLACK')
   phys_btn = Button(window, text='Physics', height=3, width=20,
                     command=phy, font=("Arial", 16, "bold"),
                     bg='#f5e2e3', fg='BLACK')
   chem_btn = Button(window, text='Chemistry', height=3, width=20,
                     command=chem, font=("Arial", 16, "bold"),
                     bg='#cfe3cb', fg='BLACK')
   back_btn = Button(window, text='Back', command=show_name_screen,
                     font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')

   place(math_btn, 450, 160)
   place(phys_btn, 450, 250)
   place(chem_btn, 450, 340)
   place(back_btn, 140, 340)

next_btn = Button(window, text='Next', width=7, height=1,
                 font=("Arial", 16, "bold"), bg='floral white', fg='BLACK',
                 command=step2)

# -----------------------------------------------------------
# MATH SCREEN
# -----------------------------------------------------------
def maths():
   clear_widgets()
   msg = Label(window, text="Enter Formula Name", font=('Arial', 25), bg='floral white')
   place(msg, 450, 80)
   e = Entry(window, font=('Arial', 25))
   place(e, 450, 160)

   def submit():
       var = e.get()
       cursor.execute('SELECT * FROM math')
       data = cursor.fetchall()
       result = ""
       for i in data:
           if var.lower().strip() in i[1].lower().strip():
               result += f"SNo: {i[0]} | Formula Name: {i[1]}\nFormula: {i[2]}\n\n"
       # hide entry/label by showing results (show_scrolling_result clears widgets first)
       show_scrolling_result(result, maths)

   submit_btn = Button(window, text='Submit', command=submit,
                       font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   back_btn = Button(window, text='Back', command=step2,
                     font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   place(submit_btn, 740, 160)
   place(back_btn, 140, 340)

# -----------------------------------------------------------
# PHYSICS SCREEN (with "by formula name" and "by variables" improved)
# -----------------------------------------------------------
def phy():
   clear_widgets()
   msg = Label(window, text="Search Physics: choose method", font=('Arial', 24), bg='floral white')
   place(msg, 450, 80)

   p1_btn = Button(window, text='By Formula Name', height=2, width=20, command=p_choice1,
                   font=("Arial", 14, "bold"), bg='#e6f7ff')
   p2_btn = Button(window, text='By Variables', height=2, width=20, command=p_choice2,
                   font=("Arial", 14, "bold"), bg='#fff1f0')
   back_btn = Button(window, text='Back', command=step2, font=("Arial", 14, "bold"), bg='floral white')

   place(p1_btn, 450, 150)
   place(p2_btn, 450, 220)
   place(back_btn, 140, 340)


def p_choice1():
   """Search physics by formula name (column i[1])"""
   clear_widgets()
   msg = Label(window, text="Enter Formula Name", font=('Arial', 25), bg='floral white')
   place(msg, 450, 80)
   e = Entry(window, font=('Arial', 25))
   place(e, 450, 160)

   def submit():
       var = e.get()
       cursor.execute('SELECT * FROM physics')
       data = cursor.fetchall()
       result = ""
       for i in data:
           if var.lower().strip() in i[1].lower().strip():
               result += f"SNo: {i[0]} | Formula Name: {i[1]}\nFormula: {i[2]}\nVariables: {i[3]}\nSI Unit: {i[4]}\nConstants: {i[5]}\n\n"
       show_scrolling_result(result, p_choice1)

   submit_btn = Button(window, text='Submit', command=submit,
                       font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   back_btn = Button(window, text='Back', command=phy, font=("Arial", 14, "bold"), bg='floral white')
   place(submit_btn, 740, 160)
   place(back_btn, 140, 340)


def p_choice2():
   """Search physics by multiple variable names (column i[3])"""
   clear_widgets()
   msg = Label(window, text="Enter Variable(s) (e.g. v, a, t)", font=('Arial', 25), bg='floral white')
   place(msg, 450, 80)
   e = Entry(window, font=('Arial', 25))
   place(e, 450, 160)

   def submit():
       raw = e.get()
       if not raw.strip():
           show_scrolling_result("Please enter at least one variable.", p_choice2)
           return

       # Split variables by comma and clean them
       vars_input = [v.strip().lower() for v in raw.split(',') if v.strip()]
       cursor.execute('SELECT * FROM physics')
       data = cursor.fetchall()
       result = ""
       found = set()

       for i in data:
           variables_in_formula = i[3].lower().replace(" ", "")
           for v in vars_input:
               if v in variables_in_formula:
                   if i[0] not in found:  # avoid duplicates
                       found.add(i[0])
                       result += f"SNo: {i[0]} | Formula Name: {i[1]}\nFormula: {i[2]}\nVariables: {i[3]}\nSI Unit: {i[4]}\nConstants: {i[5]}\n\n"
                   break  # move to next formula if any match found

       if not result:
           result = "No formulas found for given variable(s)."

       show_scrolling_result(result, p_choice2)

   submit_btn = Button(window, text='Submit', command=submit,
                       font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   back_btn = Button(window, text='Back', command=phy, font=("Arial", 14, "bold"), bg='floral white')
   place(submit_btn, 740, 160)
   place(back_btn, 140, 340)

def p_choice2():
   """Search physics by variables (i[3])"""
   clear_widgets()
   msg = Label(window, text="Enter Variable Name", font=('Arial', 25), bg='floral white')
   place(msg, 450, 80)
   e = Entry(window, font=('Arial', 25))
   place(e, 450, 160)

   def submit():
       var = e.get()
       cursor.execute('SELECT * FROM physics')
       data = cursor.fetchall()
       result = ""
       for i in data:
           # variable column assumed to be i[3] as in your earlier schema
           if var.lower().strip() in i[3].lower().strip():
               result += f"SNo: {i[0]} | Formula Name: {i[1]}\nFormula: {i[2]}\nSI Unit: {i[4]}\nConstants: {i[5]}\n\n"
       show_scrolling_result(result, p_choice2)

   submit_btn = Button(window, text='Submit', command=submit,
                       font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   back_btn = Button(window, text='Back', command=phy, font=("Arial", 14, "bold"), bg='floral white')
   place(submit_btn, 740, 160)
   place(back_btn, 140, 340)

# -----------------------------------------------------------
# CHEMISTRY SCREEN
# -----------------------------------------------------------
def chem():
   clear_widgets()
   msg = Label(window, text="Enter Formula Name", font=('Arial', 25), bg='floral white')
   place(msg, 450, 80)
   e = Entry(window, font=('Arial', 25))
   place(e, 450, 160)

   def submit():
       var = e.get()
       cursor.execute('SELECT * FROM chemistry')
       data = cursor.fetchall()
       result = ""
       for i in data:
           if var.lower().strip() in i[1].lower().strip():
               result += f"SNo: {i[0]} | Formula Name: {i[1]}\nFormula: {i[2]}\nSI Unit: {i[4]}\nConstants: {i[5]}\n\n"
       show_scrolling_result(result, chem)

   submit_btn = Button(window, text='Submit', command=submit,
                       font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   back_btn = Button(window, text='Back', command=step2,
                     font=("Arial", 14, "bold"), bg='floral white', fg='BLACK')
   place(submit_btn, 740, 160)
   place(back_btn, 140, 340)

# -----------------------------------------------------------
# START PROGRAM
# -----------------------------------------------------------
show_name_screen()
window.mainloop()