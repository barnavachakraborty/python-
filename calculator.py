from tkinter import *

root = Tk()

Expression = Entry(
    root,
    font=("Monospace", 20),
    justify="left",
)
Expression.insert(0, '0')
Expression.grid(row=0, column=0, columnspan=5, sticky="we", pady=10)

def click(val):
    current = Expression.get()
    if current == "0":
        Expression.delete(0, END)
        Expression.insert(0, val)
    else:
        Expression.insert(END, val)

def equal():
    try:
        exp = Expression.get()
        exp = exp.replace("x","*")
        Expression.delete(0,END)
        Expression.insert(0,eval(exp))
    except:
        Expression.delete(0,END)
        Expression.insert(0,"Error")

layout = [
    ['7','8','9','Del','AC'],
    ['4','5','6','x','/'],
    ['1','2','3','+','-']
]

for r, row in enumerate(layout):
    for c, char in enumerate(row):
        if char == 'Del':
            cmd = lambda: Expression.delete(len(Expression.get())-1,END) if Expression.get() != 'Error' else Expression.delete(0,END)
        elif char == 'AC':
            cmd = lambda: Expression.delete(0,END)
        else: cmd = lambda ch = char: click(ch)
        btn = Button(
            root,
            text=char,
            padx = 20,
            pady = 20,
            command=cmd
        )
        btn.grid(row = r+1,column = c,sticky = "we")    

zero_btn = Button(
    root,
    text = '0',
    padx = 20,
    pady = 20,
    command= lambda:click('0')
)
zero_btn.grid(row = 4,column=0,sticky="we",columnspan=2)

equal_btn = Button(
    root,
    text = '=',
    padx = 20,
    pady = 20,
    command= equal
)
equal_btn.grid(row = 4,column=2,sticky="we",columnspan=2)
root.iconbitmap('E:/python/tkinter/Frame 1.ico')

root.mainloop()