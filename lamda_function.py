import json
import base64


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


def bai_category(bai):
    if bai < 21:
        return "Low"
    elif bai < 33:
        return "Normal"
    return "High"


def whr_category(whr):
    if whr < 0.9:
        return "Low Risk"
    elif whr < 1.0:
        return "Moderate Risk"
    return "High Risk"


def lambda_handler(event, context):
    try:
        body = event.get("body", event)

        if event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8")

        if isinstance(body, str):
            body = json.loads(body)

        if not body:
            raise ValueError("Request body is missing")

        required = ["name", "height", "weight", "waist", "hip"]
        for field in required:
            if field not in body:
                raise ValueError(f"Missing field: {field}")

        name = body["name"]
        height = float(body["height"])
        weight = float(body["weight"])
        waist = float(body["waist"])
        hip = float(body["hip"])

        bmi = weight / (height ** 2)
        bai = (hip / (height ** 1.5)) - 18
        whr = waist / hip

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "name": name,
                "bmi": round(bmi, 2),
                "bmi_category": bmi_category(bmi),
                "bai": round(bai, 2),
                "bai_category": bai_category(bai),
                "whr": round(whr, 2),
                "whr_category": whr_category(whr)
            })
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }

    