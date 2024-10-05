**Personal Finance Tracker**


*Description:*
The Personal Finance Tracker is a web application designed to help users manage their income and expenses effectively.
It provides a user-friendly interface to track financial transactions, visualize spending through graphs, and maintain a record of entries with dates.
Users can create accounts to secure their financial data and have a personalized experience.

*Key Features:*
* User registration and login functionality
* Add, edit, and delete income and expense entries
* View transactions on a dashboard
* Generate visual representations of spending through graphs
* Date tracking for each entry

*Technologies Used:*
* Python
* Flask
* SQLAlchemy
* HTML
* CSS

*Prerequisite:*
Python 3.x installed on your machine.


*Steps to run (Paste the following commands in terminal):*
  * >git clone https://github.com/your-username/Income_manager.git
  * >cd Income_manager
  * >python -m venv venv
    * >venv\Scripts\activate (For Windows)
    * >source venv/bin/activate (For macOS/Linux)
  * >pip install -r requirements.txt
  * >pip install Flask-Migrate
  * >flask db init
  * >flask db migrate -m "Initial migration."
  * >flask db upgrade
  * >flask run



http://127.0.0.1:5000/login

Click the link to open the project



*To create userid-password:*
  * >python
  * >from app import db, User
  * >new_user = User(username='your_username', password='your_password')
  * >db.session.add(new_user)
  * >db.session.commit()
  * >exit()



