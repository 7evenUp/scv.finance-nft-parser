import requests
import time
import os
import json
import shutil
import pprint

nft_names = {
    "lucky", "lottie", "claire", "syrup-soak",
    "easter-caker", "easter-flipper", "easter-storm", 
    "bullish", "hiccup"
}

def load_data():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "accept": "application/json, text/plain, */*"
    }
    offset = 0
    is_ended = False
    result_dict = {}

    while not is_ended:
        payload = {
            "limit": 50,
            "offset": offset,
            "contractAddr":"0xdf7952b35f24acf7fc0487d01c8d5690a60dba07",
            "sort":"latest",
            "filters":{
                "category":"fixed-price",
                "priceMin": None,
                "priceMax": None,
                "attributes": { }
            }
        }
        url = "https://scv.finance/api/nft/market/search"

        response = requests.post(url=url, headers=headers, json=payload)
        print(f"[#] LOADIND FROM OFFSET № {offset}")
        try:
            data = response.json()["right"]

            if not data:
                is_ended = True
                break

            for item in data:
                image = item["image"]
                name = image[image.rfind('/')+1:image.rfind('.')]
                
                if name in nft_names:
                    token_id = item["token_id"]
                    price = item["price"]

                    if result_dict.get(name):
                        prices_list = result_dict[str(name)]
                        prices_list.append(price)
                    else:
                        result_dict[name] = [price]
                    
                    
                # print(token_id, price, name)

            offset = offset + 50

        except Exception as _ex:
            print(_ex)
        
    print(f"[#] NFTs ARE DOWNLOADED")

    return result_dict

def load_data_into_folders(nfts_list):
    date = time.strftime("%x", time.localtime(time.time())).replace("/", ".")

    for nft_name in nfts_list:
        result_list = [{
            "nft_name": nft_name,
            "prices": nfts_list[nft_name],
            "total_nfts": len(nfts_list[nft_name])
        }]

        if not os.path.exists(f"data/{nft_name}"):
            os.mkdir(f"data/{nft_name}")

        if os.path.exists(f"data/{nft_name}/{date}"):
            shutil.rmtree(f"data/{nft_name}/{date}")
            print("[#] Folder was deleted")

        os.mkdir(f"data/{nft_name}/{date}")

        print(f"[#] Folder called ./data/{nft_name}/{date}/ was created")

        with open(f"data/{nft_name}/{date}/result_list.json", "a") as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)
            print("[#] JSON was added into folder")

def main():
    start_time = time.time()

    result = load_data()

    for key in result.keys():
        result[key].sort()

    load_data_into_folders(result)

    finished_time = time.time() - start_time

    print(f"Work has been done for {finished_time}")

if __name__ == "__main__":
    main()