# Item Spec

# Base Items vs Specific items

base items are items that contain the base stats for an item
base items are used to make specific items that can then be given to a champion

a specific item is an item that initially inherits its base counterpart but also contains stats for item level and item glory

# upgrading items

to updarade an item you use a stat pack, stat packs are themselves items with type=="statPack", this means that they can be bought and applied to specific items to increase their stats

# difference between items and weapons

items and weapons both inherit from the Item class so they will often be lumped in together in places like the shop, they are different because they will have different stats so when you are doing anything that is stat specific with an item you will have to check isinstance() to make sure that you are working on the correct stats