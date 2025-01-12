from datetime import datetime
import tkinter as tk
import ttkbootstrap as tkb
import os
import subprocess

def get_last_pass_set(username):
    command = f'Get-Aduser -identity {username} -Properties * -ErrorAction Stop | fl PasswordLastSet'
    result = subprocess.run(['powershell.exe', command], capture_output=True, encoding='cp862')
    print(result.stdout)
    clean_date = get_clean_date(result.stdout)
    get_dates_diff(clean_date)

def get_clean_date(date):
    listed_string = list(date.split(' '))
    print(listed_string)
    print(len(listed_string))
    clean_date = listed_string[2]
    print(clean_date)
    return clean_date


    '''delta = clean_date - today
    print(delta.days)'''


def get_dates_diff(last_date):
    last_date = datetime.strptime(last_date, '%m/%d/%Y')
    print(last_date)
    today = datetime.today()
    print(today)
    diff = today - last_date
    print(diff.days)

# Create Main Window

window = tkb.Window(themename='sandstone')
window.title('Password Reminder')
window.geometry('600x400+150+150')
window.minsize(600, 400)
#window.iconbitmap(img)

logged_user = os.getlogin()
test = 'dimam'
last_pass_set = get_last_pass_set(logged_user)



if __name__ == '__main__':
    window.mainloop()