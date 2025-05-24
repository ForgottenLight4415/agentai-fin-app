from flask import Flask, request, render_template
from finscraper.scraper_tool.fetcher import fetch_stock_data_yf
# from agent_module.agent_chain import generate_insight

app = Flask(__name__)
@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/app', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if not ticker:
            return render_template('app.html', error="Please enter a ticker.")

        try:
            # Use real scraper tool
            data = fetch_stock_data_yf(ticker.upper())
            print(data)
            # If insight chain is ready, uncomment below:
            # insight = generate_insight(ticker.upper(), data)
            return render_template('app.html', data=data, ticker=ticker.upper())
        except Exception as e:
            return render_template('app.html', error=f"Error: {str(e)}")

    return render_template('app.html')
