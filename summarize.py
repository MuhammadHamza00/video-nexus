import google.generativeai as genai
import os
import markdown2
# json file link
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Jsonfile.json"

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

global raw_content
def get_summary(content,lang,prompt):
    global raw_content
    response = model.generate_content(f"{prompt} {content} in {lang} and also format it properly.")
    raw_content = content
    plain_text = markdown2.markdown(response.text)
    return  plain_text

def get_chat(query):
    global raw_content
    prompt = f"Respond to question: {query} in context of following transcribe {raw_content}.If it's not mention in transcribe,reply it and tell the user."
    chat = model.start_chat()
    response = chat.send_message(prompt)
    
    return response.text
