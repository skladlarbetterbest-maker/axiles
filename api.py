from flask import Flask, request, jsonify, render_template_string
import easyocr
from PIL import Image
import io

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>OCR API</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .upload-box { border: 2px dashed #ccc; padding: 30px; text-align: center; margin: 20px 0; border-radius: 5px; }
        input[type="file"] { display: none; }
        .upload-btn { background: #4CAF50; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .upload-btn:hover { background: #45a049; }
        select { padding: 10px; font-size: 16px; margin: 10px 0; width: 100%; }
        .result { background: #e8f5e9; padding: 15px; margin-top: 20px; border-radius: 5px; display: none; }
        .result h3 { margin-top: 0; color: #2e7d32; }
        .result pre { background: white; padding: 10px; overflow-x: auto; white-space: pre-wrap; }
        .error { background: #ffebee; color: #c62828; padding: 15px; margin-top: 20px; border-radius: 5px; display: none; }
        .status { text-align: center; padding: 10px; margin-top: 10px; }
        .preview { max-width: 100%; max-height: 300px; margin: 10px 0; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>OCR API (EasyOCR)</h1>
        
        <div class="upload-box">
            <input type="file" id="fileInput" accept="image/*" onchange="previewFile()">
            <label for="fileInput" class="upload-btn">Rasm tanlash</label>
            <p id="fileName"></p>
            <img id="preview" class="preview">
        </div>
        
        <select id="language">
            <option value="en">English</option>
            <option value="ru">Russian</option>
            <option value="en,ru">English + Russian</option>
        </select>
        
        <div class="status" id="status"></div>
        
        <div class="result" id="result">
            <h3>Natija:</h3>
            <pre id="resultText"></pre>
        </div>
        
        <div class="error" id="error"></div>
    </div>
    
    <script>
        function previewFile() {
            const file = document.getElementById('fileInput').files[0];
            if (!file) return;
            document.getElementById('fileName').textContent = file.name;
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('preview').src = e.target.result;
                document.getElementById('preview').style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
        
        document.getElementById('fileInput').addEventListener('change', uploadFile);
        
        function uploadFile() {
            const file = document.getElementById('fileInput').files[0];
            if (!file) return;
            
            document.getElementById('status').textContent = 'Ishlanmoqda...';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            const formData = new FormData();
            formData.append('file', file);
            formData.append('language', document.getElementById('language').value);
            
            fetch('/ocr', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('status').textContent = '';
                if (data.success) {
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('resultText').textContent = JSON.stringify(data, null, 2);
                } else {
                    document.getElementById('error').style.display = 'block';
                    document.getElementById('error').textContent = 'Xato: ' + data.error;
                }
            })
            .catch(error => {
                document.getElementById('status').textContent = '';
                document.getElementById('error').style.display = 'block';
                document.getElementById('error').textContent = 'Xato: ' + error;
            });
        }
    </script>
</body>
</html>
"""

reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en', 'ru'], gpu=False, verbose=False)
    return reader

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/ocr", methods=["POST"])
def ocr_image():
    try:
        if "file" not in request.files:
            return jsonify({"success": False, "error": "File yuborilmadi"}), 400
            
        file = request.files["file"]
        language = request.form.get("language", "en")
        
        image = Image.open(file.stream)
        
        ocr_reader = get_reader()
        result = ocr_reader.readtext(image)
        
        texts = []
        full_text = ""
        
        for item in result:
            bbox, text, conf = item
            texts.append({
                "text": text,
                "confidence": float(conf)
            })
            full_text += text + "\n"
        
        return jsonify({
            "success": True,
            "count": len(texts),
            "text": full_text.strip(),
            "results": texts
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
