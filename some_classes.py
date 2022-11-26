
from enum import Enum, auto
from random import random
from typing import List


class Fraction(Enum):
    LONER = auto()
    BANDIT = auto()
    FREEDOM = auto()
    DUTY = auto()
    MERCENARY = auto()  # Наёмник
    MILITARY = auto()
    SCIENTIST = auto()
    MONOLITH = auto()
    ZOMBIFIED = auto()


class Ammunition(Enum):
    Ammo9x18 = auto()
    Ammo9x18_Piercing = auto()
    Ammo9x19 = auto()
    Ammo9x39 = auto()
    Ammo7_62x54 = auto()
    Ammo5_7x28 = auto()
    Ammo5_56x45 = auto()
    Ammo5_45x39 = auto()
    Ammo12x76_Slug = auto()  # Zhekan
    Ammo12x76_Dart = auto()
    Ammo12x70_Buckshot = auto()
    AmmoNone = auto()


class Creature:
    def __init__(self,
                 max_hp: int,
                 physical_resistance: int,  # protection against blows, explosions and bites of mutants
                 fire_resistance: int,
                 radiation_resistance: int,
                 chemical_burns_resistance: int,
                 electricity_resistance: int,
                 bleeding_resistance: int,
                 psy_resistance: int,
                 armor: int,  # protection from gunshot wounds
                 max_stamina: int):
        self.max_hp = max_hp
        self.physical_resistance = physical_resistance
        self.fire_resistance = fire_resistance
        self.radiation_resistance = radiation_resistance
        self.chemical_burns_resistance = chemical_burns_resistance
        self.electricity_resistance = electricity_resistance
        self.bleeding_resistance = bleeding_resistance
        self.psy_resistance = psy_resistance
        self.armor = armor
        self.max_stamina = max_stamina
        self.hp = max_hp
        self.stamina = self.max_stamina
        self.radiation = 0

    def take_damage(self,
                    physical_damage: int,
                    fire_damage: int,
                    radiation_damage: int,
                    chemical_burns_damage: int,
                    electricity_damage: int,
                    bleeding_damage: int,
                    psy_damage: int,
                    bullet_damage: int) -> None:
        self.hp -= physical_damage * (1 - 0.01 * self.physical_resistance) \
                   + fire_damage * (1 - 0.01 * self.fire_resistance) \
                   + radiation_damage * (1 - 0.01 * self.radiation_resistance) \
                   + chemical_burns_damage * (1 - 0.01 * self.chemical_burns_resistance) \
                   + electricity_damage * (1 - 0.01 * self.electricity_resistance) \
                   + bleeding_damage * (1 - 0.01 * self.bleeding_resistance) \
                   + psy_damage * (1 - 0.01 * self.psy_resistance) \
                   + bullet_damage * (1 - 0.01 * self.armor)

    def __str__(self):
        return f"HP: {self.hp}\n" \
               f"Stamina: {self.stamina}\n" \
               f"Radiation: {self.radiation}\n" \
               f"|\n" \
               f"Max HP: {self.max_hp}\n" \
               f"Max stamina: {self.max_stamina}\n" \
               f"Physical resistance: {self.physical_resistance}\n" \
               f"Fire resistance: {self.fire_resistance}\n" \
               f"Radiation resistance: {self.radiation_resistance}\n" \
               f"Chemical burns resistance: {self.chemical_burns_resistance}\n" \
               f"Electricity resistance: {self.electricity_resistance}\n" \
               f"Bleeding resistance: {self.bleeding_resistance}\n" \
               f"Psy Resistance: {self.psy_resistance}\n" \
               f"Armor: {self.armor}\n"


class Item:
    def __init__(self, name: str, cost: int, weight: float):
        self.name = name
        self.cost = cost
        self.weight = weight

    def __str__(self):
        return f"Name: {self.name}\nCost: {self.cost}\nWeight: {self.weight}\n\n"


class Ammo(Item):
    def __init__(self,
                 type_of_ammunition: Ammunition,
                 cost: int,  # for 60
                 weight: float,  # for 60
                 amount: int):
        self.ammo_weight = weight
        self.ammo_cost = cost
        self.amount = amount
        self.type_of_ammunition = type_of_ammunition
        super().__init__(type_of_ammunition.__str__(), int(cost * amount / 60), weight * amount / 60)

    def __str__(self):
        return f"-------------------\n" \
               f"Type of ammunition " \
               + super().__str__() + \
               f"Amount: {self.amount}\n" \
               f"-------------------\n\n"


class Weapon(Item):
    def __init__(self,
                 name: str,
                 damage: int,
                 accuracy: int,
                 clip_capacity: int,
                 rate_of_fire: int,
                 feeding: List[Ammunition],
                 cost: int,
                 weight: float):
        super().__init__(name, cost, weight)
        self.damage = damage
        self.accuracy = accuracy
        self.clip_capacity = clip_capacity
        self.rate_of_fire = rate_of_fire
        self.feeding = feeding
        # self.clip = Ammo(feeding[0], 0, 0, clip_capacity)
        self.clip = clip_capacity

    def shoot(self, target: Creature) -> None:
        for shoot in range(self.rate_of_fire):
            if self.clip > 0:
                self.clip -= 1
                if random() < self.accuracy * 0.01:
                    target.take_damage(0, 0, 0, 0, 0, 5, 0, self.damage)
                else:
                    print("Miss")
            else:
                print("Out of ammo")

    def reload(self, ammo: Ammo) -> bool:
        result = False
        if self.clip != self.clip_capacity:
            if self.feeding.index(ammo.type_of_ammunition) != ValueError:
                if ammo.amount >= self.clip_capacity - self.clip:
                    ammo.amount -= self.clip_capacity - self.clip
                    self.clip += self.clip_capacity - self.clip
                    ammo.weight = ammo.ammo_weight * ammo.amount / 60
                    ammo.cost = ammo.ammo_cost * ammo.amount / 60
                    result = True
                else:
                    print("There is not enough ammo in this")
                    if ammo.amount > 0:
                        self.clip += ammo.amount
                        ammo.amount = 0
                        ammo.weight = 0
                        ammo.cost = 0
                        result = True
                    else:
                        print("And there is no ammo in this")
            else:
                print("This ammo don't fit")
        else:
            print("There is no need to reload")
        return result

    def __bool__(self):
        return not self.name == ''

    def __str__(self):
        return f"-------------------\n" \
               + super().__str__() + \
               f"Damage: {self.damage}\n" \
               f"Accuracy: {self.accuracy}\n" \
               f"Clip capacity: {self.clip_capacity}\n" \
               f"Rate of fire: {self.rate_of_fire}\n" \
               f"Feeding: {self.feeding}\n" \
               f"-------------------\n"


class Armor(Item):
    def __init__(self,
                 name: str,
                 cost: int,
                 weight: int,
                 physical_resistance: int,
                 fire_resistance: int,
                 radiation_resistance: int,
                 chemical_burns_resistance: int,
                 electricity_resistance: int,
                 psy_resistance: int,
                 armor: int,
                 max_weight: int,
                 count_of_containers: int):
        super().__init__(name, cost, weight)
        self.physical_resistance = physical_resistance
        self.fire_resistance = fire_resistance
        self.radiation_resistance = radiation_resistance
        self.chemical_burns_resistance = chemical_burns_resistance
        self.electricity_resistance = electricity_resistance
        self.bleeding_resistance = physical_resistance
        self.psy_resistance = psy_resistance
        self.armor = armor
        self.max_weight = max_weight
        self.count_of_containers = count_of_containers

    def __str__(self):
        return f"-----------------------------\n" \
               + super().__str__() + \
               f"Physical resistance: {self.physical_resistance}\n" \
               f"Fire resistance: {self.fire_resistance}\n" \
               f"Radiation resistance: {self.radiation_resistance}\n" \
               f"Chemical burns resistance: {self.chemical_burns_resistance}\n" \
               f"Electricity resistance: {self.electricity_resistance}\n" \
               f"Bleeding resistance: {self.bleeding_resistance}\n" \
               f"Psy Resistance: {self.psy_resistance}\n" \
               f"Armor: {self.armor}\n" \
               f"Max weight: {self.max_weight}" \
               f"Count of containers: {self.count_of_containers}" \
               f"-----------------------------\n\n"


SEVA = Armor("SEVA",
             cost=25_000,
             weight=10,
             physical_resistance=15,
             fire_resistance=15,
             radiation_resistance=9,
             chemical_burns_resistance=19,
             electricity_resistance=17,
             psy_resistance=20,
             armor=4,
             max_weight=0,
             count_of_containers=2)
None_armor = Armor("None", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def get_weight(item: Item) -> float:
    return item.weight


class Artifact(Item):
    def __init__(self,
                 name: str,
                 cost: int,
                 max_hp: int,
                 physical_resistance: int,
                 fire_resistance: int,
                 radiation_resistance: int,
                 chemical_burns_resistance: int,
                 electricity_resistance: int,
                 bleeding_resistance: int,
                 psy_resistance: int,
                 max_stamina: int,
                 max_weight: int):
        super().__init__(name, cost, 0.5)
        self.max_hp = max_hp
        self.physical_resistance = physical_resistance
        self.fire_resistance = fire_resistance
        self.radiation_resistance = radiation_resistance
        self.chemical_burns_resistance = chemical_burns_resistance
        self.electricity_resistance = electricity_resistance
        self.bleeding_resistance = bleeding_resistance
        self.psy_resistance = psy_resistance
        self.max_stamina = max_stamina
        self.max_weight = max_weight

    def __str__(self):
        return f"-----------------------------\n" \
               + super().__str__() + \
               (f"Max HP: {self.max_hp}\n" if self.max_hp != 0 else f"") + \
               (f"Physical resistance: {self.physical_resistance}\n" if self.physical_resistance != 0 else f"") + \
               (f"Fire resistance: {self.fire_resistance}\n" if self.fire_resistance != 0 else f"") + \
               (f"Radiation resistance: {self.radiation_resistance}\n" if self.radiation_resistance != 0 else f"") + \
               (f"Chemical burns resistance: {self.chemical_burns_resistance}\n"
                if self.chemical_burns_resistance != 0 else f"") + \
               (f"Electricity resistance: {self.electricity_resistance}\n"
                if self.electricity_resistance != 0 else f"") + \
               (f"Bleeding resistance: {self.bleeding_resistance}\n" if self.bleeding_resistance != 0 else f"") + \
               (f"Psy resistance: {self.psy_resistance}\n" if self.psy_resistance != 0 else f"") + \
               (f"Max stamina: {self.max_stamina}\n" if self.max_stamina != 0 else f"") + \
               (f"Max weight: {self.max_weight}\n" if self.max_weight != 0 else f"") + \
               f"-----------------------------\n\n"


class Human(Creature):
    def __init__(self, name: str, fraction: Fraction):
        super().__init__(100, 0, 0, 0, 0, 0, 0, 5, 0, 100)
        self.name = name
        self.fraction = fraction
        self.primary_weapon = Weapon('PMm', 15, 53, 8, 1, [Ammunition.Ammo9x18, Ammunition.Ammo9x18_Piercing],
                                     400, 0.53)
        self.secondary_weapon = Weapon('', 0, 0, 0, 0, [Ammunition.AmmoNone], 0, 0.0)
        self.balance = 0
        self.backpack = []
        # self.backpack = List[Item]
        self.weight = 0.53
        self.max_weight = 50
        self.wearing_armor = None_armor
        self.count_of_containers = 2
        # self.artifacts = List[Artifact]
        self.artifacts = []

    def put_on_armor(self, armor: Armor):
        self.physical_resistance -= self.wearing_armor.physical_resistance
        self.fire_resistance -= self.wearing_armor.fire_resistance
        self.radiation_resistance -= self.wearing_armor.radiation_resistance
        self.chemical_burns_resistance -= self.wearing_armor.chemical_burns_resistance
        self.electricity_resistance -= self.wearing_armor.electricity_resistance
        self.bleeding_resistance -= self.wearing_armor.physical_resistance
        self.psy_resistance -= self.wearing_armor.psy_resistance
        self.armor -= self.wearing_armor.armor
        self.max_weight -= self.wearing_armor.max_weight
        self.count_of_containers -= self.wearing_armor.count_of_containers

        self.wearing_armor = armor
        self.physical_resistance += armor.physical_resistance
        self.fire_resistance += armor.fire_resistance
        self.radiation_resistance += armor.radiation_resistance
        self.chemical_burns_resistance += armor.chemical_burns_resistance
        self.electricity_resistance += armor.electricity_resistance
        self.bleeding_resistance += armor.physical_resistance
        self.psy_resistance += armor.psy_resistance
        self.armor += armor.armor
        self.max_weight += armor.max_weight
        self.count_of_containers += armor.count_of_containers

    def put_on_artifact(self, artifact: Artifact):
        if self.artifacts.__len__() < self.count_of_containers:  # TODO: ??????????????
            self.artifacts.append(artifact)
            self.weight += artifact.weight
            self.max_hp += artifact.max_hp
            self.physical_resistance += artifact.physical_resistance
            self.fire_resistance += artifact.fire_resistance
            self.radiation_resistance += artifact.radiation_resistance
            self.chemical_burns_resistance += artifact.chemical_burns_resistance
            self.electricity_resistance += artifact.electricity_resistance
            self.bleeding_resistance += artifact.bleeding_resistance
            self.psy_resistance += artifact.psy_resistance
            self.max_stamina += artifact.max_stamina
            self.max_weight += artifact.max_weight
        else:
            print("There is no place for artifacts")

    def remove_artifact(self, artifact: Artifact):
        if self.artifacts.index(artifact) != ValueError:
            self.artifacts.remove(artifact)
            self.weight -= artifact.weight
            self.max_hp -= artifact.max_hp
            self.physical_resistance -= artifact.physical_resistance
            self.fire_resistance -= artifact.fire_resistance
            self.radiation_resistance -= artifact.radiation_resistance
            self.chemical_burns_resistance -= artifact.chemical_burns_resistance
            self.electricity_resistance -= artifact.electricity_resistance
            self.bleeding_resistance -= artifact.bleeding_resistance
            self.psy_resistance -= artifact.psy_resistance
            self.max_stamina -= artifact.max_stamina
            self.max_weight -= artifact.max_weight

    def shoot_from_primary(self, target: Creature) -> None:
        if self.primary_weapon:
            self.primary_weapon.shoot(target)
        else:
            print("Primary weapon is not found")

    def get_primary_weapon(self, weapon: Weapon) -> None:
        self.weight -= self.primary_weapon.weight
        self.primary_weapon = weapon
        self.weight += weapon.weight

    def get_secondary_weapon(self, weapon: Weapon) -> None:
        self.weight -= self.secondary_weapon.weight
        self.secondary_weapon = weapon
        self.weight += weapon.weight

    def shoot_from_secondary(self, target: Creature) -> None:
        if self.secondary_weapon:
            self.secondary_weapon.shoot(target)
        else:
            print("Secondary weapon is not found")

    def reload_primary_weapon(self) -> None:
        reloaded = False
        i = 0
        while len(self.backpack) != 0 and \
                (not reloaded or self.primary_weapon.clip < self.primary_weapon.clip_capacity) and \
                i < self.backpack.__len__():
            # if type(self.backpack[i]) is Ammo
            # if issubclass(type(self.backpack[i]), Ammo)
            if isinstance(self.backpack[i], Ammo):  # Экземпляр
                old_weight = get_weight(self.backpack[i])
                reloaded = self.primary_weapon.reload(self.backpack[i])
                if reloaded:
                    self.weight -= old_weight
                    self.weight += get_weight(self.backpack[i])
            i += 1
        if not reloaded:
            print("Failed to reload")

    def put_in_a_backpack(self, item: Item) -> None:
        self.backpack.append(item)  # TODO: ????????????????????
        self.weight += item.weight

    def throw_out_of_backpack(self, item: Item) -> None:
        if self.backpack.index(item) != ValueError:
            # self.backpack.pop(self.backpack.index(item))
            self.backpack.remove(item)
            self.weight -= item.weight

    def __str__(self):
        return f"=============================\n" \
               f"Name: {self.name}\n" \
               f"Balance: {self.balance}\n" \
               f"Weight: {self.weight}\n" \
               f"Primary:\n{self.primary_weapon}" \
               f"Secondary:\n{self.secondary_weapon}" \
               f"Inventory: [\n\n" \
               f"{''.join([str(i) for i in self.backpack])}]\n" \
               + super().__str__() + \
               f"=============================\n"


class Monster(Creature):
    def __init__(self,
                 max_hp: int,
                 physical_resistance: int,
                 fire_resistance: int,
                 radiation_resistance: int,
                 chemical_burns_resistance: int,
                 electricity_resistance: int,
                 bleeding_resistance: int,
                 psy_resistance: int,
                 armor: int,
                 max_stamina: int):
        super().__init__(max_hp, physical_resistance, fire_resistance, radiation_resistance,
                         chemical_burns_resistance, electricity_resistance, bleeding_resistance,
                         psy_resistance, armor, max_stamina)


class Animal(Creature):
    def __init__(self,
                 max_hp: int,
                 physical_resistance: int,
                 fire_resistance: int,
                 radiation_resistance: int,
                 chemical_burns_resistance: int,
                 electricity_resistance: int,
                 bleeding_resistance: int,
                 psy_resistance: int,
                 armor: int,
                 max_stamina: int,
                 damage: int):
        super().__init__(max_hp, physical_resistance, fire_resistance, radiation_resistance,
                         chemical_burns_resistance, electricity_resistance, bleeding_resistance,
                         psy_resistance, armor, max_stamina)
        self.damage = damage

    def bite(self, target: Creature) -> None:
        target.take_damage(self.damage, 0, 10, 0, 0, 10, 0, 0)


class BlindDog(Animal):
    def __init__(self):
        super().__init__(50, 20, 10, 60, 30, 10, 25, 10, 15, 150, 10)


class Battery(Artifact):
    def __init__(self):
        super().__init__('Battery', 6000, 0, 0, 0, -1, 0, 0, 0, 0, 2, 0)


class Shell(Artifact):  # Пустышка
    def __init__(self):
        super().__init__('Shell', 12000, 0, 0, 0, -2, 0, 0, 0, 0, 4, 0)


class Snowflake(Artifact):
    def __init__(self):
        super().__init__('Snowflake', 18000, 0, 0, 0, -3, 0, 0, 0, 0, 6, 0)


class Soul(Artifact):
    def __init__(self):
        super().__init__('Soul', 6000, 2, 0, 0, -2, 0, 0, 0, 0, 0, 0)


class Kolobok(Artifact):
    def __init__(self):
        super().__init__('Kolobok', 12000, 4, 0, 0, -2, 0, 0, 0, 0, 0, 0)


class Firefly(Artifact):
    def __init__(self):
        super().__init__('Firefly', 18000, 6, 0, 0, -3, 0, 0, 0, 0, 0, 0)


class MamasBeads(Artifact):
    def __init__(self):
        super().__init__('Mama\'s Beads', 6000, 0, 0, 0, -1, 0, 0, 2, 0, 0, 0)


class Eye(Artifact):
    def __init__(self):
        super().__init__('Eye', 12000, 0, 0, 0, -2, 0, 0, 4, 0, 0, 0)


class Flame(Artifact):
    def __init__(self):
        super().__init__('Flame', 18000, 0, 0, 0, -3, 0, 0, 6, 0, 0, 0)


class NightStar(Artifact):
    def __init__(self):
        super().__init__('NightStar', 6000, 0, 0, 0, -1, 0, 0, 0, 0, 0, max_weight=4)


class Gravi(Artifact):
    def __init__(self):
        super().__init__('Gravi', 12000, 0, 0, 0, -2, 0, 0, 0, 0, 0, max_weight=8)


class Goldfish(Artifact):
    def __init__(self):
        super().__init__('Goldfish', 18000, 0, 0, 0, -3, 0, 0, 0, 0, 0, max_weight=12)


class Jellyfish(Artifact):
    def __init__(self):
        super().__init__('Jellyfish', 4000, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0)


class Wrenched(Artifact):
    def __init__(self):
        super().__init__('Wrenched', 8000, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0)


class Bubble(Artifact):
    def __init__(self):
        super().__init__('Bubble', 12000, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0)


if __name__ == '__main__':
    my_Stalker = Human('Alexander Degtyarev', Fraction.LONER)
    SVD = Weapon('SVD', 89, 88, 10, 1, [Ammunition.Ammo7_62x54], 16000, 4.9)
    bandit = Human('Bandit', Fraction.BANDIT)

    my_Stalker.get_primary_weapon(SVD)
    my_Stalker.shoot_from_primary(bandit)
    print(bandit.hp)
    my_Stalker.shoot_from_secondary(bandit)

    dog_tail = Item('Dog tail', 50, 0.3)
    my_Stalker.put_in_a_backpack(dog_tail)
    ammo_pack7_62x54 = Ammo(Ammunition.Ammo7_62x54, 2400, 0.48, 5)
    my_Stalker.put_in_a_backpack(ammo_pack7_62x54)
    art1 = Firefly()
    my_Stalker.put_in_a_backpack(art1)
    my_Stalker.put_in_a_backpack(dog_tail)
    print(my_Stalker)

    print(my_Stalker.primary_weapon.clip)
    my_Stalker.reload_primary_weapon()
    print(my_Stalker.backpack[1])
    print(my_Stalker.primary_weapon.clip)
    print(my_Stalker)

    my_Stalker.put_on_armor(SEVA)
    print(my_Stalker)
    my_Stalker.put_on_artifact(Flame())
    print(my_Stalker.bleeding_resistance)
    my_Stalker.remove_artifact(my_Stalker.artifacts[0])
    print(my_Stalker.bleeding_resistance)

    my_Stalker.put_on_artifact(Flame())
    my_Stalker.put_on_artifact(Flame())
    my_Stalker.put_on_artifact(Flame())
    my_Stalker.put_on_artifact(Flame())
    my_Stalker.put_on_artifact(Flame())
    my_Stalker.put_on_artifact(Flame())
    print(my_Stalker.artifacts)
    print(my_Stalker.bleeding_resistance)

    dog = BlindDog()
    for iterator in range(12):
        my_Stalker.shoot_from_primary(dog)
    print(my_Stalker.primary_weapon.clip)
    ammo_pack7_62x54 = Ammo(Ammunition.Ammo7_62x54, 2400, 0.48, 60)
    my_Stalker.put_in_a_backpack(ammo_pack7_62x54)
    my_Stalker.reload_primary_weapon()
    print(f"Inventory: [\n\n{''.join([str(i) for i in my_Stalker.backpack])}]\n")
    print(my_Stalker.primary_weapon.clip)
