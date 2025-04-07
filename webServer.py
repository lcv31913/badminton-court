from flask import Flask, Response, request, render_template
import badminton
app = Flask(__name__)

@app.route('/')
def home():    
    return render_template('index.html')

@app.route('/search')
def search():
    device_type = ""
    ua = request.headers.get("User-Agent")
    
    if any(keyword in ua for keyword in ["Mobile", "iPhone", "Android", "iPad"]):
        device_type = "mobile"
    else:
        device_type = "desktop"

    response = badminton.getDate(request.args['account'], request.args['password'], device_type)
    print(response)
    return response
    #return device_type

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = 80
    app.run(host=ip, port=port)
