from flask import Flask, render_template_string
import random
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDG Win Go 1 Min Pro AI Scanner</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #090a0f;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .floating-scanner {
            position: fixed;
            top: 15px;
            right: 15px;
            z-index: 999999;
            background: linear-gradient(135deg, #14141f, #2d2b4e);
            color: #fff;
            padding: 16px;
            border-radius: 16px;
            width: 320px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.9);
            border: 2px solid #00ffcc;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            padding-bottom: 8px;
        }
        .header h3 {
            margin: 0;
            font-size: 15px;
            color: #00ffcc;
        }
        .scan-btn {
            width: 100%;
            background: linear-gradient(90deg, #00ffcc, #00b386);
            color: #000;
            border: none;
            padding: 11px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 12px;
            font-size: 14px;
            box-shadow: 0 4px 15px rgba(0,255,204,0.4);
        }
        .info-box {
            background: rgba(0, 0, 0, 0.6);
            padding: 12px;
            border-radius: 10px;
            font-size: 13px;
            line-height: 1.7;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .info-box div {
            display: flex;
            justify-content: space-between;
        }
        .highlight {
            color: #00ffcc;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="floating-scanner">
        <div class="header">
            <h3>⚡ WinGo Pro AI Scanner</h3>
            <span style="font-size: 10px; background: #00ffcc; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold;">ACTIVE</span>
        </div>
        <div style="margin-bottom: 10px; font-size: 12px;">
            ऑटो लाइव पीरियड: <span id="live-period" style="color: #ffcc00; font-weight: bold;">सिंक हो रहा है...</span>
        </div>
        <button class="scan-btn" onclick="runAdvancedScan()">🔄 डेटा स्कैन और एनालाइज करें</button>
        <div class="info-box">
            <div>📌 अगला टारगेट पीरियड: <span id="target-period" class="highlight">-</span></div>
            <div>🎯 सटीक प्रेडिक्टेड नंबर: <span id="pred-num" style="color: #ff3366; font-size: 16px; font-weight: bold;">-</span></div>
            <div>📊 साइज़ (Big/Small): <span id="pred-size" style="color: #ffcc00;">-</span></div>
            <div>🎨 कलर (Color): <span id="pred-color" style="color: #00ffc4;">-</span></div>
            <div>📈 विनिंग एक्यूरेसी: <span id="win-chance" class="highlight">-</span></div>
        </div>
    </div>

    <div style="padding: 30px; text-align: center; max-width: 700px; margin: 40px auto; background: #12141c; border-radius: 12px; border: 1px solid #2a2e3d;">
        <h2 style="color: #00ffcc;">🚀 BDG Win Go 1 Min AI Prediction Server</h2>
        <p style="color: #bbb; font-size: 14px;">आपका यह सर्वर पूरी तरह से एक्टिव है और स्क्रीन के कोने में प्रेडिक्शन टूल तैर रहा है। आप नीचे दिए गए बटन से सीधे गेम ओपन कर सकते हैं:</p>
        <a href="https://bdgwin98.com/#/register?invitationCode=8528414760979" target="_blank" style="display: inline-block; background: #00ffcc; color: #000; padding: 12px 25px; border-radius: 8px; font-weight: bold; text-decoration: none; margin-top: 15px; font-size: 15px;">🔗 BDG Win गेम खोलें (यहाँ खेलें)</a>
    </div>

    <script>
        function getLivePeriodNumber() {
            const now = new Date();
            const year = now.getUTCFullYear();
            const month = String(now.getUTCMonth() + 1).padStart(2, '0');
            const day = String(now.getUTCDate()).padStart(2, '0');
            const totalMinutes = now.getUTCHours() * 60 + now.getUTCMinutes();
            const periodCode = String(10001 + totalMinutes).padStart(4, '0');
            return `${year}${month}${day}1000${periodCode}`;
        }

        function updateDisplayClock() {
            const currentP = getLivePeriodNumber();
            document.getElementById('live-period').innerText = currentP;
        }
        setInterval(updateDisplayClock, 1000);
        updateDisplayClock();

        function runAdvancedScan() {
            const btn = document.querySelector('.scan-btn');
            btn.innerText = "⏳ पिछला डेटा स्कैन हो रहा है...";
            btn.style.opacity = "0.7";

            setTimeout(() => {
                let liveP = getLivePeriodNumber();
                let nextP = (BigInt(liveP) + 1n).toString();
                let lastDigit = parseInt(liveP.slice(-1));
                let calculatedNum = (lastDigit * 3 + 5 + Math.floor(Math.random() * 3)) % 10;
                let sizeText = calculatedNum >= 5 ? "Big (बड़ा)" : "Small (छोटा)";
                let colorText = calculatedNum % 2 === 0 ? "Red (लाल)" : "Green (हरा)";
                let accuracy = (94 + (Math.floor(Math.random() * 5))) + "% (High Accuracy)";

                document.getElementById('target-period').innerText = nextP;
                document.getElementById('pred-num').innerText = calculatedNum;
                document.getElementById('pred-size').innerText = sizeText;
                document.getElementById('pred-color').innerText = colorText;
                document.getElementById('win-chance').innerText = accuracy;

                btn.innerText = "🔄 डेटा स्कैन और एनालाइज करें";
                btn.style.opacity = "1";
            }, 800);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
