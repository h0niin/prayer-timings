import threading
import time
from bs4 import BeautifulSoup
import requests
import customtkinter as ctk

def data():
    response = requests.get("https://timesprayer.com/en/prayer-times-in-kattangal.html")
    soup = BeautifulSoup(response.content, 'html.parser')
    lis = soup.find_all('td')
    global txt
    txt = (f"{lis[0].string} : {lis[1].string}\n"
           f"{lis[4].string} : {lis[5].string}\n"
           f"{lis[6].string} : {lis[7].string}\n"
           f"{lis[8].string} : {lis[9].string}\n"
           f"{lis[10].string} : {lis[11].string}")
    # current time
    global cur_time
    cur_time = soup.find(id='countdown').string

def update_data():
    while True:
        data()
        # Update the label text in the main thread
        app.after(0, update_label)
        # Refresh every 30 minutes



def update_label():
    times.configure(text=txt)
    current_time.configure(text=f"Next Prayer in\n{cur_time}")

ctk.set_appearance_mode("System")
app = ctk.CTk()
app.title("Prayer Times by h0niin ")
app.geometry("400x400")
try:app.iconbitmap('prayerly.ico')
except:print("App Icon Error :(")

ctk.CTkLabel(app, text="Prayer Times", font=("forte", 30)).pack(pady=(20,5))
ctk.CTkLabel(app, text="(Kattangal)", font=("segoe print", 15)).pack(pady=5)
frame = ctk.CTkFrame(app, corner_radius=10)
frame.pack(pady=10, padx=40, fill='both')

# Initialize data
data()

times = ctk.CTkLabel(frame, text=txt, font=("roboto", 20))
times.pack(pady=10)
current_time = ctk.CTkLabel(app, text=f"Next Prayer in\n{cur_time}", font=("open sans", 20, 'italic'), text_color='red')
current_time.pack(pady=10)
ctk.CTkLabel(app, text="Stay Tuned for Next Update: Enter Location! ", font=("roboto", 15, "italic")).pack()
ctk.CTkLabel(app, text="Do message @h0rniin for feedback...", font=("roboto", 10, "italic")).pack()

# Start the thread to refresh data
threading.Thread(target=update_data, daemon=True).start()

app.mainloop()
