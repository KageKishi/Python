import Calculator
import json

with open('RECIPES.json', 'r') as file:
    data = json.load(file)

Calculator.main(data["HYPERION1"])
