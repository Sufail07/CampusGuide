import random
import json
import torch
import speech_recognition as sr

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('dataset2.JSON', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data4.pth"
data = torch.load(FILE, weights_only=True)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Academia"

def get_text_from_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        print("Processing audio...")
        text = recognizer.recognize_google(audio)
        print(f"Text from speech: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        return None


def get_response(msg):
    # Preprocess input
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = torch.from_numpy(X).unsqueeze(0).to(device)  # Combine reshape and tensor creation
    
    # Model inference
    model.eval()
    with torch.no_grad():
        output = model(X)
    
    # Get prediction and confidence
    _, predicted = torch.max(output, dim=1)
    prob = torch.softmax(output, dim=1)[0][predicted.item()]
    
    #print(f"Predicted probability: {prob.item()}")  # Add this line to inspect confidence
    
    if prob.item() > 0.99999:
        tag = tags[predicted.item()]
        # Use a dictionary for faster lookups
        intent_dict = {intent["tag"]: intent for intent in intents["intents"]}
        if tag in intent_dict:
            return random.choice(intent_dict[tag]['responses'])
    else:
        return "I do not understand"

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # Use speech-to-text
        audio_text = get_text_from_speech()

        if audio_text:
            print(f"You (speech): {audio_text}")
            response = get_response(audio_text)
            print(f"Bot: {response}")

        # Alternatively, you can uncomment the lines below to allow text input
            sentence = input("You: ")
            if sentence.lower() == "quit":
                break
            response = get_response(sentence)
            print(f"Bot: {response}")
