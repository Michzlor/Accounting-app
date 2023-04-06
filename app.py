from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

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

    def __repr__(self):
        return f"<{self.id}><{self.item}><{self.price}><{self.ammount}>"


class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100))
    date = db.Column(db.DateTime)


alembic = Alembic()
alembic.init_app(app)

bal = Balance(balance=0)
with app.app_context():
    db.session.add(bal)
    db.session.commit


def create_db():
    with app.app_context():
        db.create_all()


def save_to_db(manager):
    # stok = []
    with app.app_context():
        # TODO querry balnace table change value
        try:
            # db.session.query(User).filter(User.username=="robergo").all()
            bal = db.session.query(Balance).filter(Balance.id == 1).first()
            bal.balance = manager.acc_val
            db.session.add(bal)
        except Exception as err:
            print(err)
            bal = Balance(balance=manager.acc_val)
            db.session.add(bal)
        for thing in manager.stock:
            if thing[0] == None:
                break
            try:
                stok = db.session.query(Stock).filter(Stock.item == thing[0]).first()
                print(stok)
                stok.ammount = thing[2]
                stok.price = thing[1]
                db.session.add(stok)
            except Exception as err:
                print(err)
                stok = (Stock(item=thing[0], price=thing[1], ammount=thing[2]))
                db.session.add(stok)
        aud = Audit(action=manager.audit_log[-1], date=datetime.now())
        db.session.add(aud)
        db.session.commit()


def save_balance_db(manager):
    bal = Balance(balance=manager.acc_val)
    with app.app_context():
        db.session.add(bal)
        db.session.commit()


def save_stock_db():
    for item in manager.stock:
        if item[0] == None:
            break

        stok = (Stock(item=item[0], price=item[1], ammount=item[2]))

        with app.app_context():
            db.session.add(stok)
            db.session.commit()


def save_audit_db(manager):
    aud = Audit(action=manager.audit_log[-1], datetime=datetime.now())
    with app.app_context():
        db.session.add(aud)
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
        if request.form.get('balance') != '' and request.form.get('balance') != None:
            val = float(request.form.get('balance'))
            # save_balance_db(manager)
            manager.acc_val = manager.execute("balance", val)
            save_to_db(manager)
        elif request.form.get('buy-item') != '' and request.form.get('buy-item') != None:
            ammount = int(request.form.get('buy-ammount'))
            price = float(request.form.get('buy-price'))
            manager.execute("buy", item=request.form.get('buy-item'), ammount=ammount,
                            price=price)
            save_to_db(manager)
        elif request.form.get('sell-ammount') != '' and request.form.get('sell-ammount') != None:
            ammount = int(request.form.get('sell-ammount'))
            manager.execute("sale", item=request.form.get('sell-item'), ammount=ammount)
            save_to_db(manager)
        else:
            print("Huh?")
    return render_template("index.html", acc_val=round(manager.acc_val, 2), stock=manager.stock, item_list=item_list)


@app.route("/history/<start>/<end>")
@app.route("/history/")
def history(start=0, end=len(manager.audit_log)):
    log = []
    # if end == 0 or 1:
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
