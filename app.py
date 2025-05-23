from flask import Flask, request, render_template
# from scraper_module.fetch import fetch_stock_data  # temporarily disabled
#from agent_module.agent_chain import generate_insight

app = Flask(__name__)

def mock_stock_data(ticker):
    return {
        "ticker": ticker,
        "price": 341.17,
        "pe_ratio": 52.3,
        "eps": 6.52,
        "market_cap": "1.2T",
        "revenue": "24.7B"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if not ticker:
            return render_template('index.html', error="Please enter a ticker.")

        try:
            # Use mock data instead of real scraper
            data = mock_stock_data(ticker.upper())
            #insight = generate_insight(ticker.upper(), data)
            return render_template('index.html', data=data,  ticker=ticker.upper())
        except Exception as e:
            return render_template('index.html', error=f"Error: {str(e)}")

    return render_template('index.html')
