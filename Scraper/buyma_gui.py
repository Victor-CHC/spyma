from tkinter import *
import buyma_scraper
import pandas as pd

root = Tk()

e1 = Entry(root, width=50)
e1.pack()
e1.insert(0, 'https://www.buyma.com/buyer/4880785/sales_1.html')

e2 = Entry(root, width=50)
e2.pack()
e2.insert(0, '1')

def myClick():
    input1 = e1.get()
    input2 = e2.get()
    
    try:
        seller_list_results = buyma_scraper.seller_list(input1, int(input2))
        waitLabel = Label(root, text='Results Downloading Shortly')
        waitLabel.pack()
    except:
        errorLabel = Label(root, text='Invalid Entry')
        errorLabel.pack()
        seller_list_results = None
    
    if seller_list_results:
        pd.DataFrame(seller_list_results).to_excel('seller_list.xlsx', index=False)
        
    myLabel = Label(root, text=(input1 + input2))
    myLabel.pack()
    

    
myButton = Button(root, text="Generate Item List", command=myClick)
myButton.pack()


root.mainloop()