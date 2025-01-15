import finnhub
import customtkinter as ctk 
import tkinter.messagebox as tkmb 
from PIL import Image
import os

finnhub_client = finnhub.Client(api_key="ctdgjmhr01qng9geib1gctdgjmhr01qng9geib20")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("950x600")
app.title("Stock Analysis App")

try:
    bg_image = ctk.CTkImage(
        light_image=Image.open("background.png"),
        dark_image=Image.open("background.png"),
        size=(950, 600)
    )
    bg_label = ctk.CTkLabel(app, image=bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Error loading background image: {e}")


def register():
    Entered_Username = user_entry.get()
    Entered_Password = user_pass.get()
    db = open("Database.txt", "w")
    db.write(Entered_Username + ":" + Entered_Password + "\n")
    tkmb.showwarning(title='Cerdentials Saved!!!',message='Please login with your new credentails')

def auth():
    db = open("Database.txt", "r")
    Entered_Username = user_entry.get()
    Entered_Password = user_pass.get()
    Usernames = []
    Passwords = []
    for i in db:
        Username,Password = i.split(":")
        Password = Password.strip()
        Usernames.append(Username)
        Passwords.append(Password)
        data = dict(zip(Usernames, Passwords))
    try:
        if data[Entered_Username]:
            try:
                if Entered_Password == data[Entered_Username]:
                    tkmb.showinfo(title='Login Successfull!!!',message='Welcome to the Stock Analysis App')
                    return True
            except:
                tkmb.showerror(title='Invalid credentials!!!',message='Please try again')
                register()
                login()
    except:
        tkmb.showerror(title='Invalid credentials!!!',message='Please try again')
        register()
        login()
def Submit():
    
    return True
def login(): 
    if auth():
        app.withdraw()
        Main_window = ctk.CTkToplevel(app)
        Main_window.title("Stock Anaylysis App")
        Main_window.geometry("950x600")
        right_frame = ctk.CTkFrame(Main_window, width=700, height=600, bg_color="black")
        right_frame.place(relx=0.1, rely=0.5, anchor="center", relwidth=0.5, relheight=1)
        Welcome_msg = ctk.CTkLabel(Main_window, text = f"Welcome to the Stock Analysis APP \n please enter a stock symbol to continue!", bg_color ="darkblue", font=("Times New Roman", 20))
        Welcome_msg.place(relx=0.17, rely=0.05, anchor="center")
        Welcome_msg = ctk.CTkLabel(Main_window, text = f"Please Enter Stock Name!", font=("Times New Roman", 20))
        Welcome_msg.place(relx=0.17, rely=0.48, anchor="center")
        Stock_entry= ctk.CTkEntry(Main_window,placeholder_text="BTC")
        Stock_entry.place(relx=0.17,rely=0.55, anchor= "center")
        Submit_btn = ctk.CTkButton(Main_window,text='Submit',corner_radius=32, command=Submit)
        Submit_btn.place(relx=0.17, rely=0.61, anchor= "center")    



#login Page setup

x_pos = 0.85 #Must be between 0-1
y_pos = 0.55 #Must be between 0-1
user_entry= ctk.CTkEntry(master=app,placeholder_text="Username")
user_entry.place(relx=x_pos,rely=y_pos, anchor= "center")
user_pass= ctk.CTkEntry(master=app,placeholder_text="Password",show="*")
user_pass.place(relx=x_pos,rely=(y_pos+0.05), anchor= "center")
button = ctk.CTkButton(master=app,text='Login',corner_radius=32, command=login)
button.place(relx=x_pos, rely=(y_pos+0.1), anchor= "center") 




app.mainloop()