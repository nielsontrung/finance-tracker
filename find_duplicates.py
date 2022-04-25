import csv
# find . ! -empty -type f -exec md5sum {} + | sort | uniq -w32 -dD
duplicates = {}
with open('all-transactions.csv') as f:
    spamreader = csv.reader(f, delimiter=' ', quotechar='|')
    count = 0
    for row in spamreader:
        if count != 0:
            transaction_tokens = ', '.join(row).split(',')
            transaction = '-'.join(transaction_tokens[1:])
            id = transaction_tokens[0]
            if not transaction in duplicates:
                duplicates[transaction] = [id]
            else:
                duplicates[transaction].append(id)

        count += 1

    with open('duplicate_transactions.txt', 'w') as duplicates_txt:
        for key in duplicates.keys():
            if len(duplicates[key]) > 1:
                print(key, duplicates[key])
                duplicates_txt.write(', '.join(duplicates[key]+[key]) + '\n')
    duplicates_txt.close()
