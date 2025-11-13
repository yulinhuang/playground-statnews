import pandas as pd

from src.utils.env import INDICATOR_URL


def main():
    print("Hello from statnews!")


if __name__ == "__main__":
    df = pd.read_excel(INDICATOR_URL, sheet_name="Variation annuelle", dtype=str)
    