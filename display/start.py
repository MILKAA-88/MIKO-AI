from tkinter import *

def show_boot_screen():
    root = Tk()
    root.title("MIKO AI")
    root.geometry("1080x720")
    root.minsize(480, 360)
    root.config(background="#000000")

    label_title = Label(root, text="MIKO AI", font=("Times New Roman", 40), fg="white", bg="black")
    label_title.pack(expand=True)

    def next1():
        label_title.config(text="I'm coming, just wait one second buddy.")
    def next2():
        label_title.config(text="Loading...")
    def next3():
        label_title.config(text="Initializing Systems...")
    def next4():
        label_title.config(text="Time is infinite. But is it so?")
    def next5():
        label_title.config(text="...")
    def next6():
        label_title.config(text="Almost ready...")
    def next7():
        label_title.config(text="I got install by 6.")
        root.after(10000, root.destroy)

    root.after(1000,  next1)
    root.after(3000,  next2)
    root.after(5000,  next3)
    root.after(7000,  next4)
    root.after(9000,  next5)
    root.after(11000, next6)
    root.after(13000, next7)

    root.mainloop()

   