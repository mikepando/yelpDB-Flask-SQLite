from flask import Flask, render_template, request
import sqlite3
from flask import g

app = Flask(__name__)
app.config["DEBUG"] = True

DATABASE = 'static/yelpDB'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def returnUniqueElements(dataList):
    unique=set()   
    for x in dataList:  
        y=x[0]  
        if y.find(",")==-1:    
            unique.add(y)     
        else:
            elements=y.split(",")  
            unique.update(elements)  
                                     
    return unique
    
@app.route("/", methods=["GET","POST"])
def index():
    db = get_db()
    cursor = db.cursor()    
    dataList=cursor.execute("select category from company").fetchall()
    unique=list(returnUniqueElements(dataList))
    unique.sort()
    return render_template('main_page.html',categories=unique)

@app.route("/response", methods=["POST"])
def response():
    minRating=request.form["minRating"]
    category=request.form["category"]
    sorting=request.form["sorting"]
    if sorting=='rating':
        sortstring='rating DESC'
    elif sorting=='neighborhood':
        sortstring='neighborhood'
    else:
        sortstring='rating DESC, neighborhood ASC'
    db = get_db()
    cursor = db.cursor()
    dataList=cursor.execute("select * from company where rating>="+minRating+" and category like '%"+category+"%' order by "+sortstring).fetchall()
    return render_template('results_page.html',data=dataList)

        
if __name__ == '__main__':
    app.run(debug=True)
