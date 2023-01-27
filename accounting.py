acc_val = 1000
stock = [["a", 5, 200], ["b", 4 ,300],[None]]
audit = []
bop = len(stock)






i = 1
while i == 1:
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
        val = float(input("Provide value to add to account(negative value to substract): "))
        if acc_val + val < 0 :
            print("Debt not allowed\n\n")
        else:
            acc_val += val
            print("New account balance is:", round(acc_val, 2), "$")
        balance = (val, acc_val)
        audit.append(val)
#DONE2-sale: input product, price, ammount; check: if product in stock,
#remove product ammount from stock, add price to acc_val; add to audit
# negative value check, remove items from stock, add income to acc_val
    elif inp == "2":
        item = input("Input item: ")
        price = float(input("Input price: "))
        ammount = int(input("Input ammount: "))
        if price < 0 or ammount < 0:
            print("\n\nInvalid value")
            continue
        #if not item in stock:
            #print("\n\nItem not in stock")
        for idx in range(len(stock)):
            if stock[idx][0] == item:
                if stock[idx][2] < ammount:
                    print("Insufficent stock to make sale\n\n")
                else:
                    stock[idx][2] -= ammount
                    acc_val += price * ammount
            elif stock[idx][0] == None or stock[idx][2] == 0:
                print("\n\nItem not in stock")
        sale = ("sale", item, price, ammount)
        audit.append(sale)
#DONE3-buy: input product, price, ammount; check if prduct in stock, add if not
#add product to stock, substrackt price from acc_val, check if acc_val is negative
#add to audit, negative value check, substract costs from acc_val
    elif inp == "3":
        item = input("Input item: ")
        price = float(input("Input price: "))
        ammount = int(input("Input ammount: "))
        if price <= 0 or ammount <= 0:
            print("\n\nInvalid value")
            continue
        for idx in range(bop):
            if acc_val - ammount*price < 0:
                print("\n\nInsufficent funds")
                break
            if stock[idx][0] == None:
                stock.insert(-1, [item, price, ammount])
                acc_val -= price*ammount
                break
            if stock[idx][0] == item:
                stock[idx][2] += ammount
                acc_val -= price*ammount
                break


        buy = ("buy", item, price, ammount)
        audit.append(buy)
#DONE4-print acc_val
    elif inp == "4":
        print("Account balance is:", round(acc_val, 2), "$")
#DONE5-list stock: print product, price, ammount for evry item in stock
    elif inp == "5":
        #for k, v in stock.items():
           #print("{}: {}".format(k, v))
        for idx in range(len(stock)-1):
            print("Item:{}  ;  Price:{}$  ;  Ammount:{}".format(stock[idx][0], stock[idx][1], stock[idx][2]))
#DONE6-list item: input product; print ammount for input
    elif inp == "6":
        inp = input("Input item ")
        for idx in range(len(stock)):
            if stock[idx][0] == inp:
                print("Item:{}  ;  Price:{}$  ;  Ammount:{}".format(stock[idx][0], stock[idx][1], stock[idx][2]))
            elif stock[idx][0] == None:
                print("Not in stock\n\n")
#DONE7-audit: input from, to; print recorded actions with index from-to: add range
    elif inp == "7":
        start = input("Insert start of range: ")
        end = input("Insert end of range: ")
        if start == "":
            idx = 0
        else:
            idx = int(start)-1
        if end == "":
            end = len(audit)
        else:
            end = (int(end))-1
        while idx < end:
            print(audit[idx])
            idx += 1
#DONE8-break
    elif inp == "8":
        print("\n\nHave a nice day\n\n")
        break