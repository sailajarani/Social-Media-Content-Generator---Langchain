# Social Media Content Generator

This project helps you automatically create social media content for LinkedIn and Instagram based on any topic you choose. It researches the topic, writes a LinkedIn post, creates an Instagram reel script, and merges both into a single, easy-to-use output.

## How It Works

1. **Setup**
   - The script loads your API keys and model names from a `.env` file for secure access to external services.

2. **Research**
   - Searches the web for the latest information and trends about your topic.
   - Summarizes the findings in clear, simple language.

3. **LinkedIn Post Creation**
   - Uses the research summary to write a professional LinkedIn post.
   - The post includes a catchy hook, bullet points, actionable advice, a question for engagement, emojis, and hashtags.

4. **Instagram Reel Script Creation**
   - Uses the same research summary to write a script for an Instagram reel.
   - The script is fast-paced, attention-grabbing, and includes visual cues and a call to action.

5. **Merging**
   - Combines the LinkedIn post and Instagram reel script into one formatted output.
   - Clearly labels each section for easy posting.

## How to Use

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Add your API keys and model names to a `.env` file.**

3. **Run the script:**
   ```
   python langgraph_app.py
   ```

4. **Enter your topic.**
   - The script will print the LinkedIn post and Instagram reel script in the console.

## File Overview

- `langgraph_app.py`: Main script with all logic for research, content creation, and merging.
- `.env`: Stores your API keys and model names (not included in version control).
- `README.md`: This guide.

## Notes

- You do not need to know anything about AI or technical jargon to use this project.
- Just provide a topic, and the script does the rest.
- The output is ready to copy and post on