from flask import __version__

html_template = (
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask App</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f8f9fa; /* Light gray background */
        }

        .container {
            background-color: #ffffff; /* White container background */
            padding: 40px; /* Increased padding for a larger container */
            border-radius: 12px; /* Rounded corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        h1 {
            color: #343a40; /* Dark gray text */
            font-size: 32px; /* Increased font size */
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            margin: 15px 0; /* Increased margin */
        }

        a {
            color: #007bff; /* Business blue link color */
            text-decoration: none;
        }

        p {
            color: #6c757d; /* Medium gray text */
        }
    </style>"""
    + f"""
</head>
<body>
    <div class="container">
        <h1>Hello from Flask@{__version__} app</h1>
        <h3>get started?</h3>
        <hr>
        <ul>
            <li><h2><a href="/swagger-ui">/swagger-ui</a></h2></li>
            <li><h2><a href="/redoc-ui">/redoc-ui</a></h2></li>
            <li><h2><a href="/admin">/admin</a></h2></li>
        <hr>
        </ul>
        <p>:)</p>
    </div>
</body>
</html>
"""
)

from flask import render_template_string
from calendarapi.wsgi import app


@app.route("/")
def root():
    return render_template_string(html_template)
