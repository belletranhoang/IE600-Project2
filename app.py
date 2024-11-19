import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration with Spotify-like theme
st.set_page_config(
    page_title="Spotify Most Streamed Songs Dashboard",
    page_icon="🎶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define Spotify-themed colors
spotify_palette = {
    'primary': '#1DB954',  
    'secondary': '#191414',  
    'accent': '#535353',  
    'highlight': '#ffffff' }
    
# Load dataset
@st.cache_data
def load_data():
    url = 'Spotify Most Streamed Songs.csv'
    return pd.read_csv(url)

data = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_artists = st.sidebar.multiselect(
    "Select Artist(s):",
    options=list(data['artist(s)_name'].unique()),
    default=None
)

selected_year_range = st.sidebar.slider(
    "Select Release Year Range:",
    min_value=int(data['released_year'].min()),
    max_value=int(data['released_year'].max()),
    value=(int(data['released_year'].min()), int(data['released_year'].max()))
)

# Filtered Data
filtered_data = data[
    (data['released_year'] >= selected_year_range[0]) &
    (data['released_year'] <= selected_year_range[1])
]

if selected_artists:
    filtered_data = filtered_data[filtered_data['artist(s)_name'].isin(selected_artists)]

# Main Content
st.title("Spotify Most Streamed Songs Dashboard")
st.write("Explore trends and insights from the most streamed songs on Spotify, "
         "including artist popularity, release trends, and song characteristics.")

# Data Preview
st.subheader("Dataset Overview")
st.dataframe(filtered_data.head(10))

# Visualization 1: Bar Chart - Top 10 Artists by Streams
st.subheader("Top 10 Artists by Total Streams")
top_artists = data.groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head(10)
# Spotify-styled bar chart
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x=top_artists.values,
    y=top_artists.index,
    palette=[spotify_palette['primary']] * len(top_artists),
    ax=ax
)
ax.set_title("Top 10 Artists by Total Streams", color=spotify_palette['highlight'])
ax.set_xlabel("Total Streams", color=spotify_palette['highlight'])
ax.set_ylabel("Artist", color=spotify_palette['highlight'])
ax.tick_params(colors=spotify_palette['highlight'])
st.pyplot(fig)

# Visualization 2: Line Chart - Song Released Over Time
st.subheader("Song Release Trends Over Time")
release_trends = filtered_data.groupby(['released_year', 'released_month'])['track_name'].count().reset_index(name='song_count')
release_trends['date'] = pd.to_datetime(release_trends['released_year'].astype(str) + '-' + release_trends['released_month'].astype(str))
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=release_trends, x='date', y='song_count', color=spotify_palette['primary'], ax=ax)
ax.set_title("Number of Songs Released Over Time", color=spotify_palette['highlight'])
ax.set_xlabel("Release Date", color=spotify_palette['highlight'])
ax.set_ylabel("Number of Songs", color=spotify_palette['highlight'])
ax.tick_params(colors=spotify_palette['highlight'])
st.pyplot(fig)

# Visualization 3: Scatter Plot - Danceability vs Energy
st.subheader("Danceability vs. Energy")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(
    data=filtered_data,
    x='danceability_%',
    y='energy_%',
    hue='artist(s)_name',
    palette='cool',
    legend=False,
    ax=ax
)
ax.set_title("Danceability vs Energy", color=spotify_palette['highlight'])
ax.set_xlabel("Danceability (%)", color=spotify_palette['highlight'])
ax.set_ylabel("Energy (%)", color=spotify_palette['highlight'])
ax.tick_params(colors=spotify_palette['highlight'])
st.pyplot(fig)

# Visualization 4: Pie Chart - Songs in Different Playlists
st.subheader("Platform Popularity")
platform_data = {"Spotify": 4955719, "Apple": 64625, "Deezer": 95913}

fig, ax = plt.subplots()
ax.pie(
    platform_data.values(),
    labels=None,
    autopct='%1.1f%%',
    startangle=0,
    colors=[spotify_palette['primary'], spotify_palette['accent'], spotify_palette['secondary']]
)
ax.axis('equal')
ax.legend(
    loc="upper right",
    title="Platforms",
    labels=[f"{key}: {value}" for key, value in platform_data.items()],
    fontsize=8
)
st.pyplot(fig)

# Visualization 5: Histogram - BPM Distribution
st.subheader("Distribution of BPM")
fig, ax = plt.subplots(figsize=(8, 6))
sns.histplot(filtered_data['bpm'], bins=20, kde=True, color=spotify_palette['primary'], ax=ax)
ax.set_title("Distribution of BPM (Beats Per Minute)", color=spotify_palette['highlight'])
ax.set_xlabel("BPM", color=spotify_palette['highlight'])
ax.set_ylabel("Frequency", color=spotify_palette['highlight'])
ax.tick_params(colors=spotify_palette['highlight'])
st.pyplot(fig)

# Conclusion
st.subheader("Insights & Summary")
st.write(
    "This dashboard reveals interesting insights about song characteristics, "
    "release trends, and artist popularity. Use the filters in the sidebar to explore more!"
)
