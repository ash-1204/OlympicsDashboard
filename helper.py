
def fetch_medal_tally(df,year, country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])    
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
        flag = 1
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    medal_tally=medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = df['region'].dropna().unique().tolist()
    country = [str(c) for c in country]
    country.sort()
    country.insert(0,'Overall')


    return years,country

def data_over_time(df,column):
    nations_over_time=df.drop_duplicates(['Year',column])['Year'].value_counts().reset_index().sort_values(by='Year')
    nations_over_time.rename(columns={'index': 'Edition', 'count': column}, inplace=True)
    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medal_Count']  # Rename for clarity
    x = x.head(15).merge(df, on='Name', how='left')[['Name', 'Medal_Count', 'Sport']].drop_duplicates('Name')
    return x

def yeareise_medal_tally(df, Country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games','Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==Country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medal Count']
    x = x.head(10).merge(df, on='Name', how='left')[['Name', 'Medal Count', 'Sport', 'Event']]

    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def most_successful_countrywise(df, country):
    # Filter for the selected country
    temp_df = df[df['region'] == country]

    # Get medal count per athlete
    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Name', 'Medals']  # Rename for clarity

    # Take top 10
    top10 = top_athletes.head(10)

    # Merge with the original dataframe to get 'Sport'
    merged = top10.merge(df[['Name', 'Sport']], on='Name', how='left')

    # Drop duplicates just in case (same athlete may appear in multiple rows due to multiple events)
    final_df = merged[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return final_df
