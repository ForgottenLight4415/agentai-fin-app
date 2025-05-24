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
        ticker = data.get('ticker')
        financial_data = data.get('financials')
        insight = data.get('insight')

        if not ticker or not financial_data or not insight:
            return jsonify({"error": "Missing required data"}), 400

        # Format string for LLM
        formatted_data = "\n".join([f"{k}: {v}" for k, v in financial_data.items()])

        # Run LangChain verifier
        response = verifier_chain.run({
            "ticker": ticker,
            "financial_data": formatted_data,
            "recommendation": insight
        })

        # Try to parse LLM JSON-like output
        import re, json
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            structured = json.loads(match.group(0))
        else:
            structured = {
                "verdict": "UNCERTAIN",
                "confidence": "N/A",
                "justification": response.strip()
            }

        return jsonify({
            "verdict": structured.get("verdict"),
            "confidence": structured.get("confidence"),
            "justification": structured.get("justification")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
