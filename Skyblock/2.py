import Skyblock.Calculator as Calculator
from Skyblock.Calculator import main
import json

with open('RECIPES.json', 'r') as file:
    data = json.load(file)

main(data["HYPERION1"])
