# from flask import Flask, request, redirect
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_migrate import Migrate
from sqlalchemy.orm import backref


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///stackoverflow.db"
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
            return '<Hello, %r>' %self.username

class Question(db.Model):
    qid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qusername = db.Column(db.String(50), nullable=False, unique=True)
    qcontent = db.Column(db.String(), nullable = False)

    def __repr__(self):
            return '<Question created: , %r>' %self.qcontent

class CommentStore(db.Model):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cusername = db.Column(db.String(50), nullable=False, unique=True)
    question_id = db.Column(db.Integer)
    comment = db.Column(db.String(), nullable = True)
    vote = db.Column(db.Integer(), nullable = True)

    def __repr__(self):
            return '<Comment: %r, Vote: %r>' %self.comment %self.vote



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/create_user', methods=["POST"])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username = username, email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
        print('User', username, ' created')

        return username
    
@app.route('/create_question', methods=["GET", "POST"])
def create_question():
    if current_user.is_authenticated:
        if request.method == "POST":
            user_id = current_user.uid
            qcontent = request.form['qcontent']
            user = User.query.filter_by(uid = user_id).first()
            question = Question(qusername = user.username, qcontent = qcontent)
            db.session.add(question)
            db.session.commit()
            return qcontent

@app.route('/update_question', methods = ["GET", "POST"])
def update_question():
    if current_user.is_authenticated:
        if request.method=="POST":
            user_id = current_user.uid
            new_qcontent = request.form['new_qcontent']
            user = User.query.filter_by(uid = user_id).first()
            question = Question.query.filter_by(qusername = user.username).first()
            question.qcontent = new_qcontent
            db.session.commit()

@app.route('/delete_question', methods = ['GET', 'POST'])
def delete_question():
    if current_user.is_authenticated():
        if request.method=="POST":
            user_id = current_user.uid
            user = User.query.filter_by(uid = user_id).first()
            db.session.query(Question).filter_by(qusername = user.username).delete()
            db.session.commit()

@app.route('/all_questions', methods=['GET', 'POST'])
def all_questions():
    all_q = Question.query.all()
    q_list=[]
    for q in all_q:
        temp = {
            'qid':q.qid,
            'qusername': q.qusername,
            'qcontent': q.qcontent
        }
        q_list.append(temp)
    print(q_list)
    return q_list

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if current_user.is_authenticated():
        if request.method=="POST":
            user_id = current_user.uid
            user = User.query.filter_by(uid = user_id).first()
            question = Question.filter_by(qusername = user.username).first()
            vote = request.form['vote']
            commentstore = CommentStore.query.all()
            new_vote = vote
            if commentstore:
                for c in commentstore:
                    new_vote = new_vote + c.vote
            vote_entry = CommentStore(cusername = user.username, question_id = question.qid, vote=new_vote)
            db.session.add(vote_entry)
            db.session.commit()


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if current_user.is_authenticated():
        if request.method=="POST":
            user_id = current_user.uid
            user = User.query.filter_by(uid = user_id).first()
            question = Question.filter_by(qusername = user.username).first()
            comment = request.form['comment']
            comment_entry = CommentStore(cusername = user.username, question_id = question.qid, comment = comment)
            db.session.add(comment_entry)
            db.session.commit()



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)