from random import choice, uniform
from read_pdf import get_category
from stats import make_stats_js
import datetime

CSV_HEADER = 'id, account, date, year, month, description, category, amount \n'
CSV_FILE = 'all-transactions.csv'


def gen_random_transactions():
    f = open(CSV_FILE, 'w')
    descriptions = ["acura", "auto", "canadian tire", "cdn tire", "compu-care", "megatire", "mitsubishi", "sudsy's", "abercrombie", "denim", "h&m", "old navy", "shoe", "simons", "skechers", "sport chek", "uniqlo", "urban planet", "value village", "vanity", "winners", "zara", "cbe", "john wiley & sons", "quizlet", "resume", "sait", "u of c", "unversity", "vitalsource", "best buy", "logitech", "memory", "microsoft", "newegg", "source", "bacchus", "cineplex", "entertainment", "games", "jagex", "minecraft", "mojang", "spotify", "stampede", "steam", "e-transfer", "fine payment", "fee", "item returned", "eleven", "esso", "gas", "highway", "husk", "mobil@", "petro", "shell", "aliexpress", "amazon", "dollar store", "miniso", "staples", "wal-mart", "canada revenue", "citizenship", "ei canada", "government", "gst canada", "payment canada", "tax refund", "atlantic superstore", "bulk barn", "co-op", "costco", "dominion", "extra foods", "farm boy", "food basics", "fortinos", "freshco", "freshmart", "grocery", "iga", "loblaws", "loeb", "longo's", "market", "maxi", "metro", "mike dean's super food stores", "no frills", "provigo", "quality foods", "quickly", "rabba", "real cdn", "real canadian superstore", "safeway",
                    "save-on-foods", "saveeasy", "sobeys", "steinberg's (supermarket)", "superstore", "thrifty foods", "valu-mart", "independent grocer", "zehrs markets", "ahs", "brunet", "dental", "drug", "dr.", "familiprix", "jean coutu group", "lawtons", "lens", "london drugs", "pharmachoice", "pharmacy", "rexall", "shoppers drug mart", "lowe", "rona", "south peak", "the home depot", "investment", "questrade", "special deposit", "loan", "bell", "fido", "koodo", "rogers", "telus", "other", "cut", "hair", "nail", "protein", "salon", "spa", "a&w", "barcelos", "bbq", "beef", "black bull", "bobby", "breakfast", "brewsters", "cafe", "chatime", "chef", "chianti", "chicken", "chinese", "coco tea", "crunchy", "dairy", "deli", "denny's", "donday", "doordash", "dynasty", "five guys", "food", "grey eagle", "grill", "huong", "irish", "kebab", "kitchen", "korean", "mango", "manrijangsung", "marble", "mcdonald", "moxie's", "nando's", "pho", "pizza", "ramen", "restaurant", "rotisserie", "saigon", "saltlik", "samosa", "shawarma", "ssome", "sushi", "tea", "thai", "vietnam", "wendy's", "wok", "airport", "bus", "park", "transit", "aviva", "cable", "enmax", "insurance", "cash", "withdrawal", "transfer to deposit", "deposit"]
    years = [str(i) for i in range(2014, datetime.date.today().year + 1)]
    months = [str(i).zfill(2) for i in range(1, 13)]
    days = [str(i).zfill(2) for i in range(1, 28)]
    id = 0
    account = '12345XXX67890'
    date, description, category, transaction = ('',) * 4
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
                id += 1
                transaction = ", ".join(
                    (str(id), account, date, year, month, description, category, str(amount))) + '\n'
                f.write(transaction)
    f.close()


def main():
    gen_random_transactions()
    make_stats_js(CSV_FILE, 2014, int(datetime.date.today().year))


if __name__ == '__main__':
    main()
