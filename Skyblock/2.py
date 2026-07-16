import Calculator
from Calculator import main
import json

with open('RECIPES.json', 'r') as file:
    data = json.load(file)

main(data["HYPERION1"])
