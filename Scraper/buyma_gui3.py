from tkinter import *
from tkinter import filedialog
import buyma_scraper
import pandas as pd


    

def sellerListClick():
    input1 = seller_list_url.get()
    input2 = seller_list_prev_days_slider.get()
    
    # If detailed list button is not checked, do a basic scrape
    if details_toggle.get() == 0:
        
        try:
            seller_list_results = buyma_scraper.seller_list(input1, int(input2))
            if len(seller_list_results) == 0:
                messagebox.showerror("Error","No items found. Try a different URL.")
        except:
            messagebox.showerror("Error", "Unable to get results. Invalid URL or Number.")
            seller_list_results = None
    # If detailed list button is not checked, do a detailed scrape
    else:

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


def importFileClick():
    global import_list
    
    filename = filedialog.askopenfilename(filetypes=[('Excel', ('*.xls', '*.xlsx'))])
    df = pd.read_excel(filename)
    df_dict = df.T.to_dict()
    import_list = list(df_dict.values())


def fileMatchListClick():
    input1 = excel_item_query.get()
    input2 = import_list
    input3 = excel_threshold_slider.get()
    
    try:
        results = buyma_scraper.similar_items(import_list, 90)
    except:
        results = None
        messagebox.showerror("Error", "Invalid File")
    
    if results:
        directory = filedialog.asksaveasfilename()
        pd.DataFrame(results).to_excel(directory+'.xlsx', index=False)        

    



root = Tk()
buyma_title_label = Label(root, text="Buyma Spy")
buyma_title_label.grid(row=0, column=0, pady=10, padx=20, sticky='w')



# --- Seller List ---
user_item_frame = LabelFrame(root, text="Sold Items List")
user_item_frame['bg'] = 'white'
user_item_frame.config(font=("Calibri", 18))
user_item_frame.grid(row=1, column=0, pady=10, padx=20, sticky='n')

seller_list_URL_title = Label(user_item_frame, text="USER'S SALE PAGE URL:")
seller_list_URL_title['bg'] = 'white'
seller_list_URL_title.config(font=("Calibri", 12, 'bold'))
seller_list_URL_title.grid(row=2, column=0, pady=(20,0), padx=20, sticky='w')


seller_list_url = Entry(user_item_frame, width=50)
seller_list_url.grid(row=3, column=0, pady=(0,20), padx=20, sticky='w')
seller_list_url['bg'] = 'white'
seller_list_url.insert(0, 'https://www.buyma.com/buyer/4880785/sales_1.html')


seller_list_prev_days_title = Label(user_item_frame, text="PREVIOUS DAYS:")
seller_list_prev_days_title['bg'] = 'white'
seller_list_prev_days_title.config(font=("Calibri", 12, 'bold'))
seller_list_prev_days_title.grid(row=4, column=0, pady=0, padx=20, sticky='w')

seller_list_prev_days_slider = Scale(user_item_frame, from_=0, to=100,
                                     tickinterval=20, length=300, orient=HORIZONTAL)
seller_list_prev_days_slider.set(30)
seller_list_prev_days_slider['bg'] = 'white'
seller_list_prev_days_slider.grid(row=5, column=0, pady=(0,20), padx=20, sticky='w')

details_toggle = IntVar()
seller_list_details_button = Checkbutton(user_item_frame, text="FULL DETAILS",
                                         variable=details_toggle, anchor='w')
seller_list_details_button['bg'] = 'white'
seller_list_details_button.config(font=("Calibri", 12, 'bold'))
seller_list_details_button.grid(row=6,  pady=5, padx=5, sticky='w')

seller_list_details_caution1 = Label(user_item_frame, 
                                     text="CAUTION: Getting full details may take several minutes.")
seller_list_details_caution2 = Label(user_item_frame, 
                                     text="Be patient and wait for the process to finish.")

seller_list_details_caution1['bg'] = 'white'
seller_list_details_caution2['bg'] = 'white'
seller_list_details_caution1.grid(row=7, column=0, pady=0, padx=20, sticky='w')
seller_list_details_caution2.grid(row=8, column=0, pady=0, padx=20, sticky='w')


sellerListButton = Button(user_item_frame, text="Download Item List", 
                          command=sellerListClick)
sellerListButton['bg'] = 'white'
sellerListButton.grid(row=10, column=0, pady=30, padx=20, sticky='w')




# --- Item Matching ---

item_matching_frame = LabelFrame(root, text="Matching Items Search")
item_matching_frame['bg'] = 'white'
item_matching_frame.config(font=("Calibri", 18))
item_matching_frame.grid(row=1, column=1, pady=10, padx=20, sticky='n')

fuzzy_item_queryL_title = Label(item_matching_frame, text="SEARCH WORDS:")
fuzzy_item_queryL_title['bg'] = 'white'
fuzzy_item_queryL_title.config(font=("Calibri", 12, 'bold'))
fuzzy_item_queryL_title.grid(row=2, column=0, pady=(20,0), padx=20, sticky='w')


fuzzy_item_query = Entry(item_matching_frame, width=50)
fuzzy_item_query.grid(row=3, column=0, pady=(0,20), padx=20, sticky='w')
fuzzy_item_query['bg'] = 'white'
fuzzy_item_query.insert(0, 'Dior トップス Tシャツ')


fuzzy_threshold_slider_title = Label(item_matching_frame, text="WORD MATCH THRESHOLD")
fuzzy_threshold_slider_title['bg'] = 'white'
fuzzy_threshold_slider_title.config(font=("Calibri", 12, 'bold'))
fuzzy_threshold_slider_title.grid(row=4, column=0, pady=0, padx=20, sticky='w')

fuzzy_threshold_slider = Scale(item_matching_frame, from_=0, to=100,
                                     tickinterval=20, length=300, orient=HORIZONTAL)
fuzzy_threshold_slider.set(90)
fuzzy_threshold_slider['bg'] = 'white'
fuzzy_threshold_slider.grid(row=5, column=0, pady=(0,20), padx=20, sticky='w')


itemMatchListButton = Button(item_matching_frame, text="Download Item List", 
                          command=itemMatchListClick)
itemMatchListButton['bg'] = 'white'
itemMatchListButton.grid(row=10, column=0, pady=30, padx=20, sticky='w')


# --- Item Matching From List---
matching_user_item_frame = LabelFrame(root, text="Matching Items From File")
matching_user_item_frame['bg'] = 'white'
matching_user_item_frame.config(font=("Calibri", 18))
matching_user_item_frame.grid(row=1, column=2, pady=10, padx=20, sticky='n')


import_excel_title = Label(matching_user_item_frame, text="IMPORT EXCEL FILE:")
import_excel_title['bg'] = 'white'
import_excel_title.config(font=("Calibri", 12, 'bold'))
import_excel_title.grid(row=2, column=0, pady=(20,0), padx=20, sticky='w')

open_file_btn = Button(matching_user_item_frame, text="Open File", 
                       command=importFileClick)
open_file_btn['bg'] = 'white'
open_file_btn.grid(row=3, column=0, pady=(0,20), padx=20, sticky='w')

excel_threshold_slider_title = Label(matching_user_item_frame, text="WORD MATCH THRESHOLD")
excel_threshold_slider_title['bg'] = 'white'
excel_threshold_slider_title.config(font=("Calibri", 12, 'bold'))
excel_threshold_slider_title.grid(row=4, column=0, pady=0, padx=20, sticky='w')

excel_threshold_slider = Scale(matching_user_item_frame, from_=0, to=100,
                                     tickinterval=20, length=300, orient=HORIZONTAL)
excel_threshold_slider.set(90)
excel_threshold_slider['bg'] = 'white'
excel_threshold_slider.grid(row=5, column=0, pady=(0,20), padx=20, sticky='w')


fileMatchListButton = Button(matching_user_item_frame, text="Download Matching Item List", 
                          command=fileMatchListClick)
fileMatchListButton['bg'] = 'white'
fileMatchListButton.grid(row=6, column=0, pady=30, padx=20, sticky='w')


root.mainloop()