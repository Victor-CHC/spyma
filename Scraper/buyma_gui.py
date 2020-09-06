from tkinter import *
from tkinter import filedialog
import buyma_scraper
import pandas as pd


    

def sellerListClick():
    input1 = seller_list_url.get()
    input2 = seller_list_prev_days.get()
    try:
        seller_list_results = buyma_scraper.seller_list(input1, int(input2))
        if len(seller_list_results) == 0:
            messagebox.showerror("Error","No items found. Try a different URL.")
    except:
        messagebox.showerror("Error", "Unable to get results. Invalid URL or Number.")
        seller_list_results = None
    
    root.config(cursor="")
    
    if seller_list_results:
        directory = filedialog.asksaveasfilename()
        pd.DataFrame(seller_list_results).to_excel(directory+'.xlsx', index=False)

        
def sellerListExtraClick():
    input1 = seller_list_url.get()
    input2 = seller_list_prev_days.get()
    try:
        seller_list_results = buyma_scraper.all_listed_items_details(input1, int(input2))
        if len(seller_list_results) == 0:
            messagebox.showerror("Error","No items found. Try a different URL.")
    except:
        messagebox.showerror("Error", "Unable to get results. Invalid URL or Number.")
        seller_list_results = None
    
    root.config(cursor="")
    
    if seller_list_results:
        directory = filedialog.asksaveasfilename()
        pd.DataFrame(seller_list_results).to_excel(directory+'.xlsx', index=False)        

        
def itemMatchListClick():
    input1 = fuzzy_item_query.get()
    input2 = fuzzy_threshold_slider.get()
  
    try:
        item_list_results = buyma_scraper.similar_extra_search(input1, int(input2))
        item_count = len(item_list_results)
        if item_count==0:
            messagebox.showerror("Error","No similar items found. Try a different search query or lower the threshold.")
    except:
        messagebox.showerror("Error", "Invalid URL")
        item_list_results = None

    if item_list_results:
        directory = filedialog.asksaveasfilename()
        pd.DataFrame(item_list_results).to_excel(directory+'.xlsx', index=False)
    
    
root = Tk()

# Seller List
buyma_user_label = Label(root, text="Get Buyma User's Items List")
buyma_user_label.pack()

seller_list_url = Entry(root, width=50)
seller_list_url.pack()
seller_list_url.insert(0, 'https://www.buyma.com/buyer/4880785/sales_1.html')

seller_list_prev_days = Entry(root, width=50)
seller_list_prev_days.pack()
seller_list_prev_days.insert(0, '1')

sellerListButton = Button(root, text="Generate Item List", command=sellerListClick)
sellerListButton.pack()

# Seller List Extra
buyma_user_extra_label = Label(root, text="Get Buyma User's Items List With Additional Details")
buyma_user_extra_label.pack()

seller_list_extra_url = Entry(root, width=50)
seller_list_extra_url.pack()
seller_list_extra_url.insert(0, 'https://www.buyma.com/buyer/4880785/sales_1.html')

seller_list_extra_prev_days = Entry(root, width=50)
seller_list_extra_prev_days.pack()
seller_list_extra_prev_days.insert(0, '1')

sellerListExtraButton = Button(root, text="Generate Item List", command=sellerListExtraClick)
sellerListExtraButton.pack()

# Item Matching
item_matching_label = Label(root, text="Get Similar Items List")
item_matching_label.pack()

fuzzy_item_query = Entry(root, width=50)
fuzzy_item_query.pack()
fuzzy_item_query.insert(0, 'Dior トップス Tシャツ')

fuzzy_threshold_slider = Scale(root, from_=0, to=100,tickinterval=20, length=300, orient=HORIZONTAL)
fuzzy_threshold_slider.set(90)
fuzzy_threshold_slider.pack()

itemMatchListButton = Button(root, text="Generate Item List", command=itemMatchListClick)
itemMatchListButton.pack()


root.mainloop()