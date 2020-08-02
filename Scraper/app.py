from flask import Flask, render_template, request
from buyma_scraper import seller_list

# Declare the app
app = Flask(__name__)

# Start an app route which is '/'
@app.route('/')
# Declare the main function
def main():
    return render_template('app.html')


# Form Submission Route
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
        # Calculation IF Statements
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

