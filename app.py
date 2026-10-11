from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/spin", methods=["POST"])
def spin():
    payload = request.get_json(silent=True) or {}
    try:
        bet = int(payload.get("bet", 10))
    except (TypeError, ValueError):
        bet = 10
    bet = max(1, min(bet, 1000))

    numbers = [random.randint(1, 9) for _ in range(3)]
    a, b, c = numbers

    if numbers == [7, 7, 7]:
        result = "🔥 JACKPOT! ТРИ СЕМЁРКИ!"
        multiplier = 10
        kind = "jackpot"
    elif a == b == c:
        result = "🏆 ТРИ ОДИНАКОВЫХ!"
        multiplier = 5
        kind = "triple"
    elif a == b or a == c or b == c:
        result = "💰 ПАРА!"
        multiplier = 2
        kind = "pair"
    else:
        result = "Попробуй ещё раз!"
        multiplier = 0
        kind = "lose"

    return jsonify({
        "numbers": numbers,
        "result": result,
        "multiplier": multiplier,
        "payout": bet * multiplier,
        "kind": kind
    })

if __name__ == "__main__":
    app.run(debug=True)
