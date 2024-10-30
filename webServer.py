from flask import Flask, Response, request
import badminton
app = Flask(__name__)

@app.route('/')
def home():    
    response = badminton.getDate(request.args['username'], request.args['password'])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <title>球場查詢</title>
    </head>
    <body>
        <p>{response}</p>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = 5000
    app.run(host=ip, port=port)
