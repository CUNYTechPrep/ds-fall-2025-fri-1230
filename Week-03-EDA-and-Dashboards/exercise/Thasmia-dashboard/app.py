from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="MovieLens Dashboard (Week 3)", layout="wide")


@st.cache_data(ttl=3600)
def load_movie_ratings() -> pd.DataFrame:
    f"""Load the movie ratings dataset from the Week 3 data folder.

    The app is located at: Week-03-EDA-and-Dashboards/exercise/name_dashboard/app.py
    The data lives at:      Week-03-EDA-and-Dashboards/data/movie_ratings.csv
    """
    data_path = Path(__file__).resolve().parents[2] / "data" / "movie_ratings.csv"
    df = pd.read_csv(data_path)
    return df


def render_header() -> None:
    st.title("MovieLens Dashboard")
    st.caption("Week 3 — EDA and Dashboards")


def render_sidebar(df: Optional[pd.DataFrame]) -> dict:
    with st.sidebar:
        st.header("Controls")
        show_raw = st.toggle("Show raw data preview", value=False)

        controls = {"show_raw": show_raw}
        return controls


def main() -> None:
    render_header()

    # Load data
    try:
        df = load_movie_ratings()
    except FileNotFoundError:
        st.error(
            "Could not find data file at ../data/movie_ratings.csv. "
            "Verify the project layout matches the course repo."
        )
        return

    controls = render_sidebar(df)

    if controls.get("show_raw"):
        with st.expander("Raw data (first 50 rows)", expanded=False):
            st.dataframe(df.head(50), use_container_width=True)

    # Tabs per question (outline only for now)
    tabs = st.tabs(
        [
            "Q1: Genre breakdown",
            "Q2: Avg rating by genre",
            "Q3: Avg rating by release year",
            "Q4: Top movies by ratings (placeholder)",
        ]
    )

    with tabs[0]:
        st.subheader("Q1: What's the breakdown of genres for the movies that were rated?")
        # Aggregate counts by genre (data is already pre-exploded)
        genre_counts = (
            df.groupby("genres", dropna=False)
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .reset_index(drop=True)                  # reset index so top rows = top counts
        )

###### bar chart
        # Plotly bar chart (horizontal, sorted)
        fig = px.bar(
            genre_counts,
            x="count",
            y="genres",
            orientation="h",              
            labels={"count": "Number of Movies Rated", "genres": "Genre"},
            title="Genre Breakdown of Rated Movies",
            height = 800
        )

        fig.update_layout(yaxis=dict(autorange="reversed"), bargap=0.3, title_x=0.5,  )  # biggest on top
        top_n = 5
        labels = genre_counts["count"].where(
            genre_counts.index < top_n, ""   # only show top N labels
        )

        fig.update_traces(
            text=labels,
            textposition="outside"
        )

        st.plotly_chart(fig, use_container_width=True)

#######  pie chart
        st.caption("Pie chart of rating counts by pre-exploded 'genres'.")

        # Controls for grouping small slices
        min_pct = st.slider(
            "Group slices under this percentage into 'Other'",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.5,
            help="Genres contributing less than this percent will be grouped as 'Other'.",
        )

        

        total = genre_counts["count"].sum()
        genre_counts["pct"] = 100 * genre_counts["count"] / max(total, 1)

        # Group small categories into 'Other'
        major = genre_counts[genre_counts["pct"] >= min_pct].copy()
        minor = genre_counts[genre_counts["pct"] < min_pct]
        if not minor.empty:
            other_row = pd.DataFrame({
                "genres": ["Other"],
                "count": [int(minor["count"].sum())],
                "pct": [minor["pct"].sum()],
            })
            display_df = pd.concat([major, other_row], ignore_index=True)
        else:
            display_df = major

        fig = px.pie(
            display_df,
            names="genres",
            values="count",
            title="Composition of Ratings by Genre",
            hole=0.0,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

###Avg ratings by genre
    with tabs[1]:
        st.subheader("Q2: Which genres have the highest viewer satisfaction?")
        avg_ratings = df.groupby("genres")["rating"].mean().reset_index()
        # Sort descending by rating
        avg_ratings = avg_ratings.sort_values("rating", ascending=False)

        # Ensure x-axis follows descending order
        x_categories = avg_ratings["genres"].tolist()

        # Line traces first (the sticks)
        line_traces = [
            go.Scatter(
                x=[genre, genre],
                y=[0, rating],
                mode="lines",
                line=dict(color="lightgray", width=2),
                showlegend=False
            )
            for genre, rating in zip(avg_ratings["genres"], avg_ratings["rating"])
        ]

        # Dot trace
        dot_trace = go.Scatter(
            x=avg_ratings["genres"],
            y=avg_ratings["rating"],
            mode="markers+text",
            text=avg_ratings["rating"].round(2), textfont=dict(color="white", size=12),
            textposition="middle center",
            marker=dict(size=30, color="royalblue"), showlegend = False
        )

        fig = go.Figure(data=line_traces + [dot_trace])
        fig.update_layout(
            title="Average Viewer Satisfaction by Genre",
            title_x=0.5,          # center title
            xaxis_title="Genre",
            yaxis_title="Average Rating",
            xaxis=dict(categoryorder="array", categoryarray=x_categories, showgrid=False),  # forces descending
            yaxis=dict(range=[avg_ratings["rating"].min() - 0.1, avg_ratings["rating"].max() + 0.1], showgrid=False)
        )

        st.plotly_chart(fig, use_container_width=True)


    with tabs[2]:
        st.subheader("Q3: How does mean rating change across movie release years?")
###### scatter
        # Compute mean rating per year
        avg_by_year = df.groupby("year")["rating"].mean().reset_index()

        # Smooth with rolling window
        avg_by_year["rating_smooth"] = avg_by_year["rating"].rolling(window=3, center=True).mean()

        # Plot smoothed line
        fig_t = px.line(
            avg_by_year,
            x="year",
            y="rating_smooth",
            labels={"year": "Release Year", "rating_smooth": "Average Rating (3-yr rolling)"},
            title="Smoothed Mean Movie Rating Over Years"
        )

        # add original yearly points
        fig_t.add_scatter(
            x=avg_by_year["year"],
            y=avg_by_year["rating"],
            mode="markers",
            marker=dict(color="lightgray", size=6),
            name="Yearly mean"
        )
        st.plotly_chart(fig_t)


 ###########       
        st.caption("Interactive line chart of mean rating by release year.")

        # Controls
        min_year, max_year = int(df["year"].min()), int(df["year"].max())
        year_range = st.slider(
            "Year range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1,
        )
        col1, col2 = st.columns([1, 1])
        with col1:
            min_count_year = st.number_input(
                "Minimum ratings per year",
                min_value=0,
                max_value=100000,
                value=50,
                step=10,
            )
        with col2:
            smooth_window = st.slider(
                "Rolling mean window (years)", min_value=1, max_value=9, value=1, step=1
            )

        # Aggregate by year
        year_stats = (
            df.groupby("year", dropna=False)
            .agg(mean_rating=("rating", "mean"), n_ratings=("rating", "size"))
            .reset_index()
        )
        # Filter by selected range and min count
        lo, hi = year_range
        mask = (year_stats["year"] >= lo) & (year_stats["year"] <= hi)
        year_filtered = year_stats[mask & (year_stats["n_ratings"] >= min_count_year)].copy()
        year_filtered = year_filtered.sort_values("year")

        # Optional smoothing
        if smooth_window and smooth_window > 1 and not year_filtered.empty:
            year_filtered["mean_rating_smoothed"] = (
                year_filtered["mean_rating"].rolling(window=smooth_window, center=True).mean()
            )
        else:
            year_filtered["mean_rating_smoothed"] = year_filtered["mean_rating"]

        fig3 = px.line(
            year_filtered,
            x="year",
            y="mean_rating_smoothed",
            hover_data={"n_ratings": True, "mean_rating": ":.2f"},
            title="Movie Release Year vs Average Rating",
        )
        fig3.update_layout(xaxis_title="Movie Release Year", yaxis_title="Average Rating")
        st.plotly_chart(fig3, use_container_width=True)
#########
    with tabs[3]:
        st.subheader("Q4: Top movies by average rating (interactive)")
####### table
        # Compute average rating and count per movie
        movie_stats = df.groupby("title")["rating"].agg(['mean','count']).reset_index()
        movie_stats.rename(columns={'mean':'avg_rating','count':'num_ratings'}, inplace=True)

        

        # Top 5 movies with ≥50 ratings
        top_50 = movie_stats[movie_stats['num_ratings'] >= 50].sort_values('avg_rating', ascending=False).head(5)
        top_50 = top_50[['title','avg_rating']].rename(columns={'avg_rating':'Average Rating'}).reset_index(drop=True)
        top_50['Average Rating'] = top_50['Average Rating'].round(2)
        top_50['Average Rating'] = top_50['Average Rating'].apply(lambda x: '{:.2f}'.format(x).rstrip('0').rstrip('.'))


        # Top 5 movies with ≥150 ratings
        top_150 = movie_stats[movie_stats['num_ratings'] >= 150].sort_values('avg_rating', ascending=False).head(5)
        top_150 = top_150[['title','avg_rating']].rename(columns={'avg_rating':'Average Rating'}).reset_index(drop=True)
        top_150['Average Rating'] = top_150['Average Rating'].round(2)
        top_150['Average Rating'] = top_150['Average Rating'].apply(lambda x: '{:.2f}'.format(x).rstrip('0').rstrip('.'))

        # Titles appearing in both top 5 lists
        common_titles = set(top_50['title']).intersection(set(top_150['title']))

        # Highlight function
        def highlight_common(row, common_set):
            styles = []
            for col in row.index:
                if col == 'title' and row[col] in common_set:
                    styles.append('background-color: lightgreen')
                else:
                    styles.append('')
            return styles

        # Display side by side
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top 5 Movies with ≥50 Ratings")
            st.dataframe(top_50.style.apply(highlight_common, common_set=common_titles, axis=1).hide(axis=0), use_container_width=True)

        with col2:
            st.subheader("Top 5 Movies with ≥150 Ratings")
            st.dataframe(top_150.style.apply(highlight_common, common_set=common_titles, axis=1).hide(axis="index"), use_container_width=True)


    
        st.caption("Horizontal bar chart of top movies; size = number of ratings.")

        col1, col2 = st.columns([1, 1])
        with col1:
            min_ratings_movie = st.number_input(
                "Minimum number of ratings per movie",
                min_value=1,
                max_value=100000,
                value=50,
                step=10,
            )
        with col2:
            top_n = st.slider("Top N movies", min_value=3, max_value=25, value=5, step=1)

        movie_stats = (
            df.groupby(["movie_id", "title"], dropna=False)
            .agg(mean_rating=("rating", "mean"), n_ratings=("rating", "size"))
            .reset_index()
        )
        movie_filtered = movie_stats[movie_stats["n_ratings"] >= min_ratings_movie].copy()
        top_movies = movie_filtered.sort_values(
            ["mean_rating", "n_ratings"], ascending=[False, False]
        ).head(top_n)

        # Plot horizontal bar where bar length is mean rating; marker size encodes n_ratings
        fig4 = px.bar(
            top_movies,
            y="title",
            x="mean_rating",
            orientation="h",
            hover_data={"n_ratings": True, "mean_rating": ":.2f"},
            title=f"Top {top_n} Movies by Average Rating (min {min_ratings_movie} ratings)",
        )
        fig4.update_layout(xaxis_title="Average Rating (1–5)", yaxis_title="Movie Title")
        st.plotly_chart(fig4, use_container_width=True)


if __name__ == "__main__":
    main()






