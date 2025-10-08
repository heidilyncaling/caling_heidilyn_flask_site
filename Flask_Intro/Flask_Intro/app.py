from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# --------------------
# ROUTES
# --------------------

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Works page (handles multiple forms)
@app.route('/works', methods=['GET', 'POST'])
def works():
    uppercase_result = ''
    circle_area = ''
    triangle_area = ''

    if request.method == 'POST':
        # To Uppercase
        if 'text' in request.form and request.form['text'].strip():
            text = request.form['text']
            uppercase_result = text.upper()

        # Area of Circle
        elif 'radius' in request.form and request.form['radius'].strip():
            try:
                r = float(request.form['radius'])
                circle_area = round(3.1416 * (r ** 2), 2)
            except ValueError:
                circle_area = 'Invalid input'

        # Area of Triangle
        elif ('base' in request.form and request.form['base'].strip() and
              'height' in request.form and request.form['height'].strip()):
            try:
                b = float(request.form['base'])
                h = float(request.form['height'])
                triangle_area = round(0.5 * b * h, 2)
            except ValueError:
                triangle_area = 'Invalid input'

    return render_template(
        'works.html',
        uppercase_result=uppercase_result,
        circle_area=circle_area,
        triangle_area=triangle_area
    )

# --------------------
# RUN SERVER
# --------------------
if __name__ == '__main__':
    app.run(debug=True)