import json # библиотеки
import time
import random
import os.path
print("Добро пожаловать в мою игру-квест «Без взрослых»!") # приветствие
step = "1" # значения переменных по умолчанию
sila = 20 # сила игрока
sp = [] # инвентарь
rub = 0 # количество денег
k = 0 # вспомогательные переменные
vr = True # переменная, останавливающая секундомер после ограбления банка (когда игрок успевает сбежать из магазина, она принимает значение False)
j = 0 # переменная для работы механики с силой
ar = False # при проходе магазина становится True
b = 3000
while True: # цикл для начала игры
    otv = input("Вы хотите начать новую игру или продолжить старую? Новая игра/Продолжить\n")
    if otv != "Новая игра" and otv != "Продолжить":
        print("Или новая игра или продолжить")
    if otv == "Новая игра":
        f = open("orig.json", encoding="utf8")
        save1 = open("save1.json", "w", encoding="utf8")
        break
    elif otv == "Продолжить":
        if os.path.exists("save1.json") is False:
            print("Вы ещё не играли.")
            continue
        f = open("sohr.json", encoding="utf8")
        save1 = open("save1.json", encoding="utf8")
        sl1 = json.load(save1)
        step = sl1["step"]
        sp = sl1["inv"]
        rub = sl1["rub"]
        sila = sl1["sila"]
        time1 = time.time()
        ar = sl1["ar"]
        break
sl = json.load(f) # загрузка карты
while True: # основной цикл
    if "time" in sl[step]: # механика времени
        tt = step
        time1 = time.time()
        vr = False
    if vr is False:
        if step == sl[tt]["time"][1]: # успешно сбежал из магазина
            vr = True
        if time.time() - time1 > sl[tt]["time"][0]: # смерть в магазине
            step = "22"
    if ("Касса" in sp or "Продукты" in sp) and ar is False: # пропуск пройденных шагов
        del sl["100"]["go"][sl["100"]["to go"].index("Продуктовый")]
        del sl["100"]["to go"][sl["100"]["to go"].index("Продуктовый")]
        ar = True
    if "Доступ в оружейный." in sp:
        sl["100"]["go"][sl["100"]["to go"].index("Оружейный")] = "29"
        sl["29"]["text"] = ""
    if "dop" in sl[step]:
        for p in sl[step]["dop"]:
            if p not in sp:
                del sl[step]["to go"][sl[step]["dop"].index(p)]
                del sl[step]["rand"][sl[step]["dop"].index(p)]
    if len(sl[step]["text"]) == 0 and sl[step]["items"][0] == "bitva": # сражение
        if sila >= sl[step]["items"][1]: # однозначная победа
            step = str(sl[step]["go"][0])
        else: # неоднозначная победа
            if sila >= random.randint(1, 100):
                step = str(sl[step]["go"][1])
            else:
                step = str(sl[step]["go"][0])
        continue
    for i in sl[step]["text"]: # вывод текста
        time.sleep(1.5)
        print(i)
    if "end" in sl[step]["to go"]: # завершение игры
        time.sleep(5)
        break
    if len(sl[step]["items"]) != 0: # система вещей
        if len(sl[step]["items"]) == 1 and type(sl[step]["items"][0]) is int:
            sila += sl[step]["items"][0]
        else:
            for h in sl[step]["items"]:
                if type(h) is int:
                    k = sl[step]["items"].index(h)
                    j = h
                elif "рублей" in h and "-" not in h:
                    rub += int(h.split()[0])
                    continue
                elif type(h) is str and "-" not in h and len(h) != 0:
                    sp.append(h)
    time.sleep(1)
    save = {"step": step, "inv": sp, "rub": rub, "sila": sila, "ar": ar} # сохранение
    save1 = open("save1.json", "w", encoding="utf8")
    json.dump(save, save1)
    f = open("sohr.json", "w", encoding="utf8")
    json.dump(sl, f, ensure_ascii=False, indent=2)
    while True:
        for g in sl[step]["to go"]: # вывод вариантов ходов
            print(sl[step]["to go"].index(g) + 1, "-", g)
        b = input() # ввод номера выбранного пути
        if b in "0123456789" and len(b) != 0: # проверка ввода
            if int(b) > len(sl[step]["go"]) and "rand" not in sl[step]:
                print("Нет такого варианта.")
                time.sleep(1)
            else:
                b = int(b)
                break
        else:
            print("Нет такого варианта.")
    if len(sl[step]["items"]) != 0: # система магазина
        if "-" in str(sl[step]["items"][b - 1]) and "рублей" in str(sl[step]["items"][b - 1]):
            if int(sl[step]["items"][b - 1].split()[1]) > rub:
                print("Недостаточно средств.")
                time.sleep(1)
            else:
                rub -= int(sl[step]["items"][b - 1].split()[1])
                if len(sl[step]["items"][b - 1].split()) > 3:
                    sila += int(sl[step]["items"][b - 1].split()[3])
                print("Спасибо за покупку! Приходите ещё!")
                b = 4
    if b == k + 1:  # добавление силы игроку
        sila += j
        k = 1000
    if "rand" in sl[step]: # система случайных событий
        y = sl[step]["rand"][b - 1]
        if random.randint(1, 100) < y:
            if len(sl[step]["go"][b - 1]) != 0:
                step = str(sl[step]["go"][0])
        else:
            step = sl[step]["neudacha"]
    else:
        if len(sl[step]["go"][b - 1]) != 0:
            step = str(sl[step]["go"][b - 1])
