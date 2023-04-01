from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_sqlalchemy import SQLAlchemy


import accounting

manager = accounting.manager
app = Flask(__name__)
app.secret_key = "very secret"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///accounting.db'
db = SQLAlchemy(app)
class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float)
    ammount = db.Column(db.Integer)

class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100))

# with app.app_context():
#     db.create_all()

blah = Balance(balance = manager.acc_val)
with app.app_context():
    db.session.add(blah)
    db.session.commit()
item_list = []


@app.route('/', methods=['POST', 'GET'])
def index():
    item_list = []
    for item in manager.stock:
        if item[0] == None:
            break
        item_list.append(item[0])
    if request.method == 'POST':
        print(request.form)
        print(request.form.get('balance'))
        if request.form.get('balance') != '' and request.form.get('balance') != None:
            val = float(request.form.get('balance'))
            manager.acc_val = manager.execute("balance", val)
        elif request.form.get('buy-item') != '' and request.form.get('buy-item') != None:
            ammount = int(request.form.get('buy-ammount'))
            price = float(request.form.get('buy-price'))
            manager.execute("buy", item=request.form.get('buy-item'), ammount=ammount,
                            price=price)
        elif request.form.get('sell-ammount') != '' and request.form.get('sell-ammount') != None:
            ammount = int(request.form.get('sell-ammount'))
            manager.execute("sale", item=request.form.get('sell-item'), ammount=ammount)
        else:
            print("Huh?")
    return render_template("index.html", acc_val=round(manager.acc_val, 2), stock=manager.stock, item_list=item_list)


@app.route("/history/<start>/<end>")
@app.route("/history/")
def history(start=0, end=len(manager.audit_log)):
    log = []
    if end == 0:
        end = len(manager.audit_log)
    print(f"start: {start}, end: {end}")
    try:
        print("try")
        log = manager.execute("audit", start, end)
    except IndexError as err:

        flash(f"IndexError valid range is 0-{len(manager.audit_log)}")
        start = int(start)
        end = int(end)

    return render_template("history.html", audit=log)
