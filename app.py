# main.py
from flask import Flask, render_template
from func.screenshot import capture_screenshot
from func.llm_api import extract_question, extract_type, process_question
from flask_socketio import SocketIO
import threading
import keyboard
import pyautogui
import time
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
is_idle = True
stop_typing = False
lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected.")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected.")

def handle_alt_v():
    global is_idle
    global stop_typing
    with lock:
        if not is_idle:
            print("System busy, please wait...")
            return
        is_idle = False

    try:
        img_path = capture_screenshot()
        question = extract_question(img_path)
        if not question:
            raise ValueError("Failed to extract question.")
        question_type = extract_type(img_path)
        if not question_type:
            raise ValueError("Failed to determine question type.")
        answer = process_question(question, question_type)
        if not answer:
            raise ValueError("Failed to process question.")

        socketio.emit('update_answer', {'answer': answer})
        typing_types = ["[Open-Ended]", "[Short-Answer]", "[Fill-in-the-Blank]"]
        if question_type in typing_types:
            stop_typing = False
            type_answer(answer)
    except Exception as e:
        socketio.emit('update_answer', {'answer': f"Error: {str(e)}"})
    finally:
        with lock:
            is_idle = True

def handle_alt_2():
    stop_typing = True
    print("Typing stopped.")

def type_answer(answer):
    global stop_typing
    for char in answer:
        if stop_typing:
            print("Typing stopped.")
            break
        pyautogui.press(char)
        time.sleep(0.015)
    stop_typing = False

if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: socketio.run(app, port=5000, debug=True, use_reloader=False))
    flask_thread.start()
    keyboard.add_hotkey('alt+v', handle_alt_v)
    keyboard.add_hotkey('alt+2', handle_alt_2)
    print("Press 'Alt+V' to trigger AI Test Helper...")
    print("Press 'Alt+2' to stop typing.")