#from buyma_scraper import seller_list

import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import buyma_scraper
import pandas as pd

LARGE_FONT = ("Verdana", 12)


class BuymaSpyApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, "black.ico")
        tk.Tk.wm_title(self, "Buyma Spy")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo, PageThree):
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        # Bring frame to the front
        frame.tkraise()
        
    def sellerListClick(self):
        input1 = self.seller_list_url.get()
        input2 = self.seller_list_prev_days.get()
        try:
            seller_list_results = buyma_scraper.seller_list(input1, int(input2))
            if len(seller_list_results) == 0:
                tk.messagebox.showerror("Error","No items found. Try a different URL.")
        except:
            tk.messagebox.showerror("Error", "Unable to get results. Invalid URL or Number.")
            seller_list_results = None
        
        #tk.Tk().config(cursor="")
        
        if seller_list_results:
            directory = filedialog.asksaveasfilename()
            pd.DataFrame(seller_list_results).to_excel(directory+'.xlsx', index=False)
        


class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = tk.Label(self, text="Buyma Spy", font = ("Calibri", 16))
        title_label.grid(row=0, column=0, pady=10, padx=10)

        about_label = tk.Label(self, text="About", font = LARGE_FONT)
        about_label.grid(row=1, column=1, pady=10, padx=10)
        
        # Unclickable button (image)
        home_label = tk.Label(self, text="About", font = ("Calibri", 12))
        home_label.grid(row=1, column=0, pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Page 1", 
                            command=lambda: controller.show_frame(PageOne))
        button1.grid(row=2, column=0, pady=20, padx=20)  
        
        button2 = ttk.Button(self, text="Page 2", 
                            command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=3, column=0, pady=20, padx=20)    
        
        button3 = ttk.Button(self, text="Page 3", 
                            command=lambda: controller.show_frame(PageThree))
        button3.grid(row=4, column=0, pady=20, padx=20)
        
        about_text = tk.Label(self, text="Buyma Spy is a free tool. Don't be a fool", font = ("Calibri", 12))
        about_text.grid(row=2, column=1, pady=10, padx=10)        
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = tk.Label(self, text="Buyma Spy", font = ("Calibri", 16))
        title_label.grid(row=0, column=0, pady=10, padx=10)
        
        label_heading = tk.Label(self, text="Get Buyma User's Items List", font = LARGE_FONT)
        label_heading.grid(row=1, column=1, pady=10, padx=10)
        
        homeButton = ttk.Button(self, text="About", 
                            command=lambda: controller.show_frame(StartPage))
        homeButton.grid(row=1, column=0, pady=20, padx=20)
        
        # Unclickable button (image)
        button1_label = tk.Label(self, text="Page 1", font = ("Calibri", 12))
        button1_label.grid(row=2, column=0, pady=10, padx=10)        

        button2 = ttk.Button(self, text="Page 2", 
                            command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=3, column=0, pady=20, padx=20)
        
        button3 = ttk.Button(self, text="Page 3", 
                            command=lambda: controller.show_frame(PageThree))
        button3.grid(row=4, column=0, pady=20, padx=20)
        
        # Seller List        
        self.seller_list_url = tk.Entry(self, width=50)
        self.seller_list_url.grid(row=2, column=1)
        self.seller_list_url.insert(0, 'https://www.buyma.com/buyer/4880785/sales_1.html')
        
        self.seller_list_prev_days = tk.Entry(self, width=50)
        self.seller_list_prev_days.grid(row=3, column=1)
        self.seller_list_prev_days.insert(0, '1')
        
        sellerListButton = ttk.Button(self, text="Generate Item List", 
                                      command=BuymaSpyApp.sellerListClick)
        sellerListButton.grid(row=4, column=1)
    

        

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = tk.Label(self, text="Buyma Spy", font = ("Calibri", 16))
        title_label.grid(row=0, column=0, pady=10, padx=10)
        
        label = tk.Label(self, text="Page 2", font = LARGE_FONT)
        label.grid(row=1, column=1, pady=10, padx=10)
        
        homeButton = ttk.Button(self, text="About", 
                            command=lambda: controller.show_frame(StartPage))
        homeButton.grid(row=1, column=0, pady=20, padx=20)
        
        button1 = ttk.Button(self, text="Page 1", 
                            command=lambda: controller.show_frame(PageOne))
        button1.grid(row=2, column=0, pady=20, padx=20) 
        
        # Unclickable button (image)
        button2_label = tk.Label(self, text="Page 2", font = ("Calibri", 12))
        button2_label.grid(row=3, column=0, pady=10, padx=10)  

        button3 = ttk.Button(self, text="Page 3", 
                            command=lambda: controller.show_frame(PageThree))
        button3.grid(row=4, column=0, pady=20, padx=20) 

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = tk.Label(self, text="Buyma Spy", font = ("Calibri", 16))
        title_label.grid(row=0, column=0, pady=10, padx=10)        
        
        label = tk.Label(self, text="Graph Page", font = LARGE_FONT)
        label.grid(row=1, column=1, pady=10, padx=10)
        
        homeButton = ttk.Button(self, text="About", 
                            command=lambda: controller.show_frame(StartPage))
        homeButton.grid(row=1, column=0, pady=20, padx=20)
        
        button1 = ttk.Button(self, text="Page 1", 
                            command=lambda: controller.show_frame(PageOne))
        button1.grid(row=2, column=0, pady=20, padx=20)  
        
        button2 = ttk.Button(self, text="Page 2", 
                            command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=3, column=0, pady=20, padx=20)    

        # Unclickable button (image)
        button3_label = tk.Label(self, text="Page 3", font = ("Calibri", 12))
        button3_label.grid(row=4, column=0, pady=10, padx=10)
        
        # f = Figure(figsize=(5,5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1,2,3,4,5,6,7,8], [7,6,8,5,3,5,2,1])
        
        # # We need to bring the plot to the foreground
        # canvas = FigureCanvasTkAgg(f, self)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # # Add navigation bar
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
app = BuymaSpyApp()
app.mainloop()
        
        

        