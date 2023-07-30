from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

checkpoint = "LaMini-Flan-T5-248M"
model = pipeline('summarization', model=checkpoint)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        instructions = request.form['instructions']
        abstractive = request.form.get('abstractive') == 'on'

        # Count the number of words in the input_text
        num_words_input = len(input_text.split())

        # Generate the summary using the model with additional parameters
        input_prompt = input_text + " " + instructions
        if abstractive:
            output = model(input_prompt, do_sample=True)[0]['summary_text']
        else:
            output = model(input_prompt, do_sample=False)[0]['summary_text']

        return render_template('index.html', input_text=input_text, instructions=instructions, summary=output, num_words_input=num_words_input, abstractive=abstractive)

    return render_template('index.html', input_text='', instructions='', summary='', num_words_input=0, abstractive=False)


if __name__ == '__main__':
    app.run(debug=True)
