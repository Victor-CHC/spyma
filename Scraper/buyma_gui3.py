from tkinter import *
from tkinter import filedialog
import buyma_scraper
import pandas as pd


    

def sellerListClick():
    input1 = seller_list_url.get()
    input2 = seller_list_prev_days_slider.get()
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
    input2 = seller_list_extra_prev_days_slider.get()
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
buyma_title_label = Label(root, text="Buyma Spy")
buyma_title_label.grid(row=0, column=1, pady=10, padx=20)


# Seller List
user_item_frame = LabelFrame(root, text="Items List")
user_item_frame['bg'] = 'white'
user_item_frame.config(font=("Calibri", 18))
user_item_frame.grid(row=1, column=0, pady=10, padx=20)

seller_list_url = Entry(user_item_frame, width=50)
seller_list_url.grid(row=2, column=0, pady=10, padx=20, sticky='w')
seller_list_url['bg'] = 'white'
seller_list_url.insert(0, 'https://www.buyma.com/buyer/4880785/sales_1.html')

seller_list_prev_days_slider = Scale(user_item_frame, from_=0, to=100,tickinterval=20, length=300, orient=HORIZONTAL)
seller_list_prev_days_slider.set(30)
seller_list_prev_days_slider['bg'] = 'white'
seller_list_prev_days_slider.grid(row=3, column=0, pady=10, padx=20, sticky='w')

var1 = IntVar()
seller_list_details_button = Checkbutton(user_item_frame, text="Full Details",
                                         variable=var1, anchor='w')
seller_list_details_button['bg'] = 'white'
seller_list_details_button.grid(row=4,  pady=5, padx=20, sticky='w')

seller_list_details_caution = Label(user_item_frame, 
                                    text="CAUTION: Getting full details requires more time", 
                                    anchor='w')
seller_list_details_caution['bg'] = 'white'
seller_list_details_caution.grid(row=5, column=0, pady=5, padx=20, sticky='w')

sellerListButton = Button(user_item_frame, text="Download Item List", command=sellerListClick)
sellerListButton['bg'] = 'white'
sellerListButton.grid(row=6, column=0, pady=10, padx=20, sticky='w')

# Seller List Extra
user_item_extra_frame = LabelFrame(root, text="Get Buyma User's Items List With Additional Details")
user_item_extra_frame.grid(row=1, column=1, pady=10, padx=20)

seller_list_extra_url = Entry(user_item_extra_frame, width=50)
seller_list_extra_url.grid(row=2, column=1, pady=10, padx=20)
seller_list_extra_url.insert(0, 'https://www.buyma.com/buyer/4880785/sales_1.html')

seller_list_extra_prev_days_slider = Scale(user_item_extra_frame, from_=0, to=100,tickinterval=20, length=300, orient=HORIZONTAL)
seller_list_extra_prev_days_slider.set(30)
seller_list_extra_prev_days_slider.grid(row=3, column=1, pady=10, padx=20)

sellerListExtraButton = Button(user_item_extra_frame, text="Generate Item List", command=sellerListExtraClick)
sellerListExtraButton.grid(row=4, column=1, pady=10, padx=20)

# Item Matching
item_matching_frame = LabelFrame(root, text="Get Similar Items List")
item_matching_frame.grid(row=1, column=2, pady=10, padx=20)

fuzzy_item_query = Entry(item_matching_frame, width=50)
fuzzy_item_query.grid(row=2, column=2, pady=10, padx=20)
fuzzy_item_query.insert(0, 'Dior トップス Tシャツ')

fuzzy_threshold_slider = Scale(item_matching_frame, from_=0, to=100,tickinterval=20, length=300, orient=HORIZONTAL)
fuzzy_threshold_slider.set(90)
fuzzy_threshold_slider.grid(row=3, column=2, pady=10, padx=20)

itemMatchListButton = Button(item_matching_frame, text="Generate Item List", command=itemMatchListClick)
itemMatchListButton.grid(row=4, column=2, pady=10, padx=20)


root.mainloop()