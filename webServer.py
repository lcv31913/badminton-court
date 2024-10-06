from flask import Flask, Response, request
import badminton
app = Flask(__name__)

@app.route('/')
def home():    
    dates = badminton.getDate(request.args['username'], request.args['password'])
    date = [str(int(date)) for date in dates]
    response = ', '.join(date) + ".<br>" + "(大同運動中心)這些是可以預約的羽球球場日期"

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
