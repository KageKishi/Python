"""
Hypixel Skyblock Upgrade Cost Calculator
-----------------------------------------
Fetches LIVE Bazaar prices from the official Hypixel API (public endpoint,
no API key required) and calculates the total cost to gather all
materials needed for an item upgrade (e.g. a Necron's Blade upgrade,
a Pulse Ring upgrade, a Hot Potato Book stack, etc.).

Usage:
    1. Edit the RECIPE dictionary below with the Bazaar product IDs and
       quantities required for your upgrade.
    2. Run: python skyblock_upgrade_cost.py
    3. (Optional) Pass --sell-offer to price using "sell offer" price
       instead of the default "instant buy" price.

Finding product IDs:
    Bazaar product IDs are usually the item's internal Skyblock ID,
    e.g. "ENCHANTED_LAPIS_LAZULI", "HOT_POTATO_BOOK", "RECOMBOBULATOR_3000".
    You can browse all valid IDs by looking at the raw API response
    (see print_all_products() below) or checking the Skyblock wiki /
    NEU repo for an item's internal name.
"""

import argparse
import sys
import urllib.request
import json

BAZAAR_API_URL = "https://api.hypixel.net/skyblock/bazaar"

# ---------------------------------------------------------------------
# EDIT THIS: define what your upgrade requires -> {product_id: quantity}
# Example below is a rough Necron's Blade -> Hyperion style material list.
# Replace with whatever your actual upgrade needs.
# ---------------------------------------------------------------------
HYPERION = {
    "HOT_POTATO_BOOK": 10,
    "RECOMBOBULATOR_3000": 1,
    "ENCHANTED_LAPIS_LAZULI": 5,
    "ENCHANTED_GOLD_BLOCK": 3,
}


def fetch_bazaar_data():
    """Pull the current bazaar snapshot from the Hypixel API."""
    try:
        with urllib.request.urlopen(BAZAAR_API_URL, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Failed to fetch Bazaar data: {e}", file=sys.stderr)
        sys.exit(1)

    if not data.get("success", False):
        print("Hypixel API returned an unsuccessful response.", file=sys.stderr)
        sys.exit(1)

    return data["products"]


def get_price(products, product_id, use_sell_offer=False):
    """
    Return the relevant unit price for a product.
    - Default ("instant buy"): the lowest sell-order price on the bazaar,
      i.e. what YOU pay to buy instantly -> quick_status['buyPrice'].
    - --sell-offer: price if you instead place a buy order and wait,
      approximated by sellPrice (top of buy orders) -> usually cheaper
      but not instant.
    """
    product = products.get(product_id)
    if product is None:
        return None

    status = product.get("quick_status", {})
    if use_sell_offer:
        price = status.get("sellPrice")
    else:
        price = status.get("buyPrice")

    return price


def calculate_cost(recipe, use_sell_offer=False):
    products = fetch_bazaar_data()

    total = 0.0
    breakdown = []
    missing = []

    for product_id, qty in recipe.items():
        unit_price = get_price(products, product_id, use_sell_offer)
        if unit_price is None:
            missing.append(product_id)
            continue

        line_cost = unit_price * qty
        total += line_cost
        breakdown.append((product_id, qty, unit_price, line_cost))

    return total, breakdown, missing


def print_all_products():
    """Utility: dump all valid Bazaar product IDs, useful for building a recipe."""
    products = fetch_bazaar_data()
    for pid in sorted(products.keys()):
        print(pid)


def main(RECIPE):
    parser = argparse.ArgumentParser(description="Hypixel Skyblock upgrade cost calculator")
    parser.add_argument(
        "--sell-offer",
        action="store_true",
        help="Price using buy-order (sellPrice) instead of instant-buy (buyPrice)",
    )
    parser.add_argument(
        "--list-products",
        action="store_true",
        help="Print every valid Bazaar product ID and exit",
    )
    args = parser.parse_args()

    if args.list_products:
        print_all_products()
        return

    total, breakdown, missing = calculate_cost(RECIPE, use_sell_offer=args.sell_offer)

    price_mode = "Sell-offer (buy order) price" if args.sell_offer else "Instant-buy price"
    print(f"Pricing mode: {price_mode}\n")
    print(f"{'Item':30} {'Qty':>6} {'Unit Price':>15} {'Line Total':>15}")
    print("-" * 68)
    for product_id, qty, unit_price, line_cost in breakdown:
        print(f"{product_id:30} {qty:>6} {unit_price:>15,.1f} {line_cost:>15,.1f}")

    if missing:
        print("\nWarning: no bazaar price found for (not tradeable on bazaar, or "
              "invalid ID):")
        for m in missing:
            print(f"  - {m}")

    print("-" * 68)
    print(f"{'TOTAL':30} {'':6} {'':15} {total:>15,.1f} coins")


if __name__ == "__main__":
    main(HYPERION)