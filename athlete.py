import streamlit as st
import pandas as pd
import preprocessor , helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load data inside the function to avoid global scope & repeated processing
df = pd.read_csv(r'C:\Users\Aksha\OneDrive\Desktop\Placement Prep\Analytics\Project\Olympics\DS\athlete_events.csv')
region_df = pd.read_csv(r'C:\Users\Aksha\OneDrive\Desktop\Placement Prep\Analytics\Project\Olympics\DS\noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise analysis','Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select country",country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} overall performance")

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} performance in {selected_year}")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.title("Top Statistics")
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Athletes")
        st.title(athletes)
    
    with col3:
        st.header("Nations")
        st.title(nations)

    nations_over_time=helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Year", y="region")
    st.title("Participating Nations Over Time")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Year", y="Event")
    st.title("Number of Events Over Time")
    st.plotly_chart(fig)

    athletes_over_time=helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x="Year", y="Name")
    st.title("Number of Athlets Over Time")
    st.plotly_chart(fig)

    st.title("No of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise analysis':

    st.title('Countrywise medal analysis')

    #Creating a selection box for selecting countries
    country_list=df['region'].unique().tolist()
    country_list = [str(item) for item in country_list]
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select a Country',country_list)

    # Assuming 'df' is your main DataFrame
    country_df = helper.yeareise_medal_tally(df, selected_country)
    fig=px.line(country_df,x="Year",y="Medal")
    st.title(selected_country+" Medal Tally over the years")
    st.plotly_chart(fig)
  
    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


