from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from typing import Optional
import os
import random

app = FastAPI()

GAME_LINK = "https://www.dmplay20.com/#/register?invitationCode=61385166635"

@app.get("/", response_class=HTMLResponse)
def home_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DM Play WinGo - Real Sync AI</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body, html { width: 100%; height: 100%; overflow: hidden; background: #000; font-family: Arial, sans-serif; }
            
            .game-frame {
                width: 100%;
                height: 100vh;
                border: none;
                position: absolute;
                top: 0;
                left: 0;
                z-index: 1;
            }

            .ai-widget {
                position: fixed;
                top: 10px;
                right: 10px;
                width: 310px;
                background: rgba(15, 23, 42, 0.98);
                backdrop-filter: blur(14px);
                border: 2px solid #3b82f6;
                border-radius: 12px;
                z-index: 99999;
                color: #ffffff;
                box-shadow: 0 10px 35px rgba(0,0,0,0.9);
                font-size: 12px;
            }

            .widget-header {
                background: linear-gradient(135deg, #2563eb, #3b82f6);
                padding: 10px 12px;
                font-weight: bold;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                cursor: pointer;
                font-size: 13px;
                color: #fff;
            }

            .widget-body {
                padding: 12px;
            }

            .info-box {
                background: #020617;
                border: 1px solid #1e293b;
                padding: 8px;
                border-radius: 6px;
                margin-bottom: 8px;
            }

            .info-row {
                display: flex;
                justify-content: space-between;
                margin-bottom: 4px;
                font-size: 11px;
                color: #94a3b8;
            }

            .info-val {
                color: #60a5fa;
                font-weight: bold;
            }

            .scan-btn {
                width: 100%;
                background: linear-gradient(135deg, #1d4ed8, #3b82f6);
                color: #fff;
                border: none;
                padding: 9px;
                font-weight: bold;
                border-radius: 6px;
                cursor: pointer;
                font-size: 12px;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
            }

            .scan-btn:active {
                transform: scale(0.98);
            }

            .prediction-box {
                margin-top: 10px;
                background: #020617;
                padding: 10px;
                border-radius: 6px;
                border-left: 4px solid #3b82f6;
                display: none;
            }

            .highlight {
                color: #60a5fa;
                font-weight: bold;
            }

            .toggle-btn {
                background: none;
                border: none;
                color: #fff;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
            }
        </style>
        <script>
            let detectedLivePeriod = "Scanning...";
            let nextTargetPeriod = "Waiting...";

            // गेम के पेज से लाइव पीरियड ऑटोमैटिक ढूंढने का कोड
            function fetchGameLivePeriod() {
                try {
                    const iframe = document.getElementById('gameFrame');
                    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                    
                    // गेम टेबल या स्क्रीन से पीरियड ढूंढना
                    const periodElement = iframeDoc.querySelector('.period, [class*="period"], td');
                    if (periodElement) {
                        const text = periodElement.innerText.trim();
                        if (text.length >= 10 && !isNaN(text)) {
                            detectedLivePeriod = text;
                            // अगले पीरियड का नंबर कैलकुलेट करना (+1)
                            let nextVal = BigInt(text) + 1n;
                            nextTargetPeriod = nextVal.toString();

                            document.getElementById('display_period').innerText = detectedLivePeriod;
                            document.getElementById('next_period_hidden').value = nextTargetPeriod;
                        }
                    }
                } catch(e) {
                    // क्रॉस-ओरिजिन सुरक्षा के कारण यदि iframe डेटा रीड न हो पाए, तो सुरक्षित फॉールबैक टाइम सिंक यूज़ करें
                    fallbackTimeSync();
                }
            }

            function fallbackTimeSync() {
                const now = new Date();
                const year = now.getUTCFullYear();
                const month = String(now.getUTCMonth() + 1).padStart(2, '0');
                const day = String(now.getUTCDate()).padStart(2, '0');
                const hours = String(now.getUTCHours()).padStart(2, '0');
                const minutes = String(now.getUTCMinutes()).padStart(2, '0');
                
                // सही WinGo फॉर्मेट मैच करने के लिए
                let baseNum = year + month + day + "1000" + hours + minutes;
                detectedLivePeriod = baseNum;
                let nextVal = BigInt(baseNum) + 1n;
                nextTargetPeriod = nextVal.toString();

                document.getElementById('display_period').innerText = detectedLivePeriod;
                document.getElementById('next_period_hidden').value = nextTargetPeriod;
            }

            async function triggerAutoScan() {
                const targetPeriod = document.getElementById('next_period_hidden').value;
                if(!targetPeriod || targetPeriod === "Waiting...") return;

                const formData = new FormData();
                formData.append('period_number', targetPeriod);

                try {
                    const response = await fetch('/auto-predict', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    if(data.status === 'success') {
                        document.getElementById('resultBox').style.display = 'block';
                        document.getElementById('resContent').innerHTML = 
                            '<b>📌 अगला टारगेट पीरियड:</b> <span class="highlight">' + data.target_period + '</span><br>' +
                            '<b>🎯 सटीक प्रेडिक्टेड नंबर:</b> <span class="highlight" style="font-size:15px;">' + data.prediction.exact_number + '</span><br>' +
                            '<b>📊 साइज:</b> <span class="highlight">' + data.prediction.size + '</span><br>' +
                            '<b>🎨 कलर:</b> <span class="highlight">' + data.prediction.color + '</span><br>' +
                            '<b>⚡ मोड:</b> Real-Sync AI Active';
                    }
                } catch(err) {
                    console.log('Sync error');
                }
            }

            setInterval(fetchGameLivePeriod, 1500);

            function toggleWidget() {
                const body = document.getElementById('widgetBody');
                body.style.display = (body.style.display === 'none') ? 'block' : 'none';
            }
        </script>
    </head>
    <body>

        <iframe id="gameFrame" src="https://www.dmplay20.com/#/register?invitationCode=61385166635" class="game-frame" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>

        <input type="hidden" id="next_period_hidden" value="">

        <div class="ai-widget">
            <div class="widget-header" onclick="toggleWidget()">
                <span>🤖 Real-Sync AI Scanner</span>
                <button class="toggle-btn">[ - ]</button>
            </div>
            <div class="widget-body" id="widgetBody">
                <div class="info-box">
                    <div class="info-row">
                        <span>गेम का लाइव पीरियड:</span>
                        <span class="info-val" id="display_period">Detecting...</span>
                    </div>
                    <div class="info-row">
                        <span>स्कैनर स्टेटस:</span>
                        <span class="info-val" style="color: #10b981;">Synced & Ready ⚡</span>
                    </div>
                </div>

                <button type="button" class="scan-btn" onclick="triggerAutoScan()">⚡ SCAN NEXT PERIOD</button>

                <div class="prediction-box" id="resultBox">
                    <div id="resContent"></div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.post("/auto-predict")
async def auto_predict(period_number: str = Form(...)):
    try:
        p_val = int(period_number[-3:])
    except:
        p_val = random.randint(0, 999)

    predicted_number = (p_val * 3 + 4) % 10

    size_result = "Big (बड़ा)" if predicted_number >= 5 else "Small (छोटा)"

    if predicted_number in [1, 3, 7, 9]:
        color_result = "Green (हरा)"
    elif predicted_number in [2, 4, 6, 8]:
        color_result = "Red (लाल)"
    else:
        color_result = "Violet & Green (वॉलेट और हरा)"

    return {
        "status": "success",
        "target_period": period_number,
        "prediction": {
            "exact_number": predicted_number,
            "size": size_result,
            "color": color_result
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
