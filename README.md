# AI Test Helper

A desktop application that automatically answers test questions using AI vision and typing capabilities.

**AI Test Helper** is a desktop application that assists users in answering questions captured from screenshots. Using a hotkey (Alt+V), the application captures the screen, processes the image to extract questions, determines the type of questions, and provides answers directly on the screen. 

## Features

- **Hotkey Trigger**: Use `Alt+V` to trigger the AI processing.
- **Screenshot Capture**: Automatically captures the current screen.
- **Question Extraction**: Extracts questions from the screenshot using AI.
- **Question Type Determination**: Identifies the type of questions (e.g., Multiple-Choice, Open-Ended).
- **Answer Generation**: Uses AI to generate answers and types them directly into the active window.

## Prerequisites

- Python 3.8 or higher
- Environment variables(create .env file, add OPENAI_API_KEY=your_api_key and DEEPSEEK_API_KEY=your_api_key):   
  - `OPENAI_API_KEY`: Your OpenAI API key.
  - `DEEPSEEK_API_KEY`: Your DeepSeek API key.

## Features
- Automatic question detection from screenshots
- AI-powered answer generation using OpenAI GPT-4 and DeepSeek
- Real-time answer display in web interface
- Automatic typing for open-ended questions
- Hotkey controls (Alt+V to trigger, Alt+2 to stop typing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/newMeta98/AI_test_helper.git

cd ai-test-helper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create .env file in project root:

env

OPENAI_API_KEY="your-openai-api-key"
DEEPSEEK_API_KEY="your-deepseek-api-key"

## Usage

1. Start the application:

```bash
python app.py
```
2. Navigate to test environment where questions are displayed

3. IMPORTANT: Click on or select the input field where the answer needs to be typed

4. Press Alt+V when question is visible:

Application will capture screenshot

Process question using AI

Display answer in web interface (http://localhost:5000)

Automatically type answers for open-ended questions directly into selected field

5. Press Alt+2 to stop typing at any time if needed or let it write the answer

## Configuration
Modify these values in .env:

env

OPENAI_API_KEY=your_openai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here

## Technologies Used
OpenAI GPT-4 Vision API

DeepSeek LLM

Flask (Web Interface)

PyAutoGUI (Screen capture and typing)

Socket.IO (Real-time updates)

## Notes

**Critical**: Always select the answer input field before pressing Alt+V

Keep the question window active during processing

Works best with clear text-based questions

Typing speed is optimized for most test platforms

Ensure proper API permissions and quotas

## Project Structure
func/

screenshot.py: Handles screenshot capture.

llm_api.py: Manages interactions with OpenAI and DeepSeek APIs.

static/

style.css: Styles for the web interface.

templates/

index.html: Frontend for displaying answers.

app.py: The main application file using Flask and SocketIO, type_answer: Types the generated answers on the screen.

.gitignore: Specifies ignored files for version control.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
MIT License
