from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def base():
    return render_template('base.html')


@app.route('/team')
def teammembers():
    return render_template('teammembers.html')


@app.route('/docs')
def documentation():
    return render_template('documentation.html')


if __name__ == '__main__':
    app.run(debug=True)
