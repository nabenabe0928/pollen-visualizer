from argparse import ArgumentParser
import datetime

import pandas as pd


def fetch_data() -> pd.DataFrame:
    # https://wxtech.weathernews.com/pollen/index.html
    citycode_url = "https://wxtech.weathernews.com/pollen/citycode.html"
    parser = ArgumentParser()
    parser.add_argument("--citycode", default=13116, help=f"Check {citycode_url}.")
    parser.add_argument("--start", default=None, type=str, help="Give by YYYYMMDD")
    parser.add_argument("--end", default=None, type=str, help="Give by YYYYMMDD")
    parser.add_argument("--cum", default="False", type=str, choices=["True", "False"])
    args = parser.parse_args()
    start = args.start
    end = args.end
    citycode = args.citycode
    today = datetime.datetime.now()

    if start is None:
        start = f"{today.year}{today.month:0>2}{today.day:0>2}"
    if end is None:
        end = f"{today.year}{today.month:0>2}{today.day:0>2}"
    if len(start) != 8 or len(end) != 8:
        raise ValueError(
            f"start and end must take the format of YYYYMMMMDD, but got {start=} and {end=}."
        )
    if start[:4] != end[:4]:
        raise ValueError(
            f"The year for start and end must be identical, but got {start=} and {end=}."
        )
    if start > end:
        raise ValueError(f"start must be earlier than end, but got {start=} and {end=}.")

    base_url = "https://wxtech.weathernews.com/opendata/v1/pollen?"
    target_url = f"{base_url}citycode={citycode}&start={start}&end={end}"
    print(f"Fetch the data from {target_url}")
    df = pd.read_csv(target_url, encoding="shiftjis")
    df = df.drop(columns=["citycode"])
    df.loc[df["pollen"] == -9999, "pollen"] = 0
    if eval(args.cum):
        df["pollen"] = df["pollen"].cumsum()

    return df
