import streamlit as st
from streamlit_option_menu import option_menu
import os
import time
import pandas as pd
from dotenv import load_dotenv
import plotly.express as px
from PIL import Image
from streamlit_elements import elements, mui, html, sync
import plotly.graph_objects as go
import requests



# Read the Csv file
agg_insurance_data=pd.read_csv('https://raw.githubusercontent.com/Shobana1310/Phonepe-Pulse/main/DataSet/agg_insurance_data.csv')
agg_transaction_data=pd.read_csv('https://raw.githubusercontent.com/Shobana1310/Phonepe-Pulse/main/DataSet/agg_transaction_data.csv')
agg_user_data=pd.read_csv('https://raw.githubusercontent.com/Shobana1310/Phonepe-Pulse/main/DataSet/agg_user_data.csv')
map_insurance_data=pd.read_csv('https://raw.githubusercontent.com/Shobana1310/Phonepe-Pulse/main/DataSet/map_insurance_data.csv')
map_transaction_data=pd.read_csv('https://raw.githubusercontent.com/Shobana1310/Phonepe-Pulse/main/DataSet/map_transaction_data.csv')
map_user_data=pd.read_csv('https://raw.githubusercontent.com/Shobana1310/Phonepe-Pulse/main/DataSet/map_user_data.csv')
map_user_data['District']=map_user_data['District'].str.strip()
map_insurance_data['District']=map_insurance_data['District'].str.strip()
map_transaction_data['State']=map_transaction_data['State'].str.replace('Andaman And Nicobar Islands','Andaman & Nicobar')
map_insurance_data['State']=map_insurance_data['State'].str.replace('Andaman & Nicobar Islands','Andaman & Nicobar')
map_user_data['State']=map_user_data['State'].str.replace('Andaman & Nicobar Islands','Andaman & Nicobar')


class Convert:
    @staticmethod
    def millions(transaction):
        c = transaction / 1_000_000
        d = '{:.2f}'.format(c)
        return f'{d}M'

    @staticmethod
    def billions(transaction):
        c = transaction / 1_000_000_000
        d = '{:.2f}'.format(c)
        return f'{d}B'

    @staticmethod
    def trillions(transaction):
        c = transaction / 1_000_000_000_000
        d = '{:.2f}'.format(c)
        return f'{d}T'

    @staticmethod
    def crores(transaction):
        c = transaction / 10_000_000
        d = '{:.2f}'.format(c)
        return f'{d}Cr'

    @staticmethod
    def thousands(transaction):
        c = transaction / 1_000
        d = '{:.2f}'.format(c)
        return f'{d}K'

    @staticmethod
    def rupees(transaction):
        if transaction <= 1_000:
            return str(transaction)
        elif transaction <= 1_000_000:
            return Convert.thousands(transaction)
        elif transaction <= 1_000_000_000:
            return Convert.millions(transaction)
        elif transaction <= 1_000_000_000_000:
            return Convert.billions(transaction)
        else:
            return Convert.trillions(transaction)


state_geojson_links = { "Andaman & Nicobar":"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ANDAMAN%20%26%20NICOBAR_DISTRICTS.geojson",
                            'Andhra Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ANDHRA%20PRADESH_DISTRICTS.geojson",
                            'Arunachal Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ARUNACHAL%20PRADESH_DISTRICTS.geojson",
                            'Assam':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ASSAM_DISTRICTS.geojson", 
                            'Bihar':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/BIHAR_DISTRICTS.geojson", 
                            'Chandigarh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/CHANDIGARH_DISTRICTS.geojson", 
                            'Chhattisgarh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/CHHATTISGARH_DISTRICTS.geojson",
                            'Dadra and Nagar Haveli and Daman and Diu':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/Dadra%20And%20Nagar%20Haveli%20And%20Daman%20And%20Diu%20DISTRICTS.geojson", 
                            'Delhi' :"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/DELHI_DISTRICTS.geojson", 
                            'Goa':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/GOA_DISTRICTS.geojson",
                            'Gujarat':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/GUJARAT_DISTRICTS.geojson", 
                            'Haryana':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/HARYANA_DISTRICTS.geojson", 
                            'Himachal Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/HIMACHAL%20PRADESH_DISTRICTS.geojson", 
                            'Jammu & Kashmir': "https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/JAMMU%20%26%20KASHMIR_DISTRICTS.geojson",
                            'Jharkhand':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/JHARKHAND_DISTRICTS.geojson", 
                            'Karnataka':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/KARNATAKA_DISTRICTS.geojson", 
                            'Kerala':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/KERALA_DISTRICTS.geojson", 
                            'Ladakh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/LADAKH_DISTRICTS.geojson", 
                            'Lakshadweep':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/LAKSHADWEEP_DISTRICTS.geojson",
                            'Madhya Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MADHYA%20PRADESH_DISTRICTS.geojson", 
                            'Maharashtra':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MAHARASHTRA_DISTRICTS.geojson", 
                            'Manipur':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MANIPUR_DISTRICTS.geojson", 
                            'Meghalaya':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MEGHALAYA_DISTRICTS.geojson", 
                            'Mizoram':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/MIZORAM_DISTRICTS.geojson",
                            'Nagaland':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/NAGALAND_DISTRICTS.geojson", 
                            'Odisha':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/ODISHA_DISTRICTS.geojson", 
                            'Puducherry':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/PUDUCHERRY_DISTRICTS.geojson", 
                            'Punjab':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/PUNJAB_DISTRICTS.geojson", 
                            'Rajasthan':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/RAJASTHAN_DISTRICTS.geojson",
                            'Sikkim':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/SIKKIM_DISTRICTS.geojson", 
                            'Tamil Nadu':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/TAMIL%20NADU_DISTRICTS.geojson", 
                            'Telangana':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/TELANGANA_DISTRICTS.geojson", 
                            'Tripura': "https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/TRIPURA_DISTRICTS.geojson", 
                            'Uttar Pradesh':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/UTTAR%20PRADESH_DISTRICTS.geojson",
                            'Uttarakhand':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/UTTARAKHAND_DISTRICTS.geojson", 
                            'West Bengal':"https://raw.githubusercontent.com/navinds/PhonePe-Pulse-Data-Visualization-and-Exploration/main/India%20Geo/States/WEST%20BENGAL_DISTRICTS.geojson"}


def india_geojson():
        india = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        return india  


zoom = { "Andaman & Nicobar": 5,
                            'Andhra Pradesh':5.5,
                            'Arunachal Pradesh':5.5,
                            'Assam':5.5, 
                            'Bihar':5.5, 
                            'Chandigarh':9, 
                            'Chhattisgarh':5.5,
                            'Dadra and Nagar Haveli and Daman and Diu':8, 
                            'Delhi' :8, 
                            'Goa':7,
                            'Gujarat':5.5, 
                            'Haryana':6, 
                            'Himachal Pradesh':6, 
                            'Jammu & Kashmir': 5.5,
                            'Jharkhand':5.5, 
                            'Karnataka':5.5, 
                            'Kerala':6, 
                            'Ladakh':5, 
                            'Lakshadweep':6,
                            'Madhya Pradesh':5.5, 
                            'Maharashtra':5.5, 
                            'Manipur':7, 
                            'Meghalaya':7, 
                            'Mizoram':7,
                            'Nagaland':7, 
                            'Odisha':5.5, 
                            'Puducherry':7, 
                            'Punjab':6, 
                            'Rajasthan':5.5,
                            'Sikkim':5, 
                            'Tamil Nadu':5.5, 
                            'Telangana':5.5, 
                            'Tripura': 7, 
                            'Uttar Pradesh':5.5,
                            'Uttarakhand':6, 
                            'West Bengal':5}

state_coordinates = {
        "Andaman & Nicobar": {"lat": 10.7449, "lon": 92.5000},
        "Andhra Pradesh": {"lat": 15.9129, "lon": 79.7400},
        "Arunachal Pradesh": {"lat": 28.2180, "lon": 94.7278},
        "Assam": {"lat": 26.2006, "lon": 92.9376},
        "Bihar": {"lat": 25.0961, "lon": 85.3131},
        "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
        "Chhattisgarh": {"lat": 21.2787, "lon": 81.8661},
        "Dadra and Nagar Haveli and Daman and Diu": {"lat": 20.1809, "lon": 73.0169},
        "Delhi": {"lat": 28.7041, "lon": 77.1025},
        "Goa": {"lat": 15.2993, "lon": 74.1240},
        "Gujarat": {"lat": 22.2587, "lon": 71.1924},
        "Haryana": {"lat": 29.0588, "lon": 76.0856},
        "Himachal Pradesh": {"lat": 31.1048, "lon": 77.1734},
        "Jammu & Kashmir": {"lat": 33.7782, "lon": 76.5762},
        "Jharkhand": {"lat": 23.6102, "lon": 85.2799},
        "Karnataka": {"lat": 15.3173, "lon": 75.7139},
        "Kerala": {"lat": 10.8505, "lon": 76.2711},
        "Ladakh": {"lat": 34.1526, "lon": 77.5770},
        "Lakshadweep": {"lat": 10.5667, "lon": 72.6417},
        "Madhya Pradesh": {"lat": 22.9734, "lon": 78.6569},
        "Maharashtra": {"lat": 19.7515, "lon": 75.7139},
        "Manipur": {"lat": 24.6637, "lon": 93.9063},
        "Meghalaya": {"lat": 25.4670, "lon": 91.3662},
        "Mizoram": {"lat": 23.1645, "lon": 92.9376},
        "Nagaland": {"lat": 26.1584, "lon": 94.5624},
        "Odisha": {"lat": 20.9517, "lon": 85.0985},
        "Puducherry": {"lat": 11.9416, "lon": 79.8083},
        "Punjab": {"lat": 31.1471, "lon": 75.3412},
        "Rajasthan": {"lat": 27.0238, "lon": 74.2179},
        "Sikkim": {"lat": 27.5330, "lon": 88.5122},
        "Tamil Nadu": {"lat": 11.1271, "lon": 78.6569},
        "Telangana": {"lat": 18.1124, "lon": 79.0193},
        "Tripura": {"lat": 23.9408, "lon": 91.9882},
        "Uttar Pradesh": {"lat": 26.8467, "lon": 80.9462},
        "Uttarakhand": {"lat": 30.0668, "lon": 79.0193},
        "West Bengal": {"lat": 22.9868, "lon": 87.8550}}



icon_url='https://asset.brandfetch.io/idcE0OdG8i/id8Yth9ASQ.svg?updated=1668075190583'
st.set_page_config(page_title="PhonePe  |  Pulse", page_icon=icon_url, layout="wide")
violet_color = "#6F36AD"


selected = option_menu("Navigation",
                       options=["ABOUT","HOME","TOP INSIGHTS", "GEO VISUALIZATION","REPORT"],
                       icons=["info-circle","house", "bar-chart","globe-americas","file-text"],
                       default_index=1,
                       orientation="horizontal")

if selected=='ABOUT':
      text_to_center = "PhonePe Pulse"
      logo_url='https://asset.brandfetch.io/idcE0OdG8i/id8Yth9ASQ.svg?updated=1668075190583'
      st.markdown(f"""
      <div style='text-align: center;'>
      <img src="{logo_url}" alt="PhonePe Logo" style="width: 85px; height: auto; margin-bottom: 10px;"> 
      <span style='background-image: linear-gradient(to right, white 0%, purple 100%);
                     -webkit-background-clip: text;
                     -webkit-text-fill-color: transparent;
                     font-size: 50px; font-weight: bold; font-family: 'Araboto Normal', sans-serif;'>{text_to_center}</span>
      </div>
      """, unsafe_allow_html=True)
      text_to_center1= "PhonePe Pulse offers insights on digital transaction trends in India, including popular payment methods, categories, and regional preferences. Users benefit by understanding their spending habits and market trends. Businesses leverage the data for targeted marketing and strategy adjustments. Ultimately, PhonePe Pulse enhances transparency and empowers informed financial decisions."
      st.markdown(f"<div style='text-align: center; font-size: 20px; font-family: 'Araboto Normal', sans-serif;'>{text_to_center1}</div>", unsafe_allow_html=True)
      with st.container():
         left_column,right_column=st.columns(2)
         with left_column:
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.header(':orange[About Top Insights 📈]')
            st.write('**In the top analysis you can  analyze trends over time, such as fluctuations in transaction volumes, changes in popular payment methods, or shifts in spending patterns across different categories. This helps  gain a deeper understanding of how digital payments are evolving and make informed decisions based on these insights.**')

      with st.container():
         left_column,right_column=st.columns(2)
         with right_column:
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.header(':orange[About Geo Visulization 🌐]')
            st.write('**The map feature helps users understand where digital transactions are most prevalent geographically. This can be useful for both consumers and businesses to identify regions with high digital payment adoption rates and tailor their strategies accordingly**')

      underline = "__________" 
      st.markdown(f"# Purpose of PhonePe Pulse\n{underline}")
      st.header(':violet[🛍️ Consumer Empowerment]')
      st.write('**By providing insights into usage patterns within their own state and district, PhonePe Pulse empowers consumers with knowledge about how people in their locality utilize PhonePe, enabling them to make informed decisions about their financial activities**')
      st.write('')
      st.write('')
      st.header(':violet[🧠 Business Intelligence]')
      st.write('**For businesses, PhonePe Pulse serves as a tool for market research and business intelligence. It provides data on consumer behavior, regional preferences, and market trends, which can help businesses tailor their strategies and offerings accordingly.**')
      st.write('')
      st.write('')
      st.header(':violet[💼 Market Education]')
      st.write('**PhonePe Pulse also plays a role in educating users about the benefits and advantages of digital payments. By highlighting the growth of digital transactions and showcasing the convenience and security of digital payment methods, PhonePe Pulse contributes to increasing awareness and adoption of digital payments in India**')
      
      underline = "__________" 
      st.markdown(underline)
      st.header('About Me')
      st.write('👋 Hi there! I am Shobana, A Passionate into Data Science And Business Solutions. With a Strong Foundation In Data Analysis And Machine Learning, I Thrive On Uncovering Actionable Insights From Complex Datasets to Drive Strategic Decision-making And Enhance Business Performance. I Am Dedicated To Continuous Learning, Always Staying On Latest Trends And Technologies In The Field')
      
      st.write(':blue[**LinkedIn**]')  
      linkedin_logo="https://img.icons8.com/fluent/48/000000/linkedin.png"            # Display LinkedIn logo with a link to the profile.
      linkedin_url="https://www.linkedin.com/in/shobana-v-534b472a2"
      st.markdown(f"[![LinkedIn]({linkedin_logo})]({linkedin_url})")
    

if selected == 'HOME':
   st.write('')
   st.write('')
   image_path ="https://i.postimg.cc/qqc2RRfd/phonepe-pulse.png"
   st.image(image_path, use_column_width=True)
   st.write('')
   st.write('')
   st.write('')
   st.write('')
   st.write('')
   st.write('')
   with st.container():
         left_column,right_column=st.columns(2)
         with left_column:
            video_url = "https://www.phonepe.com/webstatic/6805/videos/page/home-fast-secure-v3.mp4"
            video_html = f"""
            <video width="100%" autoplay loop muted>
            <source src="{video_url}" type="video/mp4">
            Your browser does not support the video tag.
            </video>
            """

            st.markdown(video_html, unsafe_allow_html=True)
         with right_column:
            st.header(':violet[About PhonePe]')
            # st.write('')
            # st.write('')
            st.write('**PhonePe is a leading digital wallet using which you can transfer money through UPI, recharge prepaid mobile, make utility bill payments, and much more. Just add your bank account details and generate a UPI ID. Without worrying about recharging your wallet, you can begin shopping safely and securely. So, go ahead and download PhonePe today to enjoy great perks of online shopping!**')
            image_path ="https://i.postimg.cc/Ls7WkyJ8/bs-hero-banner-image1.png"
            st.image(image_path,width=450)
   st.write('')
   st.write('')
   st.write('')
   with st.container():
         left_column,right_column=st.columns(2)
         with left_column:
            image_path ="https://i.postimg.cc/h4wGzgDk/download.png"
            st.image(image_path,width=100)
            st.header(':violet[Secure from the start]')
            st.write('')
            st.write('**Every transaction on PhonePe needs your fingerprint/face ID, UPI PIN and password for authentication.**')
         with right_column:
            image_path ="https://i.postimg.cc/FR5M5WNn/download-1.png"
            st.image(image_path,width=100)
            st.header(':violet[Payment Privacy]')
            st.write('')
            st.write('**Only you and the person you are transacting with will be able to see the details of your payment.**')
   with st.container():
         left_column,right_column=st.columns(2)
         with left_column:
            image_path ="https://i.postimg.cc/Njb8w5Yh/download-2.png"
            st.image(image_path,width=100)
            st.header(':violet[Risk assessment]')
            st.write('')
            st.write('**PhonePe teams monitor all transactions in real-time to block any suspicious activity. They also report fraud complaints & block fraudulent users from accessing the PhonePe platform**')
         with right_column:
            image_path ="https://i.postimg.cc/rpBNf7Mz/download-3.png"
            st.image(image_path,width=100)
            st.header(':violet[Partners in protection]')
            st.write('')
            st.write('**To aid safe transactions,PhonePe with cyber-crime cells of government law enforcement and security agencies, such as National Cybercrime Portal, CyCord and CyberSafe.**')
   st.write('')
   st.write('')
   def download_phonepe():
   
      android_link = "https://play.google.com/store/apps/details?id=com.phonepe.app"
      ios_link = "https://apps.apple.com/in/app/phonepe-secure-payments-app/id1170055821"

      st.header(":violet[Download PhonePe]")
      st.markdown("[Download on Google Play](%s)" % android_link)
      st.markdown("[Download on the App Store](%s)" % ios_link)
   download_phonepe()

   st.header(':orange[If you Want To Know More About PhonePe,Kindly Check This]')
   left_column,right_column=st.columns(2)
   with left_column:
      st.video('https://youtu.be/c_1H6vivsiA?si=lVPODg0axykJgeAZ')
   with right_column:
      st.video('https://youtu.be/Yy03rjSUIB8?si=eJRqbCm-K_RDtv0Y')

if selected=='TOP INSIGHTS':
  Analyse_method=st.radio('Select The Options',('User','Transaction','Insurance'))

  if Analyse_method=='User':
    with st.container():
           left_column,right_column=st.columns(2)
           with left_column:
               image_path ="https://i.postimg.cc/ryrSpqxH/Getty-Images-1234065228.jpg"
               st.image(image_path,width=400)
    option=st.radio('How would you like to Analyse?',['State Wise','District Wise'],index=None,horizontal=True)         
    st.write('You selected:', option)

    if option=='State Wise':
        questions = ["The Top10 States In India Has Highest Registered Users",
                                "States Has Very Lowest Registered Users in India",
                                "PhonePe Growth Among Users in India"]         
        selected_query = st.selectbox("Select a Query", questions,index= None)

        if selected_query==questions[0]:
             tab1, tab2,tab3 = st.tabs(["📈 Chart", "🗃 Data","📄 Insight Points"])
             with tab1:
               filter_df=map_user_data.groupby('State')['Registered_Users'].sum().sort_values(ascending=False).reset_index().nlargest(10,'Registered_Users')
               fig = px.bar(filter_df, 
               x='State', 
               y='Registered_Users',
               title='Top 10 States has Highest Registered Users',
               labels={'Registered_Users': 'Registered_Users Count', 'State': 'States'},
               color='State',
               color_discrete_sequence=px.colors.qualitative.Light24_r,
               template='plotly_white')
               fig.update_traces(texttemplate='%{y}', textposition='outside')
               st.plotly_chart(fig, use_container_width=True)
             with tab2:
                st.dataframe(filter_df)
             with tab3:
               text1 = "🔹 Maharashtra has big cities like Mumbai and Pune are money and tech centers. People there use PhonePe for payments."
               text2 = "🔹 Karnataka, particularly Bengaluru, is known as India's Silicon Valley. A large young and tech-savvy population combined with a strong entrepreneurial spirit drives the adoption of digital platforms."
               text3 = "🔹 Rajasthan's vibrant tourism sector attracts both domestic and international visitors. Government initiatives to promote digital payments in tourist spots and cities like Jaipur likely contribute to higher PhonePe adoption."
               text4 = "🔹 In Tamil Nadu there are lots of factories and IT companies, especially in places like Chennai. Workers there often use digital payments for convenience."

               def generate_text1():
                  for word in text1.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text2():
                  for word in text2.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text3():
                  for word in text3.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text4():
                  for word in text4.split():
                     yield word + " "
                     time.sleep(0.03)
               st.write_stream(generate_text1)
               st.write_stream(generate_text2)
               st.write_stream(generate_text3)
               st.write_stream(generate_text4)


           
        elif selected_query==questions[1]:
             tab1, tab2,tab3 = st.tabs(["📈 Chart", "🗃 Data","📄 Insight Points"])
             with tab1:
               filter_df=map_user_data.groupby('State')['Registered_Users'].sum().reset_index().nsmallest(5,'Registered_Users')
               filter_df = filter_df.sort_values(by='Registered_Users', ascending=False).reset_index(drop=True)
               fig = px.bar(filter_df, 
               x='State', 
               y='Registered_Users',
               title='The lowest 5 States Based On Registered Users',
               labels={'Registered_Users': 'Registered_Users Count', 'State': 'States'},
               color='State',
               color_discrete_sequence=px.colors.qualitative.Safe_r,
               template='plotly_white')
               fig.update_traces(texttemplate='%{y}', textposition='outside')
               st.plotly_chart(fig,use_container_width=True)
             with tab2:
                st.dataframe(filter_df)
             with tab3:
               text5 = "🔹 Sikkim is a small state with fewer people. Also, the mountains there can make it hard to get good internet, which might make it tough for people to use PhonePe."
               text6 = "🔹 Being a group of islands, Andaman & Nicobar face challenges related to connectivity and infrastructure, which may hinder the widespread adoption of PhonePe."
               text7 = "🔹 Lakshadweep's remote island location and limited connectivity might make it challenging for people to access and use digital payment platforms regularly."
               def generate_text5():
                  for word in text5.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text6():
                  for word in text6.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text7():
                  for word in text7.split():
                     yield word + " "
                     time.sleep(0.03)
               st.write_stream(generate_text5)
               st.write_stream(generate_text6)
               st.write_stream(generate_text7)
           
        elif selected_query==questions[2]:
           tab1, tab2,tab3 = st.tabs(["📈 Chart", "🗃 Data","📄 Insight Points"])
           with tab1:
              filter_df=map_user_data.groupby('Year')['Registered_Users'].sum().reset_index()
              fig = px.bar(filter_df, 
               x='Year', 
               y='Registered_Users',
               title='Phonepe Growth Among Users',
               labels={'Registered_Users': 'Registered_Users Count', 'State': 'States'},
               color='Year',
               color_continuous_scale='cividis',
               template='plotly_white')
              fig.update_traces(texttemplate='%{y}', textposition='outside')
              st.plotly_chart(fig,use_container_width=True)
           with tab2:
              st.dataframe(filter_df)
           with tab3:
               text8 = "🔹 PhonePe started with 292,797,872 registered users in its early years, indicating a growing interest and adoption of digital payment platforms in India."
               text9 = "🔹 In 2020, the COVID-19 pandemic acted as a catalyst for digital payments. With people avoiding physical transactions, the registered users soared to 922,009,385, reflecting a sharp increase in digital transactions."
               text10 = "🔹 With 1,927,042,597 registered users by 2023, PhonePe solidified its position as a leading digital payment platform in India. The continued growth reflects its strong brand loyalty."

               def generate_text8():
                  for word in text8.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text9():
                  for word in text9.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text10():
                  for word in text10.split():
                     yield word + " "
                     time.sleep(0.03)

               st.write_stream(generate_text8)
               st.write_stream(generate_text9)
               st.write_stream(generate_text10)
               


    elif option=='District Wise':
        questions = ["All over The India The Top10 Districts Has Highest Users ",
                     "Districts Has Highest Users In Each State"]         
        selected_query = st.selectbox("Select a Query", questions,index= None)

        if selected_query==questions[0]:
            tab1, tab2,tab3 = st.tabs(["📈 Chart", "🗃 Data","📄 Insight Points"])
            with tab1:
               filter_df=map_user_data.groupby('District')['Registered_Users'].sum().reset_index().nlargest(10,'Registered_Users').reset_index(drop=True)
               fig = px.bar(filter_df, 
               x='District', 
               y='Registered_Users',
               title='The Top 10 Districts Has Highest Registered Users',
               labels={'Registered_Users': 'Registered_Users Count', 'District': 'Districts'},
               color='District',
               color_discrete_sequence=px.colors.qualitative.Antique,
               template='plotly_white')
               fig.update_traces(texttemplate='%{y}', textposition='outside')
               st.plotly_chart(fig,use_container_width=True)
            with tab2:
               filter_df
            with tab3:
               text11 = "🔹 The top districts with the highest number of PhonePe users are primarily urban centers with a strong presence of IT, business, tourism, and connectivity."
               text12 = "🔹 These districts benefit from their economic activities, urbanization, and tech-savvy population, driving the adoption and growth of digital payment."

               def generate_text11():
                  for word in text11.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text12():
                  for word in text12.split():
                     yield word + " "
                     time.sleep(0.03)
               st.write_stream(generate_text11)
               st.write_stream(generate_text12)
               

           
        elif selected_query==questions[1]:
           selected_state= st.selectbox('Choose a State',(map_user_data['State'].unique()),index=None,placeholder="Select The States...",)
           st.write('You selected:', selected_state)
           if selected_state:
               tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
               with tab1:
                  def top10_districts_has_highestusers(df,state):
                        filter_df=df.loc[(df['State']==state)].reset_index(drop=True)
                        top_10=filter_df.groupby(['State','District'])['Registered_Users'].sum().sort_values(ascending=False).reset_index().nlargest(10,'Registered_Users')
                        fig = px.bar(top_10, 
                              x='District', 
                              y='Registered_Users',
                              title=f'The Top10 districts has highest Users in {state}',
                              labels={'Registered_Users': 'Registered_Users Count', 'District': 'Districts'},
                              color='District',
                              color_continuous_scale='cividis',
                              template='plotly_white')
                        fig.update_traces(texttemplate='%{y}', textposition='outside')

                        st.plotly_chart(fig,use_container_width=True)
                  top10_districts_has_highestusers(map_user_data,selected_state)
          
               if selected_state=='Tamil Nadu':
                  with st.expander('See Explanation'):
                     st.write("Chennai and Thiruvallur ,Lots of people live here, and many have smartphones. It's just easier to have PhonePe for bills, shopping, and maybe even catching a ride! Plus, Thiruvallur being close to Chennai might be catching on to the digital payment trend.")
                     st.write("Coimbatore, the industrial center . Lots of businesses here, and people working in those places are probably comfortable using apps like PhonePe.")
               
               if selected_state=='Andhra Pradesh':
                  with st.expander('See Explanation'):
                     st.write( " Visakhapatnam, being a major port city and hub for industries and services, likely has a growing urban population that is increasingly adopting digital payment with PhonePe.")
                     st.write("East Godavari, known for its agricultural activities and economic development, may have a significant number of users using PhonePe for transactions related to agriculture, businesses, and daily activities.")
                     st.write("Factors such as urbanization, economic growth, agricultural activities, and government initiatives promoting digital payments likely contribute to the adoption and growth of PhonePe in these districts.")
               
               if selected_state=='Arunachal Pradesh':
                  with st.expander('See Explanation'):
                     st.write("West Kameng, known for its scenic beauty and tourist attractions, may have a growing population of visitors and residents using PhonePe for transactions related to tourism, businesses, and daily activities.")
                     st.write("Changlang's economic development, infrastructure growth, and increasing connectivity may encourage the adoption of PhonePe among its growing population and businesses.")
            
               if selected_state=='Delhi':
                  with st.expander('See Explanation'):
                     st.write("West Delhi & south east Delhi, with its mix of commercial and residential areas, likely has a significant number of users using PhonePe for daily transactions, shopping, and bill payments.")
                     st.write("New Delhi & central Delhi, being the capital territory and a major administrative and commercial hub, likely has a high number of users familiar with and adopting digital payment platforms like PhonePe.")

               
               if selected_state=='Kerala':
                  with st.expander('See Explanation'):
                     st.write( "Ernakulam, Trivandrum being a major economic and commercial hub in Kerala with cities like Kochi, likely has a high number of users using PhonePe for various transactions, shopping, and bill payments.")
                     st.write("Alappuzha's focus on tourism, economic activities, and connectivity likely encourage the adoption of PhonePe among its diverse population and businesses.")
                     st.write("Kottayam's educational institutions, economic activities, and connectivity likely contribute to the adoption of PhonePe among its residents and businesses.")
           

                              
               with tab2:
                  def top10_districts_has_highestusers_data(df,state):
                     filter_df=df.loc[(df['State']==state)].reset_index(drop=True)
                     top_10=filter_df.groupby(['State','District'])['Registered_Users'].sum().sort_values(ascending=False).reset_index().nlargest(10,'Registered_Users')

                     st.dataframe(top_10[['District','Registered_Users']])
                  top10_districts_has_highestusers_data(map_user_data,selected_state)
           else:
              st.warning('Please Select The Above Options')
         
              
    
    
  if Analyse_method=='Transaction':
        with st.container():
           left_column,right_column=st.columns(2)
           with left_column:
               image_path ="https://i.postimg.cc/C1FrCz0m/phone-pe-yes-bank-768x384.jpg"
               st.image(image_path, use_column_width=True)

        option=st.radio('How would you like to Analyse?',['State Wise','District Wise'],index=None,horizontal=True)  
        st.write('You selected:', option)

        if option=='State Wise':
            questions = ["The Top5 States Highest Transaction",
                         "Transaction In Each Payment Type",
                          "Transaction In Each Year",
                          "Transaction Growth Across Year"]         
            selected_query = st.selectbox("Select a Query", questions,index= None)

            if selected_query==questions[0]:
              tab1,tab2=st.tabs(['Transaction Count Based Chart 📈','Transaction Amount Based Chart 📈'])
              with tab1:
                 total_transaction=agg_transaction_data.groupby('State')['Trans_count'].sum().sort_values(ascending=True).reset_index()
                 top_5_states = total_transaction.nlargest(5, 'Trans_count').reset_index(drop=True)
                 fig = px.bar(top_5_states, 
                              x='State', 
                              y='Trans_count',
                              title='Top 5 States by Transaction Count',
                              labels={'Trans_count': 'Total Transactions', 'State': 'States'},
                              color='State',
                              color_discrete_sequence=px.colors.qualitative.Vivid)
                 st.plotly_chart(fig,use_container_width=True)
                 st.dataframe(top_5_states)
              with tab2:
                 total_amount=agg_transaction_data.groupby('State')['Amount'].sum().sort_values(ascending=True).reset_index()
                 top_5_states = total_amount.nlargest(5, 'Amount').reset_index(drop=True)
                 fig = px.bar(top_5_states, 
                              x='State', 
                              y='Amount',
                              title='Top 5 States by Transaction Amount',
                              labels={'Amount': 'Total Amount', 'State': 'States'},
                              color='State',
                              color_discrete_sequence=px.colors.qualitative.Vivid)
                 st.plotly_chart(fig,use_container_width=True)
                 st.dataframe(top_5_states)
                 
            elif selected_query==questions[1]:
              tab1, tab2,tab3 = st.tabs(["📈 Count Based Chart", "📈 Amount Based Chart","📄 Insight Points"])
              with tab1:
                 payment_type=agg_transaction_data.groupby('Name')['Trans_count'].sum().sort_values(ascending=False).reset_index()
                 fig = px.bar(payment_type, 
                           x='Name', 
                           y='Trans_count',
                           title='Transaction in each payment type',
                           labels={'Name': 'Payment Types', 'Trans_count': 'Transaction Count'},
                           color='Name',
                           color_discrete_sequence=px.colors.qualitative.Bold,text_auto=True)
                 fig.update_layout(
                                 font=dict(
                                    family="sans-serif,verdana",
                                    size=12,
                                    color="black"))
                 st.plotly_chart(fig,use_container_width=True)
                 st.dataframe(payment_type)
              with tab2:
                 payment_type=agg_transaction_data.groupby('Name')['Amount'].sum().sort_values(ascending=False).reset_index()
                 fig = px.bar(payment_type, 
                              x='Name', 
                              y='Amount',
                              title='Amount of transaction on each Payment Types',
                              labels={'Name': 'Transaction Types', 'Amount': 'Amount'},
                              color='Name',
                              color_discrete_sequence=px.colors.qualitative.Bold,text_auto=True)
                 fig.update_layout(
                     font=dict(
                        family="sans-serif,verdana",
                        size=12,
                        color="black"))
                 st.plotly_chart(fig,use_container_width=True)
                 st.dataframe(payment_type)
              with tab3:
               text25 = "🔹 Merchant payments are the most common type of transaction on PhonePe, accounting for over half (51.36%) of all transactions. This suggests that PhonePe is widely used for making payments to businesses."
               text26 = "🔹 Peer-to-peer payments are also quite common, representing 38.12% of all transactions. This indicates that PhonePe is a popular platform for sending and receiving money between individuals."
               text27 = "🔹 Recharge & bill payments account for a smaller proportion of transactions (10.28%). This could be due to the presence of other recharge and bill payment options available to users."
               text28 = "🔹 Transactions categorized as 'Others' and 'Financial Services' make up a very small percentage of the total."

               def generate_text25():
                  for word in text25.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text26():
                  for word in text26.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text27():
                  for word in text27.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text28():
                  for word in text28.split():
                     yield word + " "
                     time.sleep(0.03)
               
               st.write_stream(generate_text25)
               st.write_stream(generate_text26)
               st.write_stream(generate_text27)
               st.write_stream(generate_text28)
                 


            elif selected_query==questions[2]:
              selected_Year= st.selectbox('Choose a Year',(agg_transaction_data['Year'].unique()),index=None,placeholder="Select The Year...",)
              st.write('You selected:', selected_Year)
              if selected_Year:
               tab1,tab2=st.tabs(['Transaction Count Based Chart 📈','Transaction Amount Based Chart 📈'])
               with tab1:
                  def Total_Transaction_count_byYear(df,Year):
                        df1=df.loc[df['Year']==Year].reset_index(drop=True)
                        total=df1.groupby('State')['Trans_count'].sum().sort_values(ascending=False).reset_index()
                        fig = px.bar(total, 
                                    x='State', 
                                    y='Trans_count',
                                    title=f'Total Transaction count in {Year}',
                                    labels={'State': 'States', 'Trans_count': 'Transaction Count'},
                                    color='State',
                                    color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig.update_layout(
                           font=dict(
                                 family="sans-serif,verdana",
                                 size=12,
                                 color="black"))
                        st.plotly_chart(fig,use_container_width=True)
                        st.dataframe(total)
                  Total_Transaction_count_byYear(agg_transaction_data,selected_Year)
               with tab2:
                     def Total_Transaction_Amount_byYear(df,Year):
                        df2=df.loc[df['Year']==Year].reset_index(drop=True)
                        total=df2.groupby('State')['Amount'].sum().sort_values(ascending=False).reset_index()
                        fig = px.bar(total, 
                                    x='State', 
                                    y='Amount',
                                    title=f'Total Transaction Amount in {Year}',
                                    labels={'State': 'States', 'Amount': 'Total_Amount'},
                                    color='State',
                                    color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig.update_layout(
                           font=dict(
                                 family="sans-serif,verdana",
                                 size=12,
                                 color="black"))
                        fig.update_traces(marker_line_width=0)
                        st.plotly_chart(fig,use_container_width=True)
                        st.dataframe(total)
                     Total_Transaction_Amount_byYear(agg_transaction_data,selected_Year)
              else:
                 st.warning('Please Select The Above Options')
               
            elif selected_query==questions[3]:
              tab1, tab2,tab3 = st.tabs(["📈 Chart", "🗃 Data","📄 Insight Points"])
              with tab1:
               def seasonal_trends(df):
                     grouped_df = df.groupby(['Year', 'Quarter', 'Name']).agg({'Amount': 'sum', 'Trans_count': 'sum'}).reset_index()

                     fig = px.line(grouped_df, x='Quarter', y='Amount', color='Name', facet_col='Year',
                                    labels={'Amount': 'Total Amount', 'Quarter': 'Quarter'}, title='Transaction Growth Across Year',
                                    template='seaborn')

                     
                     fig.add_scatter(x=grouped_df['Quarter'], y=grouped_df['Trans_count'], mode='lines',
                                    name='Trans_count')

                     st.plotly_chart(fig,use_container_width=True)
               seasonal_trends(agg_transaction_data)
              with tab2:
                     def seasonal_trends_data(df):
                        grouped_df = df.groupby(['Year', 'Quarter', 'Name']).agg({'Amount': 'sum', 'Trans_count': 'sum'}).reset_index()
   
                        st.dataframe(grouped_df)
                     seasonal_trends_data(agg_transaction_data)
              with tab3:
                  text29 = "🔹 Overall, transaction count on PhonePe has grown significantly from 2018 to 2023."
                  text30 = "🔹 Peer-to-peer payments seem to be the fastest growing payment type, with a sharp increase in transaction count between 2020 and 2021."
                  text31 = "🔹 Merchant payments also show steady growth throughout the years."
                  text32 = "🔹 Recharge & bill payments and Other transactions appear to have a slower and steadier growth rate over the years.Financial Services transactions seem to be the least used payment type on PhonePe"
                  def generate_text29():
                     for word in text29.split():
                        yield word + " "
                        time.sleep(0.03)
                  def generate_text30():
                     for word in text30.split():
                        yield word + " "
                        time.sleep(0.03)
                  def generate_text31():
                     for word in text31.split():
                        yield word + " "
                        time.sleep(0.03)
                  def generate_text32():
                     for word in text32.split():
                        yield word + " "
                        time.sleep(0.03)
                  st.write_stream(generate_text29)
                  st.write_stream(generate_text30)
                  st.write_stream(generate_text31)
                  st.write_stream(generate_text32)


            
              
        elif option=='District Wise':
            questions = ["The Top10 Districts Basedon Each Year",
                         "Highest Transaction Districts In Each State",
                         "QuarterWise Transaction on Each Year"]         
            selected_query = st.selectbox("Select a Query", questions,index= None)

            if selected_query==questions[0]:
              selected_Year= st.selectbox('Choose a Year',(map_transaction_data['Year'].unique()),index=None,placeholder="Select The Year...",)
              st.write('You selected:', selected_Year)
              if selected_Year:
                  tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
                  with tab1:
                        def top_10_districts_year(df,Year):
                           filter_df=df.loc[(map_transaction_data['Year']==Year)]
                           top_10=filter_df.groupby('District')['Trans_Count'].sum().reset_index().nlargest(10,'Trans_Count')
                           fig= px.pie(top_10, values='Trans_Count', names='District', title=f'All over India Top 10 districts on {Year} based on Transaction',hole=0.4,
                                       color_discrete_sequence=px.colors.sequential.Emrld_r)
                           fig.update_traces(textinfo='percent', textfont=dict(size=10))
                           

                           st.plotly_chart(fig,use_container_width=True)
                           
                        top_10_districts_year(map_transaction_data,selected_Year)
                        with st.expander('See Explanation'):
                           st.write("In every year Bangalore, Pune, Hyderabad have the highest transactions.These cities have large populations, which translates to a bigger potential user base for PhonePe")
                           st.write("These cities are major hubs for the IT industry and attract a young, tech-savvy population comfortable with adopting new technologies.People in these cities might have higher disposable income, leading to more online transactions")

                  
                  with tab2:
                        def top_10_districts_year(df,Year):
                              filter_df=df.loc[(map_transaction_data['Year']==Year)]
                              top_10=filter_df.groupby('District')['Trans_Count'].sum().reset_index().nlargest(10,'Trans_Count').reset_index(drop=True)
                              st.dataframe(top_10)
                        top_10_districts_year(map_transaction_data,selected_Year)
              else:
                 st.warning('Please Select The Above Options')


            elif selected_query==questions[2]:
               selected_Year= st.selectbox('Choose a Year',(map_transaction_data['Year'].unique()),index=None,placeholder="Select The Year...",)
               st.write('You selected:', selected_Year)

               selected_state= st.selectbox('Choose a State',(map_transaction_data['State'].unique()),index=None,placeholder="Select The State...",)
               st.write('You selected:', selected_state)
               if selected_Year and selected_state:
                     tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
                     with tab1:
                        def transaction_count_byQuarters(df,year,state):
                           filter_df=df.loc[(df['State']==state)&(df['Year']==year)].reset_index(drop=True)
                           quarter_wise=filter_df.groupby('Quartar')['Trans_Count'].sum().reset_index()
                           fig = px.bar(quarter_wise, 
                                       x='Quartar', 
                                       y='Trans_Count',
                                       title=f'Transaction Count for 4 Quarters & year on {year} of {state}',
                                       labels={'Quarter':'Quarters','Trans_Count': 'Transaction Count'},
                                       color='Quartar',
                                       color_continuous_scale ='viridis',
                                       text_auto=True)
         
            
                           fig.update_xaxes(title_text='Quarter',tickvals=[1,2,3,4],ticktext=['Q1(Jan,Feb,Mar)','Q2(Apr,May,Jun)','Q3(Jul,Aug,Sep)','Q4(Oct,Nov,Dec)'])
                           st.plotly_chart(fig,use_container_width=True)

                        transaction_count_byQuarters(map_transaction_data,selected_Year,selected_state)
                        if selected_state=='Tamil Nadu':
                           with st.expander('See Explanation'):
                              st.write('The fourth quarter in Tamil Nadu (October to December) coincides with the festive season, including **Diwali** and **Christmas**. People tend to spend more during this time on things like gifts, travel, and holiday shopping. This increased spending could lead to more digital transactions with PhonePe')

                        if selected_state=='Andaman And Nicobar Islands':
                           with st.expander('See Explanation'):
                            st.write("Tourism is a major industry in the Andaman and Nicobar Islands. The peak tourist season coincides with the fourth quarter (October to December), which could lead to a rise in transactions as tourists use PhonePe for various purposes:\n- Booking travel and accommodation\n- Paying for local services like restaurants, tours, and activities\n- Sending money back home")


                        if selected_state=='Kerala':
                           with st.expander('See Explanation'):
                            st.write("Kerala-Onam, the biggest festival in Kerala, falls in the latter half of Q3 (August/September). This festive season is a time for increased spending on New clothes and jewelry, Gifts for family and friends, Travel to visit relatives")
                        
                  
                     with tab2:
                        def transaction_count_byQuarters_data(df,year,state):
                           filter_df=df.loc[(df['State']==state)&(df['Year']==year)].reset_index(drop=True)
                           quarter_wise=filter_df.groupby('Quartar')['Trans_Count'].sum().reset_index()
                           st.dataframe(quarter_wise)
                        transaction_count_byQuarters_data(map_transaction_data,selected_Year,selected_state)
               else:
                  st.warning('Please Select The Above Options')


            elif selected_query==questions[1]:
               selected_state= st.selectbox('Choose a State',(map_transaction_data['State'].unique()),index=None,placeholder="Select The State...",)
               st.write('You selected:', selected_state)
               if selected_state:
                     tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
                     with tab1:
                        def top_5_districts_eachState(df,state):
                           filter_df=df.loc[(map_transaction_data['State']==state)]
                           top_5=filter_df.groupby('District')['Trans_Count'].sum().reset_index().nlargest(5,'Trans_Count')
                           fig= px.pie(top_5, values='Trans_Count', names='District', title=f'Top 5 districts on {state} based on Transaction',hole=0.4,
                                       color_discrete_sequence=px.colors.sequential.haline)
                           fig.update_traces(textinfo='percent', textfont=dict(size=10))
                           
                           st.plotly_chart(fig,use_container_width=True)

                        top_5_districts_eachState(map_transaction_data,selected_state)
                     with tab2:
                        def top_5_districts_eachState_data(df,state):
                           filter_df=df.loc[(map_transaction_data['State']==state)]
                           top_5=filter_df.groupby('District')['Trans_Count'].sum().reset_index().nlargest(5,'Trans_Count')
                           st.dataframe(top_5)

                        top_5_districts_eachState_data(map_transaction_data,selected_state)
               else:
                  st.warning('Please Select The Above Options')



       
  if Analyse_method=='Insurance':
        with st.container():
           left_column,right_column=st.columns(2)
           with left_column:
               image_path ='https://i.postimg.cc/66zV4Mys/Phone-Pe-Copy.jpg'
               st.image(image_path, use_column_width=True)
        option=st.radio('How would you like to Analyse?',['State Wise','District Wise'],index=None,horizontal=True)  
        st.write('You selected:', option)

        if option=='State Wise':
            questions = ["The Top10 States Highest Insurance Policy With PhonePe ",
                         "The Least 10 States Lowest Insurance Policy With PhonePe ",
                         "Growth Of Insurance In Each State"]         
            selected_query = st.selectbox("Select a Query", questions,index= None)

            if selected_query==questions[0]:
              tab1, tab2,tab3 = st.tabs(["📈 Chart", "🗃 Data","📄 Insight Points"])
              with tab1:
               filter_df=agg_insurance_data.groupby('State')['Insurance_count'].sum().sort_values(ascending=False).reset_index().nlargest(10,'Insurance_count')
               fig = px.bar(filter_df, 
                              x='State', 
                              y='Insurance_count',
                              title='The Top 10 States has Highest Insuarance Policy with Phonepe',
                              labels={'Insurance_count': 'Insurance_counts', 'State': 'States'},
                              color='State',
                              color_discrete_sequence=px.colors.qualitative.Antique_r,
                              template='plotly_white')
               fig.update_traces(texttemplate='%{y}', textposition='outside')
               st.plotly_chart(fig,use_container_width=True)
              with tab2:
                 st.dataframe(filter_df)
              with tab3:
               text41 = "🔹 Kerala People in Kerala are well-educated and know the importance of insurance. They might find it easy to buy insurance on PhonePe because they're good with technology. Plus, the government's health insurance programs could also encourage them to get insurance online."

               text42 = "🔹 Andhra Pradesh The government in Andhra Pradesh is trying hard to make sure everyone has access to banking and financial services. This effort, along with government promotions and specific insurance plans for people's needs, could be why many are buying insurance on PhonePe."

               text43 = "🔹 Maharashtra, Karnataka, and Tamil Nadu: These states have big cities and lots of people working in tech. Young people who are used to shopping online might choose to get insurance on PhonePe. Also, these states might have more people with insurance because of their growing economy and awareness campaigns."

               text44 = "🔹 Uttar Pradesh Even though many people in Uttar Pradesh might not be well-educated, there are just so many people there. PhonePe might be doing special ads or offering insurance deals (like with phone top-ups) to get more people interested in buying insurance."



               def generate_text41():
                  for word in text41.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text42():
                  for word in text42.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text43():
                  for word in text43.split():
                     yield word + " "
                     time.sleep(0.03)
               def generate_text44():
                  for word in text44.split():
                     yield word + " "
                     time.sleep(0.03)
               st.write_stream(generate_text41)
               st.write_stream(generate_text42)
               st.write_stream(generate_text43)
               st.write_stream(generate_text44)

            elif selected_query==questions[1]:
               tab1, tab2,tab3 = st.tabs(["📈 Chart", "🗃 Data","📄 Insight Points"])
               with tab1:
                  filter_df=agg_insurance_data.groupby('State')['Insurance_count'].sum().reset_index().nsmallest(10,'Insurance_count')
                  filter_df=filter_df.sort_values(by='Insurance_count',ascending=False)
                  fig = px.bar(filter_df, 
                              x='State', 
                              y='Insurance_count',
                              title='The Least 10 States has Lowest Insuarance Policy with Phonepe',
                              labels={'Insurance_count': 'Insurance_counts', 'State': 'States'},
                              color='State',
                              color_discrete_sequence=px.colors.qualitative.Antique_r,
                              template='plotly_white')
                  fig.update_traces(texttemplate='%{y}', textposition='outside')
                  st.plotly_chart(fig,use_container_width=True)
               with tab2:
                  st.dataframe(filter_df)
               with tab3:
                  text45 = "🔹 These districts generally have smaller populations compared to major cities. A smaller population base translates to a lower potential customer pool for PhonePe insurance products."

                  text46 = "🔹 Many of these districts are predominantly rural, with lower internet and smartphone penetration compared to urban areas. This can limit access to and awareness of online insurance with PhonePe."

                  def generate_text45():
                     for word in text45.split():
                        yield word + " "
                        time.sleep(0.03)
                  def generate_text46():
                     for word in text46.split():
                        yield word + " "
                        time.sleep(0.03)
                  
                  st.write_stream(generate_text45)
                  st.write_stream(generate_text46)
            

            elif selected_query==questions[2]:
               selected_state= st.selectbox('Choose a State',(agg_insurance_data['State'].unique()),index=None,placeholder="Select The State...",)
               st.write('You selected:', selected_state)
               if selected_state:
                  def find_insurance_growth(df,state):
                     filter_df=df.loc[(df['State']==state)]
                     fig = px.line(filter_df, x='Quartar', y='Insurance_count', color='Year', facet_col='Year',
                                    title=f'Growth of Insurance Count on Each Quarter in {state}',
                                    labels={'x': 'Quartar', 'y': 'Insurance_count'},
                                    template='seaborn')

                     fig.update_xaxes(title_text='Quarter', tickvals=[1, 2, 3, 4],
                                          ticktext=['1', '2', '3', '4'])

                     fig.update_traces(line=dict(width=2.5))

                     st.plotly_chart(fig,use_container_width=True)
                  find_insurance_growth(agg_insurance_data,selected_state)
               else:
                  st.warning('Please The Select The Above option')
              

        elif option=='District Wise':
            questions = ["The Top10 Districts Highest Insurance Policy With PhonePe",
                         "The Least Districts Lowest Insurance Policy With Phonepe",
                         "Highest Insurance Count Districts In Each State",
                         "Lowest Insurance Count Districts In Each State",
                         "High Paying Districts In Each State",
                         "Low Paying Districts In Each State"]         
            selected_query = st.selectbox("Select a Query", questions,index= None)

            if selected_query==questions[0]:
               tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
               with tab1:
                  filter_df=map_insurance_data.groupby('District')['Insurance_count'].sum().sort_values().reset_index().nlargest(10,'Insurance_count').reset_index(drop=True)
                  fig = px.bar(filter_df, 
                              x='District', 
                              y='Insurance_count',
                              title=f'Top 10 Districts In India which Has highest Insurance Policy with Phonepe',
                              labels={'District': 'Districts', 'Insurance_count': 'Insurance_counts'},
                              color='District',
                              color_discrete_sequence=px.colors.qualitative.Pastel,text_auto=True)
                  fig.update_layout(
                     font=dict(
                        family="sans-serif,verdana",
                        size=12,
                        color="black"
                     )
                  )
                  st.plotly_chart(fig,use_container_width=True)
               with tab2:
                  st.dataframe(filter_df)
            elif selected_query==questions[1]:
               tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
               with tab1:
                  filter_df=map_insurance_data.groupby('District')['Insurance_count'].sum().reset_index().nsmallest(10,'Insurance_count')
                  filter_df=filter_df.sort_values(by='Insurance_count',ascending=False).reset_index(drop=True)
                  fig = px.bar(filter_df, 
                              x='District', 
                              y='Insurance_count',
                              title=f'10 Districts In India which Has Very Lowest Insurance Policy with Phonepe',
                              labels={'District': 'Districts', 'Insurance_count': 'Insurance_counts'},
                              color='District',
                              color_discrete_sequence=px.colors.qualitative.Light24_r,text_auto=True)
                  fig.update_layout(
                     font=dict(
                        family="sans-serif,verdana",
                        size=12,
                        color="black"
                     )
                  )
                  st.plotly_chart(fig,use_container_width=True)
                  with tab2:
                    st.dataframe(filter_df)

            elif selected_query==questions[2]:
                 selected_state= st.selectbox('Choose a State',(map_insurance_data['State'].unique()),index=None,placeholder="Select The State...",)
                 st.write('You selected:', selected_state)
                 if selected_state:
                     tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
                     with tab1:
                        def Districts_EachState_Insurance(df,state):
                              filter_df=df.loc[df['State']==state]
                              top_10=filter_df.groupby('District')['Insurance_count'].sum().reset_index().nlargest(10,'Insurance_count')
                              fig = px.bar(top_10, 
                                          x='District', 
                                          y='Insurance_count',
                                          title=f'Highest Insurance Count Districts in {state}',
                                          labels={'District': 'Districts', 'Insurance_count': 'Insurance_counts'},
                                          color='District',
                                          color_discrete_sequence=px.colors.qualitative.Pastel,text_auto=True)
                              fig.update_layout(
                                 font=dict(
                                       family="sans-serif,verdana",
                                       size=12,
                                       color="black"
                                 )
                              )
                              st.plotly_chart(fig,use_container_width=True)
                        Districts_EachState_Insurance(map_insurance_data,selected_state)
                              
                           
                     with tab2:
                           def Districts_EachState_Insurance_data(df,state):
                              filter_df=df.loc[df['State']==state]
                              top_10=filter_df.groupby('District')['Insurance_count'].sum().reset_index().nlargest(10,'Insurance_count').reset_index(drop=True)
                              st.dataframe(top_10)
                           Districts_EachState_Insurance_data(map_insurance_data,selected_state)
                 else:
                    st.warning('Please Select The Above Options')
                        
               
            elif selected_query==questions[3]:
                 selected_state= st.selectbox('Choose a State',(map_insurance_data['State'].unique()),index=None,placeholder="Select The State...",)
                 st.write('You selected:', selected_state)
                 if selected_state:
                     tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
                     with tab1:
                        def Districts_EachState_Insurance_low(df,state):
                              filter_df=df.loc[map_insurance_data['State']==state]
                              top_10=filter_df.groupby('District')['Insurance_count'].sum().reset_index().nsmallest(10,'Insurance_count')
                              top_10=top_10.sort_values(by='Insurance_count',ascending=False)
                              fig = px.bar(top_10, 
                                          x='District', 
                                          y='Insurance_count',
                                          title=f'The Districts Has Lowest Insurance Counts on {state}',
                                          labels={'District': 'Districts', 'Insurance_count': 'Insurance_counts'},
                                          color='District',
                                          color_discrete_sequence=px.colors.qualitative.Pastel,text_auto=True)
                              fig.update_layout(
                                 font=dict(
                                    family="sans-serif,verdana",
                                    size=12,
                                    color="black"
                                 )
                              )
                              st.plotly_chart(fig,use_container_width=True)
                        Districts_EachState_Insurance_low(map_insurance_data,selected_state)
                              
                           
                     with tab2:
                           def Districts_EachState_Insurance_low_data(df,state):
                              filter_df=df.loc[df['State']==state]
                              top_10=filter_df.groupby('District')['Insurance_count'].sum().reset_index().nsmallest(10,'Insurance_count')
                              top_10=top_10.sort_values(by='Insurance_count',ascending=False).reset_index()
                              st.dataframe(top_10)
                           Districts_EachState_Insurance_low_data(map_insurance_data,selected_state)
                 else:
                    st.warning('Please Select The Above Options')


            elif selected_query==questions[4]:
                 selected_state= st.selectbox('Choose a State',(map_insurance_data['State'].unique()),index=None,placeholder="Select The State...",)
                 st.write('You selected:', selected_state)
                 if selected_state:
                     tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
                     with tab1:
                        def high_pay_districts(df,state):
                              filter_df=df.loc[df['State']==state]
                              top_5=filter_df.groupby('District')['Amount'].sum().reset_index().nlargest(5,'Amount')
                              fig= px.pie(top_5, values='Amount', names='District', title=f'High Pay Districts in {state} ',
                                             color_discrete_sequence=px.colors.sequential.haline)

                              fig.update_traces(textinfo='percent', textfont=dict(size=10))
                              st.plotly_chart(fig,use_container_width=True)
                        high_pay_districts(map_insurance_data,selected_state)
                     with tab2:
                           def high_pay_districts_data(df,state):
                                 filter_df=df.loc[df['State']==state]
                                 top_5=filter_df.groupby('District')['Amount'].sum().reset_index().nlargest(5,'Amount').reset_index(drop=True)
                                 st.dataframe(top_5)
                           high_pay_districts_data(map_insurance_data,selected_state)
                 else:
                    st.warning('Please Select The Above Options')
                    
               

            elif selected_query==questions[5]:
                selected_state= st.selectbox('Choose a State',(map_insurance_data['State'].unique()),index=None,placeholder="Select The State...",)
                st.write('You selected:', selected_state)
                if selected_state:
                     tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
                     with tab1:
                        def low_pay_districts(df,state):
                              filter_df=df.loc[df['State']==state]
                              top_5=filter_df.groupby('District')['Amount'].sum().reset_index().nsmallest(5,'Amount')
                              top_5=top_5.sort_values(by='Amount',ascending=False)
                              fig= px.pie(top_5, values='Amount', names='District', title=f'Low pay Districts in {state}',
                                             color_discrete_sequence=px.colors.sequential.haline)

                              fig.update_traces(textinfo='percent', textfont=dict(size=10))
                              st.plotly_chart(fig,use_container_width=True)
                        low_pay_districts(map_insurance_data,selected_state)
                     with tab2:
                           def low_pay_districts_data(df,state):
                                 filter_df=df.loc[df['State']==state]
                                 top_5=filter_df.groupby('District')['Amount'].sum().reset_index().nsmallest(5,'Amount').reset_index(drop=True)
                                 top_5=top_5.sort_values(by='Amount',ascending=False).reset_index(drop=True)
                                 st.dataframe(top_5)
                           low_pay_districts_data(map_insurance_data,selected_state)
                else:
                    st.warning('Please Select The Above Options')

if selected=='GEO VISUALIZATION':
   method=st.radio('Select The Options',('User','Transaction','Insurance'))
   if method=='User':
       option=st.radio('Select The Map Method',['State Wise','District Wise'],index=None,horizontal=True) 
       if option=='State Wise':
         on = st.toggle('Year Wise')
         if not on:
            def total_user1():
               df=map_user_data.groupby('State').agg({'Registered_Users':['sum','mean']}).reset_index()
               df.columns=['State', 'Total_User_Count', 'Average_User_Count']
               formated_Total_user_count = [Convert.rupees(amount) for amount in df['Total_User_Count']]
               formated_Average_user_count =  [Convert.rupees(amount) for amount in df['Average_User_Count']]
               hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Users: %{customdata[0]}<br>"
                                    "Average Yearly Users: %{customdata[1]}<br>"
                              )

               customdata = list(zip(formated_Total_user_count, formated_Average_user_count))

               fig = px.choropleth_mapbox(
                  df,
                  geojson= india_geojson(),
                  locations='State',
                  mapbox_style="carto-positron",
                  zoom=3.5,
                  center={"lat": 21.7679, "lon": 78.8718}, 
                  opacity=1,
                  featureidkey='properties.ST_NM', 
                  color='Total_User_Count', 
                  color_continuous_scale= px.colors.sequential.dense_r
                  )
               fig.update_geos(fitbounds="locations", visible=False)
               fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
               fig.update_layout(geo_bgcolor="#210D38")
               fig.update_traces(hovertemplate=hover_template, customdata=customdata)
               fig.update_layout(height=600)
               fig.update_coloraxes(colorbar_title_text='Total User Count')
               st.subheader("Showing Total User Count: Sum of All Years")
               st.plotly_chart(fig,use_container_width = True)
            total_user1()
         if on:
            selected_year= st.slider('Select The Year', 2018,2023)
            def total_user2(year):
               df=map_user_data.loc[map_user_data['Year']==year].groupby('State').agg({'Registered_Users':['sum','mean']}).reset_index()
               df.columns=['State', 'Total_User_Count', 'Average_User_Count']   
               formated_Total_user_count = [Convert.rupees(amount) for amount in df['Total_User_Count']]
               formated_Average_user_count =  [Convert.rupees(amount) for amount in df['Average_User_Count']]
               hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Users: %{customdata[0]}<br>"
                                    "Average Yearly Users: %{customdata[1]}<br>"
                              )

               customdata = list(zip(formated_Total_user_count, formated_Average_user_count))

               fig = px.choropleth_mapbox(
                  df,
                  geojson= india_geojson(),
                  locations='State',
                  mapbox_style="carto-positron",
                  zoom=3.5,
                  center={"lat": 21.7679, "lon": 78.8718}, 
                  opacity=1,
                  featureidkey='properties.ST_NM', 
                  color='Total_User_Count', 
                  color_continuous_scale= px.colors.sequential.dense_r
                  )
               fig.update_geos(fitbounds="locations", visible=False)
               fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
               fig.update_layout(geo_bgcolor="#210D38")
               fig.update_traces(hovertemplate=hover_template, customdata=customdata)
               fig.update_layout(height=600)
               fig.update_coloraxes(colorbar_title_text='Total User Count')
               st.subheader(f"Showing Total User Count in {year}")
               st.plotly_chart(fig,use_container_width = True)
               
            total_user2(selected_year)

       if option=='District Wise':
         selected_state= st.selectbox('Choose a State',(map_user_data['State'].unique()),index=None,placeholder="Select The State...",)
         if selected_state is not None:
            selected_coordinate=state_coordinates[selected_state]
            selected_zoom=zoom[selected_state]
            selected_link=state_geojson_links[selected_state]

            on = st.toggle('Year Wise')
            if not on:
               def district_wise_usercount1(state,geojson_link,coordinate,zoom_level):
                  df = map_user_data.loc[map_user_data['State'] == state].groupby("District", as_index = False).agg({"Registered_Users":["sum","mean"]})
                  df.columns=['District', 'Total_User_Count', 'Average_User_Count']   
                  formated_Total_user_count = [Convert.rupees(amount) for amount in df['Total_User_Count']]
                  formated_Average_user_count = [Convert.rupees(amount) for amount in df['Average_User_Count']]

                  hover_template = (
                        "<b>%{location}</b><br>"
                        "Total Users: %{customdata[0]}<br>"
                        "Average Yearly Users: %{customdata[1]}<br>")

                  customdata = list(zip(formated_Total_user_count, formated_Average_user_count))
                  fig = px.choropleth_mapbox(
                     df,
                     geojson=geojson_link,
                     locations='District',
                     mapbox_style="carto-positron",
                     zoom=zoom_level,
                     center=coordinate, 
                     featureidkey='properties.dtname', 
                     color='Total_User_Count', 
                     color_continuous_scale= px.colors.sequential.Viridis)
                  fig.update_geos(fitbounds="locations", visible=False)
                  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                  fig.update_layout(geo_bgcolor="#210D38")
                  fig.update_coloraxes(colorbar_title_text='Total User Count')
                  fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                  st.subheader(f"Showing Total UserCount of {selected_state}")
                  st.plotly_chart(fig,use_container_width = True)  
               district_wise_usercount1(selected_state,selected_link,selected_coordinate,selected_zoom)
      
            if on:
               selected_year= st.slider('Select The Year', 2018,2023)
               def district_wise_usercount2(state,year,geojson_link,coordinate,zoom_level):
                  df = map_user_data.loc[(map_user_data['State'] == state)& (map_user_data['Year']==year)].groupby("District", as_index = False).agg({"Registered_Users":["sum","mean"]})
                  df.columns=['District', 'Total_User_Count', 'Average_User_Count'] 
                  formated_Total_user_count = [Convert.rupees(amount) for amount in df['Total_User_Count']]
                  formated_Average_user_count = [Convert.rupees(amount) for amount in df['Average_User_Count']]
                  hover_template = (
                        "<b>%{location}</b><br>"
                        "Total Users: %{customdata[0]}<br>"
                        "Average Yearly Users: %{customdata[1]}<br>")

                  customdata = list(zip(formated_Total_user_count, formated_Average_user_count))
                  fig = px.choropleth_mapbox(
                     df,
                     geojson=geojson_link,
                     locations='District',
                     mapbox_style="carto-positron",
                     zoom=zoom_level,
                     center=coordinate, 
                     featureidkey='properties.dtname', 
                     color='Total_User_Count', 
                     color_continuous_scale= px.colors.sequential.Viridis)
                  fig.update_geos(fitbounds="locations", visible=False)
                  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                  fig.update_layout(geo_bgcolor="#210D38")
                  fig.update_coloraxes(colorbar_title_text='Total User Count')
                  fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                  st.subheader(f"Showing Total UserCount of {selected_state} in {year}")
                  st.plotly_chart(fig,use_container_width = True)  
               district_wise_usercount2(selected_state,selected_year,selected_link,selected_coordinate,selected_zoom)
              


   if method=='Transaction':
      option=st.radio('Select The Map Method',['State Wise','District Wise'],index=None,horizontal=True) 
      if option=='State Wise':
         on = st.toggle('Year Wise')
         if not on:
            def total_transaction1():
               df = agg_transaction_data.groupby(["State"]).agg({"Amount":["sum","mean"],"Trans_count":["sum","mean"]}).reset_index()
               df.columns = ['State', 'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
               formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
               formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
               formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
               formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
               hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Transaction Value: %{customdata[0]}<br>"
                                    "Average Transaction Value: %{customdata[1]}<br>"
                                    "Total Transaction: %{customdata[2]}<br>"
                                    "Average Transaction: %{customdata[3]}"
                              )
                                                
               customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))

               fig = px.choropleth_mapbox(
                  df,
                  geojson= india_geojson(),
                  locations='State',
                  mapbox_style="carto-positron",
                  zoom=3.5,
                  center={"lat": 21.7679, "lon": 78.8718}, 
                  opacity=1,
                  featureidkey='properties.ST_NM', 
                  color='Total_Transaction_Amount', 
                  color_continuous_scale=px.colors.sequential.Viridis,
                  )
               fig.update_geos(fitbounds="locations", visible=False)
               fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
               fig.update_layout(geo_bgcolor="#1f77b4")
               fig.update_traces(hovertemplate=hover_template, customdata=customdata)
               fig.update_coloraxes(colorbar_title_text='Total Transaction Value')
               fig.update_layout(height=600)
               st.subheader("Total Transaction Value: Sum of All Years")
               st.plotly_chart(fig,use_container_width = True)
            total_transaction1()
         if on:
            selected_year= st.slider('Select The Year', 2018,2023)
            def total_transaction2(year):
               df = agg_transaction_data.loc[agg_transaction_data['Year']==year].groupby(["State"]).agg({"Amount":["sum","mean"],"Trans_count":["sum","mean"]}).reset_index()
               df.columns = ['State', 'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
               formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
               formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
               formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
               formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
               hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Transaction Value: %{customdata[0]}<br>"
                                    "Average Transaction Value: %{customdata[1]}<br>"
                                    "Total Transaction: %{customdata[2]}<br>"
                                    "Average Transaction: %{customdata[3]}"
                              )
                                                
               customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))

               fig = px.choropleth_mapbox(
                  df,
                  geojson= india_geojson(),
                  locations='State',
                  mapbox_style="carto-positron",
                  zoom=3.5,
                  center={"lat": 21.7679, "lon": 78.8718}, 
                  opacity=1,
                  featureidkey='properties.ST_NM', 
                  color='Total_Transaction_Amount', 
                  color_continuous_scale=px.colors.sequential.Viridis,
                  )
               fig.update_geos(fitbounds="locations", visible=False)
               fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
               fig.update_layout(geo_bgcolor="#1f77b4")
               fig.update_traces(hovertemplate=hover_template, customdata=customdata)
               fig.update_coloraxes(colorbar_title_text='Total Transaction Value')
               fig.update_layout(height=600)
               st.subheader(f"Total Transaction Value on {year}")
               st.plotly_chart(fig,use_container_width = True)
            total_transaction2(selected_year)


      if option=='District Wise':

         selected_state= st.selectbox('Choose a State',(map_transaction_data['State'].unique()),index=None,placeholder="Select The State...",)
         if selected_state is not None:
            selected_coordinate=state_coordinates[selected_state]
            selected_zoom=zoom[selected_state]
            selected_link=state_geojson_links[selected_state]

            on = st.toggle('Year Wise')
            if not on:
               def statewise_map1(state,geojson_link,coordinate,zoom_level):
                  df = map_transaction_data.loc[map_transaction_data['State'] == state].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                  df.columns = ["District",'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                  formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                  formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                  formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                  formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                  hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Transaction Value: %{customdata[0]}<br>"
                                    "Average Transaction Value: %{customdata[1]}<br>"
                                    "Total Transaction: %{customdata[2]}<br>"
                                    "Average Transaction: %{customdata[3]}"
                                 )

                  customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))
                  fig = px.choropleth_mapbox(
                     df,
                     geojson=geojson_link,
                     locations='District',
                     mapbox_style="carto-positron",
                     zoom=zoom_level,
                     center=coordinate, 
                     featureidkey='properties.dtname', 
                     color='Total_Transaction_Amount', 
                     color_continuous_scale= px.colors.sequential.Viridis)
                  fig.update_geos(fitbounds="locations", visible=False)
                  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                  fig.update_layout(geo_bgcolor="#210D38")
                  fig.update_coloraxes(colorbar_title_text='Total Transaction Value')
                  fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                  st.subheader(f"Showing Total Transaction Value of {selected_state}")
                  st.plotly_chart(fig,use_container_width = True)  
               statewise_map1(selected_state,selected_link,selected_coordinate,selected_zoom)
      
            if on:
               selected_year= st.slider('Select The Year', 2018,2023)
               def statewise_map2(state,year,geojson_link,coordinate,zoom_level):
                  df = map_transaction_data.loc[(map_transaction_data['State'] == state)& (map_transaction_data['Year']==year)].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Trans_Count":["sum","mean"]})
                  df.columns = ["District",'Total_Transaction_Amount', 'Average_Transaction_Amount', 'Total_Transaction_Count', 'Average_Transaction_Count']
                  formated_Total_Transaction_Amount = [Convert.rupees(amount) for amount in df['Total_Transaction_Amount']]
                  formated_Average_Transaction_Amount = [Convert.rupees(amount) for amount in df['Average_Transaction_Amount']]
                  formated_Total_Transaction_Count =  [Convert.rupees(amount) for amount in df['Total_Transaction_Count']]
                  formated_Average_Transaction_Count =  [Convert.rupees(amount) for amount in df['Average_Transaction_Count']]
                  hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Transaction Value: %{customdata[0]}<br>"
                                    "Average Transaction Value: %{customdata[1]}<br>"
                                    "Total Transaction: %{customdata[2]}<br>"
                                    "Average Transaction: %{customdata[3]}"
                                 )

                  customdata = list(zip(formated_Total_Transaction_Amount, formated_Average_Transaction_Amount, formated_Total_Transaction_Count, formated_Average_Transaction_Count))
                  fig = px.choropleth_mapbox(
                     df,
                     geojson=geojson_link,
                     locations='District',
                     mapbox_style="carto-positron",
                     zoom=zoom_level,
                     center=coordinate, 
                     featureidkey='properties.dtname', 
                     color='Total_Transaction_Amount', 
                     color_continuous_scale= px.colors.sequential.Viridis)
                  fig.update_geos(fitbounds="locations", visible=False)
                  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                  fig.update_layout(geo_bgcolor="#210D38")
                  fig.update_coloraxes(colorbar_title_text='Total Transaction Value')
                  fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                  st.subheader(f"Showing Transaction Value of {selected_state} in {selected_year}")
                  st.plotly_chart(fig,use_container_width = True)  
               statewise_map2(selected_state,selected_year,selected_link,selected_coordinate,selected_zoom)
         



   if method=='Insurance':
      option=st.radio('Select The Map Method',['State Wise','District Wise'],index=None,horizontal=True) 
      if option=='State Wise':
         on = st.toggle('Year Wise')
         if not on:
            def insurance_statewise1():
                  df = agg_insurance_data.groupby(["State"]).agg({"Amount":["sum","mean"],"Insurance_count":["sum","mean"]}).reset_index()
                  df.columns = ['State', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                  formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                  formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                  formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                  formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                  hover_template = (
                                       "<b>%{location}</b><br>"
                                       "Total Insurance Value: %{customdata[0]}<br>"
                                       "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                       "Total Insurance Count: %{customdata[2]}<br>"
                                       "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                 )
                  
                  customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))

                                                

                  fig = px.choropleth_mapbox(
                     df,
                     geojson= india_geojson(),
                     locations='State',
                     mapbox_style="carto-positron",
                     zoom=3.5,
                     center={"lat": 21.7679, "lon": 78.8718}, 
                     opacity=1,
                     featureidkey='properties.ST_NM', 
                     color='Total_Ins_Amount', 
                     color_continuous_scale=px.colors.sequential.Viridis,
                     )
                  fig.update_geos(fitbounds="locations", visible=False)
                  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                  fig.update_layout(geo_bgcolor="#1f77b4")
                  fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                  fig.update_coloraxes(colorbar_title_text='Total Insurance Amount')
                  fig.update_layout(height=600)
                  st.subheader("Total Insurance Value: Sum of All Years")
                  st.plotly_chart(fig,use_container_width = True)
            insurance_statewise1()
      
         if on:
            selected_year= st.slider('Select The Year', 2020,2023)
            def insurance_statewise2(year):
                  df = agg_insurance_data.loc[agg_insurance_data['Year']==year].groupby(["State"]).agg({"Amount":["sum","mean"],"Insurance_count":["sum","mean"]}).reset_index()
                  df.columns = ['State', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                  formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                  formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                  formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                  formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                  hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Insurance Value: %{customdata[0]}<br>"
                                    "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                    "Total Insurance Count: %{customdata[2]}<br>"
                                    "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                 )

                  customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))

                                             

                  fig = px.choropleth_mapbox(
                     df,
                     geojson= india_geojson(),
                     locations='State',
                     mapbox_style="carto-positron",
                     zoom=3.5,
                     center={"lat": 21.7679, "lon": 78.8718}, 
                     opacity=1,
                     featureidkey='properties.ST_NM', 
                     color='Total_Ins_Amount', 
                     color_continuous_scale=px.colors.sequential.Viridis,
                     )
                  fig.update_geos(fitbounds="locations", visible=False)
                  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                  fig.update_layout(geo_bgcolor="#1f77b4")
                  fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                  fig.update_coloraxes(colorbar_title_text='Total Insurance Amount')
                  fig.update_layout(height=600)
                  st.subheader(f"Total Insurance Value in {year}")
                  st.plotly_chart(fig,use_container_width = True)
            insurance_statewise2(selected_year)
      

      if option=='District Wise':

         selected_state= st.selectbox('Choose a State',(map_transaction_data['State'].unique()),index=None,placeholder="Select The State...",)
         if selected_state is not None:
            selected_coordinate=state_coordinates[selected_state]
            selected_zoom=zoom[selected_state]
            selected_link=state_geojson_links[selected_state]

            on = st.toggle('Year Wise')
            if not on:
               def insurance_statewise1(state,geojson_link,coordinate,zoom_level):
                  df = map_insurance_data.loc[map_insurance_data['State'] == state].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Insurance_count":["sum","mean"]})
                  df.columns = ['District', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                  formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                  formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                  formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                  formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                  hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Insurance Value: %{customdata[0]}<br>"
                                    "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                    "Total Insurance Count: %{customdata[2]}<br>"
                                    "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                 )

                  customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))

                  fig = px.choropleth_mapbox(
                     df,
                     geojson=geojson_link,
                     locations='District',
                     mapbox_style="carto-positron",
                     zoom=zoom_level,
                     center=coordinate, 
                     featureidkey='properties.dtname', 
                     color='Total_Ins_Count', 
                     color_continuous_scale= px.colors.sequential.Viridis)
                  fig.update_geos(fitbounds="locations", visible=False)
                  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                  fig.update_layout(geo_bgcolor="#210D38")
                  fig.update_coloraxes(colorbar_title_text='Total Insurance Count')
                  fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                  st.subheader(f"Showing Total Insurance Value of {selected_state}")
                  st.plotly_chart(fig,use_container_width = True)  
               insurance_statewise1(selected_state,selected_link,selected_coordinate,selected_zoom)
      
            if on:
               selected_year= st.slider('Select The Year', 2020,2023)
               def insurance_statewise2(state,year,geojson_link,coordinate,zoom_level):
                  df = map_insurance_data.loc[(map_insurance_data['State'] == state) & (map_insurance_data['Year']==year)].groupby("District", as_index = False).agg({"Amount":["sum","mean"],"Insurance_count":["sum","mean"]})
                  df.columns = ['District', 'Total_Ins_Amount', 'Average_Ins_Amount','Total_Ins_Count','Average_Ins_Count']
                  formated_Total_ins_amount = [Convert.rupees(amount) for amount in df['Total_Ins_Amount']]
                  formated_Average_ins_amount =  [Convert.rupees(amount) for amount in df['Average_Ins_Amount']]
                  formated_Total_Insurance_Count =  [Convert.rupees(amount) for amount in df['Total_Ins_Count']]
                  formated_Average_Insurance_Count =  [Convert.rupees(round(amount)) for amount in df['Average_Ins_Count']]
                  hover_template = (
                                    "<b>%{location}</b><br>"
                                    "Total Insurance Value: %{customdata[0]}<br>"
                                    "Average Yearly Insurance Value: %{customdata[1]}<br>"
                                    "Total Insurance Count: %{customdata[2]}<br>"
                                    "Average Yearly Insurance Count: %{customdata[3]}<br>"
                                 )

                  customdata = list(zip(formated_Total_ins_amount, formated_Average_ins_amount,formated_Total_Insurance_Count,formated_Average_Insurance_Count))

                  fig = px.choropleth_mapbox(
                     df,
                     geojson=geojson_link,
                     locations='District',
                     mapbox_style="carto-positron",
                     zoom=zoom_level,
                     center=coordinate, 
                     featureidkey='properties.dtname', 
                     color='Total_Ins_Count', 
                     color_continuous_scale= px.colors.sequential.Viridis)
                  fig.update_geos(fitbounds="locations", visible=False)
                  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                  fig.update_layout(geo_bgcolor="#210D38")
                  fig.update_coloraxes(colorbar_title_text='Total Insurance Count')
                  fig.update_traces(hovertemplate=hover_template, customdata=customdata)
                  st.subheader(f"Showing Total Insurance Value of {selected_state} in {year}")
                  st.plotly_chart(fig,use_container_width = True)  
               insurance_statewise2(selected_state,selected_year,selected_link,selected_coordinate,selected_zoom)
         
if selected=='REPORT':
   with st.container():
           left_column, right_column = st.columns([1, 2])
           with left_column:
               st.header(':violet[REPORT]')
               image_path ="https://i.postimg.cc/t4S8rRsk/Brown-Autumn-Photo-Collage.png"
               st.image(image_path, use_column_width=True)
           with right_column:
               first_half, second_half = right_column.columns(2)
               with first_half:
                  image_path ="https://i.postimg.cc/fbSVYn7g/Edit-Logo-Design-and-Branding.png"
                  st.image(image_path, use_column_width=True)
               with second_half:
                 st.header(':violet[You Can Download This Report Book Here ⬇️]')
                 st.write(' ')
                 st.write(' ')
                 st.write(' ')
                 st.write(' ')
                 st.write(' ')
                 st.write(' ')
                 url = "https://drive.google.com/uc?export=download&id=1Z0vVoqSG1n6X0Osz-tk720pfXETjy2e9"
                 response = requests.get(url)
                 pdf_bytes = response.content

                  
                 st.download_button(
                     label="Download The Report Book",
                     data=pdf_bytes,
                     file_name="Report Book.pdf",
                     mime="application/pdf"
                  )
   st.header(':violet[FAQ]')
   with st.expander("Who is the Founder of Phonepe"):
       st.write('**Sameer Nigam founded PhonePe in 2015 and serves as its Chief Executive Officer.**')
   with st.expander('What Is PhonePe'):
       st.write('**PhonePe is a mobile payment platform using which you can transfer money using UPI, recharge phone numbers, pay utility bills, etc. PhonePe works on the Unified Payment Interface (UPI) system and all you need is to feed in your bank account details and create a UPI ID**')
   with st.expander('How many countries use PhonePe?'):
      st.write('**PhonePe will offer the UPI services UAE, Singapore, Mauritius, Nepal and Bhutan. PhonePe, an Indian digital payments platform, primarily operates within India. Its designed to facilitate transactions within the country**')
   with st.expander('What Is a Digital Wallet?'):
      st.write('**A digital wallet (or electronic wallet) is a financial transaction application that runs on any connected device. It securely stores your payment information and passwords in the cloud. Digital wallets may be accessible from a computer; mobile wallets, which are a subset, are primarily used on mobile devices.**') 
   with st.expander('What Are The Other Services PhonePe Provide?'):
      st.write('**UPI Payments, Investment, Insurance, Recharges, DTH & More**')
   with st.expander('How can I Get The Data Used In This Project?'):
      url = 'https://github.com/PhonePe/pulse'
      st.markdown(f"**Check out this** [link]({url})")
   with st.expander('How Can I Use PhonePe Pulse'):
      st.write('**In the top analysis section, you can find charts and analysis points. In the geo visualization section, you can explore map visualization. Finally, in the report section, you can access the project report for download**')
   with st.expander('What is the highest transaction limit in PhonePe?'):
      st.write('**The PhonePe UPI transaction limit is Rs. 1 lakh (Rs 100,000) daily for all users. This limit applies to both P2P and P2M transactions. The PhonePe UPI transaction limit is set by the National Payments Corporation of India (NPCI).**')
   with st.expander('What is the mission of PhonePe?'):
      st.write('**PhonePe core mission is centered around revolutionizing digital payments and making financial services accessible to all, bridging the gap between traditional banking and modern technology.**')
