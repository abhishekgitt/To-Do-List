from flask import Flask ,render_template ,request, redirect ,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(500),nullable=False)
    date_time = db.Column(db.DateTime,default= datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"ID : {self.id} title : {self.title}"
    

@app.route('/')
def mainPage():
    todos = Todo.query.all()
    return render_template('index.html',todos = todos)


@app.route('/add', methods = ['GET','POST'])
def addTodo():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content: 
            return "Title and Content cannot be empty", 400

        new_todo = Todo(title=title, content=content)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    return render_template('/add.html')

@app.route('/delete/<int:id>')
def deleteTodo(id):
    
    todo_instance = Todo.query.get_or_404(id)
    db.session.delete(todo_instance)
    db.session.commit()
    return redirect(url_for('mainPage'))
    

@app.route('/update/<int:id>', methods =['GET','POST'])
def updateTodo(id):
    todo_instance = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo_instance.title = request.form['title']
        todo_instance.content = request.form['content']
        db.session.commit()
        return redirect(url_for('mainPage'))
    return render_template('add.html',todo = todo_instance, is_update=True)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




