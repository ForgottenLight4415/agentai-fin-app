from flask import Flask, request, jsonify
from flask_cors import CORS
from finscraper.scraper_tool.fetcher import fetch_stock_data_yf
# from agent_module.agent_chain import generate_insight

app = Flask(__name__)
CORS(app)  # Allow frontend access from Orchids/React

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()

        if not ticker:
            return jsonify({"error": "Ticker is required."}), 400

        financials = fetch_stock_data_yf(ticker)

        return jsonify({
            "ticker": ticker,
            "financials": financials
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insight', methods=['POST'])
def get_insight():
    try:
        data = request.get_json()
        ticker = data.get('ticker')
        financials = data.get('financials')

        if not ticker or not financials:
            return jsonify({"error": "Missing ticker or financials"}), 400

        # Use this when LangChain agent is ready:
        # insight = generate_insight(ticker, financials)
        insight = f"Recommendation: BUY – Based on strong EPS and healthy P/E ratio for {ticker}."

        return jsonify({
            "ticker": ticker,
            "insight": insight
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verifier', methods=['POST'])
def verify_insight():
    try:
        data = request.get_json()
        financials = data.get('financials')
        insight = data.get('insight')

        if not financials or not insight:
            return jsonify({"error": "Missing data or insight"}), 400

        pe_ratio = float(financials.get('pe_ratio', 100))
        verdict = "BUY" if pe_ratio < 80 else "HOLD"

        return jsonify({
            "verdict": verdict,
            "final_summary": f"{verdict} based on P/E ratio and agent cross-checks."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
