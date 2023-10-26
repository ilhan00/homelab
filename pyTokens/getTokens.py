import os
from dotenv import load_dotenv
import requests
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")


url = "https://papi.boraportal.com/assets/v2/tokens"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
data = response.json()

data_points = []
for address, info in data["payload"].items():
    data_points.append(
        influxdb_client.Point("tokens")
        .tag("name", info["name"])
        .tag("symbol", info["symbol"])
        .field("USDValue", float(info["usdValue"]))
        .field("KRWValue", float(info["krwValue"])),
    )

client = influxdb_client.InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG
)
write_api = client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=data_points)
