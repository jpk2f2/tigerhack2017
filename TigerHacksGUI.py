# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tkinter as tk
from tkinter import *
#class login:
#    def __init__(self, master):
#        self.master = master
#        self.frame = tk.Frame(self.master)
#        self.username=tk.Entry(self.frame,width=25).grid(row=1,column=0)
#        self.password=tk.Entry(self.frame,width=25).grid(row=2,column=0)
#        self.button1 = tk.Button(self.frame, text = 'Login', width = 25, command = self.new_window)
#        #self.username.pack()
#        #self.password.pack()
#       # self.button1.pack()
#       # self.frame.pack()
#
#    def new_window(self):
#        self.newWindow = tk.Toplevel(self.master)
#        self.app = Reader(self.newWindow)
#
#class Reader:
#    def __init__(self, master):
#        self.master = master
#        self.frame = tk.Frame(self.master)
#        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
#        self.quitButton.pack()
#        self.frame.pack()
#
#    def close_windows(self):
#        self.master.destroy()

def main(): 
    username=StringVar()
    password=StringVar()
    root = tk.Tk()
    
    usernameLabel=tk.Entry(width=25,variable=username).grid(row=0,column=1,padx=10,pady=10)
    passwordLabel=tk.Entry(width=25,variable=username).grid(row=1,column=1,padx=10,pady=10)
    Label(text='Username:',width=25).grid(row=0,column=0,pady=10)
    Label(text='Password:',width=25).grid(row=1,column=0,pady=10)
    loginButton=tk.Button(text='Login',width=25).grid(row=3,columnspan=2,pady=10,padx=10)
    
    mainloop()

if __name__ == '__main__':
    main()
