with open("/home/ranhart/Desktop/py/ad/lab2/input1.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

participants = lines[0].split()
n = int(lines[1])

spent = {name: 0 for name in participants}
for i in range(2, 2 + n):
    name, amount = lines[i].split()
    spent[name] += int(amount)

total = sum(spent.values())
avg = round(total / len(participants), 2)

balances = {name: round(spent[name] - avg, 2) for name in participants}

debtors = []
creditors = []
for name, bal in balances.items():
    if bal < 0:
        debtors.append([name, -bal])   # должен
    elif bal > 0:
        creditors.append([name, bal])  # ему должны

transfers = []
i, j = 0, 0
while i < len(debtors) and j < len(creditors):
    debtor, debt = debtors[i]
    creditor, credit = creditors[j]

    amount = min(debt, credit)

    transfers.append((debtor, creditor, amount))

    debtors[i][1] -= amount
    creditors[j][1] -= amount

    if debtors[i][1] == 0:
        i += 1
    if creditors[j][1] == 0:
        j += 1

print(len(transfers))
for d, c, a in transfers:
    print(f"{d} {c} {a:.2f}")

