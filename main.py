from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 30, 800, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

# Create some items
potion = Item("Potion", "potion", "Heals 100 HP", 100)
hipotion = Item("Hi-Potion", "potion", "Heals 400 HP", 400)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega-Elixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]


#Instantiate People
player1 = Person("Valos", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Steve", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot", 3089, 174, 288, 34, player_spells, player_items)
enemy = Person("Magus", 11200, 701, 525, 25, [], [])

players = [player1, player2, player3]

running = True
i=0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("===================")

    print("\n")
    print("NAME                     HP                                  MP")
    for player1 in players:
        player1.get_stats()

    print("\n")

    enemy.get_enemy_stats()

    for player1 in players:

        player1.choose_action()
        index = int(input("        Choose action: ")) -1

        if index == 0:
            print(" ")
            dmg = player1.generate_damage()
            enemy.take_damage(dmg)
            print(player1.name, "attacked", enemy.name, "for", dmg, "points of damage.")

        elif index == 1:
            print(" ")
            player1.choose_magic()
            magic_choice = int(input("        Choose magic: ")) -1

            if magic_choice == -1:
                continue

            spell = player1.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player1.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP!\n" + bcolors.ENDC)
                continue

            player1.reduce_mp(spell.cost)

            if spell.type == "white":
                player1.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif index == 2:
            print(" ")
            player1.choose_items()
            item_choice = int(input("        Choose item: ")) -1

            if item_choice == -1:
                    continue

            item = player1.items[item_choice]["item"]

            if player1.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player1.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player1.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player1.hp = player1.maxhp
                    player1.mp = player1.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + player1.name + "'s " + item.name + " deals", enemy.name, str(item.prop),
                      "points of damage" + bcolors.ENDC)


    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemy.generate_damage()



    players[target].take_damage(enemy_dmg)
    print(enemy.name, "attacks", players.name, "for", enemy_dmg, "points of damage.")

    print("-----------------")

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    elif player1.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False
