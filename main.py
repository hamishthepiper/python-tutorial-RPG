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

enemy1 = Person("Imp  ", 1250, 130, 560, 325, [], [])
enemy2 = Person("Magus", 11200, 701, 525, 25, [], [])
enemy3 = Person("Imp  ", 1250, 130, 560, 325, [], [])

players = [player2, player1, player3]
enemies = [enemy1, enemy2, enemy3]
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

    for enemy in enemies:

        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        index = int(input("        Choose action: ")) -1

        if index == 0:
            print(" ")
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(player.name, "attacked", enemies[enemy].name, "for", dmg, "points of damage.")

        elif index == 1:
            print(" ")
            player.choose_magic()
            magic_choice = int(input("        Choose magic: ")) -1

            #Uses "0" as an option to go back in the menu
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP!\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + "HP" + bcolors.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(player.name, "casts", spell.name, "against", enemies[enemy].name, "for", str(magic_dmg), "points of damage.")

                #enemy.take_damage(magic_dmg)
                #print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif index == 2:
            print(" ")
            player.choose_items()
            item_choice = int(input("        Choose item: ")) -1

            #Uses "0" as an option to go back in the menu
            if item_choice == -1:
                    continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

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
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + player.name + "'s " + item.name + " deals", enemies[enemy].name, str(item.prop),
                      "points of damage" + bcolors.ENDC)


    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemies[0].generate_damage()

    players[target].take_damage(enemy_dmg)
    '''
    Need to find a way to specify what the enemy's target was and what kind of damage they took. Possibly use a function that would be called from
        print(players.name)
    '''
    print(enemies[enemy].name, "attacks for", int(enemy_dmg), "points of damage.")

    if enemy.get_hp() == 0:
        print("-----------------")
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    elif player.get_hp() == 0:
        print("-----------------")
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False
