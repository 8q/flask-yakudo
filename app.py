from flask import Flask, render_template, request, abort, make_response
from convert import convert_img

app = Flask(__name__, static_url_path='/static')


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', title='yakudo')


@app.route("/upload", methods=['POST'])
def upload():
    try:
        input_data = request.files['file'].read()
        output_data = convert_img(input_data)
        del input_data
        res = make_response()
        res.data = output_data
        res.headers['Content-Disposition'] = 'inline;'
        res.headers['Content-Type'] = 'image/png'
        return res
    except:
        abort(500)


if __name__ == '__main__':
    app.run()
