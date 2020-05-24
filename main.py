import tkinter as tk #tkinter app
from web_scrap import scrap_OLX #second file

#result of program
def print_average_value(): 
    label.config(text=f'{scrap_OLX(regions[region_var.get()], surface_min.get(), surface_max.get(), var_dealer.get(), media_on.get())}')

#tkinter initial window
window = tk.Tk() #window
window.title('OLX Projekt') #Set title
#window.geometry('800x400') #Set geometry

#surfaces menu
surfaces = [100, 300,500,800,1000,1500]
surfaces.extend([x for x in range(2000, 10001,1000)])
surfaces.append(25000)

surface_min = tk.IntVar() #var surface minimum
surface_max = tk.IntVar() #var surface maximum

tk.Label(window, text='Powierzchnia dzialki m^2').grid(row=0, column =0, sticky = tk.W)
tk.Label(window, text='Od').grid(row=1, column =0, sticky = tk.W)
tk.Label(window, text='Do').grid(row=1, column =0, sticky = tk.E)

t1 = tk.OptionMenu(window, surface_min, *surfaces) #option menu surface_min
t2 = tk.OptionMenu(window, surface_max, *surfaces) #option menu surface_max

t1.grid(row=2, column =0, sticky = tk.W)
t2.grid(row=2, column =0, sticky = tk.E)

media_on = tk.BooleanVar() #boolen value for media
tk.Checkbutton(window, text='Media',variable=media_on, onvalue=True, offvalue=False).grid(row=3, column =0) #checkbutton

#cities read with image_read
regions = {
    'Aleksandrów Łódzki':'Aleksandrow-Lodzki',
    'Bełchatów':'Belchatow',
    'Głowno':'Glowno',
    'Konstantynów Łódzki':'Konstantynow-Lodzki', 
    'Kutno':'Kutno', 
    'Łask':'Lask', 
    'Łęczyca':'Leczyca', 
    'Łódź':'Lodz',
    'Łowicz':'Lowicz', 
    'Opoczno':'Opoczno', 
    'Ozorków':'Ozorkow',
    'Pabianice':'Pabianice', 
    'Piotrków Trybunalski':'Piotrkow-Trybunalski', 
    'Radomsko':'Radomsko',
    'Rawa Mazowiecka':'Rawa-Mazowiecka', 
    'Sieradz':'Sieradz',
    'Skierniewice':'Skierniewice', 
    'Tomaszów Mazowiecki':'Tomaszow-Mazowiecki', 
    'Wielun':'Wielun',
    'Zduńska Wola':'Zdunska-Wola',    
    'Zgierz':'Zgierz'
    }

#set default value of option menu
region_var = tk.StringVar() 
region_var.set("Łódź")

#label localization
tk.Label(text='Lokalizacja').grid(row=4, column =0, sticky=tk.W)
tk.OptionMenu(window, region_var, *regions.keys()).grid(row=4, column =0, sticky=tk.W) #option menu cities

#dealers
dealers = [
        ("Prywatne", "private"),
        ("Biura/Deweloperzy", "business"),
        ("Wszystkie", " "),
    ]

var_dealer = tk.StringVar()
var_dealer.set("") # initialize

i=5
for text, mode in dealers:
    b = tk.Radiobutton(window, text=text, variable=var_dealer, value=mode)
    b.grid(row=i,column=0, sticky = tk.W)
    i+=1

#button
tk.Button(window, text ="Oblicz", command = print_average_value).grid(row=8, column =0, sticky = tk.W)

#result
label = tk.Label(window, bg='white', width=50, text='') #set parametr
label.grid(row=9, column = 0,rowspan = 5 , sticky = tk.W)


window.mainloop() #starting application