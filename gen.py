"""Module providing a function printing python version."""

import datetime
import json
from random import choice, uniform
from read_rbc_pdf import get_category

CSV_HEADER = "id, account, date, year, month, description, category, amount \n"
CSV_FILE = "all-transactions.csv"


def gen_random_transactions():
    """generates a csv file 'all-transactions.csv' populated with random transactional data."""
    f = open(CSV_FILE, "w", encoding="utf-8")
    descriptions = [
        "acura",
        "auto",
        "canadian tire",
        "cdn tire",
        "compu-care",
        "megatire",
        "mitsubishi",
        "sudsy's",
        "abercrombie",
        "denim",
        "h&m",
        "old navy",
        "shoe",
        "simons",
        "skechers",
        "sport chek",
        "uniqlo",
        "urban planet",
        "value village",
        "vanity",
        "winners",
        "zara",
        "cbe",
        "john wiley & sons",
        "quizlet",
        "resume",
        "sait",
        "u of c",
        "unversity",
        "vitalsource",
        "best buy",
        "logitech",
        "memory",
        "microsoft",
        "newegg",
        "source",
        "bacchus",
        "cineplex",
        "entertainment",
        "games",
        "jagex",
        "minecraft",
        "mojang",
        "spotify",
        "stampede",
        "steam",
        "e-transfer",
        "fine payment",
        "fee",
        "item returned",
        "eleven",
        "esso",
        "gas",
        "highway",
        "husk",
        "mobil@",
        "petro",
        "shell",
        "aliexpress",
        "amazon",
        "dollar store",
        "miniso",
        "staples",
        "wal-mart",
        "canada revenue",
        "citizenship",
        "ei canada",
        "government",
        "gst canada",
        "payment canada",
        "tax refund",
        "atlantic superstore",
        "bulk barn",
        "co-op",
        "costco",
        "dominion",
        "extra foods",
        "farm boy",
        "food basics",
        "fortinos",
        "freshco",
        "freshmart",
        "grocery",
        "iga",
        "loblaws",
        "loeb",
        "longo's",
        "market",
        "maxi",
        "metro",
        "mike dean's super food stores",
        "no frills",
        "provigo",
        "quality foods",
        "quickly",
        "rabba",
        "real cdn",
        "real canadian superstore",
        "safeway",
        "save-on-foods",
        "saveeasy",
        "sobeys",
        "steinberg's (supermarket)",
        "superstore",
        "thrifty foods",
        "valu-mart",
        "independent grocer",
        "zehrs markets",
        "ahs",
        "brunet",
        "dental",
        "drug",
        "dr.",
        "familiprix",
        "jean coutu group",
        "lawtons",
        "lens",
        "london drugs",
        "pharmachoice",
        "pharmacy",
        "rexall",
        "shoppers drug mart",
        "lowe",
        "rona",
        "south peak",
        "the home depot",
        "investment",
        "questrade",
        "special deposit",
        "loan",
        "bell",
        "fido",
        "koodo",
        "rogers",
        "telus",
        "other",
        "cut",
        "hair",
        "nail",
        "protein",
        "salon",
        "spa",
        "a&w",
        "barcelos",
        "bbq",
        "beef",
        "black bull",
        "bobby",
        "breakfast",
        "brewsters",
        "cafe",
        "chatime",
        "chef",
        "chianti",
        "chicken",
        "chinese",
        "coco tea",
        "crunchy",
        "dairy",
        "deli",
        "denny's",
        "donday",
        "doordash",
        "dynasty",
        "five guys",
        "food",
        "grey eagle",
        "grill",
        "huong",
        "irish",
        "kebab",
        "kitchen",
        "korean",
        "mango",
        "manrijangsung",
        "marble",
        "mcdonald",
        "moxie's",
        "nando's",
        "pho",
        "pizza",
        "ramen",
        "restaurant",
        "rotisserie",
        "saigon",
        "saltlik",
        "samosa",
        "shawarma",
        "ssome",
        "sushi",
        "tea",
        "thai",
        "vietnam",
        "wendy's",
        "wok",
        "airport",
        "bus",
        "park",
        "transit",
        "aviva",
        "cable",
        "enmax",
        "insurance",
        "cash",
        "withdrawal",
        "transfer to deposit",
        "deposit",
    ]
    stop_year = datetime.date.today().year + 1
    start_year = stop_year - 4
    years = [str(i) for i in range(start_year, stop_year)]
    months = [str(i).zfill(2) for i in range(1, 13)]
    days = [str(i).zfill(2) for i in range(1, 28)]
    unique_id = 0
    account = "12345XXX67890"
    date, description, category, transaction = ("",) * 4
    amount = 0

    f.write(CSV_HEADER)

    for year in years:
        for month in months:
            for i in range(8):
                day = choice(days)
                date = "/".join((year, month, day))
                description = choice(descriptions)
                category = get_category(description)
                amount = round(uniform(10.00, 50.00), 2)
                if not category in ["deposit", "government"]:
                    amount = -amount
                unique_id += 1
                transaction = (
                    str(unique_id),
                    account,
                    date,
                    year,
                    month,
                    description,
                    category,
                    str(amount),
                )
                transaction = ", ".join(transaction) + "\n"
                f.write(transaction)
    f.close()


def read_json_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in '{filename}'.")
        return None


# Example usage:
filename = "example.json"
json_data = read_json_file(filename)
if json_data:
    print("JSON data:")
    print(json_data)


CSV_HEADER = "id, account, date, year, month, description, category, amount, points, sourceFile \n"
CSV_FILE = "all-transactions.csv"


def main():
    """"""
    gen_random_transactions()
    current_year = date.today().year
    min_year = current_year - 5
    make_stats_js(CSV_FILE, min_year, int(current_year))


if __name__ == "__main__":
    main()
