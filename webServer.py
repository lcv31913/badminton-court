from flask import Flask, Response, request, render_template
import badminton
app = Flask(__name__)

@app.route('/')
def home():    
    return render_template('index.html')

@app.route('/search')
def search():    
    response = badminton.getDate(request.args.get('account'), request.args.get('password'), request.args.get('shortcut'))
    
    return Response(response, content_type='text/plain; charset=utf-8')

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = 3636
    app.run(host=ip, port=port)
