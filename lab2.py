import requests
import pandas as pd
import boto3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

url = "https://bank.gov.ua/NBU_Exchange/exchange_site"
params = {
    "start": "20210101",
    "end": "20211231",
    "valcode": "usd",
    "sort": "exchangedate",
    "order": "desc",
    "json": ""
}

response = requests.get(url, params=params)
data = response.json()

pdDF = pd.DataFrame(data)
pdDF.to_csv("data_2021.csv", index=False)

s3 = boto3.client("s3")
bucket_name = 'ladaawslab4bucket'
file_name = "data_2021.csv"

with open(file_name, "rb") as file:
    s3.upload_fileobj(file, bucket_name, file_name)

params = {
    "start": "20210101",
    "end": "20211231",
    "valcode": "eur",
    "sort": "exchangedate",
    "order": "desc",
    "json": ""
}

response = requests.get(url, params=params)
data_eur = response.json()

df_usd = pd.DataFrame(data)
df_eur = pd.DataFrame(data_eur)

df_usd['exchangedate'] = pd.to_datetime(df_usd['exchangedate'])
df_eur['exchangedate'] = pd.to_datetime(df_eur['exchangedate'])

fig, graph = plt.subplots()

graph.plot(df_usd["exchangedate"], df_usd["rate"], label='USD')
graph.plot(df_eur["exchangedate"], df_eur["rate"], label='EUR')

graph.set_title("Currency Exchange Rates - 2021")
graph.set_ylabel("Rate Value")
graph.legend()

graph.set_xticklabels([])

pic_name = "rate_usd_eur_2021.png"

plt.savefig(pic_name)

s3.upload_file(pic_name, bucket_name, pic_name)
