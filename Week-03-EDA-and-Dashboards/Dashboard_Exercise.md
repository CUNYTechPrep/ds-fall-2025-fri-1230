# Week 3 Dashboard Exercise: MovieLens Data Analysis

## Overview
In this exercise, you will create visualizations or a small dashboard to analyze movie ratings from the MovieLens 100k dataset. Your goal is to answer analytical questions with clear, well-designed charts.

## Dataset
**File**: `data/movie_ratings.csv`

This dataset contains 100,000 movie ratings from 943 users on 1,682 movies, with demographic and movie metadata.

### Columns
- **user_id**: Unique user identifier
- **movie_id**: Unique movie identifier
- **rating**: Rating (1–5 scale)
- **timestamp**: When the rating was given
- **age**: User age
- **gender**: User gender (M/F)
- **occupation**: User occupation
- **zip_code**: User ZIP code
- **title**: Movie title with year
- **year**: Movie release year
- **decade**: Movie release decade
- **genres**: Pipe-separated genres for each movie
- **rating_year**: Year the rating was given

## Questions to Answer (4)
1. Which genres have the highest viewer satisfaction?
   - Suggested: Horizontal bar chart of mean rating by genre with count annotations and a minimum-n threshold.
2. How do ratings vary across movie release decades?
   - Suggested: Dual-axis chart — bars for number of ratings, line for mean rating by decade.
3. What are the best-rated movies after a minimum-ratings threshold?
   - Suggested: Top-10 horizontal bars, label counts, tie-break by volume.
4. Do age groups favor certain genres?
   - Suggested: Heatmap of average rating by age group × genre (filter to popular genres).

## Optional Extensions (if time permits)
5. Popularity vs. Quality by Genre (Scatter)
   - Plot mean rating (y) vs. number of ratings (x) per genre; optionally size by count.
   - Label a few notable genres; discuss the trade-off.

6. Genre Composition of Ratings (Pie)
   - Show share of total ratings by genre. Limit to top 8 genres and group the rest as "Other".
   - Use simple labeling; avoid 3D effects.

## Notes and Caveats
- Movies can belong to multiple genres. Exploding genres is acceptable for preference profiling but not for market share.
- Use minimum sample thresholds (e.g., n ≥ 50 or 100) to avoid small-sample noise.
- Decade and age-group distributions are uneven; include counts or context where relevant.

## Deliverables

### Option A: Streamlit Dashboard (Recommended)
Create an interactive Streamlit app that:
- Loads and displays the dataset
- Contains visualizations answering each question
- Includes interactive filters (age ranges, occupations, genres, etc.)
- Has clear titles, labels, and explanations for each chart
- Provides insights and conclusions based on the visualizations

### Option B: Jupyter Notebook
Create a comprehensive notebook that:
- Explores the dataset with summary statistics
- Creates static visualizations answering each question
- Includes markdown explanations of findings
- Uses professional-quality plots with proper styling

### Option C: Other Dashboard Tools
Feel free to use other tools like:
- **Tableau** - Professional data visualization platform (great for interactive dashboards)
- **Plotly Dash** - Python web app framework
- **Panel** - Python dashboard library
- **Power BI** - Microsoft's business analytics tool
- **Observable** - Web-based data visualization platform

As long as you can demonstrate your visualizations effectively and answer the analytical questions.

## Technical Requirements

### Data Processing
- Load and clean the data appropriately
- Handle missing values if any
- Create derived metrics as needed (e.g., age groups, popularity scores)

### Visualizations
- Use appropriate chart types for each question
- Include proper titles, axis labels, and legends
- Use color effectively to enhance understanding
- Ensure charts are readable and professional

### Code Quality
- Write clean, commented code
- Use meaningful variable names
- Structure your code logically
- Include error handling where appropriate

## Getting Started

1. **Load the data**:
```python
import pandas as pd
df = pd.read_csv('data/movie_ratings.csv')
```

2. **Explore the dataset**:
```python
print(df.info())
print(df.describe())
print(df.head())
```

3. **Start with basic visualizations** for each question
4. **Iterate and improve** based on insights
5. **Add interactivity** if using Streamlit or similar tools

## Evaluation Criteria

- **Data Understanding** (20%): Demonstrates clear understanding of the dataset
- **Visualization Quality** (30%): Charts are appropriate, clear, and well-designed  
- **Analytical Insights** (25%): Provides meaningful answers to the questions
- **Technical Implementation** (15%): Code is clean and functions properly
- **Presentation** (10%): Professional appearance and clear communication

## Resources

### Visualization Libraries & Tools
- [Streamlit Documentation](https://docs.streamlit.io/) - Build interactive web apps
- [Plotly Python Documentation](https://plotly.com/python/) - Interactive plots
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html) - Static plotting
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html) - Statistical visualization
- [Tableau Public](https://public.tableau.com/) - Free version of Tableau
- [Power BI Learning](https://docs.microsoft.com/en-us/power-bi/) - Microsoft's BI tool

### Data Analysis
- [Pandas Documentation](https://pandas.pydata.org/docs/) - Data manipulation
- [NumPy Documentation](https://numpy.org/doc/) - Numerical computing

### Design & Best Practices
- [Data Visualization Catalogue](https://datavizcatalogue.com/) - Chart type selection guide
- [Storytelling with Data](https://www.storytellingwithdata.com/) - Visualization best practices

## Submission
- Submit your code files (`.py` for Streamlit apps, `.ipynb` for notebooks)
- Include a brief README with instructions to run your code
- If using Streamlit, include a `requirements.txt` file

Good luck, and have fun exploring the data.
