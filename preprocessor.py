import pandas as pd

# Preprocessing function
def preprocess(df,region_df):
    
    # Filter only Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region data
    df = df.merge(region_df, on='NOC', how='left')

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Avoid adding columns multiple times
    if not set(['Gold', 'Silver', 'Bronze']).issubset(df.columns):
        df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df


