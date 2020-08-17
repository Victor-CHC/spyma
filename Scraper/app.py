from io import StringIO
import csv

from flask import Flask, render_template, request, make_response
from buyma_scraper import seller_list, all_listed_items_details


# Declare the app
app = Flask(__name__)

# Start an app route which is '/'
@app.route('/')
# Declare the main function
def main():
    return render_template('app.html')


# Form Submission Route
@app.route('/scrape_basic', methods=['POST'])
def send_basic():
    if request.method == 'POST':
        # Start Pulling Data from Form Input
        try:
            buyer_page_url = request.form['buyer_page_url_basic']
            previous_days = float(request.form['previous_days'])
            buyer_id = buyer_page_url.split('/')[4]
        except:
            return render_template('app.html', 
                    scrape_results_basic='Input a valid number for previous days')
        
        # IF both inputs are valid:
        if buyer_page_url and previous_days:
            try:
                scrape_results = seller_list(buyer_page_url, previous_days)
            except:
                scrape_results = None
        if scrape_results:
            try:
                scrape_results_headers = [list(scrape_results[0].keys())]
                scrape_results_list = [list(r.values()) for r in scrape_results]
                si = StringIO()
                cw = csv.writer(si)
                cw.writerows(scrape_results_headers + scrape_results_list)
                output = make_response(si.getvalue())
                output.headers["Content-Disposition"] = "attachment; filename=export_basic_{}_{}days.csv".format(
                    buyer_id, previous_days)
                output.headers["Content-type"] = "text/csv"
                render_template('app.html', 
                        scrape_results_basic='Results found - downloading CSV file')
                return output
            except:
                return render_template('app.html', 
                        scrape_results_basic='ERROR: Results could not be downloaded')
        else:
            return render_template('app.html', 
                    scrape_results_basic='No Items Found')
    else:
        return render_template('app.html')

# Form Submission Route
@app.route('/scrape_all', methods=['POST'])
def send_all():
    if request.method == 'POST':
        # Start Pulling Data from Form Input
        try:
            buyer_page_url = request.form['buyer_page_url_all']
            previous_days = float(request.form['previous_days'])
            buyer_id = buyer_page_url.split('/')[4]
        except:
            return render_template('app.html', 
                    scrape_results_all='Input a valid number for previous days')
        
        # IF both inputs are valid:
        if buyer_page_url and previous_days:
            try:
                scrape_results = all_listed_items_details(buyer_page_url, previous_days)
            except:
                scrape_results = None
        if scrape_results:
            try:
                scrape_results_headers = [list(scrape_results[0].keys())]
                scrape_results_list = [list(r.values()) for r in scrape_results]
                si = StringIO()
                cw = csv.writer(si)
                cw.writerows(scrape_results_headers + scrape_results_list)
                output = make_response(si.getvalue())
                output.headers["Content-Disposition"] = "attachment; filename=export_all_{}_{}days.csv".format(
                    buyer_id, previous_days)
                output.headers["Content-type"] = "text/csv"
                render_template('app.html', 
                        scrape_results_all='Results found - downloading CSV file')
                return output
            except:
                return render_template('app.html', 
                        scrape_results_all='ERROR: Results could not be downloaded')
        else:
            return render_template('app.html', 
                    scrape_results_all='No Items Found')
    else:
        return render_template('app.html')

'''
@app.route('/scrape', methods=['POST'])
def send():
    if request.method == 'POST':
        # Start Pulling Data from Form Input
        try:
            buyer_page_url = request.form['buyer_page_url']
            previous_days = float(request.form['previous_days'])
        except:
            return render_template('app.html', 
                    scrape_results='Input a valid number for previous days')
        
        # IF both inputs are valid:
        if buyer_page_url and previous_days:
            try:
                scrape_results = seller_list(buyer_page_url, previous_days)
            except:
                scrape_results = None
        if scrape_results:
            return render_template('app.html', 
                    scrape_results=scrape_results)
        else:
            return render_template('app.html', 
                    scrape_results='No Items Found')
    else:
        return render_template('app.html')
        '''