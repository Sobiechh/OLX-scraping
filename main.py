import tkinter as tk
#import web_scrap

#tkinter 
window = tk.Tk() #window
window.title('OLX Projekt') #Set title
window.geometry('800x400') #Set geometry
 
l = tk.Label(window, bg='white', width=20, text='empty') 
l.pack()
 
def result():
    if (var1.get() == 1) & (var2.get() == 0):
        l.config(text='I love Python ')
    elif (var1.get() == 0) & (var2.get() == 1):
        l.config(text='I love C++')
    elif (var1.get() == 0) & (var2.get() == 0):
        l.config(text='I do not anything')
    else:
        l.config(text='I love both')

var1 = tk.IntVar()
var2 = tk.IntVar()
 
c1 = tk.Checkbutton(window, text='Python',variable=var1, onvalue=1, offvalue=0, command=result)
c1.pack()
c2 = tk.Checkbutton(window, text='C++',variable=var2, onvalue=1, offvalue=0, command=result)
c2.pack()

variable = tk.StringVar()
variable.set("Lodz")

w = tk.OptionMenu(window, 
'Aleksandrow-Lodzki',
'Belchatow',
'Glowno',
'Konstantynow-Lodzki', 
'Kutno', 
'Lask', 
'Leczyca', 
'Lodz',
'Lowicz', 
'Opoczno', 
'Ozorkow',
'Pabianice', 
'Piotrkow-Trybunalski', 
'Radomsko',
'Rawa-Mazowiecka', 
'Sieradz',
'Skierniewice', 
'Tomaszow-Mazowiecki', 
'Wielun',
'Zdunska-Wola',    
'Zgierz')
w.pack()


window.mainloop()