from flask import Flask, render_template, request, abort, make_response
from convert import convert_img
from yakudo_error import YakudoError

app = Flask(__name__, static_url_path='/static')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'gif', 'jpeg']


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', title='yakudo')


@app.route("/upload", methods=['POST'])
def upload():
    try:
        img_file = request.files['file']
        if not allowed_file(img_file.filename):
            raise YakudoError("Allow only png, jpg, gif file.")
        input_data = img_file.read()
        output_data = convert_img(input_data)
        res = make_response()
        res.data = output_data
        res.headers['Content-Disposition'] = 'inline;'
        res.headers['Content-Type'] = 'image/jpeg'
        return res
    except YakudoError as e:
        return str(e)


if __name__ == '__main__':
    app.run()
