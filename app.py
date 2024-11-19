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
st.bar_chart(top_artists)

# Visualization 2: Line Chart - Song Released Over Time
st.subheader("Song Release Trends Over Time")
release_trends = filtered_data.groupby(['released_year', 'released_month'])['track_name'].count().reset_index(name='song_count')
release_trends['date'] = pd.to_datetime(release_trends['released_year'].astype(str) + '-' + release_trends['released_month'].astype(str))
plt.figure(figsize=(10, 5))
sns.lineplot(data=release_trends, x='date', y='song_count')
plt.title("Number of Songs Released Over Time")
plt.xlabel("Release Date")
plt.ylabel("Number of Songs")
st.pyplot(plt)

# Visualization 3: Scatter Plot - Danceability vs Energy
st.subheader("Danceability vs. Energy")
plt.figure(figsize=(8, 6))
sns.scatterplot(data=filtered_data, x='danceability_%', y='energy_%', hue='artist(s)_name', legend=False)
plt.title("Danceability vs Energy")
plt.xlabel("Danceability (%)")
plt.ylabel("Energy (%)")
st.pyplot(plt)

# Visualization 4: Pie Chart - Songs in Different Playlists
st.subheader("Platform Popularity")

# Convert columns to numeric, setting errors='coerce' to handle any non-numeric values
filtered_data['in_spotify_playlists'] = pd.to_numeric(filtered_data['in_spotify_playlists'], errors='coerce')
filtered_data['in_apple_playlists'] = pd.to_numeric(filtered_data['in_apple_playlists'], errors='coerce')
filtered_data['in_deezer_playlists'] = pd.to_numeric(filtered_data['in_deezer_playlists'], errors='coerce')

# Calculate platform popularity
platform_data = {
    'Spotify': filtered_data['in_spotify_playlists'].sum(),
    'Apple': filtered_data['in_apple_playlists'].sum(),
    'Deezer': filtered_data['in_deezer_playlists'].sum()
}

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    platform_data.values(),
    labels=None,
    autopct=lambda pct: f"{pct:.1f}%" if pct > 2 else "",  # Show percentages only above 2%
    startangle=90,
    textprops=dict(color="w")  # White text color for visibility
)

# Adjust text properties
for text in texts:
    text.set_fontsize(10)
    text.set_color("black")  # Change labels outside the pie chart to black

for autotext in autotexts:
    autotext.set_fontsize(8)

# Add a legend
ax.legend(
    loc="upper right",
    title="Platforms",
    labels=[f"{key}: {value}" for key, value in platform_data.items()],
    fontsize=9
)

ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
st.pyplot(fig)

# Visualization 4: Pie Chart - Songs in Different Playlists
st.subheader("Platform Popularity")

# Convert columns to numeric, setting errors='coerce' to handle any non-numeric values
filtered_data['in_spotify_playlists'] = pd.to_numeric(filtered_data['in_spotify_playlists'], errors='coerce')
filtered_data['in_apple_playlists'] = pd.to_numeric(filtered_data['in_apple_playlists'], errors='coerce')
filtered_data['in_deezer_playlists'] = pd.to_numeric(filtered_data['in_deezer_playlists'], errors='coerce')

# Calculate platform popularity
platform_data = {
    'Spotify': filtered_data['in_spotify_playlists'].sum(),
    'Apple': filtered_data['in_apple_playlists'].sum(),
    'Deezer': filtered_data['in_deezer_playlists'].sum()
}

fig, ax = plt.subplots()
ax.pie(platform_data.values(), labels=None, autopct='%1.1f%%', startangle=0)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

# Add a legend
ax.legend(
    loc="upper right",
    title="Platforms",
    labels=[f"{key}: {value}" for key, value in platform_data.items()],
    fontsize=9)
st.pyplot(fig)

# Visualization 5: Histogram - BPM Distribution
st.subheader("Distribution of BPM")
plt.figure(figsize=(8, 6))
sns.histplot(filtered_data['bpm'], bins=20, kde=True, color='blue')
plt.title("Distribution of BPM (Beats Per Minute)")
plt.xlabel("BPM")
plt.ylabel("Frequency")
st.pyplot(plt)

# Conclusion
st.subheader("Insights & Summary")
st.write(
    "This dashboard reveals interesting insights about song characteristics, "
    "release trends, and artist popularity. Use the filters in the sidebar to explore more!"
)
