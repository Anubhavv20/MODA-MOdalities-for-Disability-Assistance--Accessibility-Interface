# MODA-MOdalities-for-Disability-Assistance
# Accessibility Assistant 

**A multimodal accessibility interface combining voice control and real-time sign language recognition** to support users with speech or hearing impairments. Built with a focus on inclusive design, the assistant bridges communication gaps using audio and visual modalities through an intuitive GUI.

---

## 🔑 Project Highlights
- Voice command recognition and TTS (Text-to-Speech)
- Real-time sign language gesture detection using webcam
- Accessible GUI with toggle buttons and keyboard shortcuts
- Output console for feedback visibility
- Modular design for extendibility

---

## 🛠️ Technical Stack
- **Language**: Python 3.x  
- **Libraries**:
  - `speech_recognition`, `pyttsx3` – Voice recognition and synthesis  
  - `cv2`, `mediapipe`, `numpy` – Sign language gesture detection  
  - `tkinter`, `ttk` – GUI interface  
  - `pynput` – Global keyboard shortcut handling  
- **Architecture**: Modular, event-driven, multithreaded

---

## ✨ Features
- 🔊 **Voice Mode**: Start/stop listening via GUI or F1 key  
- ✋ **Sign Mode**: Recognizes signs like Hello, Yes, No, OK, Help, etc.  
- 🧠 **Smart Feedback**: Text and audio-based response to commands  
- 🖥️ **GUI Console**: Visual feedback log of interactions  

---

## 🔐 Security & Privacy
- No external data transmission; all recognition is performed locally  
- No persistent audio/video recording — only live session data is used  
- Camera access is session-based and disabled when not in use  

---

## 🎨 UI/UX Design
- Accessible fonts and contrast-friendly color palette  
- Logical grouping of functions for intuitive navigation  
- Real-time status indicators  
- Large buttons for ease of interaction  

---

## 📱 Responsive Design
- Dynamic resizing using Tkinter layout managers  
- Scrollable console for small screens  
- Keyboard shortcuts (F1 for voice, F2 for sign) for quick access  

---

## 🚀 Future Scope
- 🔤 Broader sign language dataset for alphabet/word detection  
- 🌐 NLP-based task execution (email, calendar, browsing)  
- 📱 Cross-platform mobile app with camera & mic access  
- 🧩 Plugin system for adding new modalities (eye tracking, Braille IO)  

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/accessibility-assistant.git

# Navigate into the project folder
cd accessibility-assistant

# Install required packages
pip install -r requirements.txt

# Run the assistant
python code.py
```

---

## 📬 Contact / Issues
For contributions, feature requests, or bug reports, please open an issue or reach out via GitHub.
## 🤝 Contributing
Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome.

**Let's build inclusive tech, one modality at a time.**
