from flask import Flask, request, jsonify

app = Flask(__name__)


# --- パラメータ解析 ---

def parse_threshold(args):
    raw = args.get("threshold")

    if raw is None or raw.strip() == "":
        return None, (jsonify({"error": "threshold is required"}), 400)

    try:
        return int(raw), None
    except ValueError:
        return None, (jsonify({"error": "threshold must be integer"}), 400)


def parse_nums(args):
    raw = args.get("nums")

    if raw is None or raw.strip() == "":
        return None, (jsonify({"error": "nums is required"}), 400)

    nums = []
    for p in raw.split(","):
        p = p.strip()
        if p == "":
            return None, (jsonify({"error": "invalid nums"}), 400)
        try:
            nums.append(int(p))
        except ValueError:
            return None, (jsonify({"error": "nums must be integers"}), 400)

    return nums, None


# --- 計算ロジック（純粋関数） ---

def analyze_numbers(nums, threshold):
    total = len(nums)
    total_sum = sum(nums)
    avg = total_sum / total if total > 0 else None
    minimum = min(nums) if total > 0 else None
    maximum = max(nums) if total > 0 else None

    above_sum = 0
    negative_count = 0
    has_zero = False

    for n in nums:
        if n > threshold:
            above_sum += n
        if n < 0:
            negative_count += 1
        if n == 0:
            has_zero = True

    return {
        "total": total,
        "sum": total_sum,
        "avg": avg,
        "min": minimum,
        "max": maximum,
        "above_sum": above_sum,
        "negative_count": negative_count,
        "has_zero": has_zero
    }


# --- APIエンドポイント ---

@app.route("/analyze")
def analyze():
    threshold, error = parse_threshold(request.args)
    if error:
        return error

    nums, error = parse_nums(request.args)
    if error:
        return error

    return jsonify(analyze_numbers(nums, threshold))


@app.route("/")
def home():
    return "Flask is running!"


if __name__ == "__main__":
    app.run(debug=True)
