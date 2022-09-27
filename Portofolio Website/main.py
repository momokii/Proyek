from flask import Flask, render_template
import requests



app = Flask(__name__)


medium_rul = 'https://mediumpostsapi.vercel.app/api/kelanach'

data = requests.get(medium_rul).json()['dataMedium'][:6]

@app.route('/')
def porto():
    return render_template('index.html', data_blog = data)


if __name__ == "__main__":
    app.run(debug= True)

