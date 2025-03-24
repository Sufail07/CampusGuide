# CampusGuide

A conversational AI assistant for KMCT College of Engineering students that provides campus information and helps students access their academic data.

## Overview

CampusGuide is an intelligent chatbot designed to assist students at KMCT College of Engineering with campus-related queries. The system uses Natural Language Processing to understand student questions and provides information about college facilities, courses, events, and more. It can also fetch personalized academic data including attendance records, assignment details, and internal marks when provided with valid student credentials.

## Features

- **Campus Information**: Get details about college facilities, departments, courses, fees, and more
- **Academic Support**: Information about placements, scholarships, academic calendar, and exams
- **Event Details**: Learn about college festivals, sports events, and other activities
- **Personal Academic Data**: Retrieve student-specific attendance records, assignment details, and internal marks
- **Multi-Modal Interaction**: Support for both text and speech input

## Technology Stack

- **Backend**: Flask
- **Natural Language Processing**: PyTorch for intent classification
- **Speech Recognition**: SpeechRecognition library
- **Web Scraping**: Selenium for retrieving student data
- **Fallback Model**: Gemini AI for handling out-of-scope queries

## Project Structure

```
CampusGuide/
├── app.py                 # Main Flask application
├── chat.py                # Chatbot logic and speech processing
├── model.py               # Neural network model definition
├── nltk_utils.py          # Text processing utilities
├── train.py               # Model training script
├── scrape.py              # Web scraper for academic data
├── dataset2.json          # Training data with intents and responses
├── data4.pth              # Trained model weights
├── requirements.txt       # Project dependencies
└── templates/             # HTML templates for the web interface
    └── website2.html
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sufail07/CampusGuide.git
   cd CampusGuide
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup your Gemini API key in a `.env` file:
   ```
   gemini=YOUR_GEMINI_API_KEY
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Access the application in your browser at `http://localhost:5000`

## Usage

1. **General Queries**: Ask questions about college facilities, courses, events, etc.
   ```
   "What courses are offered at KMCT?"
   "Tell me about the hostel facilities"
   "When is the annual tech fest?"
   ```

2. **Academic Data Retrieval**: To access personal academic data
   ```
   "Show me my attendance"
   ```
   Then provide your username and password when prompted in the format: `studentID, password`

## Training the Model

If you want to enhance the model with additional data:

1. Add new intents, patterns, and responses to `dataset2.json`
2. Run the training script:
   ```bash
   python train.py
   ```
3. The updated model will be saved as `data4.pth`
