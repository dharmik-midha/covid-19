import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly
import folium
import math
import os
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import tensorflow as tf
from pandas.io.json import json_normalize
from streamlit_folium import folium_static
from streamlit.script_request_queue import RerunData



st.set_page_config(
page_title="Covid-19 Dashboard",
#page_icon=":microbe:",
layout="centered",
initial_sidebar_state="expanded",
)



# Read the data
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')

confirmed_total = int(country_df['Confirmed'].sum())
active_total = int(country_df['Active'].sum())
deaths_total = int(country_df['Deaths'].sum())
recovered_total = int(country_df['Recovered'].sum())


# Data Preprocessing
country_df['Incident_Rate'].fillna(0, inplace=True)
country_df['Mortality_Rate'].fillna(0, inplace=True)
country_df['Active'] = country_df['Active'].apply(lambda x : 0 if x < 0 else x)

st.markdown("""
                <link rel="preconnect" href="https://fonts.gstatic.com">
                <link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@200&display=swap" rel="stylesheet">

                <style>
                #white theme ,#black theme
                .css-h9oeas,.css-1v3fvcr{ 
                    color:black
                }
                .css-ffhzg2{
                    background-color:white;
                }
                .css-vfskoc {
                    color:black
                }
                .shadow{
                    box-shadow:0.1em 0.1em 0.7em 0.1em orangered;

                }   
                .card1{ margin:auto; width:100%;margin-bottom: 35px;}
                .card li{
                    font-size:large;
                }

                .card{                                      
                    padding:5%;
                    color:#000000;
                    margin-bottom:35px;
                    text-align:justify;
                    font-size:large;
                }
                .card_img{ 
                    margin:auto;
                    box-shadow:0em 0em 0.7em 0.1em white;
                    background:url('https://www.fda.gov/files/Coronavirus_3D_illustration_by_CDC_1600x900.png')no-repeat center center/cover;
                    # width:300px;
                    height:300px;
                    border-radius:2vh;
                    margin-bottom:4%;
                    }
                .person1{
                    background:url('https://pbs.twimg.com/profile_images/1261754024640086023/cGtGEnwC_400x400.jpg')no-repeat center center/cover;
                    width:150px;
                    height:150px; 
                    border-radius:50%;       
                    margin:auto;
                }
                .css-qpy8u8,.css-bauj2f{color:#252627}
                .person2{
                    background:url('https://media-exp1.licdn.com/dms/image/C4D03AQHj-G7HKacpgw/profile-displayphoto-shrink_200_200/0/1590663509591?e=1633564800&v=beta&t=TyHtZhKcP9SJ4hNm2OtCPG8_uDJTu-VF3NDKxaeT58g')no-repeat center center/cover;
                    width:150px;
                    height:150px;                    
                    border-radius:50%; 
                    margin:auto;
                }
                .person3{
                    background:url('https://media-exp1.licdn.com/dms/image/C4E03AQGFVetJwmDGHQ/profile-displayphoto-shrink_200_200/0/1620400899860?e=1633564800&v=beta&t=DvBvw8RXgC00s5jHyuToXp5NMesnZUD6hU3UzBhviG8')no-repeat center center/cover;
                    width:150px;
                    height:150px;                    
                    border-radius:50%; 
                    margin:auto;
                }
                .person4{
                    background:url('https://pbs.twimg.com/profile_images/1388073650809569281/mptG7qXA_400x400.jpg')no-repeat center center/cover;
                    width:150px;
                    height:150px;                    
                    border-radius:50%; 
                    margin:auto;
                }
                .list{
                    # text-align:center;
                }
                .list li{
                    color:black;
                    font-size:large;
                }
                .container{
                    width:100%;
                    height:100%;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    flex-wrap:wrap;
                }
                .Title{
                   text-align: center; 
                   color: white; 
                   margin-bottom:20px ;
                   background-color:#252627;
                   padding:2%;
                   font-family: 'Libre Franklin', sans-serif;
                   border-bottom:2px solid white;
                    box-shadow:0px 0px 14px 1px ;
                   } 
                   .view{
                       width:100vw;
                   }               
                .profile{
                    width:45%;
                    height:50%;
                    display:flex;
                    justify-content:center;
                    align-item:center;
                    text-align:center;
                    boarder-radius:2vh;
                    padding:10%;
                    flex-direction:column;
                    box-shadow:0em 0em 0.5em 0.1em;
                    margin:auto;
                    margin-bottom:12px;
                    background-color:oldlace;
                    border-color:black;
                    color:black;     
                    }
                .profile h3{
                    font-family: 'Libre Franklin', sans-serif;
                    font-width:bolder;
                    color:black;
                    # box-shadow:0px 0px 14px 1px ;
                    

                }
                .subhead h2{
                        color:black;
                        font-family: 'Libre Franklin', sans-serif;
                        font-size:bolder;
                }
                
                tr:nth-child(odd) 
                {
                    background-color: #f2f2f2;
                    border:none;
                    border-style:hidden;
                }
                tr{
                    height:45px;
                }
                th{
                    color:white;
                    text-align:center;
                    width:420px;
                    font-size:x-large;
                    background-color:black;
                }
                table{
                    margin:auto;
                }
                th,td,tr{
                    border:none;
                    border-style:hidden;
                }
                td{                    
                    color:black;
                    text-align:center;               

                }
                @media(max-width:800px){
                   .profile{
                    width:75%;
                    height:50%;
                    margin-bottom:25px;
                    } 
                }

                .element-container{
                    align-items:center;
                }
                div.polaroid {
                width: 50%;
                background-color: white;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                margin-bottom: 25px;
                margin:auto;
                }

                .polaroid-text {
                text-align: center;
                padding:6px 18px;
                background-color:black;
                }
                .polaroid-text h2{
                color:white;     
                }       
                .grid{
                    display:grid;
                    grid-template-columns:45% 45%;
                    width:99%;
                    text-align:center;
                    justify-content:space-around;

                }    
                .grid-item{
                    box-shadow:0em 0em 0.6em 0.1em ;
                    width:100%;
                    margin-bottom:4%;
                }
                @media(max-width:800px)
                {
                    .grid{
                        display:flex;
                        justify-content:center;
                        flex-direction:column;
                        text-align:center;
                    }
                }

                .highlight{
                    background-color:black;
                    color:white;
                }
                            a{
                    # font-weight: 300;
                    # font-family:'Times New Roman', Times, serif;
                    # text-decoration:none;
                }
                .r{
                    color:red;
                }
                .g{
                    color:green;
                }
                .b{
                    color:blue;
                }
                .o{
                    color:orange;
                }

               

                /* Table Styles */

                .fl-table {
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: normal;
                    border: none;
                    border-collapse: collapse;
                    width: 100%;
                    max-width: 100%;
                    white-space: nowrap;
                    background-color: white;
                }

                .fl-table td, .fl-table th {
                    text-align: center;
                    padding: 8px;
                }

                .fl-table td ,th{
                    border-right: 1px solid #f8f8f8;
                    font-size: 12px;
                }

                .fl-table thead th {
                    color: #ffffff;
                    background: #4FC3A1;
                }


                .fl-table thead th:nth-child(odd) {
                    color: #ffffff;
                    background: #324960;
                }

                .fl-table tr:nth-child(even) {
                    background: #F8F8F8;
                }
                 .vggimg{
                       margin-top:45px;
                       box-shadow:0 0 0.3em 0.1em black;
                        
                    }
                /* Responsive */

                @media (max-width: 767px) {
                    .vggimg{
                        width:80vw;
                        
                    }
                    .fl-table {
                        display: block;
                        width: 100%;
                    }
                    .table-wrapper:before{
                        content: "Scroll horizontally >";
                        display: block;
                        text-align: right;
                        font-size: 11px;
                        color: white;
                        padding: 0 0 10px;
                    }
                    .fl-table thead, .fl-table tbody, .fl-table thead th {
                        display: block;
                    }
                    .fl-table thead th:last-child{
                        border-bottom: none;
                    }
                    .fl-table thead {
                        float: left;
                    }
                    .fl-table tbody {
                        width: auto;
                        position: relative;
                        overflow-x: auto;
                    }
                    .fl-table td, .fl-table th {
                        padding: 20px .625em .625em .625em;
                        height: 60px;
                        vertical-align: middle;
                        box-sizing: border-box;
                        overflow-x: hidden;
                        overflow-y: auto;
                        width: 120px;
                        font-size: 13px;
                        text-overflow: ellipsis;
                    }
                    .fl-table thead th {
                        text-align: left;
                        border-bottom: 1px solid #f7f7f9;
                    }
                    .fl-table tbody tr {
                        display: table-cell;
                    }
                    .fl-table tbody tr:nth-child(odd) {
                        background: none;
                    }
                    .fl-table tr:nth-child(even) {
                        background: transparent;
                    }
                    .fl-table tr td:nth-child(odd) {
                        background: #F8F8F8;
                        border-right: 1px solid #E6E4E4;
                    }
                    .fl-table tr td:nth-child(even) {
                        border-right: 1px solid #E6E4E4;
                    }
                    .fl-table tbody td {
                        display: block;
                        text-align: center;
                    }
                }
                .tableheadingset{
                   width:100%;
                   margin:auto;
                   text-align: center; 
                   color: Black; 
                   margin-bottom:20px ;
                   padding:2%;
                   font-family: 'Libre Franklin', sans-serif;
                }
                </style>""",unsafe_allow_html=True)

fig = go.Figure()
fig1 = go.Figure()

def made_by():    
    st.sidebar.image('https://cdn.pixabay.com/photo/2020/03/30/11/49/corona-virus-4984021_960_720.jpg',width=300)
    st.sidebar.markdown('<h2 style="font-family:lora">Made by:</h2>',unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-family:lora">-Ruchi Pundora<br>-Nikita Arora<br>-Dhruv Ahuja<br>-Dharmik Midha<br>',unsafe_allow_html=True)

   
def Home():
    ##############HEADING###################
    st.markdown("<h1 class ='Title'>  Covid-19 Detection Using Chest X-Ray</h1>", unsafe_allow_html=True)
    ############CORONA IMAGE##################
    st.markdown("""<div class="polaroid">
        <img src="https://www.fda.gov/files/Coronavirus_3D_illustration_by_CDC_1600x900.png" alt="5 Terre" style="width:100%">
        <div class="polaroid-text">
        <h2>SARS-CoV-2</h2>
        </div>
        </div>""",unsafe_allow_html=True)
    # st.markdown("<div class='card_img'></div>",unsafe_allow_html=True)

    ##################FIRST PARA#############
    firstpara='''<div class="card">Coronavirus disease (Covid-19) 📍 is an infectious disease caused by a newly discovered coronavirus.
    Most people infected with the Covid-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.  Older people, and those with underlying medical problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness. The best way to prevent and slow down transmission is to be well informed about the Covid-19 virus, the disease it causes and how it spreads. Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face. The Covid-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow).</div>'''
    st.markdown(firstpara,unsafe_allow_html=True)

    ####################ABOUT OUR PROJECT#########################

    # url="https://www.mohfw.gov.in/data/datanew.json"
    # r=requests.get(url)
    # df=json_normalize(r.json())

    # def marquee():
    #     structure=""
    #     for i in range(37):
    #         struc="""<a><b>"""+df.state_name[i]+"""</b></a> <i class='r'>A: """+df.active[i]+"""</i> <i class="o">P: """+df.positive[i]+"""</i> <i class="g">C: """+df.cured[i]+"""</i> <i class="b">D: """+df.death[i]+"""</i>   """
    #         structure+=struc
    #     return structure
    # m=marquee()
    # st.markdown('''<marquee>'''+m+''''</marquee>''',unsafe_allow_html=True)

    #####################Detecting covid -19###################
    st.markdown("<h1 class='Title'>Detecting Covid-19 in Chest X-Ray images using VGG-16</h1>",unsafe_allow_html=True)

    paragraph='''<div class="card">
    <li>VGG16 is a convolution neural net (CNN ) architecture which was used to win ILSVR(Imagenet) competition in 2014. It is considered to be one of the excellent vision model architecture till date. ... It follows this arrangement of convolution and max pool layers consistently throughout the whole architecture</li>
    <li>our automatic Covid-19 detector is obtaining ~95% accuracy on our sample dataset based solely on X-ray images — no other data, including geographical location, population density, etc. was used to train this model.</li>
    <img class='vggimg' src='https://miro.medium.com/max/1210/1*E7zhhan7Sp7hats4jkKdeA.png'>
   </div>'''

    st.markdown(paragraph,unsafe_allow_html=True)


    made_by()
    
    st.markdown("<h1 class='Title'>Covid-19 Detector</h1>",unsafe_allow_html=True)


    # #x-ray
    left_column,right_column=st.beta_columns(2)
    file=left_column.file_uploader("Upload Image Here",type=['jpg','png'])
    classes={0:'Covid Positive',1:'Covid Negative'}
    if file is not None:
        img=file.read()
        file_path=os.path.join("tempDir",file.name)
        st.success("Upload successfully")
        right_column.image(img)
        with open(file_path,"wb") as f: 
            f.write(img)         
        model=tf.keras.models.load_model('model_covid_transfer_95.h5')
        test_image=tf.keras.preprocessing.image.load_img(file_path,target_size=(224,224))
        os.remove(file_path)
        test_image=tf.keras.preprocessing.image.img_to_array(test_image)
        test_image=np.expand_dims(test_image,axis=0)
        result=model.predict(test_image)
        # print(classes[int(result[0][0])])
        st.success(classes[int(result[0][0])])
           
     ########################### World Map View ###########################
    st.markdown("<h1 class='Title'>World Map View</h1>",
                unsafe_allow_html=True)
            
    world_map = folium.Map(location=[11,0], tiles="cartodbpositron", zoom_start=2, max_zoom = 6, min_zoom = 2)
    for i in range(0,len(confirmed_df)-1):
        if(math.isnan(confirmed_df.iloc[i]['Lat']) or math.isnan(confirmed_df.iloc[i]['Long'])):
                continue
        else:                 
            folium.Circle(
                location=[confirmed_df.iloc[i]['Lat'], confirmed_df.iloc[i]['Long']],
                fill=True,
                radius=(int((np.log(confirmed_df.iloc[i,-1]+1.00001)))+0.2)*40000,
                color='black',
                fill_color='grey',
                tooltip = "<div  style='margin: 0; background-color: black; color: white; box-shadow:0em 0em 0.7em 0.1em teal;'>"+
                            "<h4 style='text-align:center;font-weight: bold'>"+confirmed_df.iloc[i]['Country/Region'] + "</h4>"
                            "<hr style='margin:10px;color: white;'>"+
                            "<ul style='color: white;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
                                "<li>Confirmed: "+str(confirmed_df.iloc[i,-1])+"</li>"+
                                "<li>Deaths:   "+str(death_df.iloc[i,-1])+"</li>"+
                                "<li>Death Rate: "+ str(np.round(death_df.iloc[i,-1]/(confirmed_df.iloc[i,-1]+1.00001)*100,2))+ "</li>"+
                            "</ul></div>",
                ).add_to(world_map)
    folium_static( world_map)
    st.markdown("<h4 style='text-align: center; color: #000000; margin-bottom:70px;'></h4>", unsafe_allow_html=True)
   

#################################About Page##########################################################
def About():
    st.markdown(
                '''<div class="container">
                        <div class='view'><h1 class='Title'>Front-End Developer's</h1></div>
                        <div class="profile">
                            <div class="person3"></div>
                            <h3>Ruchi Pundora</h3>
                            <p>(MCA Student)</P> 
                        </div>
                        <div class="profile">
                            <div class="person4"></div>
                            <h3>Dharmik Midha</h3>
                            <p>(MCA Student)</P>
                        </div>
                        <div class='view' ><h1 class='Title'> Back-End Developer's</h1> </div>
                        <div class="profile">
                            <div class="person1"></div>
                            <h3>Dhruv Ahuja</h3>
                            <p>(MCA Student)</P>
                        </div>
                        <div class="profile">
                            <div class="person2"></div>
                            <h3>Nikita Arora</h3>
                            <p>(MCA Student)</P>
                        </div>
                   </div>
                ''',unsafe_allow_html=True)

   
    made_by()
  



################################ Help############################################################
def Help():
    st.markdown("<h1 class='Title'>Preventions</h1>",unsafe_allow_html=True)
    secondpara='''<div class=card1>To prevent infection and slow transmission of COVID-19, do the following:
                <ul class="list">
                <li>Wash your hands regularly with soap and water, or clean them with alcohol-based hand rub.</li>
                <li>Maintain at least 1 metre distance between you and people coughing or sneezing.</li>
                <li>Avoid touching your face.</li>
                <li>Cover your mouth and nose when coughing or sneezing.</li>
                <li>Stay home if you feel unwell.</li>
                <li>Refrain from smoking and other activities that weaken the lungs.</li>
                <li>Practice physical distancing by avoiding unnecessary travel and staying away from large group of people.</li>
                <ul><div>'''
    st.markdown(secondpara,unsafe_allow_html=True)




    #######################################################################################
    st.markdown("<h1 class='Title'> What to do if you feel unwell</h1>",unsafe_allow_html=True)
    thirdpara='''
        <div class="card1">
        <ul class="list">
        <li>Know the full range of symptoms of COVID-19. The most common symptoms of COVID-19 are fever, dry cough, and tiredness. Other symptoms that are less common and may affect some patients include loss of taste or smell, aches and pains, headache, sore throat, nasal congestion, red eyes, diarrhoea, or a skin rash.</li>
        <li>Stay home and self-isolate even if you have minor symptoms such as cough, headache, mild fever, until you recover. Call your health care provider or hotline for advice. Have someone bring you supplies. If you need to leave your house or have someone near you, wear a medical mask to avoid infecting others.</li>
        <li>If you have a fever, cough and difficulty breathing, seek medical attention immediately. Call by telephone first, if you can and follow the directions of your local health authority.</li>
        <li>Keep up to date on the latest information from trusted sources, such as WHO or your local and national health authorities. Local and national authorities and public health units are best placed to advise on what people in your area should be doing to protect themselves.</li></ul>
        </div>
    '''
    st.markdown(thirdpara,unsafe_allow_html=True)
    ######################### Helpline Api #####################
    url="https://dharmikmidha.000webhostapp.com/covid/index.json"
    r=requests.get(url)
    df=json_normalize(r.json())
    # st.write(df.helpline_number[i])
    # st.write(df.state_or_UT[i]))
    
    def tr():
        tablerow=""
        for i in range(len(df)):
                tr=""" <tr> <td>"""+df.state_or_UT[i]+"""</td>
                        <td>"""+df.helpline_number[i]+"""</td>
                        </tr>
                    """
                tablerow=tablerow+tr
        return tablerow

    tablerow=tr()
    table="""<table>
                <tr><th>State</th><th>Helpline No.</th></tr>"""+tablerow
    
    st.markdown(table,unsafe_allow_html=True)
    made_by()


    ###############################################Graph#####################################
def Graphs():
    
    st.markdown("<h1 class='Title'>  Covid-19 Dashboard </h1>", unsafe_allow_html=True)
    #################################################################################
    #Different Api
    url = 'https://api.covid19api.com/countries'
    r = requests.get(url)
    df0 = json_normalize(r.json())

    #to select a country
    top_row = pd.DataFrame({'Country':['Select a Country'],'Slug':['Empty'],'ISO2':['E']})
    
    # Concat with old DataFrame and reset the Index.
    df0 = pd.concat([top_row, df0]).reset_index(drop = True)

    st.sidebar.header('Create/Filter your search')
    graph_type = st.sidebar.selectbox('Cases type',('confirmed','deaths','recovered'))
    st.sidebar.subheader('Search by country 📍')
    country = st.sidebar.selectbox('Country',df0.Country)
    if st.sidebar.button('Refresh Data'):
        country='Select a Country'
   

        
    # Select A Country
    if country != 'Select a Country':
        slug = df0.Slug[df0['Country']==country].to_string(index=False)
        #data of confirmed cases
        url = 'https://api.covid19api.com/total/dayone/country/'+slug+'/status/'+graph_type
        r = requests.get(url)
        if(r.json()==[]):
            st.markdown('''<h1 style='text-align:center; color:red; '>Data Not Available </h1>''',unsafe_allow_html=True)
            
            
        else:
            #empty array for appending color
            colors=[]
            #list of colors 
            line_color={
                'confirmed' : 'blue',
                'deaths' : 'red',
                'recovered' : 'green'
            }
            #for changing the color as per graph type
            for color in line_color:
                if color==(graph_type):
                    colors.append(line_color[color]) 
            ########################################                   

            st.write("""# Total """+graph_type+""" cases in """+country+""" are: """+str(r.json()[-1].get("Cases")))
            df1 = json_normalize(r.json())
            layout = go.Layout(
                title = country+'\'s '+graph_type+' cases Data',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'Number of cases'),)
            fig.update_layout(dict1 = layout, overwrite = True)
            fig.add_trace(go.Scatter(x=df1.Date, y=df1.Cases, mode='lines', name=country,line=dict(color=colors[0],width=5)))
            st.plotly_chart(fig, use_container_width=True)

             ###################################COnfirmed,death and recovered####################
            fig1= go.Figure()
            url1 = 'https://api.covid19api.com/total/dayone/country/'+slug+'/status/confirmed'
            url2 = 'https://api.covid19api.com/total/dayone/country/'+slug+'/status/deaths'
            url3 = 'https://api.covid19api.com/total/dayone/country/'+slug+'/status/recovered'
            r1 = requests.get(url1)
            r2 = requests.get(url2)
            r3 = requests.get(url3)
            df2=(json_normalize(r1.json()))
            df3=(json_normalize(r2.json()))
            df4=(json_normalize(r3.json()))
            layout = go.Layout(
                title = country+'\'s  cases Data',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'Number of cases'),)
            fig1.update_layout(dict1 = layout, overwrite = True)

            fig1.add_trace(go.Scatter(x=df2.Date, y=df2.Cases, mode='lines', name='Confirmed',line=dict(color='blue',width=5)))
            fig1.add_trace(go.Scatter(x=df3.Date, y=df3.Cases, mode='lines', name='Deaths',line=dict(color='red',width=5)))
            fig1.add_trace(go.Scatter(x=df4.Date, y=df4.Cases, mode='lines', name='Recovered',line=dict(color='green',width=5)))
            st.plotly_chart(fig1, use_container_width=True)




    else:
        url = 'https://api.covid19api.com/world/total'
        r = requests.get(url)
        total = r.json()["TotalConfirmed"]
        deaths = r.json()["TotalDeaths"]
        recovered = r.json()["TotalRecovered"]
        st.markdown("""<div class='subhead'><h2> Worldwide Data:<h2></div>""",unsafe_allow_html=True)
        st.write("Total cases: "+str(total)+", Total deaths: "+str(deaths)+", Total recovered: "+str(recovered))
        x = ["TotalCases", "TotalDeaths", "TotalRecovered"]
        y = [total, deaths, recovered]

        layout = go.Layout(
            title = 'World Data',
            xaxis = dict(title = 'Category'),
            yaxis = dict(title = 'Number of cases'),)
        
        fig.update_layout(dict1 = layout, overwrite = True)
        fig.add_trace(go.Bar(name = 'World Data', x = x, y = y))
        st.plotly_chart(fig, use_container_width=True)

    

    ################# Countries With Most Cases #################
    
    st.markdown("<h2 class='Title'>Countries with most number of cases</h2>",
                unsafe_allow_html=True)
    type_of_case = st.selectbox('Select type of case : ', 
                                ['Confirmed', 'Active', 'Deaths', 'Recovered'],
                                key = 'most_cases')
    selected_count = st.slider('No. of countries :', 
                            min_value=1, max_value=50, 
                            value=10, key='most_count')
    sorted_country_df = country_df.sort_values(type_of_case, ascending= False) 
    def bubble_chart(n):
        figure = px.scatter(sorted_country_df.head(n), x="Country_Region", y=type_of_case, size=type_of_case, color="Country_Region",
                hover_name="Country_Region", size_max=60)
        figure.update_layout(
        title=str(n) +" Countries with most " + type_of_case.lower() + " cases",
        xaxis_title="Countries",
        yaxis_title= type_of_case + " Cases",
        width = 800
        )
        st.plotly_chart(figure)
    bubble_chart(selected_count)
    #############################################################


    ################# Countries With Least Cases #################
    
    st.markdown("<h2 class='Title'>Countries with least number of cases</h2>",
                unsafe_allow_html=True)
    type_of_case = st.selectbox('Select type of case : ', 
                                ['Confirmed', 'Active', 'Deaths', 'Recovered'],
                                key = 'least_cases')
    selected_count = st.slider('No. of countries :', 
                            min_value=1, max_value=50, 
                            value=10, key = 'least_cases')
    sorted_country_df = country_df[country_df[type_of_case] > 0].sort_values(type_of_case, ascending= True)
    def bubble_chart(n):
        figure = px.scatter(sorted_country_df.head(n), x="Country_Region", y=type_of_case, size=type_of_case, color="Country_Region",
                hover_name="Country_Region", size_max=60)
        figure.update_layout(
        title=str(n) +" Countries with least " + type_of_case.lower() + " cases",
        xaxis_title="Countries",
        yaxis_title= type_of_case + " Cases",
        width = 800
        )   
        st.plotly_chart(figure)
    bubble_chart(selected_count)

    #############################################################
    made_by()


def Vaccine():
    url="https://www.mygov.in/sites/default/files/covid/vaccine/vaccine_counts_today.json?timestamp=1624170600"
    r=requests.get(url)
    df=json_normalize(r.json())

    st.markdown(" <h1 class='tableheadingset'>Information Regarding Vaccine's </h1>",unsafe_allow_html=True)

    def vacapi():
        struct=""   
        for i in range(37):
            structure="""<tr>
                            <td>"""+df.vacc_st_data[0][i]['st_name']+"""</td>
                            <td>"""+df.vacc_st_data[0][i]['dose1']+"""</td>
                            <td>"""+df.vacc_st_data[0][i]['dose2']+"""</td>
                            <td>"""+df.vacc_st_data[0][i]['total_doses']+"""</td>
                            <td>"""+df.vacc_st_data[0][i]['last_dose1']+"""</td>
                            <td>"""+df.vacc_st_data[0][i]['last_dose2']+"""</td>
                            <td>"""+df.vacc_st_data[0][i]['last_total_doses']+"""</td>
                        </tr>"""
            struct+=structure
        return struct

    structure=vacapi()
    st.markdown("""<div class="table-wrapper">
        <table class="fl-table">
    <thead>
        <tr>
        <th class="header">State Name</th>
        <th class="header">Sr. Citizen 1st Dose</th>
        <th class="header">Adult 1st Dose</th>
        <th class="header">Total 1st Dose</th>
        <th class="header">Sr. Citizen 2nd Dose</th>
        <th class="header">Adult 2nd Dose</th>
        <th class="header">Total 2nd Dose</th>
        </tr>
    </thead>
    <tbody>"""+structure+"""</tbody></table></div>""",unsafe_allow_html=True)
    made_by()


status=st.sidebar.radio('INDEX',("🏠 Home","📊 Graphs","💉 Vaccine","💡 Help","🧾 About"))
if(status=="💡 Help"):
    Help()
elif(status=="🏠 Home"):
    Home()
elif(status=="📊 Graphs"):
    Graphs()
elif(status=="💉 Vaccine"):
    Vaccine()
elif(status=="🧾 About"):
    About()