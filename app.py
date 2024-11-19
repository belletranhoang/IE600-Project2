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

# Setting custom theme colors
st.markdown(
    """
    <style>
        .stApp {
            background-color: #191414;
            color: white;
        }
        .css-18e3th9 {
            background-color: #1DB954; /* Spotify green */
            color: white;
        }
        .css-1d391kg {
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
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

# Visualization 4: Improved Pie Chart - Songs in Different Playlists
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

# Explode small slices for visibility
explode = [0, 0.1, 0.1]  # Explode Apple and Deezer for emphasis

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    platform_data.values(),
    labels=platform_data.keys(),
    autopct=lambda pct: f"{pct:.1f}%" if pct > 2 else "",  # Display percentage > 2%
    startangle=90,
    explode=explode,
    textprops=dict(color="black")
)

# Add leader lines for small slices
for text, wedge in zip(texts, wedges):
    theta = (wedge.theta2 + wedge.theta1) / 2  # Angle in degrees
    x = 1.1 * wedge.r * plt.cos(np.radians(theta))
    y = 1.1 * wedge.r * plt.sin(np.radians(theta))
    if wedge.theta2 - wedge.theta1 < 15:  # Adjust based on slice size
        ax.annotate(
            text.get_text(),
            xy=(x, y),
            xytext=(1.2 * x, 1.2 * y),
            arrowprops=dict(arrowstyle="->", lw=0.5),
            fontsize=10,
            ha="center"
        )
        text.set_visible(False)  # Hide default text

# Equal aspect ratio for a circular pie chart
ax.axis('equal')

# Add legend for clarity
ax.legend(
    loc="best",
    title="Platforms",
    labels=[f"{key}: {value}" for key, value in platform_data.items()],
    fontsize=9
)

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






















