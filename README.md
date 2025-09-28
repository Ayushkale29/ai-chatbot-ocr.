# ai-chatbot-ocr

AI-powered chatbot integrated with OCR (Optical Character Recognition).  
Chat with the bot or upload images to extract and process text automatically.

---

## Features
- Real-time AI chatbot responses  
- OCR support to extract text from images  
- Multi-language OCR support (via EasyOCR)  
- User-friendly web interface built with Streamlit  
- Simple setup and easy to extend

---

## Demo / Screenshots

**1. Chatbot Interface:**  
![Chatbot Screenshot](assets/chatbot_screenshot.png)

**2. OCR Text Extraction:**  
![OCR Screenshot](assets/ocr_screenshot.png)

**3. Combined Chat + OCR:**  
![Combined Screenshot](assets/combined_screenshot.png)

> Replace `assets/*.png` with your actual screenshots in your repository.
---
## Installation

1. Clone the repository:
```
git clone https://github.com/Ayushkale29/ai-chatbot-ocr.git
cd ai-chatbot-ocr
```
2.Install required Libraries
```
pip install -r requirements.txt
```
3.Run the STreamlit app
```
streamlit run ai_chatbot_ocr.py
```
## Usage

1. Open the Streamlit app in your browser  
2. Chat with the AI bot in the input box  
3. Upload an image to extract text using OCR  
4. The bot will respond based on the uploaded text or your query
   ## Dependencies
- `streamlit` – Web interface  
- `easyocr` – OCR engine  
- `Pillow` / `opencv-python` – Image processing  
- `requests` – API calls (if used for AI backend)

## Folder Structure
```
ai-chatbot-ocr/
│
├─ app.py # Main Streamlit app
├─ requirements.txt # Python dependencies
├─ README.md
├─ assets/ # Images/screenshots
└─ modules/ # Optional: separate code modules
```
## Future Enhancements
- Multi-language support for chatbot responses  
- Support for PDF and scanned documents  
- Integration with more advanced AI models like GPT-4 or Ollama  
- Real-time OCR for live camera input
  
  ## How It Works (Technical Overview)
1. **Chatbot:** Sends user queries to an AI model and returns responses  
2. **OCR Module:** Uses EasyOCR to detect and extract text from images  
3. **Integration:** Extracted text can be used as input for the chatbot  
4. **Streamlit UI:** Combines chatbot and OCR into a single interactive interface


