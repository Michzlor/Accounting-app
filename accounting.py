from flask import flash


class Manager:

    def __init__(self):
        self.actions = {}
        with open("balance.txt", "r") as f:
            self.acc_val = float(f.readline())
        with open("stock_file.txt", "r") as f:
            self.stock = []
            read = f.readlines()
            for i in range(0, len(read), 3):
                try:
                    item = [read[i].strip(), (float(read[i + 1].strip())), (int(read[i + 2].strip()))]
                    self.stock.append(item)
                except Exception as e:
                    print(e)
                    break
        self.stock.append([None])
        self.audit_log = []

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb

        return decorate

    def execute(self, name, *args, **kwarg):
        if name not in self.actions:
            print("Action not defined")
        else:
            return self.actions[name](self, *args, **kwarg)


manager = Manager()


@manager.assign("balance")
def balance(manager, val):
    acc_val = manager.acc_val
    if acc_val + val < 0:
        print("Debt not allowed\n\n")
    else:
        acc_val += val
        manager.acc_val = acc_val
        print("New account balance is:", round(acc_val, 2), "$")

    balance = (f"Balance change: {val}$ , new balance: {acc_val}$")
    manager.audit_log.append(balance)
    save_account_balance()
    save_audit()
    return acc_val


@manager.assign("sale")
def sale(manager, item, ammount):
    for idx in range(len(manager.stock)):
        if manager.stock[idx][0] == item:
            if manager.stock[idx][2] < ammount:
                flash("Insufficent stock to make sale")

                print("Insufficent stock to make sale\n\n")
            else:
                manager.stock[idx][2] -= ammount
                price = manager.stock[idx][1]
                manager.acc_val += price * ammount
                sale = (f"Sold {ammount} of {item}")
                manager.audit_log.append(sale)
                save_account_balance()
                save_stock()
                break
        # elif manager.stock[idx][0] == None or manager.stock[idx][2] == 0:
        #     print("\n\nItem not in stock")
    save_audit()
    return True


@manager.assign("buy")
def buy(manager, item, ammount, price):
    if price <= 0 or ammount <= 0:
        print("\n\nInvalid value")
    for idx in range(len(manager.stock)):
        if manager.acc_val - ammount * price < 0:
            print("\n\nInsufficent funds")
            break
        elif manager.stock[idx][0] == None:
            manager.stock.insert(-1, [item, price, ammount])
            manager.acc_val -= price * ammount
            break
        elif manager.stock[idx][0] == item:
            manager.stock[idx][2] += ammount
            manager.acc_val -= price * ammount
            break
    sale = (f"Purchased {ammount} of {item} at price: {price}$")
    manager.audit_log.append(sale)
    save_account_balance()
    save_stock()
    return True


@manager.assign("account")
def print_acc_val(manager):
    print("Account balance is:", round(manager.acc_val, 2), "$")


@manager.assign("stock")
def list_stock(manager):
    for idx in range(len(manager.stock) - 1):
        print("Item:{}  ;  Price:{}$  ;  Ammount:{}".format(manager.stock[idx][0], manager.stock[idx][1],
                                                            manager.stock[idx][2]))


@manager.assign("item")
def list_item(manager):
    inp = input("Input item ")
    for idx in range(len(manager.stock)):
        if manager.stock[idx][0] == inp:
            print("Item:{}  ;  Price:{}$  ;  Ammount:{}".format(manager.stock[idx][0], manager.stock[idx][1],
                                                                manager.stock[idx][2]))
            break
        elif manager.stock[idx][0] == None:
            print("Not in stock\n\n")


@manager.assign("audit")
def audit_func(manager, start=0, end=len(manager.audit_log)):
    log = []
    idx = int(start)
    end = int(end)
    while idx < end:
        log.append(manager.audit_log[idx])
        idx += 1
    return log


@manager.assign("exit")
def exit(manager):
    print("\n\nHave a nice day\n\n")
    print(manager.audit_log)
    with open("log.txt", "a") as log:
        for i in range(len(manager.audit_log)):
            log.write("________\n")
            for v in range(len(manager.audit_log[i])):
                log.write(str(manager.audit_log[i][v]))
                log.write("\n")
    with open("balance.txt", "w") as f:
        f.write(str(manager.acc_val))
    with open("stock_file.txt", "w") as f:
        for i in range(len(manager.stock)):
            if manager.stock[i][0] == None:
                break
            for v in range(3):
                f.write(str(manager.stock[i][v]))
                f.write("\n")
        f.write("\n")


def save_account_balance():
    with open("balance.txt", "w") as f:
        f.write(str(manager.acc_val))


def save_stock():
    with open("stock_file.txt", "w") as f:
        for i in range(len(manager.stock)):
            if manager.stock[i][0] == None:
                break
            for v in range(3):
                f.write(str(manager.stock[i][v]))
                f.write("\n")


def save_audit():
    with open("log.txt", "a") as log:
        log.write("________\n")
        log.write(str(manager.audit_log[-1]))
        log.write("\n")

# while True:
#     # 0-lista+input
#     print("*Balance(1)\n"
#           "*Sale(2)\n"
#           "*Purshase(3)\n"
#           "*Account(4)\n"
#           "*List stock(5)\n"
#           "*List item(6)\n"
#           "*Audit(7)\n"
#           "*Exit(8)\n")
#     inp = input("Choose action: ")
#     # DONE1-balance: input +- acc_val; add acc_val to audit
#     if inp == "1":
#         manager.acc_val = manager.execute("balance")
#     # DONE2-sale: input product, price, ammount; check: if product in stock,
#     # remove product ammount from stock, add price to acc_val; add to audit
#     # negative value check, remove items from stock, add income to acc_val
#     elif inp == "2":
#         manager.execute("sale")
#     # DONE3-buy: input product, price, ammount; check if prduct in stock, add if not
#     # add product to stock, substrackt price from acc_val, check if acc_val is negative
#     # add to audit, negative value check, substract costs from acc_val
#     elif inp == "3":
#         manager.execute("buy")
#     # DONE4-print acc_val
#     elif inp == "4":
#         manager.execute("account")
#     # DONE5-list stock: print product, price, ammount for evry item in stock
#     elif inp == "5":
#         manager.execute("stock")
#
#     # DONE6-list item: input product; print ammount for input
#     elif inp == "6":
#         manager.execute("item")
#     # DONE7-audit: input from, to; print recorded actions with index from-to: add range
#     elif inp == "7":
#         manager.execute("audit")
#     # DONE8-break
#     elif inp == "8":
#         manager.execute("exit")
#         break
