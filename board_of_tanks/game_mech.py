import random


class Tank:
    def __init__(self, number, name, power, armour, speed, min_range, critical_hit_chance):
        self.number = number
        self.name = name
        self.power = power
        self.armour = armour
        self.speed = speed
        self.min_range = min_range
        self.critical_hit_chance = critical_hit_chance

    def tank_options(self):
        print(f"№{self.number}: {self.name}, {self.power=} {self.armour=} {self.speed=} {self.min_range=} "
              f"{self.critical_hit_chance=}")

    def move(self, d):
        d[0] -= self.speed
        print(f"До вражеского танка осталось {d[0]} метров")
        # return d

    def calc_accuracy(self, d):
        # шанс попадания 0%, если дальность стрельбы меньше дистанции
        if self.min_range < d[0]:
            full_chance = 0
        # расчитываем шанс попадания
        else:
            min_chance = 40  # задаем базовый шанс попадания в 40% (при d = range)
            chance_from_distance_modifier = self.min_range / d[0]  # доп модификатор, зависящий от дистанции до врага
            full_chance = min_chance * chance_from_distance_modifier
            if full_chance > 100:
                full_chance = 100
        print(f"Шанс попадания: {int(full_chance)}%")
        return full_chance

    def shoot(self, vs_tank, fchs):
        # global enemy_tank_is_alive
        if fchs == 0:
            print(f"Ваш снаряд не долетел до танка противника!")
        else:
            rnd = random.randint(0, 100)  
            if rnd > fchs:
                print("Вы промахнулись!")
            else:
                rnd_crit = random.randint(0, 100)
                if rnd_crit <= self.critical_hit_chance:
                    print("Критическое попадание!")
                    print(f"Вы нанесли {2 * self.power} урона танку противника {vs_tank.name}!")
                    vs_tank.armour -= 2 * self.power
                    if vs_tank.armour <= 0:
                        print(f"Танк противника {vs_tank.name} подбит!")
                        # enemy_tank_is_alive = False
                        exit(-1)
                    else:
                        print(f"У танка противника {vs_tank.name} осталось {vs_tank.armour} прочности")
                else:
                    print(f"Вы нанесли {self.power} урона танку противника {vs_tank.name}!")
                    vs_tank.armour -= self.power
                    if vs_tank.armour <= 0:
                        print(f"Танк противника {vs_tank.name} подбит!")
                        # enemy_tank_is_alive = False
                        exit(-1)
                    else:
                        print(f"У танка противника {vs_tank.name} осталось {vs_tank.armour} прочности")

    def shoot_ai(self, y_tank, fchs):
        # global your_tank_is_alive
        rnd = random.randint(0, 100)  
        if rnd > fchs:
            print("Танк противника промахнулся!")
        else:
            rnd_crit = random.randint(0, 100)
            if rnd_crit <= self.critical_hit_chance:
                print("Критическое попадание!")
                print(f"Танк противника нанес {2 * self.power} урона вашему танку {y_tank.name}!")
                y_tank.armour -= 2 * self.power
                if y_tank.armour <= 0:
                    print(f"Ваш танк {y_tank.name} подбит!")
                    # your_tank_is_alive = False
                    exit(-1)
                else:
                    print(f"У вашего танка {y_tank.name} осталось {y_tank.armour} прочности")
            else:
                print(f"Танк противника нанес {self.power} урона вашему танку {y_tank.name}!")
                y_tank.armour -= self.power
                if y_tank.armour <= 0:
                    print(f"Ваш танк {y_tank.name} подбит!")
                    # your_tank_is_alive = False
                    exit(-1)
                else:
                    print(f"У вашего танка {y_tank.name} осталось {y_tank.armour} прочности")


def pick_your_tank(lst):
    tank_choice = int(input(f"Выберите номер своего танка (введите номер от 0 до {len(lst) - 1}): "))
    print(f"Ваш танк - {lst[tank_choice].name}")
    return tank_choice


def pick_enemy_tank(lst):
    enemy_choice = int(input(f"Выберите номер танка противника (введите номер от 0 до {len(lst) - 1}): "))
    print(f"Танк врага - {lst[enemy_choice].name}")
    return enemy_choice


def on_action_choice(lst, x, y, d):
    action_choice = int(input("Хотите передвигаться или стрелять? (введите 1 или 2): "))
    if action_choice == 1:
        lst[x].move(d)
    elif action_choice == 2:
        # lst[x].calc_accuracy(d)
        lst[x].shoot(lst[y], lst[x].calc_accuracy(d))


def on_action_choice_ai(lst, y, x, d):
    # Компьютер никогда не стреляет, если дистанция выше дальности стрельбы
    # if d < self.min_range:
    if d[0] > lst[y].min_range:
        print("Танк противника едет на вас.")
        lst[y].move(d)
    else:
        print("Танк противника стреляет по вам!")
        # lst[y].calc_accuracy(d)
        lst[y].shoot_ai(lst[x], lst[y].calc_accuracy(d))


panther_tank = Tank(0, "Panthera", 25, 55, 40, 200, 15)
t34_tank = Tank(1, "T-34", 20, 50, 50, 250, 15)

tank_lst = [panther_tank, t34_tank]

for tank in tank_lst:
    tank.tank_options()

#  m
distance = [400]

#  Выбираем себе танк
your_tank = pick_your_tank(tank_lst)
#  Выбираем танк сопернику
enemy_tank = pick_enemy_tank(tank_lst)
# Устанавливаем флаги на "живые танки"
# your_tank_is_alive = True
# enemy_tank_is_alive = True
# Запускаем цикл ходов, пока один из танков не будет подбит
# while your_tank_is_alive and enemy_tank_is_alive:
while True:
    on_action_choice(tank_lst, your_tank, enemy_tank, distance)
    on_action_choice_ai(tank_lst, enemy_tank, your_tank, distance)
