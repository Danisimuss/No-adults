import json
import time
import random
print("Добро пожаловать в мою игру-квест!")
a = "1"
sila = 20
sp = []
rub = 0
k = 0
vr = True
j = 0
ar = False
while True:
    otv = input("Вы хотите начать новую игру или продолжить старую? Новая игра/Продолжить\n")
    if otv != "Новая игра" and otv != "Продолжить":
        print("Или новая игра или продолжить")
    if otv == "Новая игра":
        f = open("orig.json", encoding="utf8")
        break
    elif otv == "Продолжить":
        f = open("sohr.json", encoding="utf8")
        save1 = open("save1.json", encoding="utf8")
        sl1 = json.load(save1)
        a = sl1["a"]
        sp = sl1["inv"]
        rub = sl1["rub"]
        sila = sl1["sila"]
        time1 = time.time()
        ar = sl1["ar"]
        break
sl = json.load(f)
while True:
    save = {"a": a, "inv": sp, "rub": rub, "sila": sila, "ar": ar}
    save1 = open("save1.json", "w", encoding="utf8")
    json.dump(save, save1)
    f = open("sohr.json", "w", encoding="utf8")
    json.dump(sl, f, ensure_ascii=False, indent=2)
    if "time" in sl[a]:
        tt = a
        time1 = time.time()
        vr = False
    if vr is False:
        if a == sl[tt]["time"][1]:
            vr = True
        if time.time() - time1 > sl[tt]["time"][0]:
            a = "22"
    if ("Касса" in sp or "Продукты" in sp) and ar == False:
        del sl["100"]["to go"][1]
        del sl["100"]["go"][1]
        ar = True
    if "Доступ в оружейный." in sp:
        sl["100"]["go"][sl["100"]["to go"].index("Оружейный")] = "29"
        sl["29"]["text"] = ""
    if "dop" in sl[a]:
        for p in sl[a]["dop"]:
            if p not in sp:
                del sl[a]["to go"][sl[a]["dop"].index(p)]
                del sl[a]["rand"][sl[a]["dop"].index(p)]
    if len(sl[a]["text"]) == 0 and sl[a]["items"][0] == "bitva":
        if sila >= sl[a]["items"][1]:
            a = str(sl[a]["go"][0])
        else:
            if (sl[a]["items"][1] - sila) >= random.randint(1, 100):
                a = str(sl[a]["go"][1])
            else:
                a = str(sl[a]["go"][0])
        continue
    for i in sl[a]["text"]:
        time.sleep(1.5)
        print(i)
    if "end" in sl[a]["to go"]:
        break
    if len(sl[a]["items"]) != 0:
        if len(sl[a]["items"]) == 1 and type(sl[a]["items"]) is int:
            sila += sl[a]["items"][0]
        else:
            for h in sl[a]["items"]:
                if type(h) is int:
                    k = sl[a]["items"].index(h)
                    j = h
                elif "рублей" in h and "-" not in h:
                    rub += int(h.split()[0])
                    continue
                elif type(h) is str:
                    sp.append(h)
    time.sleep(1)
    while True:
        for g in sl[a]["to go"]:
            print(sl[a]["to go"].index(g) + 1, "-", g)
        b = int(input())
        if b > len(sl[a]["go"]) and "rand" not in sl[a]:
            print("Нет такого варианта.")
            time.sleep(1)
        else:
            break
    if len(sl[a]["items"]) != 0:
        if "-" in str(sl[a]["items"][b - 1]) and "рублей" in str(sl[a]["items"][b - 1]):
            if int(sl[a]["items"][b - 1].split()[1]) > rub:
                print("Недостаточно средств.")
                time.sleep(1)
            else:
                rub -= int(sl[a]["items"][b - 1].split()[1])
                if len(sl[a]["items"][b - 1].split()) > 3:
                    sila += int(sl[a]["items"][b - 1].split()[3])
                print("Спасибо за покупку! Приходите ещё!")
                b = 4
    if b == k - 1:
        sila += j
        k = 1000
    if len(sl[a]["rand"]) != 0:
        y = sl[a]["rand"][b - 1]
        if random.randint(1, 100) < y:
            if len(sl[a]["go"][b - 1]) != 0:
                a = str(sl[a]["go"][0])
        else:
            a = sl[a]["neudacha"]
    else:
        if len(sl[a]["go"][b - 1]) != 0:
            a = str(sl[a]["go"][b - 1])

