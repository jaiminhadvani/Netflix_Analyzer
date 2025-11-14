# Netflix Viewing History Analyzer - Project Report

## Executive Summary

This project presents a comprehensive data analysis tool designed to analyze Netflix viewing history data. The application processes exported viewing history CSV files and generates detailed insights through statistical analysis and data visualization. The tool provides users with valuable information about their viewing patterns, including top-watched content, viewing trends, binge-watching sessions, and temporal viewing behaviors.

---

## 1. Introduction

### 1.1 Project Overview
The Netflix Viewing History Analyzer is a Python-based data analysis application that transforms raw Netflix viewing history data into meaningful insights and visualizations. The project demonstrates proficiency in data processing, statistical analysis, and data visualization using Python libraries.

### 1.2 Objectives
- **Primary Objective**: Develop an automated tool to analyze Netflix viewing history and generate comprehensive reports
- **Secondary Objectives**:
  - Identify viewing patterns and trends
  - Detect binge-watching sessions
  - Visualize viewing habits across different time dimensions (daily, weekly, monthly)
  - Generate publication-ready visualizations and summary statistics

### 1.3 Scope
The project analyzes viewing history data including:
- Total viewing sessions and watch time
- Most frequently watched titles
- Titles with highest time investment
- Viewing patterns by weekday and hour
- Monthly viewing trends
- Binge-watching detection (3+ episodes of the same title in one day)

---

## 2. Methodology

### 2.1 Data Source
The application processes Netflix viewing history data exported as CSV files. The expected format includes:
- **Title**: Name of the watched content
- **Date**: Date and time of viewing
- **Duration** (optional): Watch time in minutes or formatted strings (e.g., "1h 30m")

### 2.2 Data Processing Pipeline

#### 2.2.1 Data Loading
- Automatic detection of CSV file structure
- Flexible column detection for date, title, and duration fields
- Robust error handling for missing or malformed data

#### 2.2.2 Data Cleaning and Transformation
- **Date Parsing**: Converts date strings to datetime objects with error handling
- **Duration Extraction**: Parses duration from various formats:
  - Numeric values (minutes)
  - String formats ("1h 30m", "90 min")
  - Defaults to 1 minute if duration unavailable
- **Feature Engineering**: Creates derived features:
  - `date`: Date component
  - `weekday`: Day of week name
  - `hour`: Hour of day (0-23)
  - `month`: Monthly period identifier

#### 2.2.3 Statistical Analysis
- Aggregation operations:
  - Total sessions count
  - Total watch time (minutes/hours)
  - Grouped statistics by title, date, weekday, hour, and month
- Binge detection algorithm:
  - Groups sessions by date and title
  - Identifies sessions with 3+ episodes of the same title in one day

---

## 3. Features and Functionality

### 3.1 Core Features

#### 3.1.1 Summary Statistics
- Total viewing sessions
- Total watch time (in minutes and hours)
- Most watched title by view count
- Title with highest time investment

#### 3.1.2 Top Content Analysis
- **Top 10 by Views**: Titles watched most frequently
- **Top 10 by Time**: Titles with highest cumulative watch time
- Exports results to CSV for further analysis

#### 3.1.3 Temporal Analysis
- **Weekday-Hour Heatmap**: Visualizes viewing patterns across days of week and hours of day
- **Monthly Trend**: Tracks viewing time trends over months
- **Last 30 Days**: Daily viewing time for recent period

#### 3.1.4 Binge Detection
- Identifies binge-watching sessions (3+ episodes of same title per day)
- Exports binge session data to CSV with episode counts

### 3.2 Visualization Features

#### 3.2.1 Visual Design
- Netflix-branded color scheme (Netflix Red: #E50914)
- Dark background theme for modern aesthetic
- High-resolution output (300 DPI) for publication quality
- Professional typography and layout

#### 3.2.2 Generated Visualizations
1. **Top 10 Most Watched Titles** (Horizontal Bar Chart)
   - Shows view counts for most frequently watched content
   - Includes value labels on bars

2. **Top 10 Shows by Watch Time** (Horizontal Bar Chart)
   - Displays cumulative watch time in minutes
   - Highlights titles with highest time investment

3. **Watch Time Heatmap** (Weekday vs Hour)
   - Color-coded heatmap showing viewing intensity
   - Annotated with minute values
   - Uses YlOrRd colormap for intuitive interpretation

4. **Monthly Watch Time Trend** (Line Chart)
   - Time series showing viewing trends over months
   - Filled area under curve for emphasis
   - Value labels at data points

5. **Summary Dashboard** (Multi-panel Layout)
   - Summary statistics panel
   - Top 5 by views (pie chart)
   - Top 5 by watch time (donut chart)
   - Last 30 days daily viewing (bar chart)

---

## 4. Technical Implementation

### 4.1 Technology Stack

#### 4.1.1 Programming Language
- **Python 3.x**: Primary programming language

#### 4.1.2 Libraries and Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Base plotting library
- **seaborn**: Statistical data visualization
- **datetime**: Date and time handling
- **re**: Regular expressions for string parsing
- **os**: File system operations

### 4.2 Code Architecture

#### 4.2.1 Modular Design
The code is organized into logical functions:
- `load_netflix_csv()`: Data loading with column normalization
- `detect_datetime_column()`: Automatic date column detection
- `detect_duration_column()`: Duration column identification
- `try_extract_minutes_from_str()`: Duration parsing from strings
- `main()`: Orchestrates the entire analysis pipeline

#### 4.2.2 Key Design Patterns
- **Error Handling**: Graceful handling of missing or malformed data
- **Flexible Input**: Automatic detection of CSV structure
- **Separation of Concerns**: Data processing, analysis, and visualization are separated
- **Configurable Output**: Centralized output directory management

### 4.3 Output Structure
All generated files are saved to the `netflix_output/` directory:
- `summary.csv`: Key statistics in CSV format
- `top_by_views.csv`: Top titles by view count
- `top_by_time.csv`: Top titles by watch time
- `binge_sessions.csv`: Detected binge-watching sessions
- `summary_dashboard.png`: Comprehensive dashboard visualization
- `top_by_views.png`: Top 10 by views chart
- `top_by_time.png`: Top 10 by time chart
- `heatmap_weekday_hour.png`: Temporal viewing pattern heatmap
- `monthly_trend.png`: Monthly trend visualization

---

## 5. Results and Analysis

### 5.1 Sample Results
Based on the analysis of the provided Netflix viewing history:

- **Total Sessions**: 733 viewing sessions
- **Total Watch Time**: 12 hours (733 minutes)
- **Analysis Period**: Multiple months of viewing data

### 5.2 Key Insights Generated
1. **Viewing Frequency**: Identifies most frequently accessed content
2. **Time Investment**: Highlights content with highest cumulative watch time
3. **Viewing Patterns**: Reveals preferred viewing times and days
4. **Trend Analysis**: Shows viewing habits over time
5. **Binge Behavior**: Detects binge-watching patterns

### 5.3 Visualization Outputs
The tool generates multiple high-quality visualizations that provide:
- Quick overview through the summary dashboard
- Detailed analysis through individual charts
- Exportable data for further analysis

---

## 6. Challenges and Solutions

### 6.1 Challenges Encountered

#### 6.1.1 Data Format Variability
**Challenge**: Netflix CSV exports may have different column names and formats
**Solution**: Implemented flexible column detection algorithms that search for keywords and attempt type inference

#### 6.1.2 Duration Parsing
**Challenge**: Duration data may be in various formats (numeric, "1h 30m", "90 min")
**Solution**: Created robust parsing function using regular expressions to handle multiple formats

#### 6.1.3 Missing Data
**Challenge**: Some viewing records may lack duration information
**Solution**: Implemented default values (1 minute per session) and graceful degradation

### 6.2 Design Decisions
- **Dark Theme**: Chose dark background for modern aesthetic and reduced eye strain
- **Netflix Branding**: Used Netflix red color for brand consistency
- **High DPI**: 300 DPI output ensures publication-quality images
- **CSV Exports**: Provides raw data for users who want to perform additional analysis

---

## 7. Future Enhancements

### 7.1 Potential Improvements
1. **Genre Analysis**: Categorize content by genre and analyze genre preferences
2. **Recommendation Engine**: Suggest content based on viewing history
3. **Comparative Analysis**: Compare viewing habits across different time periods
4. **Export Formats**: Support for PDF reports and interactive HTML dashboards
5. **User Interface**: Develop GUI or web interface for easier interaction
6. **Advanced Statistics**: Add statistical measures (mean, median, standard deviation)
7. **Content Rating Analysis**: Analyze viewing patterns by content ratings
8. **Device Detection**: If available, analyze viewing by device type

### 7.2 Scalability Considerations
- Optimize for larger datasets (100,000+ sessions)
- Implement caching for repeated analyses
- Add progress bars for long-running operations
- Support for multiple user profiles

---

## 8. Conclusion

### 8.1 Project Summary
The Netflix Viewing History Analyzer successfully demonstrates the application of data science techniques to personal viewing data. The project showcases:

- **Data Processing**: Robust handling of real-world data formats
- **Statistical Analysis**: Comprehensive aggregation and pattern detection
- **Data Visualization**: Professional-quality visualizations
- **Code Quality**: Well-structured, maintainable Python code

### 8.2 Learning Outcomes
This project demonstrates proficiency in:
- Python programming and best practices
- Data manipulation with pandas
- Statistical analysis and aggregation
- Data visualization with matplotlib and seaborn
- Problem-solving and error handling
- Software design and modularity

### 8.3 Impact
The tool provides users with valuable insights into their viewing habits, enabling:
- Awareness of viewing patterns
- Data-driven understanding of entertainment consumption
- Potential for behavior modification if desired
- Entertainment value through self-discovery

---

## 9. References and Resources

### 9.1 Documentation
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Seaborn Documentation](https://seaborn.pydata.org/)

### 9.2 Data Source
- Netflix Viewing History export feature (Account Settings → Viewing Activity)

---

## 10. Appendix

### 10.1 File Structure
```
Project1/
├── netflix_analyzer.py          # Main analysis script
├── NetflixViewingHistory.csv    # Input data file
├── netflix_output/              # Output directory
│   ├── summary.csv
│   ├── top_by_views.csv
│   ├── top_by_time.csv
│   ├── binge_sessions.csv
│   ├── summary_dashboard.png
│   ├── top_by_views.png
│   ├── top_by_time.png
│   ├── heatmap_weekday_hour.png
│   └── monthly_trend.png
└── PROJECT_REPORT.md            # This report
```

### 10.2 Usage Instructions
1. Export your Netflix viewing history from your Netflix account
2. Save the CSV file as `NetflixViewingHistory.csv` in the project directory
3. Run the script: `python netflix_analyzer.py`
4. View generated outputs in the `netflix_output/` directory

### 10.3 Requirements
- Python 3.6+
- pandas
- numpy
- matplotlib
- seaborn

---

**Report Generated**: 2025
**Project**: Netflix Viewing History Analyzer
**Status**: Complete

