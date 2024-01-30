import numpy as np

def medal_tally(df):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC','Games','Year','City', 'Sport','Event', 'Medal'])
    
    # gives the the gold silver and bronze medals
    medal_tally = medal_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['total'] = medal_tally['total'].astype('int')
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')

    return medal_tally


def country_year_list(df):
    #List of years  
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    #List of countries
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years,countries


def fetch_medal_tally(df, year,country):
    
    medal_df = df.drop_duplicates(subset=['Team', 'NOC','Games','Year','City', 'Sport','Event', 'Medal'])
    
    flag = 0
    
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
        
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['total'] = x['total'].astype('int')
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    return x

def data_overtime(df, column):
    nations_over_time = df.drop_duplicates(['Year', column])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition', 'count':column}, inplace=True)
    return nations_over_time

def most_successful_athlete(df, sport):
    temp_df = df.dropna(subset = ['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] ==  sport]  
    # Name, count
    x =  temp_df['Name'].value_counts().reset_index().merge(df, left_on = 'Name', right_on = 'Name', how = 'left')
    y = x[['Name', 'count', 'Sport', 'region']].drop_duplicates()
    final_df = y.rename(columns = {'Name': 'Athlete','count': 'Total_medals'})
    return final_df.head(15)

def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC','Games','Year','City', 'Sport','Event', 'Medal'], inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_sports_heatmap(df, country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC','Games','Year','City', 'Sport','Event', 'Medal'], inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index = 'Sport', columns='Year', values = 'Medal', aggfunc='count').fillna(0).astype('int')
    return pt

def most_successful(df, country):
    temp_df = df.dropna(subset = ['Medal'])
    
    temp_df = temp_df[temp_df['region'] == country]
        
    x = temp_df['Name'].value_counts().reset_index().merge(df, left_on = 'Name', right_on = 'Name', how = 'left')
    y = x[['Name', 'count', 'Sport']].drop_duplicates()
    final_df = y.rename(columns = {'Name': 'Athlete', 'count': 'Total medals'})
    return final_df