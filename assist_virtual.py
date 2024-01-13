import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import requests
import pyttsx3
from datetime import datetime

# Passo 1: Configuração do Ambiente de Desenvolvimento
recognizer = sr.Recognizer()

# Passo 2: Capturando Comandos de Voz
def capture_audio():
    with sr.Microphone() as source:
        print("Diga algo:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
    return audio

def recognize_speech(audio):
    try:
        print("Reconhecendo...")
        text = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {text}")
        return text
    except sr.UnknownValueError:
        print("Não foi possível entender a fala.")
        return ""
    except sr.RequestError as e:
        print(f"Erro na requisição para o serviço de reconhecimento de fala: {e}")
        return ""

# Passo 3: Implementando a Inteligência Artificial
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def respond_to_query(query):
    processed_query = preprocess_text(query)
    
    # Adaptação à Hora do Dia
    response = adapt_to_time_of_day()

    # Adicione mais lógica conforme necessário

    speak(response)
    return response

# Passo 4: Adicionando Recursos Interativos
def web_search(query):
    search_url = f"https://www.exemplo.com/pesquisa?q={query}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao realizar a consulta à web: {e}")
        return None

# Passo 5: Interface de Voz com pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Passo 6: Testando Seu Assistente Virtual
audio_data = capture_audio()
text = recognize_speech(audio_data)
respond_to_query(text)

# Passo 7: Toques Pessoais e Personalização
def adapt_to_time_of_day():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return "Bom dia!"
    elif 12 <= current_hour < 18:
        return "Boa tarde!"
    else:
        return "Boa noite!"

# Execute mais testes, ajuste e expanda conforme necessário
