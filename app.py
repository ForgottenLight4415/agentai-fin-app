from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import pandas as pd

# Add submodule (or inner directory) to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
inner_path = os.path.join(current_dir, "Agentmodules")
if inner_path not in sys.path:
    sys.path.insert(0, inner_path)

from agent import get_recommendation
from testing_bot import run_full_analysis

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

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/insight', methods=['POST'])
def get_insight():
    try:
        data = request.get_json()
        input_query = data.get('query')

        if not input_query:
            return jsonify({"error": "Missing ticker or company name"}), 400

        ticker = resolve_ticker(input_query)
        if not ticker:
            return jsonify({"error": "Invalid company name or ticker symbol"}), 400

        result = run_full_analysis(ticker=ticker, tone="formal", use_mock=False)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5050)