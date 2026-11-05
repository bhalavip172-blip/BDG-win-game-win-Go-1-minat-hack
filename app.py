import streamlit as st
import requests

st.set_page_config(page_title="Wingo Live Analyzer App", page_icon="🎯", layout="centered")

st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎯 Wingo Live Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>लाइव सर्वर से जुड़ा हुआ 24/7 ऑटोमैटिक प्रेडिक्शन सिस्टम</p>", unsafe_allow_html=True)

st.write("---")

if st.button("🔍 लाइव डेटा स्कैन और प्रेडिक्ट करें", use_container_width=True):
    server_url = "https://bdg-win-game-win-go-1-minat-hack-1.onrender.com/live-analysis/"
    
    try:
        res = requests.get(server_url)
        if res.status_code == 200:
            data = res.json()
            st.success("✅ सर्वर से सफलतापूर्वक कनेक्ट और स्कैन हो गया!")
            
            latest_period = data.get("prediction_result", {}).get("period", "Auto-1 Min")
            st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
                    <h3 style='margin: 0; color: #333;'>📡 अगला लाइव पीरियड नंबर</h3>
                    <h2 style='margin: 5px 0 0 0; color: #1f77b4;'>{latest_period}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            pred = data.get("prediction_result", {})
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; text-align: center;'>
                        <p style='margin: 0; font-weight: bold; color: #2e7d32;'>रंग (Color)</p>
                        <h3 style='margin: 5px 0 0 0; color: #2e7d32;'>{pred.get("predicted_color")}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                    <div style='background-color: #e3f2fd; padding: 15px; border-radius: 10px; text-align: center;'>
                        <p style='margin: 0; font-weight: bold; color: #1565c0;'>साइज़ (Size)</p>
                        <h3 style='margin: 5px 0 0 0; color: #1565c0;'>{pred.get("predicted_size")}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                    <div style='background-color: #fff3e0; padding: 15px; border-radius: 10px; text-align: center;'>
                        <p style='margin: 0; font-weight: bold; color: #ef6c00;'>विनिंग नंबर</p>
                        <h3 style='margin: 5px 0 0 0; color: #ef6c00;'>{pred.get("predicted_number")}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
            st.write("")
            st.info(f"📊 **सटीकता (Confidence):** {pred.get('confidence')}")
            
        else:
            st.error("❌ सर्वर से डेटा प्राप्त करने में त्रुटि हुई।")
    except Exception as e:
        st.error(f"⚠️ कनेक्शन एरर: {e}")
