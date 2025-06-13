
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'secret123'

# In-memory store for users and news (for demonstration)
staff_db = [
    {'id': 1, 'username': 'admin', 'password': 'admin123', 'department': 'HR'},
    {'id': 2, 'username': 'john', 'password': 'john123', 'department': 'Finance'}
]
news_list = []

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        department = request.form['department']

        for staff in staff_db:
            if staff['username'] == username and staff['password'] == password and staff['department'] == department:
                session['username'] = username
                session['department'] = department
                return redirect('/dashboard')
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    department = session['department']
    return render_template(f'dashboards/{department.lower().replace(" ", "_")}_dashboard.html',
                           username=session['username'],
                           department=department,
                           news_list=news_list)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/post_news', methods=['GET', 'POST'])
def post_news():
    if 'username' not in session or session['department'] != 'HR':
        return redirect('/login')
    if request.method == 'POST':
        news = request.form['news']
        news_list.append({'author': session['username'], 'content': news})
        return redirect('/post_news')
    return render_template('post_news.html', news_list=news_list)

@app.route('/staff_list')
def staff_list():
    if 'username' not in session or session['department'] != 'HR':
        return redirect('/login')
    return render_template('staff_list.html', staff_db=staff_db)

@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if 'username' not in session or session['department'] != 'HR':
        return redirect('/login')
    if request.method == 'POST':
        new_id = max(s['id'] for s in staff_db) + 1 if staff_db else 1
        staff_db.append({
            'id': new_id,
            'username': request.form['username'],
            'password': request.form['password'],
            'department': request.form['department']
        })
        return redirect('/staff_list')
    return render_template('add_staff.html')

@app.route('/edit_staff/<int:staff_id>', methods=['GET', 'POST'])
def edit_staff(staff_id):
    if 'username' not in session or session['department'] != 'HR':
        return redirect('/login')
    staff = next((s for s in staff_db if s['id'] == staff_id), None)
    if not staff:
        return 'Staff not found'
    if request.method == 'POST':
        staff['username'] = request.form['username']
        staff['password'] = request.form['password']
        staff['department'] = request.form['department']
        return redirect('/staff_list')
    return render_template('edit_staff.html', staff=staff)

@app.route('/delete_staff/<int:staff_id>')
def delete_staff(staff_id):
    global staff_db
    if 'username' not in session or session['department'] != 'HR':
        return redirect('/login')
    staff_db = [s for s in staff_db if s['id'] != staff_id]
    return redirect('/staff_list')

if __name__ == '__main__':
    app.run(debug=True)
