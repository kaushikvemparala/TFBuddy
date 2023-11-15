from werkzeug.utils import secure_filename
from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
import shutil
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../uploads')
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.isdir(app.config['UPLOAD_FOLDER']):
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
        os.makedirs(app.config['UPLOAD_FOLDER'])
        file.save(filename)
        file_path = os.path.join('uploads', filename)
        scalars = openFile(UPLOAD_FOLDER)
        print(scalars)
        # Here you can save the file to your database
        return {'res': scalars, 'path': file_path}

@app.route('/plot', methods=['POST'])
@cross_origin()
def plot_scalars():
    scalars = request.get_json()["text"].split(", ")
    data = getTFEvent(UPLOAD_FOLDER)
    scalar_data = []
    for scalar in scalars:
        try:
            scalar_events = data.Scalars(scalar)

            # Extract steps and values
            steps = [event.step for event in scalar_events]
            vals = [event.value for event in scalar_events]
            scalar_data.append((steps, vals))
        except:
            return {"res": None, "error": f"Error retrieving scalar {scalar}."}

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    for steps, vals in scalar_data:
        axis.plot(steps, vals)

    # Convert plot to PNG image
    png_image = BytesIO()
    FigureCanvas(fig).print_png(png_image)

    # Encode PNG image to base64 string
    png_image_b64_string = "data:image/png;base64,"
    png_image_b64_string += base64.b64encode(png_image.getvalue()).decode('utf8')

    return {"res": png_image_b64_string, "error": ""}


def openFile(file_path):
    data = EventAccumulator(file_path)
    data.Reload()
    # Get all scalar names
    scalar_names = data.Tags()['scalars']
    scalars = ""
    for name in scalar_names:
        scalars += name
        scalars += ", "
    if scalars == "":
        return "No data. Please check if you uploaded the right file."
    return scalars

def getTFEvent(file_path):
    data = EventAccumulator(file_path)
    data.Reload()
    # tags = data.Tags()['scalars']

    # # Print scalars of all tags
    # for tag in tags:
    #     print(tag)
    #     print(data.Scalars(tag))
    return data

if __name__ == "__main__":
    app.run(debug=True)
