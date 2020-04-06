import requests
import json
import pandas as pd
from datetime import datetime


def scrape_5_days_alberta(station_name: str, station_type: str) -> pd.DataFrame:
    """
    Downloads the "Most recent 5 days' data (in current time), in JSON" file from Alberta Rivers to the "Data" subdirectory
    and imports the data into a pandas dataframe.

    Parameters:
        station_name: The station code (e.g. "05AB815")
        station_type: The station type code (e.g. "M_PC")
    
    Returns:
        If successful, returns pandas dataframe of two columns (Time: DateTime object, station_type: float)
        Else returns None
    """
    filename = station_type + "_" + station_name + "_table.json"
    url = "https://environment.alberta.ca/apps/Basins/data/figures/river/abrivers/stationdata/" + filename
    r = requests.get(url, stream=True)
    with open("../Data/" + filename, 'w+') as f:
        json.dump(r.json(), f, indent=4)

    with open("../Data/" + filename, 'r') as f:
        indata = json.load(f)
        indict = indata[0]
        data_entry = []
        for item in indict['data']:
            dt = datetime.strptime(item[0],'%Y-%m-%d %H:%M:%S')
            data_entry.append((dt, item[1]))
        df = pd.DataFrame(data_entry, columns=['Time', station_type])
        df.set_index('Time', inplace=True)
        return df

    return None


df = scrape_5_days_alberta("05BA002", "R_HG")
print(df.head())
df2 = scrape_5_days_alberta("05BA815", "M_PC")
print(df2.head())