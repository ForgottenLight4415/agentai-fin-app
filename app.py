from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import pandas as pd
from flask_socketio import SocketIO, emit

# Add submodule (or inner directory) to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
inner_path = os.path.join(current_dir, "Agentmodules")
if inner_path not in sys.path:
    sys.path.insert(0, inner_path)

from agent import get_recommendation
from testing_bot import parse_financials_string,verify_recommendation
from finscraper.scraper_tool.tool import stock_data_tool,stock_news_tool

# Load NASDAQ symbol lookup table once on startup
csv_path = os.path.join(current_dir,"static", "nasdaq-listed-symbols.csv")
symbol_df = pd.read_csv(csv_path)

# Build lookup dictionaries for fast access
company_to_symbol = {
    str(row["Company Name"]).strip().lower(): str(row["Symbol"]).strip().upper()
    for _, row in symbol_df.iterrows()
    if pd.notnull(row["Company Name"]) and pd.notnull(row["Symbol"])
}

symbol_set = set(symbol_df["Symbol"].dropna().astype(str).str.upper())


def resolve_ticker(query: str) -> str:
    """Resolves a user input to a valid ticker symbol (exact ticker or partial company name)."""
    if not query:
        return None

    query_upper = query.strip().upper()
    if query_upper in symbol_set:
        return query_upper

    # Check exact lower-case match first
    query_lower = query.strip().lower()
    if query_lower in company_to_symbol:
        return company_to_symbol[query_lower]

    # Fallback: partial match in company name
    for company_name, symbol in company_to_symbol.items():
        if query_lower in company_name:
            return symbol  # return first match

    return None


# Flask app config
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

#@app.route('/insight', methods=['POST'])
@socketio.on('insight')
def handle_run_analysis(data):
    query = data.get('query')
    ticker = resolve_ticker(query)

    if not ticker:
        emit('error', {'error': 'Invalid ticker or company name'})
        return

    emit('stage_0_ack', {'message': f"🔁 Starting analysis for {ticker}"})

    try:
        # 🔍 STAGE 1: Financial + News Data
        raw_financials = stock_data_tool.run(ticker)
        financials = parse_financials_string(raw_financials)
        news = stock_news_tool.run(ticker)
        emit('stage_1_financials', {
            'ticker': ticker,
            'financials': financials,
            'news_headlines': news.split("\n")[:5]
        })

        # 🤖 STAGE 2: Generate Recommendation
        recommendation = get_recommendation(ticker)
        emit('stage_2_recommendation', {
            'recommendation': recommendation
        })

        # 🔎 STAGE 3: Verifier Bot
        result = verify_recommendation(ticker, financials, recommendation)
        emit('stage_3_verification', result)

    except Exception as e:
        emit('error', {'error': str(e)})



if __name__ == '__main__':
    socketio.run(app, debug=True, port=5050)
