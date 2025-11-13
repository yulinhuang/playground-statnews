import pandas as pd

from src.utils.env import INDICATOR_URL


def get_sheet(sheet_name: str) -> pd.DataFrame:

    df = pd.read_excel(
        INDICATOR_URL, 
        sheet_name=sheet_name, 
        index_col='Code',
        converters={
            'Code': str,
            'Niveau': str
        }
    )  
    
    df = df[~df.index.isna()]
    df = df.rename(
        columns={
            df.columns[1]: 'description' # Rename the second column to 'description' (A little bit hardcoded)
        }
    )
    return df

def get_top_variations(df: pd.DataFrame, target: float,  n: int = 5, prefix: str = '', positive: bool = True, level: str = '4') -> pd.DataFrame:

    filtered_idx = df[df.index.str.startswith(prefix)]
    filtered_idx = filtered_idx[filtered_idx['Niveau'] == level]
    # Top n positive values
    top_n = (
        filtered_idx[filtered_idx[target] > 0].nlargest(n, target)
        if positive
        else filtered_idx[filtered_idx[target] < 0].nsmallest(n, target)
    )

    # Combine them
    filtered_df = top_n
    filtered_df[target] = filtered_df[target].round(1)

    # Convert to dictionary
    result_dict = dict(zip(filtered_df['description'], filtered_df[target]))
    return result_dict


def get_target_index(df: pd.DataFrame, target: float, code: str = '') -> pd.DataFrame:
    filtered_idx = df.loc[code] 
    result = filtered_idx[target]
    return float(round(result, 1))


def get_top_variations_with_ponderation(df: pd.DataFrame, target: float,  n: int = 5, prefix: str = '', positive: bool = True, level: str = '4') -> pd.DataFrame:

    df_pond = get_sheet("Pondération")
    filtered_pond = df_pond[df_pond.index.str.startswith(prefix)]
    filtered_pond = filtered_pond[filtered_pond['Niveau'] == level]

    filtered_idx = df[df.index.str.startswith(prefix)]
    filtered_idx = filtered_idx[filtered_idx['Niveau'] == level]
    filtered_idx[target] = filtered_idx[target].round(1)

    ponderated = filtered_idx[target] * filtered_pond[int(target)]
    # Top n positive values
    top_n = (
        ponderated[ponderated > 0].nlargest(n)
        if positive
        else ponderated[ponderated < 0].nsmallest(n)
    )

    # Combine them
    top_n = top_n.round(1)

    # Convert to dictionary
    result_dict = {
        df['description'][coicop]: float(filtered_idx[target].loc[coicop])
        for coicop in top_n.index
    }
    return result_dict
