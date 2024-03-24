from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
import assemblyai as aai
from summarize import get_summary,get_chat
import os

app = Flask(__name__)

aai.settings.api_key = "92f5c6e52a224fe99d0b9b6a4c2d297e"

UPLOAD_FOLDER = 'E:\\Hackathons\\gemini\\Files'

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'avi'}  # Specify allowed file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_and_transcribe():

    # default
    if request.method == 'GET':
        return render_template('form.html', transcript_text=None)
    # query form submission
    if 'file' in request.files or 'linkInput' in request.form:
        file = request.files.get('file')
        link = request.form.get('linkInput')
        lang = request.form.get('lang')
        task = request.form.get('task')

        # prompt selection
        prompt = ''
        if task == 'summary':
            prompt = "Summarize the following transcribe:"
        elif task == 'minutes':
            prompt = "Return the minutes from meeting's transcribe:"
        elif task == 'translation':
            prompt = "Translate the following content:"
        elif task == 'transcript':
            prompt = "Create transcript from the following transcribe of video:"
        else:
            prompt = "Try again nothing is provided"

        if not lang:
            lang = 'English'
        if not file and not link:
            error = 'Please provide either filename or link.'
            return render_template('form.html', transcript_text=None, error=error)
        
        if file:
            if not allowed_file(file.filename):
                error = 'File type not allowed'
                return render_template('form.html', transcript_text=None, error=error)
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            transcriber = aai.Transcriber()         
            transcript = transcriber.transcribe(filepath)
          
        elif link:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(link)
        # get transcript
        if transcript:
            output = get_summary(transcript.text,lang,prompt)
            return render_template('form.html', transcript_text=output,raw_transcribe = transcript.text)
        else:
            error = 'No transcript available.'
            return render_template('form.html', transcript_text=None, error=error)
    # chatting form
    else:
        # Handle form submission from the JavaScript code
        data = request.get_json()
        query = data.get('query')
        # Process the query and get the response from the model
        response = get_chat(query)
        # Return the response as JSON
        return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
