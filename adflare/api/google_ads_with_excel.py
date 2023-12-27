import pandas as pd

def google_ads_with_excel(file):

    df = pd.read_excel(file)
    data = df.to_dict()

    processed_data = []
    for i in range(len(data['customer_id'])):
        processed_item = {}
        for key in data:
            processed_item[key] = data[key][i]
        processed_data.append(processed_item)

    return processed_data
