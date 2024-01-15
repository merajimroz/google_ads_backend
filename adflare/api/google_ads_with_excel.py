import pandas as pd

def google_ads_with_excel(file):
    print(file)

    df = pd.read_excel(file, engine='openpyxl')
    data = df.to_dict()

    processed_data = []
    for i in range(len(data['customer_id'])):
        processed_item = {}
        for key in data:
            processed_item[key] = data[key][i]
        processed_data.append(processed_item)

    print(processed_data)
    return processed_data

