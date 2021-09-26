import os
import json
from prettytable import PrettyTable
import prettytable

def get_prices_from_json(dirname):
    prices_list = []

    for date_dirname in os.listdir(f"./data/{dirname}"):
        f = open(f"./data/{dirname}/{date_dirname}/result_list.json")
        data = json.load(f)

        prices_list.append(data[0]["prices"][:1])

    return prices_list

def main():
    table = PrettyTable()
    table.hrules = prettytable.ALL
    is_date_added_to_field_names = False
    field_names = ["NFT name"]
    for dirname in os.listdir('./data'):
        # if dirname == "Claire" or dirname == "Stormy Easter ‘21" or dirname == "Syrup Soak":
        if not is_date_added_to_field_names:
            field_names.extend(os.listdir(f"./data/{dirname}"))
            table.field_names = field_names
            is_date_added_to_field_names = True

        prices_list = get_prices_from_json(dirname)
        row = [dirname]
        for price in prices_list:
            row.append(price)

        table.add_row(row)
        
    print(table)
                
        

if __name__ == "__main__":
    main()