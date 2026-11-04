from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "WinGo AI प्रेडिक्टर API सफलतापूर्वक चल रहा है!"}

@app.post("/predict")
def predict_result(data: dict):
    history = data.get("history", [])
    result = "Green" if len(history) % 2 == 0 else "Red"
    return {"input_history": history, "prediction": result}
  
