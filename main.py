from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load cities dataset
cities_df = pd.read_csv('k.csv')

@app.route("/relief-suggestion", methods=["GET"])
def relief_suggestion():
    area = request.args.get("area", "").strip().lower()
    
    # Search for cities containing the input (case-insensitive)
    results = cities_df[cities_df['city'].str.lower().str.contains(area)]
    
    if not results.empty:
        return jsonify({"area": area, "info": results.to_dict(orient='records')})
    else:
        return jsonify({"message": f"No data available for '{area}'."})

if __name__ == "__main__":
    app.run(debug=True)
