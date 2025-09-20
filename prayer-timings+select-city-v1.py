import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
import time, threading
from datetime import datetime

def data():
    response = requests.get(f"https://timesprayer.com/en/prayer-times-in-{city}.html")
    soup = BeautifulSoup(response.content, 'html.parser')
    lis = soup.find_all('td')
    global txt
    txt = (f"{lis[0].string} : {lis[1].string}\n"
           f"{lis[4].string} : {lis[5].string}\n"
           f"{lis[6].string} : {lis[7].string}\n"
           f"{lis[8].string} : {lis[9].string}\n"
           f"{lis[10].string} : {lis[11].string}")

def update_data():
    while True:
        data()
        # Update the label text in the main thread
        app.after(1000, update_label)
        # Refresh every second

def update_label():
    times.configure(text=txt)
    current_time.configure(text=f"{datetime.now().strftime("%H:%M:%S")}")

def setCity():
    if cityEntry.get():
        global city
        city = cityEntry.get().strip().lower().replace(" ","-")
        update_label()

ctk.set_appearance_mode("System")
app = ctk.CTk()
app.title("Prayer Times by h0niin ")
app.geometry("400x400")
try:app.iconbitmap('prayerly.ico')
except:print("App Icon Not Found :(")

city = "kattangal"
txt = ""

ctk.CTkLabel(app, text="Prayer Times", font=("forte", 30)).pack(pady=(20,5))

cityFrame = ctk.CTkFrame(app, fg_color="transparent")
cityFrame.pack(pady=5)
cityEntry = ctk.CTkEntry(cityFrame, placeholder_text="Enter City", font=("segoe print", 15))
cityEntry.pack(side="left", padx=(0,1))
cityEntry.bind("<Return>", lambda event: setCity()) # Enter Keybind
cityBtn = ctk.CTkButton(cityFrame, text="☑", width=10, height=30, command=setCity)
cityBtn.pack(side="right")

frame = ctk.CTkFrame(app, corner_radius=10)
frame.pack(pady=10, padx=40, fill='both')
data()

times = ctk.CTkLabel(frame, text=txt, font=("roboto", 20))
times.pack(pady=10)
current_time = ctk.CTkLabel(app, text=f"{datetime.now().strftime("%H:%M:%S")}", font=("open sans", 20, 'italic'), text_color='red')
current_time.pack(pady=10)
ctk.CTkLabel(app, text="@h0niin for feedback...", font=("roboto", 10, "italic")).pack()

# Start thread to refresh data
threading.Thread(target=update_data, daemon=True).start()

app.mainloop()

