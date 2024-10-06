from flask import Flask, render_template, redirect, url_for, request, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# FinanceRecord model
class FinanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='records')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='sha256')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        # If user not found
        if not user:
            flash('User not registered', 'danger')
            return redirect(url_for('login'))
        
        # If password is incorrect
        if not check_password_hash(user.password, password):
            flash('Incorrect password, please try again.', 'danger')
            return redirect(url_for('login'))

        # If login is successful
        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    records = FinanceRecord.query.filter_by(user_id=current_user.id).all()
    total_spendings = sum(record.amount for record in records)
    return render_template('dashboard.html', records=records, total_spendings=total_spendings)

@app.route('/add_record', methods=['POST'])
@login_required
def add_record():
    amount = request.form['amount']
    description = request.form['description']
    category = request.form['category']
    new_record = FinanceRecord(amount=amount, description=description, category=category, user_id=current_user.id)
    db.session.add(new_record)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/report')
@login_required
def report():
    # Fetch records by category
    records = FinanceRecord.query.filter_by(user_id=current_user.id).all()
    
    categories = {}
    for record in records:
        if record.category in categories:
            categories[record.category] += record.amount
        else:
            categories[record.category] = record.amount
    
    # Generate pie chart
    img = io.BytesIO()
    plt.figure(figsize=(5, 5))
    plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.axis('equal')
    plt.title('Spending by Category')
    plt.savefig(img, format='png')
    img.seek(0)
    pie_chart_url = base64.b64encode(img.getvalue()).decode()

    return render_template('report.html', pie_chart_url=pie_chart_url, categories=categories)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
