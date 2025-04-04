from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from docker_utils import list_redroid_containers, start_container, stop_container, restart_container, create_redroid_instance
from models import User, db
from flask import session

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    containers = list_redroid_containers()
    return render_template('index.html', containers=containers)

@app.route('/start/<name>', methods=['POST'])
@login_required
def start(name):
    if current_user.is_admin:
        start_container(name)
    return redirect(url_for('index'))

@app.route('/stop/<name>', methods=['POST'])
@login_required
def stop(name):
    if current_user.is_admin:
        stop_container(name)
    return redirect(url_for('index'))

@app.route('/restart/<name>', methods=['POST'])
@login_required
def restart(name):
    if current_user.is_admin:
        restart_container(name)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create_instance', methods=['POST'])
@login_required
def create_instance():
    if current_user.is_admin:
        create_redroid_instance()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
