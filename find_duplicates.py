"""Module for functions to delete duplicate files"""

import csv

# find . ! -empty -type f -exec md5sum {} + | sort | uniq -w32 -dD
duplicates = {}
with open("all-transactions.csv", encoding="utf-8") as f:
    spam_reader = csv.reader(f, delimiter=" ", quotechar="|")
    count = 0
    for row in spam_reader:
        if count != 0:
            transaction_tokens = ", ".join(row).split(",")
            transaction = "-".join(transaction_tokens[1:])
            unique_id = transaction_tokens[0]
            if transaction not in duplicates:
                duplicates[transaction] = [unique_id]
            else:
                duplicates[transaction].append(unique_id)

        count += 1

    with open("duplicate_transactions.txt", "w", encoding="utf-8") as duplicates_txt:
        for key, values in duplicates.items():
            if len(values) > 1:
                print(key, values)
                duplicates_txt.write(", ".join(values + [key]) + "\n")
