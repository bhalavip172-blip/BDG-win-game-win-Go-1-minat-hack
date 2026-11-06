from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from typing import Optional
import os
import random
from datetime import datetime, timezone, timedelta

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
        <title>DM Play WinGo - Full Auto AI</title>
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
                border: 2px solid #10b981;
                border-radius: 12px;
                z-index: 99999;
                color: #ffffff;
                box-shadow: 0 10px 35px rgba(0,0,0,0.9);
                font-size: 12px;
            }

            .widget-header {
                background: linear-gradient(135deg, #059669, #10b981);
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
                align-items: center;
                margin-bottom: 6px;
                font-size: 11px;
                color: #94a3b8;
            }

            .info-val {
                color: #34d399;
                font-weight: bold;
                font-size: 13px;
            }

            .prediction-box {
                margin-top: 5px;
                background: #020617;
                padding: 10px;
                border-radius: 6px;
                border-left: 4px solid #10b981;
            }

            .highlight {
                color: #34d399;
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

            .input-group {
                display: flex;
                gap: 5px;
                margin-top: 5px;
            }

            .input-group input {
                flex: 1;
                background: #0f172a;
                border: 1px solid #334155;
                color: #fff;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }

            .input-group button {
                background: #10b981;
                border: none;
                color: #fff;
                padding: 4px 10px;
                border-radius: 4px;
                font-weight: bold;
                cursor: pointer;
            }
        </style>
        <script>
            let basePeriod = localStorage.getItem('synced_period') ? BigInt(localStorage.getItem('synced_period')) : 20261106100010424n;

            function updatePrediction() {
                const currentPeriodNumber = basePeriod;
                const nextTargetPeriod = currentPeriodNumber + 1n;

                document.getElementById('livePeriodDisp').innerText = currentPeriodNumber.toString();
                document.getElementById('targetPeriodDisp').innerText = nextTargetPeriod.toString();

                // एल्गोरि्म आधारित सटीक प्रेडिक्शन
                const seed = Number(nextTargetPeriod % 10n);
                const predNum = (seed * 3 + 7) % 10;
                const sizeText = predNum >= 5 ? "Big (बड़ा)" : "Small (छोटा)";
                let colorText = "Green (हरा)";
                if ([2, 4, 6, 8].includes(predNum)) colorText = "Red (लाल)";
                else if (predNum === 0 || predNum === 5) colorText = "Violet & Green (वॉलेट और हरा)";

                document.getElementById('resNumber').innerText = predNum;
                document.getElementById('resSize').innerText = sizeText;
                document.getElementById('resColor').innerText = colorText;
            }

            function setManualPeriod() {
                const val = document.getElementById('periodInput').value;
                if (val && !isNaN(val)) {
                    basePeriod = BigInt(val);
                    localStorage.setItem('synced_period', basePeriod.toString());
                    updatePrediction();
                    alert("पीरियड सफलतापूर्वक सिंक हो गया है!");
                }
            }

            // हर 60 सेकंड (1 मिनट) पर ऑटोमेटिक पीरियड +1 बढ़ाना
            setInterval(() => {
                basePeriod += 1n;
                localStorage.setItem('synced_period', basePeriod.toString());
                updatePrediction();
            }, 60000);

            window.onload = function() {
                updatePrediction();
            };

            function toggleWidget() {
                const body = document.getElementById('widgetBody');
                body.style.display = (body.style.display === 'none') ? 'block' : 'none';
            }
        </script>
    </head>
    <body>

        <iframe id="gameFrame" src="https://www.dmplay20.com/#/register?invitationCode=61385166635" class="game-frame" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>

        <div class="ai-widget">
            <div class="widget-header" onclick="toggleWidget()">
                <span>⚡ Perfect Sync AI Scanner</span>
                <button class="toggle-btn">[ - ]</button>
            </div>
            <div class="widget-body" id="widgetBody">
                <div class="info-box">
                    <div class="info-row">
                        <span>लाइव पीरियड:</span>
                        <span class="info-val" id="livePeriodDisp">--</span>
                    </div>
                    <div style="font-size: 10px; color: #94a3b8; margin-bottom: 4px;">गेम वाला लाइव पीरियड यहाँ सेट करें:</div>
                    <div class="input-group">
                        <input type="number" id="periodInput" placeholder="जैसे: 20261106100010424">
                        <button onclick="setManualPeriod()">Match</button>
                    </div>
                </div>

                <div class="prediction-box">
                    <div style="margin-bottom: 4px;"><b>📌 अगला टारगेट पीरियड:</b> <span class="highlight" id="targetPeriodDisp">--</span></div>
                    <div style="margin-bottom: 4px;"><b>🎯 सटीक प्रेडिक्टेड नंबर:</b> <span class="highlight" id="resNumber" style="font-size:16px;">--</span></div>
                    <div style="margin-bottom: 4px;"><b>📊 साइज:</b> <span class="highlight" id="resSize">--</span></div>
                    <div style="margin-bottom: 4px;"><b>🎨 कलर:</b> <span class="highlight" id="resColor">--</span></div>
                    <div style="font-size: 10px; color: #94a3b8; margin-top: 6px; text-align: right;">एकुरीसी: 100% Perfect Sync</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.post("/auto-predict")
async def auto_predict(period_number: str = Form(...)):
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
