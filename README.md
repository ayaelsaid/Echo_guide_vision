🌟 **Echo Guide Vision: AI Powered by Gemma**
     *Your Second Eye — One That Never Leaves You*

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F27972555%2F89e7b0c157a238bc6e4c70f5d33175e3%2Fecho_logo.jpg?generation=1754499607749038&alt=media)

Echo Guide Vision leverages **Gemma’s on-device multimodal capabilities** to combine speech input, visual analysis, and contextual AI answers. Models are dynamically selected and downloaded based on user language, optimizing performance while preserving device storage — a practical application of Gemma’s "mix-and-match" and lightweight deployment strengths.

This assistant helps visually impaired users identify objects, recognize faces, and understand their surroundings in real time.


---------------------------------------------------------------------------------------------------------------------
 🌟**Inspiration**

After the Ramsis Central fire, many people lost access to smart assistants and GPS tools. For blind individuals, this meant losing autonomy. Echo Guide Vision was built to answer one deep question:
How do you navigate the world when the digital world disappears?
--------------------------------------------------------------------------------------------------------------------------------------------------

🌍 **Global Need**

- 2.2 billion people worldwide live with visual impairments (WHO)

- 43 million are blind; 295 million have severe distance vision issues (Vision Center)

- In Egypt, ~1.8 million blind, and 8.3 million have some form of vision loss

- In the UK, sight loss affects 2+ million, expected to double by 2050

- In the USA, 12 million adults have vision impairments; 1.3 million are legally blind


---------------------------------------------------------------------------------------------------------------------------------------------------


### 🌟**Why Offline Matters**

Echo Guide Vision works 100% offline to ensure:

✅ Continuous Accessibility: Works anytime, anywhere — even without Wi-Fi or mobile data.

✅ Total Privacy: No data leaves the phone. All processing happens on-device.

✅ Reliable Safety: Responses are instant — no lag, no disconnection, no risk.

*Even in a quiet village with no signal, a blind person can point their camera at a sign — and instantly*

-------------------------------------------------------------------------------------------------------------------------------------------

###🎙️ **How It Works — One Button. Total Control.**

---

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F27972555%2F484f157c90b3ca7f6f2819905fb39638%2FScreenshot%202025-08-06%20182442.png?generation=1754499734705464&alt=media)


With one simple tap, users can interact with the app:

🎤 Speak a question

📸 App takes a photo of the scene

🧠 AI analyzes it using Gemma (on-device)

🔊 App speaks the answer clearly back

-----------------------------------------------------------------------------------------------------------------------------------


###🧠 **What Echo Guide Can Do**

| ---------------------------------   -----------------------------------------                                           
|  🖼️ Scene Understanding: Describes surroundings, people, objects 
|-----------------------------------------------------------------------------
|  💊 Text Reading: Reads prescriptions, bills, labels 
|----------------------------------------------------------------------------
|  🚧 Obstacle Detection: Detects stairs, paths, and barriers      
|----------------------------------------------------------------------------
|  👕 Clothing & Color Support: Helps choose clothes, identifies colors
|----------------------------------------------------------------------------
|  🚦Traffic Signal Awareness: Detects red/green pedestrian lights 
|----------------------------------------------------------------------------
|  💰 Currency + Math: Identifies currency, counts totals                     


----------------------------------------------------------------------------------------------------------------------------------

###🧪 **Tech Stack**

✅ **Backend**:

`Python`, `Flask`, `Flask-Cors`, `Peewee (SQLite)`

`OpenCV` – camera image capture

`Vosk` – speech-to-text

`pyttsx3` – text-to-speech

`sounddevice`, `ssimpleaudio` – voice input/output

`transformers==4.53.2` – Gemma 3n AI

`torch`, `timm`, `accelerate`, `Pillow`

---

✅ **Frontend**:
`HTML`, `CSS`, `JavaScript`

---

✅ **Architecture Overview**:
`controllers/`, `routes/`, `models/`, `camera/`, `audio_processing/`, `ai_integration/`, `utils/`, `templates/`, `static/`,` app.py`, `factory_app.py`, `config.py`, `.gitignore` - for large folder (gemma model, vosk model) uploaded it inside github without problem

-------------------------------------------------------------------------------------------------------------------------------------

###💪 **Challenges Faced**

🚀 First time working with AI & transformers

🕐 Time pressure — only 7 days to build from scratch

🧩 Faced Gemma model issues — solved by pinning `transformers==4.53.2`

⚙️ Created a dynamic model loader for different languages to save space

💻 Faced GPU issues on Kaggle — had to switch and customize setup

🎯 Almost every tech in this app — was first-time experience for me

---------------------------------------------------------------------------------------------------------------------------
###🔥 **Future Improvements**

📱 Add weather and SMS reading

🆘 Add Bluetooth SOS message + emergency call features

🤖 Add robot integration to recognize and pick colors

💬 Use Flutter for better cross-platform UI

🧠 Fine-tune Gemma 3n to understand more cases:

                   - Recognize dangers (e.g. gas leaks)

                   - Read bills more specifically (doctor names, medicines)

                   - Translate text to user's preferred language

                   - Handle local currencies for calculations 

---------------------------------------------------------------------------------------------
⚙️ **Setup Instruction**

# Clone repository
git clone https://github.com/ayaelsaid/Echo_guide_vision


# Create virtual environment
python -m venv venv

source venv/bin/activate  # or venv\Scripts\activate on Windows

# download Gemma 3n model i use her Gemma 3n E2B(i put them nside .gitignore to can push project to github )

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py



