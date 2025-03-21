class Inventory:
    def __init__(self):
        self.items = []  # Initialize an empty list to store items

    def add_item(self, item):
        self.items.append(item)
        print(f"{item} added to inventory.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item} removed from inventory.")
        else:
            print(f"{item} not found in inventory.")

    def show_inventory(self):
        if self.items:
            print("Inventory:")
            for item in self.items:
                print(f"- {item}")
        else:
            print("Inventory is empty.")