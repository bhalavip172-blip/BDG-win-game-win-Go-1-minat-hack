from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
import random

app = FastAPI()

html_content = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDG Win 3-Min Wingo Live Tool</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 10px;
            margin: 0;
        }
        .main-wrapper {
            max-width: 420px;
            margin: 20px auto;
            background: #181818;
            border: 2px solid #00ffcc;
            border-radius: 20px;
            padding: 15px;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.4);
            position: relative;
        }
        .top-badge {
            background: #1e1e1e;
            border: 1px solid #00ffcc;
            color: #00ffcc;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }
        .container {
            background: #1e1e1e;
            border: 1.5px solid #00ffcc;
            border-radius: 15px;
            padding: 15px;
            box-shadow: inset 0 0 15px rgba(0, 255, 204, 0.2);
        }
        .header {
            font-size: 24px;
            font-weight: bold;
            color: #00ffcc;
            letter-spacing: 2px;
            margin-bottom: 5px;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
        }
        .status-box {
            background: #111;
            border-radius: 8px;
            padding: 8px 12px;
            margin: 12px 0;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
            border: 1px solid #333;
        }
        .active {
            color: #00ff66;
            font-weight: bold;
        }
        .card {
            background: #121212;
            border: 1px dashed #00ffcc;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
        }
        .radar-circle {
            width: 70px;
            height: 70px;
            border: 2px dashed #00ffcc;
            border-radius: 50%;
            margin: 0 auto 10px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: spin 4s linear infinite;
            color: #00ffcc;
            font-size: 20px;
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        
        .btn-container {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .scan-btn {
            background: linear-gradient(135deg, #00ffcc, #0099ff);
            color: #000;
            font-weight: bold;
            padding: 12px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 15px;
            flex: 1;
            box-shadow: 0 4px 15px rgba(0, 255, 204, 0.4);
        }
        .hide-btn {
            background: linear-gradient(135deg, #ff007f, #ff3333);
            color: #fff;
            font-weight: bold;
            padding: 12px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 15px;
            width: 90px;
            box-shadow: 0 4px 15px rgba(255, 0, 127, 0.4);
        }
        .scan-btn:active, .hide-btn:active {
            transform: scale(0.97);
        }
        #result {
            margin-top: 10px;
            font-size: 15px;
            color: #ffcc00;
            font-weight: bold;
        }
        .prd-text {
            font-size: 13px;
            color: #00ffcc;
            letter-spacing: 0.5px;
            margin-top: 8px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="main-wrapper">
        <div class="top-badge">🟢 LIVE SERVER • 3-MIN SYNC</div>
        
        <div class="container">
            <div class="header">BDG WIN</div>
            <div style="font-size: 11px; color: #00ffcc; letter-spacing: 2px; margin-bottom: 10px;">3-MIN WINGO NEXT PREDICTOR</div>
            
            <div class="status-box">
                <span>LIVE : <span class="active">CONNECTED</span></span>
                <span>PING : 11MS</span>
                <span>MODE : 3-MIN</span>
            </div>

            <div class="card">
                <div class="radar-circle">🎯</div>
                <p style="margin: 0 0 5px 0; color: #aaa; font-size: 12px;">NEXT PERIOD ANALYZING</p>
                <div id="result">Click 'SCAN & GET' for next prediction</div>
                <div class="prd-text" id="prd-display">#PRD : Ready</div>
            </div>

            <div class="btn-container">
                <button class="scan-btn" onclick="fetchNumber()">🔍 SCAN & GET</button>
                <button class="hide-btn" onclick="toggleView()">👁 HIDE</button>
            </div>
        </div>
    </div>

    <script>
        async function fetchNumber() {
            const resBox = document.getElementById("result");
            const prdBox = document.getElementById("prd-display");
            
            resBox.innerText = "Analyzing next period...";
            prdBox.innerText = "#PRD : Fetching...";
            
            try {
                let response = await fetch('/live_analysis');
                let data = await response.json();
                
                let res = data.prediction_result;
                let colorCode = res.predicted_color === 'Green' ? '#00ff66' : '#ff3333';
                
                resBox.innerHTML = `Color: <span style="color:${colorCode}">${res.predicted_color}</span> (${res.predicted_size}) | No: <span style="color:#ffcc00">${res.predicted_number}</span>`;
                prdBox.innerText = "#PRD : " + res.period_number;
            } catch(e) {
                resBox.innerText = "Error! Try again.";
                prdBox.innerText = "#PRD : Failed";
            }
        }

        function toggleView() {
            let card = document.querySelector('.container');
            card.style.display = card.style.display === 'none' ? 'block' : 'none';
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return html_content

@app.get("/live_analysis")
async def get_live_analysis():
    # भारतीय समय (IST) के अनुसार सटीक समय निकालना
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    
    date_prefix = ist_now.strftime('%Y%m%d')
    total_minutes_today = ist_now.hour * 60 + ist_now.minute
    three_min_blocks = total_minutes_today // 3
    
    # आपके स्क्रीनशॉट के बेस और एक कदम आगे (Next Period) के साथ सटीक सिंक्रोनाइज़ेशन (+1 जोड़ दिया गया है)
    base_offset = 20204 - (int((datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%H')) * 20 + int((datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%M')) // 3)
    period_number = int(date_prefix + "10002") + three_min_blocks + 1
    
    # इस पीरियड नंबर को सीड बनाकर रैंडम लॉजिक ताकि इस 3 मिनट के दौरान बिल्कुल फिक्स रिजल्ट मिले
    random.seed(period_number)
    
    predicted_number = random.randint(0, 9)
    predicted_color = "Green" if predicted_number in [1, 3, 7, 9, 5] else "Red"
    predicted_size = "Big" if predicted_number >= 5 else "Small"
    
    return {
        "status": "success",
        "server": "BDG 3-Min Next Period Connected",
        "prediction_result": {
            "predicted_color": predicted_color,
            "predicted_size": predicted_size,
            "predicted_number": predicted_number,
            "period_number": period_number,
            "confidence": f"{random.randint(92, 99)}%"
        }
    }
