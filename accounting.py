acc_val = 1000
stock = []
audit = []







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
#2-sale: input product, price, ammount; check: if product in stock,
#remove product ammount from stock, add price to acc_val; add to audit
#TODO negative price check, remove item from stock, add income to acc_val
    elif inp == "2":
        item = input("Input item: ")
        price = float(input("Input price: "))
        ammount = int(input("Input ammount: "))
        sale =(item, price, ammount)
        if not item in stock:
            print("Insufficent stock to make sale\n\n")
        audit.append(sale)
#3-purchase: input product, price, ammount; check if prduct in stock, add if not
#add product to stock, substrackt price from acc_val, check if acc_val is negative
#add to audit TODO negative value check, substract costs from acc_val
    elif inp == "3":
        item = input("Input item: ")
        price = float(input("Input price: "))
        ammount = int(input("Input ammount: "))
        purchase = (item, price, ammount)
        if not item in stock:
            stock.append([item, price, ammount])
        audit.append(purchase)
#DONE4-print acc_val
    elif inp == "4":
        print("Account balance is:", round(acc_val, 2), "$")
#DONE5-list stock: print product, price, ammount for evry item in stock
    elif inp == "5":
        for idx in range(len(stock)):
            print("Item:{}  ;  Price:{}  ;  Ammount:{}".format(stock[idx][0], stock[idx][1], stock[idx][2]))
#DONE6-list item: input product; print ammount for input
    elif inp == "6":
        inp = input("Input item ")
        for idx in range(len(stock)):
            if stock[idx][0] == inp:
                print("Item:{}  ;  Price:{}  ;  Ammount:{}".format(stock[idx][0], stock[idx][1], stock[idx][2]))
            else:
                print("Not in stock\n\n")
#7-audit: input from, to; print recorded actions with index from-to: TODO add range
    elif inp == "7":
        for idx in range(len(audit)):
            print(audit[idx])
#TODO if no input from = 0 to = -1, check if input in range if not print range
#DONE8-break
    elif inp == "8":
        print("\n\nHave a nice day\n\n")
        break