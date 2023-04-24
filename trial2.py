import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Spanish word tiers
tier1 = ["hola", "adios", "gracias", "por favor", "amigo", "casa", "agua", "gato", "perro", "comer", "beber", "dormir",
         "trabajo", "escuela", "familia"]
tier2 = ["manzana", "biblioteca", "mariposa", "elefante", "telefono", "computadora", "refrigerador", "jirafa", "ciudad",
         "pantalones", "zapatos", "camisa", "pelota", "juego", "television"]
tier3 = ["desafortunadamente", "responsabilidad", "entusiasmo", "enfurecido", "desarrollador", "independiente",
         "conmemorativo", "extraordinario", "procrastinar", "ambiguedad", "arqueologia", "controversia", "entrometido",
         "hipopotamo", "paralelepipedo"]

resources = {"sticks": 0, "rocks": 0, "logs": 0, "chunks": 0, "iron": 0, "planks": 0, "diamonds": 0, "gems": 0}
tools = {"axe": False, "chisel": False, "pickaxe": False, "saw": False, "wizard_staff": False}
learned_words = []


class SpanishMiningGame(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Spanish Mining Game")
        self.geometry("800x600")

        # Create and place other widgets with grid()

        # Add a new label for displaying the inventory
        self.inventory_label = tk.Label(self, text="", font=("Arial", 14))
        self.inventory_label.grid(row=7, column=6, columnspan=2)


        self.equipment_label = tk.Label(self, text="", font=("Arial", 14), anchor="e")
        self.equipment_label.grid(row=7, column=4, columnspan=2)

        self.label = tk.Label(self, text="", font=("Arial", 14, "bold"))
        self.label.grid(row=0, column=0, columnspan=6)



        self.word_label = tk.Label(self, text="", font=("Arial", 14))
        self.word_label.grid(row=1, column=0, columnspan=6)

        self.score_label = tk.Label(self, text="", font=("Arial", 14))
        self.score_label.grid(row=2, column=0, columnspan=6)

        # Create and place entry widget with grid()
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.grid(row=5, column=0, columnspan=6)

        # Bind enter key to process_input method
        self.bind('<Return>', lambda event: self.process_input())

        # Load images
        wood_image = Image.open("mine_wood.png").resize((100, 100))
        wood_photo = ImageTk.PhotoImage(wood_image)

        stone_image = Image.open("mine_stone.png").resize((100, 100))
        stone_photo = ImageTk.PhotoImage(stone_image)

        craft_image = Image.open("craft.png").resize((100, 100))
        craft_photo = ImageTk.PhotoImage(craft_image)

        marketplace_image = Image.open("marketplace.png").resize((100, 100))
        marketplace_photo = ImageTk.PhotoImage(marketplace_image)

        equipment_image = Image.open("inventory.png").resize((100, 100))
        equipment_photo = ImageTk.PhotoImage(equipment_image)

        inventory_image = Image.open("inventory.png").resize((100, 100))
        inventory_photo = ImageTk.PhotoImage(inventory_image)

        plank_image = Image.open("craft_plank.png").resize((100, 100))
        plank_photo = ImageTk.PhotoImage(plank_image)

        fight_demon_image = Image.open("fight_demon.png").resize((100, 100))
        fight_demon_photo = ImageTk.PhotoImage(fight_demon_image)
        # Create buttons with images
        self.wood_button = tk.Button(self, image=wood_photo, command=self.mine_wood)
        self.wood_button.image = wood_photo
        self.wood_button.grid(row=3, column=0)

        self.stone_button = tk.Button(self, image=stone_photo, command=self.mine_stone)
        self.stone_button.image = stone_photo
        self.stone_button.grid(row=3, column=1)

        self.craft_button = tk.Button(self, image=craft_photo, command=self.craft_tool)
        self.craft_button.image = craft_photo
        self.craft_button.grid(row=3, column=2)


        self.marketplace_button = tk.Button(self, image=marketplace_photo, command=self.buy_word)
        self.marketplace_button.image = marketplace_photo
        self.marketplace_button.grid(row=3, column=3)

        self.inventory_button = tk.Button(self, image=inventory_photo, command=self.show_inventory)
        self.inventory_button.image = inventory_photo
        self.inventory_button.grid(row=6, column=6)

        self.equipment_button = tk.Button(self, image=equipment_photo, command=self.show_equipment)
        self.equipment_button.image = equipment_photo
        self.equipment_button.grid(row=6, column=5, padx=10)

        self.fight_demon_button = tk.Button(self, image=fight_demon_photo, command=self.fight_demon)
        self.fight_demon_button.image = fight_demon_photo
        self.fight_demon_button.grid(row=3, column=5)

        self.plank_button = tk.Button(self, image=plank_photo, command=self.craft_plank)
        self.plank_button.image = plank_photo
        self.plank_button.grid(row=3, column=6)

        self.action = "start"
        self.user_input = ""

        self.bind('<Return>', lambda event: self.process_input())

    def process_input(self):
        self.user_input = self.entry.get()
        self.entry.delete(0, tk.END)

        if self.action == "start":
            self.start_game()
        elif self.action == "choose_action":
            self.choose_action()
        elif self.action in ["wood1", "wood2", "stone1", "stone2", "stone3"]:
            self.check_mined_resource()
        elif self.action == "craft_tool":
            crafted = self.craft_item(self.user_input)
            if crafted:
                self.label["text"] = f"You crafted a {self.user_input}."
            else:
                self.label["text"] = "You don't have the necessary resources or already own the tool."
            self.action = "choose_action"
        elif self.action == "buy_word":
            if self.user_input.lower() == "yes":
                word_tier = random.randint(1, 3)
                new_word = self.get_word(word_tier)
                if new_word not in learned_words:
                    learned_words.append(new_word)
                resources["gems"] -= 1
                self.label["text"] = f"You bought the word '{new_word}'. You have {resources['gems']} gems left."
            else:
                self.label["text"] = "You already know this word. Try again."
            self.action = "choose_action"
        elif self.action == "fight_demon":
            self.defeat_demon(self.user_input)
        elif self.user_input.lower() == "c":  # Check for "c" input for crafting
            self.craft_tool()
        else:
            self.label["text"] = "Invalid option. Try again"
            self.action = "choose_action"

    def start_game(self):
        self.label[
            "text"] = "What would you like to do? (a: mine wood, s: mine stone, craft, marketplace, inventory, fight demon)"
        self.action = "choose_action"

    def choose_action(self):
        if self.user_input == "a":
            self.mine_wood()
        elif self.user_input == "s":
            self.mine_stone()
        elif self.user_input == "c":
            self.craft_tool()
        elif self.user_input == "marketplace":
            self.buy_word()
        elif self.user_input == "inventory":
            self.show_inventory()
        elif self.user_input == "fight demon":
            self.fight_demon()
        else:
            self.label["text"] = "Invalid option. Try again"

    def get_word(self, tier):
        if tier == 1:
            return random.choice(tier1)
        elif tier == 2:
            return random.choice(tier2)
        elif tier == 3:
            return random.choice(tier3)

    def mine_resource(self, resource, tier):
        word = self.get_word(tier)
        self.label["text"] = f"Type the Spanish word for '{word}': "
        self.action = resource
        return word

    def mine_wood(self):
        if not tools["axe"]:
            word = self.mine_resource("wood", 1)
            self.action = "wood1"
        else:
            word = self.mine_resource("wood", 2)
            self.action = "wood2"

    def mine_stone(self):
        if not tools["chisel"]:
            word = self.mine_resource("stone", 1)
            self.action = "stone1"
        else:
            tier = 2 if not tools["pickaxe"] else 3
            word = self.mine_resource("stone", tier)
            self.action = "stone2" if tier == 2 else "stone3"

    def check_mined_resource(self):
        if self.action in ["wood1", "wood2", "stone1", "stone2", "stone3"]:
            resource_word = self.user_input
            if resource_word not in learned_words:
                learned_words.append(resource_word)

            if self.action == "wood1":
                if resource_word in tier1:
                    resources["sticks"] += 1
                    self.update_inventory()  # Add this line here
                    self.label["text"] = f"Received 1 stick. Total sticks: {resources['sticks']}"
                    if random.random() <= 0.05:
                        resources["gems"] += 1
                        self.update_inventory()  # Add this line here
                        self.label["text"] += f"\nFound 1 gem! Total gems: {resources['gems']}"
                else:
                    self.label["text"] = "Incorrect word. Keep trying!"

            elif self.action == "wood2":
                if resource_word in tier2:
                    resources["logs"] += 1
                    self.update_inventory()  # Add this line here
                    self.label["text"] = f"Received 1 log. Total logs: {resources['logs']}"
                    if random.random() <= 0.05:
                        resources["gems"] += 1
                        self.update_inventory()  # Add this line here
                        self.label["text"] += f"\nFound 1 gem! Total gems: {resources['gems']}"
                else:
                    self.label["text"] = "Incorrect word. Keep trying!"

            elif self.action == "stone1":
                if resource_word in tier1:
                    resources["rocks"] += 1
                    self.update_inventory()  # Add this line here
                    self.label["text"] = f"Received 1 rock. Total rocks: {resources['rocks']}"
                else:
                    self.label["text"] = "Incorrect word. Keep trying!"

            elif self.action == "stone2":
                if resource_word in tier2:
                    resources["chunks"] += 1
                    self.update_inventory()  # Add this line here
                    self.label["text"] = f"Received 1 chunk. Total chunks: {resources['chunks']}"
                    if random.random() <= 0.1:
                        resources["diamonds"] += 1
                        self.update_inventory()  # Add this line here
                        self.label["text"] += f"\nFound 1 diamond! Total diamonds: {resources['diamonds']}"
                else:
                    self.label["text"] = "Incorrect word. Keep trying!"

            elif self.action == "stone3":
                if resource_word in tier3:
                    resources["iron"] += 1
                    self.update_inventory()  # Add this line here
                    self.label["text"] = f"Received 1 iron. Total iron: {resources['iron']}"
                    if random.random() <= 0.1:
                        resources["diamonds"] += 1
                        self.update_inventory()  # Add this line here
                        self.label["text"] += f"\nFound 1 diamond! Total diamonds: {resources['diamonds']}"
                else:
                    self.label["text"] = "Incorrect word. Keep trying!"

        self.action = "choose_action"

        self.action = "choose_action"

    def craft_tool(self):
        self.label["text"] = "What would you like to craft? (axe, chisel, pickaxe, saw, wizard_staff)"
        self.action = "craft_tool"

    def craft_item(self, item):  # New method for crafting items
        crafted = False
        if item == "axe" and not tools["axe"] and resources["rocks"] >= 3 and resources["sticks"] >= 3:
            tools["axe"] = True
            resources["rocks"] -= 3
            resources["sticks"] -= 3
            crafted = True
            self.update_inventory()
        elif item == "chisel" and not tools["chisel"] and resources["rocks"] >= 5 and resources["sticks"] >= 2:
            tools["chisel"] = True
            resources["rocks"] -= 5
            resources["sticks"] -= 2
            crafted = True
        elif item == "pickaxe" and not tools["pickaxe"] and resources["chunks"] >= 3 and resources["sticks"] >= 3:
            tools["pickaxe"] = True
            resources["chunks"] -= 3
            resources["sticks"] -= 3
            crafted = True
        elif item == "saw" and not tools["saw"] and resources["logs"] >= 4 and resources["sticks"] >= 2:
            tools["saw"] = True
            resources["logs"] -= 4
            resources["sticks"] -= 2
            crafted = True
        elif item == "wizard_staff" and not tools["wizard_staff"] and resources["diamonds"] >= 2 and resources[
            "planks"] >= 5 and resources["iron"] >= 5:
            tools["wizard_staff"] = True
            resources["diamonds"] -= 2
            resources["planks"] -= 5
            resources["iron"] -= 5
            crafted = True

        return crafted

    def craft_plank(self):
        if resources["logs"] >= 1 and resources["sticks"] >= 2:
            resources["logs"] -= 1
            resources["sticks"] -= 2
            resources["planks"] += 4
            self.label["text"] = "You crafted 4 planks from 1 log and 2 sticks."
            self.update_inventory()
        else:
            self.label["text"] = "You don't have enough resources to craft planks."
        self.action = "choose_action"

    def buy_word(self):
        self.label["text"] = "Welcome to the marketplace! You can buy new Spanish words for 1 gem each."
        if resources["gems"] > 0:
            resources["gems"] -= 1
            self.update_inventory()
            self.label["text"] += "\nWould you like to buy a new word? (yes/no)"
            self.action = "buy_word"
        else:
            self.label["text"] += "\nYou don't have enough gems to buy words. Keep mining!"
            self.action = "choose_action"

    def show_inventory(self):
        if self.inventory_label["text"] == "":
            inventory_text = "Inventory:\n"
            for item, quantity in resources.items():
                inventory_text += f"{item.capitalize()}: {quantity}\n"
            self.inventory_label["text"] = inventory_text
            self.action = "choose_action"
        else:
            self.inventory_label["text"] = ""

    def update_inventory(self):
        inventory_text = "Inventory:\n"
        for item, quantity in resources.items():
            inventory_text += f"{item.capitalize()}: {quantity}\n"
        self.inventory_label["text"] = inventory_text
    def show_equipment(self):
        if self.equipment_label["text"] == "":
            equipment_text = "Equipment:\n"
            for tool, has_tool in tools.items():
                equipment_text += f"{tool.capitalize()}: {'Yes' if has_tool else 'No'}\n"
            self.equipment_label.config(text=equipment_text, anchor="w")
            self.action = "choose_action"
        else:
            self.equipment_label.config(text="", anchor="w")


    def fight_demon(self):
        if tools["wizard_staff"]:
            self.label["text"] = "You have the wizard staff! Let's fight the demon!"

            word = self.get_word(3)
            if word not in learned_words:
                learned_words.append(word)

            self.label["text"] += f"\nType the Spanish word for '{word}': "
            self.action = "fight_demon"
        else:
            self.label["text"] = "You cannot fight the demon without the wizard staff. Keep mining and crafting!"
            self.action = "choose_action"

    def defeat_demon(self, user_input):
        word = self.get_word(3)
        if user_input == word:
            self.label["text"] = "You have defeated the demon! Congratulations!"
            self.quit()
        else:
            self.label["text"] = "You entered the wrong word. The demon has defeated you."
            self.quit()

    # ... (previous code remains the same)
    def choose_action(self):
        if self.user_input == "a":
            self.mine_wood()
        elif self.user_input == "s":
            self.mine_stone()
        # ... (previous code remains the same)
        elif self.user_input == "inventory":
            self.show_inventory()
    def process_input(self):
        self.user_input = self.entry.get()
        self.entry.delete(0, tk.END)

        if self.action == "start":
            self.start_game()
        elif self.action == "choose_action":
            self.choose_action()
        elif self.action in ["wood1", "wood2", "stone1", "stone2", "stone3"]:
            self.check_mined_resource()
        elif self.action == "craft_tool":
            crafted = self.craft_item(self.user_input)
            if crafted:
                self.label["text"] = f"You crafted a {self.user_input}."
            else:
                self.label["text"] = "You don't have the necessary resources or already own the tool."
            self.action = "choose_action"
        elif self.action == "buy_word":
            if self.user_input.lower() == "yes":
                word_tier = random.randint(1, 3)
                new_word = self.get_word(word_tier)
                if new_word not in learned_words:
                    learned_words.append(new_word)
                resources["gems"] -= 1
                self.label["text"] = f"You bought the word '{new_word}'. You have {resources['gems']} gems left."
            else:
                self.label["text"] = "You already know this word. Try again."
            self.action = "choose_action"
        elif self.action == "fight_demon":
            self.defeat_demon(self.user_input)


app = SpanishMiningGame()
app.mainloop()
