import streamlit as st
import pandas as pd
import preprocessor
import new
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv('olympics_dataset.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")

user_menu=st.sidebar.radio(
    'select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)


if user_menu =='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=new.country_year_list(df)

    selected_year=st.sidebar.selectbox("select Year",years)
    selected_country=st.sidebar.selectbox("select country",country)

    medal_tally=new.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':  
        st.title("Medal Tally in " + str(selected_year) + " Olympics") 
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")     
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country+" Performance in "+ str(selected_year)+" Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    
    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nation")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time=new.data_over_time(df,'region')
    fig=px.line(nations_over_time,x="Edition",y="region")
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig) 
    
    events_over_time=new.data_over_time(df,'Event')
    fig=px.line(events_over_time,x="Edition",y="Event")
    st.title("Events Over the Years")
    st.plotly_chart(fig) 

    athletes_over_time=new.data_over_time(df,'Name')
    fig=px.line(athletes_over_time,x="Edition",y="Name")
    st.title("Athletes Over the Years")
    st.plotly_chart(fig) 

    st.title("No of Events Over Time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    

    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=new.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('select a Country',country_list)

    country_df=new.yearwise_medal_tally(df,selected_country)
    fig=px.line(country_df,x="Year",y="Medal")
    st.title(selected_country+" Medal Tally Over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = new.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes " + selected_country)
    top10_df=new.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    st.title("Men Vs Women Participation Over the Years")
    final=new.men_vs_women(df)
    fig=px.line(final,x="Year",y=["Male","Female"])
    st.plotly_chart(fig)
  
    
    st.header('Top 10 Countries Sending the Most Athletes (Overall)')
    new.plot_overall_athlete_count(df)

    st.header('Yearwise Athlete Count for Top 5 Countries')
    new.plot_yearwise_athlete_count(df)
