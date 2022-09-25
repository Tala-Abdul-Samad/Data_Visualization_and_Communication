# my_app.py, run with 'streamlit run my_app.py' from terminal

# Import libraries 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from matplotlib import pyplot as plt
import country_converter
from PIL import Image
import scipy as sp
import pandas as pd

base="light"
primaryColor="#f5acac"
backgroundColor="#fff8ee"
secondaryBackgroundColor="#ffddcb"
font = "sans serif"
textColor = '#FFFFFF'

#Load COVID-19 DataData
df = pd.read_csv("covid_19_data.csv")  # read a CSV file inside the 'data" folder next to 'app.py'

#Data Pre-processing
#Rename columns 
df=df.rename(columns={'Last Update':'LastUpdate'})
#Remove rows 
df=df[(df['Country/Region']!='Others') & (df['Country/Region']!='(\'St. Martin\',)') & (df['Country/Region']!='Gambia, The')]
#Sort "Country/Region" according to the number of confirmed cases
data_confirmed=((df.groupby('Country/Region').sum()).sort_values(by=["Confirmed"], ascending=False)).reset_index()

#Highest 10 countries in number of confirmed cases
data_confirmed_10=data_confirmed.iloc[:10,:]

#Treat missing values 
data_state=df.dropna()
data_state.isnull().sum()
data_obs= df.groupby('ObservationDate').sum().reset_index()

# Exploratory Data Analysis Using Plotly
scatter=px.scatter(data_confirmed, x="Confirmed", y="Deaths", color=data_confirmed['Country/Region'], 
        size='Deaths',
        size_max=60, width=800, height=600, title= 'Total Number of COVID-19 Deaths'
        )

pie_chart = px.pie(data_confirmed_10, values = 'Deaths',names='Country/Region', height=600, 
                  title= "Top 10 countries with highest number of COVID-19 Deaths")

pie_chart.update_traces(textposition='inside', textinfo='percent+label')

pie_chart.update_layout(
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    ))

bar = px.bar(data_confirmed_10, x="Country/Region", y=["Confirmed", "Deaths", "Recovered"], title="Top 10 countries with highest number of COVID-19 Deaths")

data_obs_vis = data_obs.melt(id_vars='ObservationDate', 
                 value_vars=['Confirmed', 
                             'Recovered', 
                             'Deaths'], 
                 var_name='Ratio', 
                 value_name='Value')

map= px.choropleth(df, locations="Country/Region",locationmode = "country names",color='Confirmed', hover_name="Country/Region",
             animation_frame="ObservationDate",color_continuous_scale=px.colors.sequential.Plasma, title= "COVID-19 Cases Over Time")

# Data Science Salary
df1=pd.read_csv(r'datascience_salaries.csv').drop(columns = ['Unnamed: 0'])

#Pre-processing Salary Data 
df1['experience_level'] = df1['experience_level'].map({'EN':'Junior', 'MI':'Middle', 'SE':'Senior', 'EX':'Executive'})
df1['company_location'] = country_converter.convert(names=df1['company_location'], to="ISO3")
df1['employee_residence'] = country_converter.convert(names=df1['employee_residence'], to="ISO3")

#Plotly Visualization
df1_job = df1['job_title'].value_counts(ascending = True).reset_index().tail(10)
fig1 = go.Figure(go.Bar(y = df1_job['index'], x = df1_job['job_title'],orientation='h',  marker = dict(color = 'blue', opacity = 0.8)))
fig1.update_layout(width = 800,height = 500, title_text="Job Title Distribution",showlegend=False)
#animation_frame="Year"
fig2 = px.scatter(df1, x = 'salary_in_usd', y = 'experience_level', size = 'salary_in_usd', hover_name = 'job_title', color = 'job_title', 
           color_discrete_sequence=px.colors.qualitative.Alphabet, 
           labels=dict(salary_in_usd = "Salary ($)", experience_level = "Experience Level", job_title = "Job Title", work_year = "Work Year"),
           animation_frame = 'work_year', title = 'Experience Level and Salary').update_yaxes(categoryarray = ['Junior', 'Middle', 'Senior', 'Executive'])

df1_comparison = df1.loc[(df1["company_location"]=="USA") | (df1.company_location=="JPN")].copy()
df1_funnel_comparison = df1_comparison.groupby(["experience_level", "company_location"]).mean()["salary_in_usd"].reset_index()
df1_funnel_comparison["salary_in_usd"] = df1_funnel_comparison["salary_in_usd"].round(2)
df1_funnel_comparison['A'] = pd.Categorical(df1_funnel_comparison.experience_level,
                                           categories=['Junior', 'Middle', 'Senior', 'Executive'],
                                           ordered=True)
df1_funnel_comparison = df1_funnel_comparison.sort_values('A').drop(columns="A")
fig3 = px.funnel(df1_funnel_comparison, x='salary_in_usd', y='experience_level', color='company_location') 
fig3.update_layout(title="<b>Average Salary By Experience Level</b>", 
                  yaxis=dict(automargin=True, title=" Experience Level"))

# Set page configuration
page_config = st.set_page_config(page_title='COVID-19 in Review', layout='wide', initial_sidebar_state='expanded')
                # layout="centered" page_icon='MSBA.png'
st.markdown("<h1 style='text-align: center; color: black;'>COVID-19 in Review</h1>", unsafe_allow_html=True)
#st.caption('VectorStock')
#st.sidebar.image("tumor_icon.png", width=100)
st.sidebar.title('Explore the Data')
#st.markdown('Please leave your feedback below')
#navigation=st.sidebar.radio('VIEW', ('Data Description', 'Explanatory Data Analysis', 'Predictive Analysis'))

box = st.sidebar.selectbox("Select Data:", [' ','COVID-19 Data','Data Science Salary'])

list_covid=['Scatter Plot', 'Pie Chart', 'Bar Plot', 'World Map']
list_salary=['Bar Chart', 'Scatter Plot', 'Funnel Chart']

# Insert space
st.markdown('###')

if box == ' ':
    # image = Image.open(r'/Users/talaabdulsamad/Desktop/recovery.jpeg')
    # st.image(image)
    video_file = open(r'/Users/talaabdulsamad/Desktop/videoplayback.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

# if navigation == 'Explanatory Data Analysis':
#     st.sidebar.selectbox("Granularity", ["Worldwide", "Country"])
if box == 'COVID-19 Data':
    
    st.write('According to the World Health Organization (WHO), the COVID-19 pandemic has led to a dramatic loss of human life worldwide and presents an unprecedented challenge to public health, food systems and the world of work. The economic and social disruption caused by the pandemic is devastating: tens of millions of people are at risk of falling into extreme poverty, while the number of undernourished people, currently estimated at nearly 690 million, could increase by up to 132 million by the end of the year. The COVID-19 dataset used below displays the number of affected cases, deaths and recovery daily.')
    st.markdown('#')
    if st.checkbox('Show Dataset'):
        st.write(df)
    st.markdown('###')
    result=st.radio('Select Chart Type:', list_covid)
    if result=='Scatter Plot':
        st.write(scatter)
    elif result=='Pie Chart':
        st.write(pie_chart)
    elif result=='Bar Plot':
        st.write(bar)
    elif result=='World Map':
        st.write(map)
    st.markdown('#')

    st.write(':warning: The number of COVID-19 cases is rapidly increasing over time. Moreover, the consequences of the pandemic on the Arab region are likely to be deep and long-lasting. Hence, Governments should introduce policies to mitigate the negative impact of COVID-19 such as ensuring access to vaccines for vulnerable groups.')
    st.markdown('#')
    st.write('Retrieved from:https://www.kaggle.com/datasets/sudalairajkumar/novel-corona-virus-2019-dataset')

if box =='Data Science Salary':

    st.write('The dataset has information about data science salaries in the past couple of years. Employment opportunities in this dataset are displayed by locations, experience level, remote ratio, company size, and others (refer to dataset below).') 
    st.write('Has COVID-19 impacted the demand on data analysts?')
    st.markdown('#')
    
    if st.checkbox('Show Dataset'):
        st.write(df1)
    st.markdown('###')
    result=st.radio('Select Chart Type:', list_salary)
    if result=='Bar Chart':
        st.write(fig1)
    
    elif result=='Scatter Plot':
        st.write(fig2)    
    elif result=='Funnel Chart':
        st.write(fig3)
    # elif result=='Box Plot with Animation':
    #     st.write(fig)

    st.markdown('#')
    st.write(':heavy_check_mark: The way companies conduct work has changed, especially after the pandemic where they had to adopt new methods of meeting and working together. Hence, the distribution of remote workers has increased from 50% in 2020 to almost 72% in 2022. There is a high demand for data scientists and business data analyst. Moreover, these jobs are among the highly paid jobs in 2022.')
    st.markdown('#')
    st.write('Retrieved from: https://www.kaggle.com/code/tmishinev/data-science-salaries-eda-plotly/notebook')
