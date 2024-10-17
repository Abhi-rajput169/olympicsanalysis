import streamlit as st
import  numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Year','City','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag=1
        temp_df=medal_df[medal_df['region'] == country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year'] == int(year)]
    if year!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['Year'] == int(year)) & (medal_df['region']== country)]
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total']=x['Gold'] + x['Silver'] + x['Bronze']

    
    return x


def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Year','City','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']= medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    
    return medal_tally

def country_year_list(df):
    Years=df['Year'].unique().tolist()
    Years.sort()
    Years.insert(0,'Overall')

    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return Years,country

def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition','count':col},inplace=True)

    return nations_over_time


def most_successful(df, sport):
    temp_df = df[df['Medal'] != 'No medal']

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')

    x.rename(columns={'count':'Medals'},inplace=True)
    
    return x

def yearwise_medal_tally(df,country):
    temp_df= df[df['Medal'] != 'No medal']
    temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Event','Medal'],inplace=True)

    new_df=temp_df[temp_df['region'] == country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df= df[df['Medal'] != 'No medal']
    temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Event','Medal'],inplace=True)

    new_df=temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df = df[df['Medal'] != 'No medal']


    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(30).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')

    x.rename(columns={'count':'Medals'},inplace=True)
    
    return x
def men_vs_women(df):
    athlete_df=df.drop_duplicates(subset=['Name','region'])

    men=athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women=athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)

    final.fillna(0,inplace=True)
    return final



def plot_overall_athlete_count(df):
    overall_athlete_count = df.groupby('NOC')['Name'].nunique().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=overall_athlete_count.head(10).index, y=overall_athlete_count.head(10).values, palette="viridis", ax=ax)
    ax.set_title('Top 10 Countries Sending the Most Athletes (Overall)')
    ax.set_ylabel('Number of Athletes')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

def plot_yearwise_athlete_count(df):
    overall_athlete_count = df.groupby('NOC')['Name'].nunique().sort_values(ascending=False)
    yearwise_athlete_count = df.groupby(['Year', 'NOC'])['Name'].nunique().reset_index()
    
    top_5_countries = overall_athlete_count.head(5).index.tolist()
    filtered_data = yearwise_athlete_count[yearwise_athlete_count['NOC'].isin(top_5_countries)]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.lineplot(x='Year', y='Name', hue='NOC', data=filtered_data, palette="tab10", ax=ax)
    
    ax.set_title('Yearwise Athlete Count for Top 5 Countries')
    ax.set_ylabel('Number of Athletes')
    
    # Display the figure using st.pyplot
    st.pyplot(fig)