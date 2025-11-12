import pandas as pd
import streamlit as st
import numpy as np
import joblib
from pathlib import Path
from sklearn.neighbors import BallTree

# Configure the Streamlit page settings with a title, icon, and layout.
st.set_page_config(
    page_title='Ad Campaign Recommender',
    page_icon=':bulb:',
    layout='wide'
)

# Set the main title for the web application.
st.title('Ad Campaign Recommender')
@st.dialog("Welcome to the Ad Campaign Recommender Capstone Project!", width='large')

def show_context():
    """
    Display context about the app's purpose, functionality, and benefits.

    This function provides an overview of how the app works and why it is useful.
    It includes details on input data fields and predictions.
    """
    st.markdown(
        """
        This web application has been developed to help predict user demographics (age and gender) based on their mobile phone usage patterns. This information can then be used to create personalized ad campaigns tailored to specific customer segments, improving user experience and driving business outcomes.
        
        The app allows you to input details about mobile phone usage, location data, and app behavior to generate predictions. Here's how it works:
        
        1. **Input Data for Prediction**  
           - **Select the Phone Model**: Provides information about the device being used.
           - **Select Week of the Month**: Helps track patterns across different weeks.
           - **Select Day of the Week**: Identifies usage trends on specific days (e.g., weekends vs. weekdays).
           - **Select Time of the Day**: Captures peak usage hours (e.g., morning, afternoon, evening).
           - **Enter App Usage**: Measures how frequently and actively users engage with apps.
           - **Enter Location**: Tracks geographical data to understand usage patterns.
           - **Enter Latitude/Longitude**: Provides precise location information for geospatial analysis.
        
        2. **Predict Button**  
           Click this button to generate predictions about the user's demographics (Gender & Age) based on the input data.
        
        ---
        
        **Why Use This App?**
        
        - **Personalized Campaigns**: Helps businesses target users with ads that match their preferences.
        - **Improved User Experience**: Users see more relevant content, increasing engagement.
        - **Data-Driven Decisions**: Businesses can make informed decisions about marketing strategies based on predicted demographics.
        
        ---
        
        **How to Get the Best Out of This App?**
        
        1. Provide accurate and detailed data for better predictions.
        2. Experiment with different inputs to see how predictions change based on usage patterns.
        3. Use the insights to refine your ad campaigns or understand user behavior.
        
        ---
        
        This tool is part of a larger capstone project focused on leveraging predictive analytics in the telecom sector. By using this app, you're contributing to more effective and targeted marketing strategies!
        """
    )

# Button to display context information when clicked.
if st.button('**What is this about?**', type='tertiary'):
    show_context()

# Initialize a DataFrame with predefined columns for input data.
X_data = pd.DataFrame(columns=['phone_brand_category_Others', 'phone_brand_category_coolpad',
       'phone_brand_category_gionee', 'phone_brand_category_htc',
       'phone_brand_category_huawei', 'phone_brand_category_lenovo',
       'phone_brand_category_meizu', 'phone_brand_category_oppo',
       'phone_brand_category_samsung', 'phone_brand_category_vivo',
       'phone_brand_category_xiaomi', 'cluster_Cluster 0', 'cluster_Cluster 1',
       'cluster_Cluster 2', 'cluster_Cluster 3', 'cluster_Cluster 4',
       'cluster_Cluster 5', 'cluster_Cluster 6', 'cluster_Cluster 7',
       'cluster_Cluster 8', 'cluster_Cluster 9', 'weekday_Friday',
       'weekday_Monday', 'weekday_Saturday', 'weekday_Sunday',
       'weekday_Thursday', 'weekday_Tuesday', 'weekday_Wednesday',
       'week_of_month_Week 1', 'week_of_month_Week 2', 'week_of_month_Week 5',
       'Hour_Category_Afternoon', 'Hour_Category_Evening',
       'Hour_Category_Morning', 'Hour_Category_Night', 'app_usage_count'], index=[0])

# Initialize all columns of the DataFrame to zero.
X_data = X_data.apply(lambda x: pd.Series([0]*len(x)))

def get_col(text):
    """
    Find a column in `X_data` that contains the specified text.

    :param text: The substring to search for within column names.
    :return: Column name if found; otherwise, None.
    """
    try:
        return X_data.columns[X_data.columns.str.contains(text)][0]

    except IndexError:
        return None

# Function to find the nearest sector based on geographical coordinates using a BallTree.
def find_nearest_sector(lat, lon):
    """
    Find the nearest cluster sector for given latitude and longitude.

    :param lat: Latitude of the location.
    :param lon: Longitude of the location.
    :return: Cluster identifier for the closest sector.
    """

    # Build the BallTree using haversine distance metric to find nearest points on a sphere (Earth).
    tree = BallTree(np.radians(sector_data[['latitude', 'longitude']].values), metric='haversine')

    # Query the tree with input coordinates to find the nearest cluster index.
    dist, idx = tree.query(np.radians([[lat, lon]]), k=1)
    return sector_data.iloc[idx[0][0]]['cluster']

def load_model(file_path: str):
    """
    Load a machine learning model from a specified file path.

    :param file_path: Path to the serialized model file.
    :return: Loaded model object.
    :raises FileNotFoundError: If the model file is not found.
    """
    try:
        model = joblib.load(file_path)
        return model

    except FileNotFoundError:
        # Display error message in Streamlit if model file cannot be loaded.
        raise st.error('Model Not Found')

# Mapping dictionaries for predicted gender and age groups.
map_gender = {0: 'Female', 1: 'Male'}

map_age = {
    0: 'age_group_Less than 20',
    1: 'age_group_20 to 24',
    2: 'age_group_25 to 29',
    3: 'age_group_30 to 34',
    4: 'age_group_35 to 39',
    5: 'age_group_40 to 44',
    6: 'age_group_45 to 49',
    7: 'age_group_50 to 54',
    8: 'age_group_55 to 60',
    9: 'age_group_Above 60'
}

# Divider for separating sections in the Streamlit interface.
st.divider()

# Create columns for layout purposes.
col1, col2 = st.columns([1.5, 0.5])

with col1:
    # Header and subheader indicating where users should input data for predictions.
    st.header('Input Data for Prediction')
    st.write('')

    # Dropdown selection for choosing a phone model.
    phone_models = ['Xiaomi', 'Samsung', 'Vivo', 'Meizu', 'Oppo', 'Huawei', 'Lenovo', 'Gionee', 'Coolpad', 'HTC', 'Others']
    st.subheader('Select the Phone Model')
    phone = st.pills("Phone Model", phone_models, selection_mode="single", label_visibility='collapsed')

    # Retrieve and update the relevant column in X_data based on selected phone model.
    if phone:
        phone = phone.lower() if phone != 'Others' else phone

        # Get Phone column
        phone = get_col(phone)

        # Update Data
        X_data[phone] = 1

    else:
        # Default to 'Others' category if no specific model is selected.
        X_data['phone_brand_category_Others'] = 1


    col3, col4 = st.columns(2)

    st.write('')

    with col3:
        st.write('')
        # Dropdown selection for week of the month.
        st.subheader('Select Week of the month')

        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']

        week = st.selectbox(label='Select Week of the month', options=weeks, label_visibility='collapsed')

        # Get Week column
        week = get_col(week)

        if week:
            # Update Data
            X_data[week] = 1


    with col4:
        st.write('')
        # Dropdown selection for day of the week.
        st.subheader('Select Day of the week')

        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        day = st.selectbox(label='Select Day of the week', options=days, label_visibility='collapsed')

        # Get Day column
        day = get_col(day)

        # Update Data
        X_data[day] = 1


    col5, col6 = st.columns(2)

    # Time of day
    with col5:
        st.write('')

        # Dropdown selection for time of day.
        st.subheader('Select Time of the day')

        times = ['Morning', 'Afternoon', 'Evening', 'Night']

        time = st.selectbox(label='Select Time of the day', options=times, label_visibility='collapsed')

        # Get Time column
        time = get_col(time)

        # Update Data
        X_data[time] = 1

    # App Usage
    with col6:
        st.write('')

        # Slider input for app usage count.
        st.subheader('Enter the App usage')
        usage = st.slider('Enter the App usage', 0, 5000, label_visibility='collapsed')

        # Update Data
        X_data['app_usage_count'] = usage

    # Load location cluster data from a Parquet file.
    sector_data = pd.read_parquet('sector_data.parquet')

    st.write('')
    st.subheader('Enter Location')

    col7, col8 = st.columns(2)

    with col7:
        lat = st.number_input('Enter Latitude', min_value=-90.00, max_value=90.00, placeholder='Latitude')

    with col8:
        lon = st.number_input('Enter Longitude', min_value=-180.00, max_value=180.00, placeholder='Longitude')

    # Find the nearest sector based on entered coordinates.
    sector = find_nearest_sector(lat, lon)
    st.caption(f'You belong to {sector}')

    # Get Sector
    sector = get_col(sector)

    # Update Data
    X_data[sector] = 1

    # Display a map showing the location point using latitude and longitude.
    st.map(pd.DataFrame(data={'lat': lat, 'lon': lon}, index=[0]))


with col2:
    # Predictions
    st.header('Perform Prediction')
    st.write('')

    if st.button('Predict', type='primary', use_container_width=True):

        # Attempt to load age prediction model.
        age_model = load_model('models/age.joblib')
        
        # Attempt to load gender prediction model.
        gender_model = load_model('models/gender.joblib')

        gender = gender_model.predict(X_data)
        gender = list(map(lambda x: map_gender[x], gender))[0]

        # Predict age group and map it to a descriptive string.
        age = age_model.predict(X_data)
        age = list(map(lambda x: map_age[x], age))[0]
        # Extract the specific age range from the mapped value.
        age = age.split('_')[-1]

        with st.container(border=True):
            # Display predicted gender and age to the user.
            st.write(f'**Predicted Gender:** {gender}')
            st.write(f'**Predicted Age:** {age}')
