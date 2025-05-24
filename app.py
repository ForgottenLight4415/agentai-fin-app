from flask import Flask, request, jsonify
from flask_cors import CORS

#from Agentmodules.finscraper.scraper_tool.fetcher import fetch_stock_data_yf
from Agentmodules.agent import get_recommendation
from Agentmodules.testing_bot import verify_recommendation, parse_financials_string

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

        # If financials are passed as raw string, parse them
        if isinstance(financials, str):
            financials = parse_financials_string(financials)

        insight = get_recommendation(ticker, tone="formal")

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
        ticker = data.get('ticker')
        financial_data = data.get('financials')
        insight = data.get('insight')

        if not ticker or not financial_data or not insight:
            return jsonify({"error": "Missing required data"}), 400

        # If financial_data is a string, parse it
        if isinstance(financial_data, str):
            financial_data = parse_financials_string(financial_data)

        result = verify_recommendation(ticker, financial_data, insight)

        return jsonify({
            "ticker": ticker,
            "verdict": result.get("verdict"),
            "confidence": result.get("confidence"),
            "justification": result.get("justification"),
            "supporting_headlines": result.get("supporting_headlines_from_llm", []),
            "news_headlines": result.get("news_headlines", [])
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
