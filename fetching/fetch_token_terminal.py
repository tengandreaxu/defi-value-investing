import os
import argparse
import time
import pandas as pd
from fetching.SimpleHttpClient import SimpleHttpClient, Endpoints

API_KEY = os.environ["TOKEN_TERMINAL_API"]
PROJECT_IDS = "data/token_terminal/project_ids.csv"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--fetch-ids", dest="fetch_ids", action="store_true", help="fetch protocols ids"
    )
    parser.set_defaults(fetch_ids=False)

    args = parser.parse_args()

    client = SimpleHttpClient()
    headers = {"Authorization": f"Bearer {API_KEY}"}

    if args.fetch_ids:
        response = client.get(Endpoints.TOKEN_TERMINAL_IDS, "", headers=headers)
        df = pd.DataFrame(response)
        df.to_csv(PROJECT_IDS, index=False)

    try:

        project_ids = pd.read_csv(
            PROJECT_IDS,
        )
    except:
        raise Exception("Project id missing, start using --fetch-ids option")

    for _, row in project_ids.iterrows():
        response = client.get(
            Endpoints.TOKEN_TERMINAL_METRICS.format(row.project_id), "", headers=headers
        )
        df = pd.DataFrame(response)
        df.to_csv(f"data/token_terminal/{row.project_id}.csv", index=False)
        print(f"Got {row.project_id}")
        time.sleep(0.15)
