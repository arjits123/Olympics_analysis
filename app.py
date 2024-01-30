import pandas as pd
import streamlit as st
import preprocessor 
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    'Select an Option', 
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,countries = helper.country_year_list(df)

    # Year and Country Selection
    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    medal_tally = helper.fetch_medal_tally(df, selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal tally in: ' + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal tally in: ' + selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal tally in: ' + str(selected_year)+ " for " + selected_country)
    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':

    edition = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sport = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    participating_nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<h2 style='text-decoration: underline;'>Editions</h2>", unsafe_allow_html=True)
        st.title(edition)

    with col2:
        st.markdown(f"<h2 style='text-decoration: underline;'>Cities</h2>", unsafe_allow_html=True)
        st.title(cities)

    with col3:
        st.markdown(f"<h2 style='text-decoration: underline;'>Sports</h2>", unsafe_allow_html=True)
        st.title(sport)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<h2 style='text-decoration: underline;'>Events</h2>", unsafe_allow_html=True)
        st.title(event)
    with col2:
        st.markdown(f"<h2 style='text-decoration: underline;'>Athletes</h2>", unsafe_allow_html=True)
        st.title(athletes)
    with col3:
        st.markdown(f"<h2 style='text-decoration: underline;'>Nations</h2>", unsafe_allow_html=True)
        st.title(participating_nations)
    
    st.markdown("---") 
    
    #For Participating nations overtime 
    nations_overtime = helper.data_overtime(df, 'region')
    fig = px.line(nations_overtime, x = 'Edition', y = 'region')
    st.title('No of Participating nations over years')
    st.plotly_chart(fig)

    # #For events over time
    event_overtime = helper.data_overtime(df, 'Event')
    fig = px.line(event_overtime, x = 'Edition', y = 'Event')
    st.title('No of Events over years')
    st.plotly_chart(fig)

    # Athletes over time
    athlete_overtime = helper.data_overtime(df, 'Name')
    fig = px.line(athlete_overtime, x = 'Edition', y = 'Name')
    st.title('No of Athletes over years')
    st.plotly_chart(fig)

    # Heat map for number of events overtime
    st.title('No of events over time (Every sport)')
    fig, ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot_table = x.pivot_table(index = 'Sport', columns='Year', values = 'Event', aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(pivot_table, annot=True)
    st.pyplot(fig)
    
    # Top 15 successful players
    st.title('Most Successful athletes')
    
    # Sports Selections
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport', sports_list)

    top_players = helper.most_successful_athlete(df,selected_sport)
    st.table(top_players.head(15))

if user_menu == 'Country-wise Analysis':
    
    #Country wise medal tally
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    st.sidebar.title('Country Medal tally')
    selected_country = st.sidebar.selectbox('Select the country: ', country_list)
    st.title(selected_country + ' Medal tally over the years')
    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.plotly_chart(fig)

    # What countries are good  at which sports?
    st.title(selected_country + ' excels in following sport')
    pt = helper.country_sports_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize = (20,20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    #top athlete from selected countries
    st.title(selected_country + "'s Top athletes")
    top = helper.most_successful(df,selected_country)
    st.table(top.head(10))



    

