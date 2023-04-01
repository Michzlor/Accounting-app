from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
import accounting

manager = accounting.manager
app = Flask(__name__)
app.secret_key = "very secret"
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
        # idx = int(start)
        # end = int(end)
        # while idx < end:
        #     log.append(manager.audit_log[idx])
        #     idx += 1
        log = manager.execute("audit", start, end)
    except IndexError as err:

        flash(f"IndexError valid range is 0-{len(manager.audit_log)}")
        start = int(start)
        end = int(end)
    # log = []
    # if start == "" or start == 0:
    #     idx = 0
    # else:
    #     idx = int(start) - 1
    # if end == "" or 0 or None:
    #     end = len(manager.audit_log)
    # else:
    #     end = (int(end)) - 1
    # while idx < end:
    #     log.append(manager.audit_log[idx])
    #     idx += 1
    # log = []

    return render_template("history.html", audit=log)
