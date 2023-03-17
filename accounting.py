with open("balance.txt", "r") as f:
    impport_acc_val = float(f.readline())
with open("stock_file.txt", "r") as f:
    import_stock = []
    read = f.readlines()
    for i in range(0, len(read), 3):
        try:
            item = [read[i].strip(), (float(read[i+1].strip())), (int(read[i+2].strip()))]
            import_stock.append(item)
        except Exception as e:
            print(e)
            break
import_stock.append([None])
class Manager:

    def __init__(self):
        self.actions = {}
        self.acc_val = impport_acc_val
        self.stock = import_stock
        self.audit = []
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
def balance(manager, acc_val, audit_log):
    val = float(input("Provide value to add to account(negative value to substract): "))

    if acc_val + val < 0:
        print("Debt not allowed\n\n")
    else:
        acc_val += val
        manager.acc_val = acc_val
        print("New account balance is:", round(acc_val, 2), "$")

    balance = (val, acc_val)
    audit_log.append(balance)
    return acc_val
@manager.assign("sale")
def sale(manager, acc_val, stock, audit_log):
    item = input("Input item: ")
    price = float(input("Input price: "))
    ammount = int(input("Input ammount: "))
    if price < 0 or ammount < 0:
        print("\n\nInvalid value")
        # ? return continue
    # if not item in stock:
    # print("\n\nItem not in stock")
    for idx in range(len(stock)):
        if stock[idx][0] == item:
            if stock[idx][2] < ammount:
                print("Insufficent stock to make sale\n\n")
            else:
                manager.stock[idx][2] -= ammount
                manager.acc_val += price * ammount
                break
        elif stock[idx][0] == None or stock[idx][2] == 0:
            print("\n\nItem not in stock")
    sale = ("sale", item, price, ammount)
    audit_log.append(sale)
@manager.assign("buy")
def buy(manager, acc_val, stock, audit_log):
    item = input("Input item: ")
    price = float(input("Input price: "))
    ammount = int(input("Input ammount: "))
    if price <= 0 or ammount <= 0:
        print("\n\nInvalid value")
        # ? continue
    for idx in range(len(stock)):
        if acc_val - ammount * price < 0:
            print("\n\nInsufficent funds")
            break
        elif stock[idx][0] == None:
            stock.insert(-1, [item, price, ammount])
            acc_val -= price * ammount
            break
        elif stock[idx][0] == item:
            stock[idx][2] += ammount
            acc_val -= price * ammount
            break
    sale = ("buy", item, price, ammount)
    audit_log.append(sale)
@manager.assign("account")
def print_acc_val(manager, acc_val):
    print("Account balance is:", round(acc_val, 2), "$")
@manager.assign("stock")
def list_stock(manager, stock):
    for idx in range(len(stock) - 1):
        print("Item:{}  ;  Price:{}$  ;  Ammount:{}".format(stock[idx][0], stock[idx][1], stock[idx][2]))
@manager.assign("item")
def list_item(manager, stock):
    inp = input("Input item ")
    for idx in range(len(stock)):
        if stock[idx][0] == inp:
            print("Item:{}  ;  Price:{}$  ;  Ammount:{}".format(stock[idx][0], stock[idx][1], stock[idx][2]))
            break
        elif stock[idx][0] == None:
            print("Not in stock\n\n")
@manager.assign("audit")
def audit_func(manager, audit_log):
    start = input("Insert start of range: ")
    end = input("Insert end of range: ")
    if start == "":
        idx = 0
    else:
        idx = int(start) - 1
    if end == "":
        end = len(audit_log)
    else:
        end = (int(end)) - 1
    while idx < end:
        print(audit_log[idx])
        idx += 1
@manager.assign("exit")
def exit(manager, acc_val, stock, audit):
    print("\n\nHave a nice day\n\n")
    print(audit)
    with open("log.txt", "a") as log:
        for i in range(len(audit)):
            log.write("________\n")
            for v in range(len(audit[i])):
                log.write(str(audit[i][v]))
                log.write("\n")
    with open("balance.txt", "w") as f:
        f.write(str(acc_val))
    with open("stock_file.txt", "w") as f:
        for i in range(len(stock)):
            if stock[i][0] == None:
                break
            for v in range(3):
                f.write(str(stock[i][v]))
                f.write("\n")
                print(stock[i][v])
        f.write("\n")


while True:
#0-lista+input
    print("*Balance(1)\n"
          "*Sale(2)\n"
          "*Purshase(3)\n"
          "*Account(4)\n"
          "*List stock(5)\n"
          "*List item(6)\n"
          "*Audit(7)\n"
          "*Exit(8)\n")
    inp = input("Choose action: ")
#DONE1-balance: input +- acc_val; add acc_val to audit
    if inp == "1" :
        manager.acc_val = manager.execute("balance", manager.acc_val, manager.audit)
#DONE2-sale: input product, price, ammount; check: if product in stock,
#remove product ammount from stock, add price to acc_val; add to audit
# negative value check, remove items from stock, add income to acc_val
    elif inp == "2":
        manager.execute("sale", manager.acc_val, manager.stock, manager.audit)
    #DONE3-buy: input product, price, ammount; check if prduct in stock, add if not
#add product to stock, substrackt price from acc_val, check if acc_val is negative
#add to audit, negative value check, substract costs from acc_val
    elif inp == "3":
        manager.execute("buy", manager.acc_val, manager.stock, manager.audit)
#DONE4-print acc_val
    elif inp == "4":
        manager.execute("account", manager.acc_val)
#DONE5-list stock: print product, price, ammount for evry item in stock
    elif inp == "5":
        manager.execute("stock", manager.stock)

#DONE6-list item: input product; print ammount for input
    elif inp == "6":
        manager.execute("item", manager.stock)
#DONE7-audit: input from, to; print recorded actions with index from-to: add range
    elif inp == "7":
        manager.execute("audit", manager.audit)
#DONE8-break
    elif inp == "8":
        manager.execute("exit", manager.acc_val, manager.stock, manager.audit)
        break
