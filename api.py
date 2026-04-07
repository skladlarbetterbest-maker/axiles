from flask import Flask, request, jsonify
import requests
import io
import base64

app = Flask(__name__)

OCR_API_KEY = "helloworld"

@app.route("/")
def home():
    return jsonify({"message": "OCR API ishga tushdi!", "status": "ok"})

@app.route("/ocr", methods=["POST"])
def ocr_image():
    try:
        if "file" in request.files:
            file = request.files["file"]
            files = {"file": (file.filename, file.stream, file.content_type)}
            data = {"language": "uzb"}
        elif "image_base64" in request.json:
            image_data = request.json["image_base64"]
            if "," in image_data:
                image_data = image_data.split(",")[1]
            files = {"file": ("image.png", base64.b64decode(image_data), "image/png")}
            data = {"language": "uzb"}
        else:
            return jsonify({"success": False, "error": "File yoki image_base64 yuboring"}), 400

        response = requests.post(
            "https://api.ocr.space/parse/image",
            files=files,
            data=data,
            headers={"apikey": OCR_API_KEY}
        )

        result = response.json()

        if result.get("IsErroredOnProcessing"):
            return jsonify({"success": False, "error": result.get("ErrorMessage", ["Unknown error"])}), 500

        parsed_results = result.get("ParsedResults", [])
        texts = []
        for item in parsed_results:
            text = item.get("ParsedResults", [{}])[0].get("ParsedText", "")
            conf = item.get("TextOverlay", {}).get("MeanConfidence", 0)
            texts.append({"text": text, "confidence": conf/100})

        return jsonify({
            "success": True,
            "count": len(texts),
            "results": texts
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
