import speedtest
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("ORG")
url = os.environ.get("INFLUXDB_URL")
bucket=os.environ.get("INFLUXDB_BUCKET")

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()
s.download(threads=threads)
s.upload(threads=threads)
s.results.share()

results_dict = s.results.dict()
results_dict['download'] = round(results_dict['download'] / 1000000, 2)
results_dict['upload'] = round(results_dict['upload'] / 1000000, 2)

write_api = write_client.write_api(write_options=SYNCHRONOUS)

#for value in range(5):
point = (
    Point("internet-speed")
    .tag("client_ip", results_dict['client']['ip'])
    .tag("client_isp", results_dict['client']['isp'])
    .tag("server_country", results_dict['server']['country'])
    .tag("server_name", results_dict['server']['name'])
    .field("download", results_dict['download'])
    .field("upload", results_dict['upload'])
    .field("ping", results_dict['ping'])
)

#time.sleep(1) # separate points by 1 second
if __name__ == "__main__":
    print(results_dict)
    write_api.write(bucket=bucket, org=org, record=point)