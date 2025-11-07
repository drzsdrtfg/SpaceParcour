import json
import pygame

LEVEL_PATH = "SpaceRunner/Level_0.ldtkl"
with open(LEVEL_PATH, "r", encoding="utf-8") as file:
    level_data = json.load(file)
#print("You have", len(level_data.get("layerInstances")), "layers in your level")
#print("You have", level_data.keys(), "layers in your level")
layers=level_data["layerInstances"]
for layer in layers:
    print (layer["__identifier"])
    if layer["__identifier"]=="Ground":
        tiles=layer["gridTiles"]
print(len(tiles))

for tile in tiles:
    print(tile.get("px"))
    pygame.draw.rect()


pygame.quit()
