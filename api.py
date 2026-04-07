from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
import uvicorn
import os

app = FastAPI()

ocr = PaddleOCR(use_angle_cls=True, lang='uz', show_log=False)

@app.get("/")
def home():
    return {"message": "PaddleOCR API ishga tushdi!", "status": "ok"}

@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    contents = await file.read()
    
    temp_path = "temp_image.jpg"
    with open(temp_path, "wb") as f:
        f.write(contents)
    
    try:
        result = ocr.ocr(temp_path, cls=True)
        
        texts = []
        if result and result[0]:
            for line in result[0]:
                texts.append({
                    "text": line[1][0],
                    "confidence": float(line[1][1])
                })
        
        os.remove(temp_path)
        
        return JSONResponse({
            "success": True,
            "count": len(texts),
            "results": texts
        })
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
