import argparse
import csv
import json
import logging
import pandas as pd
from utils import DataConnection

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def upload_data(clean_data, usr, pwd):
    success = False
    while not success:
        connection = DataConnection(usr, pwd)
        if connection.upload(clean_data):
            success = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some args")
    parser.add_argument("-f", "--file", required=True, help="Data file")
    parser.add_argument("-u", "--username", required=False, help="Username")
    parser.add_argument("-p", "--password", required=False, help="Password")
    args = parser.parse_args()
    data_file = args.file
    clean_data = []
    if data_file.endswith(".json"):
        with open(data_file) as f:
            data = json.load(f)
            events = data.get("events")
            for event in events:
                if int(event.get("data").get("year")) >= 2012:
                    clean_data.append(events)
                    print(f"Adding event: {event}")
        upload_data(clean_data, args.username, args.password)

    elif data_file.endswith(".csv"):
        with open(data_file, newline="") as f:
            try:
                spamreader = csv.reader(f, delimiter=" ", quotechar="|")
                header = next(spamreader)
                print(spamreader)
                for row in spamreader:
                    row = list((row[0].split(",")))
                    if (int(row[1])) >= 2012:
                        clean_data.append(row)
            except Exception as e:
                print(e)
        upload_data(clean_data, args.username, args.password)

    elif (data_file.endswith(".xlsx")) or (data_file.endswith(".xls")):
        df = pd.read_excel(data_file)
        for _, val in df.iterrows():
            year = str(val["year"])
            if year >= 2012:
                clean_data.append(val)
                log.info(f"Adding event: {event}")
        upload_data(clean_data, args.username, args.password)

    else:
        log.info(f"Unsupported file format: {data_file.split('.')[-1]}")