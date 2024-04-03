import tkinter
from tkinter.ttk import Frame, Label, Combobox


top = tkinter.Tk()
top.title = "TKVue Test"

frame = Frame(top)
frame.pack(fill='both', expand=1, padx=10, pady=10)

l = Label(frame, text="Available values: ", width=20)
l.pack(side='left')

c = Combobox(frame, values=['zero', 'one', 'two', 'three'])
c.pack(side='left', expand=1)

top.mainloop()
