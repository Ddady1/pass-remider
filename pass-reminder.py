from datetime import datetime
import tkinter as tk
import ttkbootstrap as tkb
import os
import subprocess
from PIL import ImageTk, Image

def get_last_pass_set(username):
    pass_change = 90
    command_pass = f'Get-Aduser -identity {username} -Properties * -ErrorAction Stop | fl PasswordLastSet'
    result_pass = subprocess.run(['powershell.exe', command_pass], capture_output=True, encoding='cp862')
    print(result_pass.stdout)
    command_fullname = f'Get-Aduser -identity {username} -ErrorAction stop | fl Name'
    result_fullname = subprocess.run(['powershell.exe', command_fullname], capture_output=True, encoding='cp862')
    print(result_fullname.stdout)
    clean_date = get_clean_date(result_pass.stdout)
    full_name = get_clean_name(result_fullname.stdout)
    diff_days = get_dates_diff(clean_date)
    days_remain = pass_change - diff_days
    if days_remain == 1:
        flag = True
        main_win(days_remain, flag, full_name)
    if days_remain <= 14 and days_remain >= 0:
        flag = False
        main_win(days_remain, flag, full_name)
    else:
        pass


def get_clean_name(fullname):
    listed_string = fullname.rstrip('\n')
    listed_string = listed_string.split(' ')
    print(listed_string)
    clean_name = listed_string[2] + ' ' + listed_string[3]
    return clean_name

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
    return diff.days

def disable_event():
    pass

def main_win(diff_days, flag, full_name):

    # Create Main Window

    window = tkb.Window(themename='sandstone')
    window.title('Password Reminder')
    window.geometry('600x400+150+150')
    window.minsize(600, 400)
    window.resizable(False, False)

    font_color = 'black'
    #window.iconbitmap(img)
    if flag:
        window.protocol("WM_DELETE_WINDOW", disable_event)
        font_color = 'red'
    logo = Image.open('//tad-afula.local/NETLOGON/IL-CAR/logo.jpg')
    logo = ImageTk.PhotoImage(logo)
    logo_label = tkb.Label(window, image=logo)
    logo_label.pack()
    main_label_frame = tkb.LabelFrame(window, text='Password expiration')
    main_label_frame.pack(ipadx=80, ipady=40)
    message_lbl = tkb.Label(main_label_frame, text=f'\n\nHello {full_name}.\nYour password will expire in {diff_days} days.'
                                                   f'\n    Please consider changing it!', font=('Helvetica', 18), foreground=font_color)
    message_lbl.pack()
    ok_button = tkb.Button(window, text='OK', command=window.destroy)
    ok_button.pack(side='right', padx=20, ipadx=50)

    window.mainloop()


if __name__ == '__main__':
    logged_user = os.getlogin()
    test = 'kerenz'
    last_pass_set = get_last_pass_set(test)
