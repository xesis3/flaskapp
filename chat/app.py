from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

# Dictionary to store user information
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html', error='')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error='Username already exists')
        else:
            users[username] = {'password': password}
            session['username'] = username
            return redirect(url_for('chat'))
    return render_template('signup.html', error='')

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        emit('chat_history', get_chat_history())

@socketio.on('join')
def handle_join(data):
    if 'username' in session:
        username = session['username']
        room = data['room']
        join_room(room)
        emit('join_message', f'{username} has joined the room.', room=room)

@socketio.on('leave')
def handle_leave(data):
    if 'username' in session:
        username = session['username']
        room = data['room']
        leave_room(room)
        emit('leave_message', f'{username} has left the room.', room=room)

@socketio.on('message')
def handle_message(data):
    if 'username' in session:
        username = session['username']
        room = data['room']
        message = data['message']
        add_to_chat_history(username, message)
        emit('message', {'username': username, 'message': message}, room=room)

def get_chat_history():
    # Implement logic to retrieve chat history based on the room
    return []

def add_to_chat_history(username, message):
    # Implement logic to add a message to the chat history based on the room
    pass

if __name__ == '__main__':
    app.secret_key = 'secret_key'
    socketio.run(app, host='0.0.0.0', port=8080)
