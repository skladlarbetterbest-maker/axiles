# OCR API Project - Jamol uchun

## Bugungi ishimiz:

1. **GitHubga kod yuklash**
   - PaddleOCR-main ni GitHubga push qildik
   - URL: https://github.com/skladlarbetterbest-maker/axiles.git

2. **API yaratish** (EasyOCR)
   - `C:\Learn\Learn\code\opencode2\PaddleOCR-main\api.py`
   - Flask + EasyOCR (Python 3.14 da ishlaydi)
   - Til tanlash: English, Russian, English+Russian
   - Web interfeys bor

3. **Ishga tushirish**
   ```bash
   cd C:\Learn\Learn\code\opencode2\PaddleOCR-main
   python api.py
   ```
   - URL: http://127.0.0.1:8000/

---

## Keyinchalik qilish kerak:

1. **GitHubga push qilish**
   ```bash
   git add api.py
   git commit -m "Add EasyOCR API with web interface"
   git push origin main
   ```

2. **Serverga qo'yish** (Render.com)
   - Build: `pip install flask easyocr`
   - Start: `python api.py`

3. **Google Apps Script bilan ulash**

---

## Hozirgi holat:
- API localhostda ishga tushgan
- Brauzerda http://127.0.0.1:8000/ ochish mumkin
- Rasm yuklab OCR natijasini olish mumkin
