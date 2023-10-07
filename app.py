from flask import Flask, request, jsonify, render_template
from openai_gpt import create_dalle_images
from openai_gpt import generate_comic_book
from stability_ai import create_stability_images
import os
import re

app = Flask(__name__)

IMAGE_PROVIDER = os.environ.get('IMAGE_PROVIDER', 'OpenAI')  # Default to OpenAI

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

def regroup_panels(split_output):
    grouped_panels = []
    temp_panel = {}

    for element in split_output:
        if "PAINEL" in element:
            if temp_panel:  # if temp_panel is not empty
                grouped_panels.append(temp_panel)
            temp_panel = {'title': element}
        elif "NARRAÇÃO:" in element:
            temp_panel['narration'] = element
        elif "DESCRIÇÃO DE IMAGEM:" in element:
            temp_panel['image_description'] = element

    if temp_panel:  # For the last panel
        grouped_panels.append(temp_panel)

    return grouped_panels  
  
@app.route('/generate_comic_output', methods=['POST'])
def generate_comic_output():
    data = request.json
    synopsis = data.get('synopsis')
    comic_output = generate_comic_book(synopsis)
    # Use regex to split by two or more newlines
    split_output = re.split(r'\n\s*\n', comic_output)
    grouped_panels = regroup_panels(split_output)    
    #print(grouped_panels)
    return jsonify({'comic_output': grouped_panels})  
  
@app.route('/generate_single_comic_panel', methods=['POST'])
def generate_single_comic_panel():
    panel_text = request.json.get('panel_text')
    #print(panel_text)
    panel_data = parse_narration_and_images(panel_text)
    #print(panel_data)
    panels = create_panels(panel_data)
    #print(panels)
    return jsonify({'comic_panel': panels[0]})  # Return the first panel as we are sending one at a time  
  
def create_panels(panels_data):
    for panel in panels_data:
        if IMAGE_PROVIDER == 'OpenAI':
            image_url = create_dalle_images(panel['image_description'])
        else:
            image_url = create_stability_images(panel['image_description'])
        panel['image_url'] = image_url
    return panels_data
  
def parse_narration_and_images(panel_data):
    narration = panel_data.get('narration', '').replace("NARRAÇÃO:", "").strip()
    image_description = panel_data.get('image_description', '').replace("DESCRIÇÃO DE IMAGEM:", "").strip()
    if narration and image_description:
        return [{'narration': narration, 'image_description': image_description + ' Cartoon.'}]
    else:
        return []

  
if __name__ == '__main__':
    app.run(debug=True)
