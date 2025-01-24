import base64
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_openai_response(image_path, system_message):
    """Get response from OpenAI API using the provided image and system message."""
    base64_image = encode_image(image_path)
    if not base64_image:
        return None

    api_key = os.getenv('OPENAI_API_KEY')
    model = "gpt-4o"  # Updated to the correct model for vision tasks
    client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_message
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ]

    try:
        chat_response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=400,
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_question(image_path):
    system_message = ("You are a helpful assistant that will look at the image and find questions. They can be in test/quiz form or conversational. "
                      "Output: [1.unedited_question+options(if provided),2.unedited_question+options(if provided),3.unedited_question+options(if provided),....]. "
                      "OUTPUT ONLY QUESTION+OPTIONS(IF PROVIDED) YOU GOT FROM THE IMAGE, DON'T EDIT THE QUESTION OR OPTIONS.")
    question = get_openai_response(image_path, system_message)
    return question

def extract_type(image_path):
    """Extract question types from the image."""
    system_message = ("You are a helpful assistant that will look at the image and break-down question:$question_type[what type of question it is?-"
                      "Multiple-Choice Questions (MCQs):These questions provide several answer options, and the respondent must choose the correct or most appropriate one. "
                      "Example: 'What is the capital of France? A) London B) Paris C) Madrid D) Rome' -Open-Ended Questions:These questions require a detailed response and allow the respondent to express their thoughts, opinions, or explanations in their own words. "
                      "Example: 'Describe the process of photosynthesis in plants.' -Short-Answer Questions: These questions require a brief, specific response, usually just a few words or a short phrase.Example: 'What is the capital of France?' (Answer: 'Paris') -"
                      "True/False Questions: These questions present a statement, and the respondent must determine whether it is true or false. Example: 'True or False: The capital of France is Paris.'-"
                      "Matching Questions: These questions provide two sets of items, and the respondent must match items from one set with items from the other set. Example: Match the capital with its country: A) Paris B) London C) Madrid D) Rome With: France United Kingdom Spain Italy -"
                      "Fill-in-the-Blank Questions: These questions present a statement with one or more blanks, and the respondent must fill in the missing word(s). Example: 'The capital of France is __________.']. "
                      "Output: [question_type](example:[Open-Ended],[Multiple-Choice]). OUTPUT ONLY [question_type] YOU GOT FROM THE IMAGE")
    question_type = get_openai_response(image_path, system_message)
    print(question_type)
    return question_type

def process_question(question, question_type):
    """Process the question and question type to get answers using DeepSeek API."""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    model = "deepseek-chat"

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    messages = [
        {
            "role": "system",
            "content": ("You are a helpful assistant"
                        "YOU will look at the questions and question_type then answer accordingly."
                        "return answer, answer2, answer3,..."
                        "return ONLY answer OR ANSWERS IF PROVIDED MULTIPLE QUESTIONS. NEVER return answer: answer! DO NOT return answer: answer!"
                        "NEVER return answer: answer! DO NOT return answer: answer!"
                        "return ONLY answer OR ANSWERS IF PROVIDED MULTIPLE QUESTIONS."
                        "return answer."
                        "## Style guideline:Avoid overused buzzwords (like ‘leverage,’ ‘harness,’ ‘elevate,’ ‘ignite,’ ‘empower,’ ‘cutting-edge,’ ‘unleash,’ ‘revolutionize,’ ‘innovate,’ ‘dynamic,’ ‘transformative power’), filler phrases (such as ‘in conclusion,’ ‘it’s important to note,’ ‘as previously mentioned,’ ‘ultimately,’ ‘to summarize,’ ‘what’s more,’ ‘now,’ ‘until recently’), clichés (like ‘game changer,’ ‘push the boundaries,’ ‘the possibilities are endless,’ ‘only time will tell,’ ‘mind-boggling figure,’ ‘breaking barriers,’ ‘unlock the potential,’ ‘remarkable breakthrough’), and flowery language (including ‘tapestry,’ ‘whispering,’ ‘labyrinth,’ ‘oasis,’ ‘metamorphosis,’ ‘enigma,’ ‘gossamer,’ ‘treasure trove,’ ‘labyrinthine’). Also, limit the use of redundant connectives and fillers like ‘moreover,’ ‘furthermore,’ ‘additionally,’ ‘however,’ ‘therefore,’ ‘consequently,’ ‘importantly,’ ‘notably,’ ‘as well as,’ ‘despite,’ ‘essentially,’ and avoid starting sentences with phrases like ‘Firstly,’ ‘Moreover,’ ‘In today’s digital era,’ ‘In the world of’. Focus on delivering the information in a concise and natural tone without unnecessary embellishments, jargon, or redundant phrases. Sound like human"
                        ),
        },
        {
            "role": "user",
            "content": f"{question},{question_type}",
        },
    ]

    try:
        chat_response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print(chat_response.choices[0].message.content)
        return chat_response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None
