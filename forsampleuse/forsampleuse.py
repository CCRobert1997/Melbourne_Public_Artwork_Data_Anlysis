from flask import Flask
from random import randint
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route("/css-generator")
def root():
    css = '''
        html, body, table {
        width: 100%;
        height: 100%;
        margin: 0;
        }
        
        table {
        border-spacing: 0;
        }
        
        td {
        border: grey 1px solid;
        }
    '''
    colour = ['0','1','2','3', '4', '5', '6','7','8','9','A','B','C','D', 'E', 'F']
    for i in range(4):
        for j in range(4):
            css = css + '''tr:nth-child(%d) td:nth-child(%d){ background-color: #%c%c%c%c%c%c;}''' %(i, j, colour[randint(0,15)], colour[randint(0,15)], colour[randint(0,15)], colour[randint(0,15)], colour[randint(0,15)], colour[randint(0,15)])

    # Write your code that generates css here
    return css, 200, {'Content-Type': 'text/css; charset=utf-8'}

if __name__ == "__main__":
    app.run(debug=True)
