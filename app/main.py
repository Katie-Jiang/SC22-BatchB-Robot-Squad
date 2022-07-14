# import requirements needed
from flask import Flask, render_template, request
from utils import get_base_url
import joblib
import numpy as np

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12367
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')
    

model = joblib.load("random_forest.joblib")

# set up the routes and logic for the webserver
@app.route(f'{base_url}' )
def home():
    return render_template('index.html')

@app.route(f'{base_url}/index' )
def index():
    return render_template('index.html')

@app.route(f'{base_url}/about')
def about():
    return render_template('about.html')

@app.route(f'{base_url}/contact')
def contact():
    return render_template('contact.html')

@app.route(f'{base_url}/post')
def post():
    return render_template('post.html')

@app.route(f'{base_url}/contact', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return(render_template('contact.html', prediction_text = ""))
    
    if request.method == 'POST':
        
        inp_features = [float(x) for x in request.form.values()]
        
        input_features = np.array(inp_features)
        
        input_features = input_features.reshape(1,-1)
        
        predictions = model.predict(input_features)[0]
        
        if predictions == 0:
            output = "No disease"
        else:
            output = "Have disease"
        
        return render_template('contact.html', prediction_text=output)


# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc7.ai-camp.dev/'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
