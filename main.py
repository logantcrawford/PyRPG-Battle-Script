from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire Ball", 10, 100, "black")
thunder = Spell("Thunder Bolt", 10, 124, "black")
blizzard = Spell("Freezing Blizzard", 10, 100, "black")
meteor = Spell("Meteor Strike", 25, 250, "black")
quake = Spell("Fire Ball", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")
curaga = Spell("Cura", 18, 500, "white")

# Create Potion Items
potion = Item("Restore", "potion", "Heals 50 HP", 50)
hipotion = Item("Large Restore", "potion", "Heals 100 HP", 100)
superpotion = Item("Full Restore", "potion", "Heals all HP", 9999)

# Create Elixer Items
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega Elixer", "elixer", "Fully restores HP/MP of entire party", 9999)

# Create Attack Items
grenade = Item("Cherry Bomb", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 7}, {"item": hipotion, "quantity": 2}, 
                {"item": superpotion, "quantity": 1}, {"item": elixer, "quantity": 2}, 
                {"item": hielixer, "quantity": 1}, {"item": grenade, "quantity": 1}]

enemy_spells1 = [fire, thunder, blizzard, meteor, cure, cura, curaga]
enemy_spells2 = [fire, cure]


# People         name,     hp,  mp, atk,df, magic,         items
player1 = Person("Valos:", 500, 45, 60, 34, player_spells, player_items)
player2 = Person("Marth:", 460, 55, 75, 34, player_spells, player_items)
player3 = Person("Roy:  ", 250, 100, 80, 34, player_spells, player_items)

# Enemies
enemy1 = Person("Imp   ", 300, 40, 60, 25, enemy_spells2, [])
enemy2 = Person("Magus ", 1200, 160, 160, 25, enemy_spells1, [])
enemy3 = Person("Imp   ", 300, 40, 60, 25, enemy_spells2, [])
enemy4 = Person("Imp   ", 300, 40, 60, 25, enemy_spells2, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3, enemy4]

running = True
i = 0

print("\n" + bcolors.FAIL + bcolors.BOLD + "An enemy challenges you." + bcolors.ENDC)

while running:
    print("-------------------")
    print("\n")
    print("NAME              HP                                      MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(bcolors.OKBLUE + player.name.replace(" ", "").replace(":", "") + bcolors.ENDC + " attacks " + bcolors.OKBLUE + enemies[enemy].name.replace(" ", "") + bcolors.ENDC + " for", dmg, "points of damage." + bcolors.ENDC)
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has fainted.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" +bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + player.name.replace(" ", "") + bcolors.ENDC + " uses " + bcolors.OKBLUE + spell.name + bcolors.ENDC + " and heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + player.name.replace(" ", "").replace(":", "") + bcolors.ENDC + " strikes " + bcolors.OKBLUE + enemies[enemy].name.replace(" ", "") + bcolors.ENDC + " with " + bcolors.OKBLUE + spell.name + bcolors.ENDC + " dealing", str(magic_dmg), "points of damage." + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has fainted." + bcolors.ENDC)
                    del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "No " + item.name + "s left..." + bcolors.ENDC + "\n")
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP." + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "Mega Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP." + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.OKBLUE + player.name.replace(" ", "").replace(":", "") + bcolors.ENDC + " uses " + bcolors.OKBLUE + item.name + bcolors.ENDC + ", dealing", str(item.prop), "points of damage to " + bcolors.OKBLUE + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has fainted." + bcolors.ENDC)
                    del enemies[enemy]

    # Check if battle is over.
    defeated_enemies = 0
    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    # Check if player won.
    if defeated_enemies == 2:
        print("\n" + bcolors.OKGREEN + "You defeated the enemies!" + bcolors.ENDC)
        for player in players:
            player.get_stats()
        print("-------------------")
        running = False
    # Check is enemies won.   
    if defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    # Enemy AI attack phase
    print("-------------------")
    print(bcolors.FAIL + "Enemy Turn" + bcolors.ENDC)
    for enemy in enemies:    

        enemy_choice = random.randrange(0, 3)

        if enemy_choice == 0:
            # Choose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.OKBLUE + enemy.name.replace(" ", "") + bcolors.ENDC + " attacks " + bcolors.OKBLUE + players[target].name.replace(" ", "").replace(":", "") + bcolors.ENDC + " for", str(enemy_dmg), "HP.")
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + bcolors.ENDC + " uses " + bcolors.OKBLUE + spell.name + bcolors.ENDC + " and heals for", str(magic_dmg), "HP.")
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + bcolors.ENDC + " strikes with " + bcolors.OKBLUE + spell.name + bcolors.ENDC + " dealing", str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "").replace(":", "") + "." + bcolors.ENDC)
                
                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + players[target].name.replace(" ", "").replace(":", "") + " has fainted." + bcolors.ENDC)
                    del players[target]
            #print("Enemy chose", spell, "damage is", magic_dmg)
        elif enemy_choice == 2:
            print("choice 3")
            '''
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "No " + item.name + "s left..." + bcolors.ENDC + "\n")
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP." + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "Mega Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP." + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.OKBLUE + player.name.replace(" ", "").replace(":", "") + bcolors.ENDC + " uses " + bcolors.OKBLUE + item.name + bcolors.ENDC + ", dealing", str(item.prop), "points of damage to " + bcolors.OKBLUE + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has fainted." + bcolors.ENDC)
                    del enemies[enemy]            
            '''