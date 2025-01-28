import customtkinter as ctk 
import tkinter.messagebox as tkmb 
from PIL import Image
import os
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    tkmb.showwarning(title='Credentials Saved!!!', message='Please login with your new credentials')

def auth():
    db = open("Database.txt", "r")
    Entered_Username = user_entry.get()
    Entered_Password = user_pass.get()
    Usernames = []
    Passwords = []
    for i in db:
        Username, Password = i.split(":")
        Password = Password.strip()
        Usernames.append(Username)
        Passwords.append(Password)
        data = dict(zip(Usernames, Passwords))
    try:
        if data[Entered_Username]:
            try:
                if Entered_Password == data[Entered_Username]:
                    tkmb.showinfo(title='Login Successful!!!', message='Welcome to the Stock Analysis App')
                    return True
            except:
                tkmb.showerror(title='Invalid credentials!!!', message='Please try again')
                register()
                login()
    except:
        tkmb.showerror(title='Invalid credentials!!!', message='Please try again')
        register()
        login()

def plot_stock_data(stock_data, right_frame):
    plt.close('all')
    for widget in right_frame.winfo_children():
        widget.destroy()
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
    ax.plot(stock_data['Close'], label='Close Price')
    ax.set_title('Stock Close Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price (USD)')
    ax.legend()
    ax.grid(True)
    
    # Embed matplotlib figure in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=ctk.BOTH, expand=True)
    canvas.draw()

def login(): 
    if auth():
        app.withdraw()
        Main_window = ctk.CTkToplevel(app)
        Main_window.title("Stock Analysis App")
        Main_window.geometry("950x600")
        
        right_frame = ctk.CTkFrame(Main_window, width=700, height=600, bg_color="black")
        right_frame.place(relx=0.75, rely=0.5, anchor="center", relwidth=0.5, relheight=1)
        Welcome_msg = ctk.CTkLabel(Main_window, text="Welcome to the Stock Analysis APP \nplease enter a stock symbol to continue!", bg_color="darkblue", font=("Times New Roman", 20))
        Welcome_msg.place(relx=0.2, rely=0.1, anchor="center")
        Welcome_msg = ctk.CTkLabel(Main_window, text="Please Enter Stock Name!", font=("Times New Roman", 20))
        Welcome_msg.place(relx=0.17, rely=0.48, anchor="center")
        Stock_entry = ctk.CTkEntry(Main_window, placeholder_text="AAPL")
        Stock_entry.place(relx=0.17, rely=0.55, anchor="center")
        def Submit():
            ticker_symbol = Stock_entry.get() or "AAPL"  # Default to AAPL if no input
            try:
                stock_data = yf.download(ticker_symbol, start='2020-01-01', end='2024-01-01')
                plot_stock_data(stock_data, right_frame)
            except Exception as e:
                tkmb.showerror("Error", f"Could not fetch stock data: {str(e)}")
        
        Submit_btn = ctk.CTkButton(Main_window, text='Submit', corner_radius=32, command=Submit)
        Submit_btn.place(relx=0.17, rely=0.61, anchor="center")

x_pos = 0.85 #Must be between 0-1
y_pos = 0.55 #Must be between 0-1
user_entry = ctk.CTkEntry(master=app, placeholder_text="Username")
user_entry.place(relx=x_pos, rely=y_pos, anchor="center")
user_pass = ctk.CTkEntry(master=app, placeholder_text="Password", show="*")
user_pass.place(relx=x_pos, rely=(y_pos+0.05), anchor="center")
button = ctk.CTkButton(master=app, text='Login', corner_radius=32, command=login)
button.place(relx=x_pos, rely=(y_pos+0.1), anchor="center")

app.mainloop()