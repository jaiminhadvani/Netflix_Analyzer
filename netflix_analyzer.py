import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

# --- Enhanced Styling ---
plt.style.use('dark_background')
sns.set_palette("husl")
plt.rcParams["figure.figsize"] = (12, 7)
plt.rcParams["font.size"] = 10
plt.rcParams["axes.facecolor"] = "#0f0f0f"
plt.rcParams["figure.facecolor"] = "#1a1a1a"

# Netflix brand colors
NETFLIX_RED = "#E50914"
NETFLIX_BLACK = "#1a1a1a"

# --- Config ---
EXPECTED_FILENAME = "NetflixViewingHistory.csv"
OUTPUT_DIR = "netflix_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_netflix_csv(path):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    return df

def detect_datetime_column(df):
    for col in df.columns:
        if 'date' in col.lower():
            return col
    for col in df.columns:
        try:
            pd.to_datetime(df[col].dropna().iloc[:5])
            return col
        except Exception:
            continue
    return None

def detect_duration_column(df):
    for col in df.columns:
        if 'duration' in col.lower() or 'minutes' in col.lower() or 'time' in col.lower():
            return col
    return None

def try_extract_minutes_from_str(s):
    if pd.isna(s): return np.nan
    s = str(s)
    mins = 0
    import re
    m_h = re.search(r'(\d+)\s*h', s)
    m_m = re.search(r'(\d+)\s*m', s)
    if m_h: mins += int(m_h.group(1))*60
    if m_m: mins += int(m_m.group(1))
    if mins > 0: return mins
    m_num = re.search(r'(\d{1,4})\s*min', s)
    if m_num:
        return int(m_num.group(1))
    return np.nan

def main():
    if not os.path.exists(EXPECTED_FILENAME):
        print(f"Put your Netflix export CSV in the working folder and name it '{EXPECTED_FILENAME}'.")
        print("If your file has a different name, change EXPECTED_FILENAME in the script.")
        return

    df = load_netflix_csv(EXPECTED_FILENAME)
    print("Columns found:", df.columns.tolist())

    date_col = detect_datetime_column(df)
    dur_col = detect_duration_column(df)
    title_col = None
    for c in df.columns:
        if 'title' in c.lower() or 'show' in c.lower() or 'name' in c.lower():
            title_col = c
            break
    if title_col is None:
        title_col = df.columns[0]

    if date_col is None:
        df['parsed_date'] = pd.to_datetime(df.index, errors='coerce')
    else:
        df['parsed_date'] = pd.to_datetime(df[date_col], errors='coerce')

    if dur_col:
        df['minutes'] = pd.to_numeric(df[dur_col], errors='coerce')
        if df['minutes'].isna().all():
            df['minutes'] = df[dur_col].apply(try_extract_minutes_from_str)
    else:
        possible_cols = [c for c in df.columns if c not in [date_col, title_col]]
        minutes = pd.Series(np.nan, index=df.index)
        for c in possible_cols:
            minutes = minutes.fillna(df[c].apply(try_extract_minutes_from_str))
        df['minutes'] = minutes

    minutes_available = df['minutes'].notna().sum() > 0
    if not minutes_available:
        df['minutes'] = 1

    df['date'] = df['parsed_date'].dt.date
    df['weekday'] = df['parsed_date'].dt.day_name()
    df['hour'] = df['parsed_date'].dt.hour
    df['month'] = df['parsed_date'].dt.to_period('M').astype(str)

    total_sessions = len(df)
    total_minutes = df['minutes'].sum()
    total_hours = int(total_minutes / 60)
    print(f"\n{'='*50}")
    print(f"📊 NETFLIX VIEWING STATISTICS")
    print(f"{'='*50}")
    print(f"Total sessions: {total_sessions:,}")
    print(f"Total minutes: {total_minutes:,.0f}")
    print(f"Total hours: {total_hours:,}")
    print(f"{'='*50}\n")

    top_by_views = df.groupby(title_col).size().sort_values(ascending=False).head(10)
    top_by_time = df.groupby(title_col)['minutes'].sum().sort_values(ascending=False).head(10)
    top_by_views.to_csv(os.path.join(OUTPUT_DIR, "top_by_views.csv"))
    top_by_time.to_csv(os.path.join(OUTPUT_DIR, "top_by_time.csv"))

    # --- Enhanced Top 10 by Views ---
    fig, ax = plt.subplots(figsize=(12, 7))
    top_by_views.plot(kind='barh', ax=ax, color=NETFLIX_RED)
    ax.set_xlabel('Number of Views', fontsize=12, fontweight='bold')
    ax.set_ylabel('Title', fontsize=12, fontweight='bold')
    ax.set_title('🎬 Top 10 Most Watched Titles', fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    for i, v in enumerate(top_by_views.values):
        ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_by_views.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # --- Enhanced Top 10 by Time ---
    fig, ax = plt.subplots(figsize=(12, 7))
    top_by_time.plot(kind='barh', ax=ax, color='#FF6B35')
    ax.set_xlabel('Minutes Watched', fontsize=12, fontweight='bold')
    ax.set_ylabel('Title', fontsize=12, fontweight='bold')
    ax.set_title('⏱️ Top 10 Shows by Watch Time', fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    for i, v in enumerate(top_by_time.values):
        ax.text(v + 10, i, f'{int(v)}m', va='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_by_time.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # --- Enhanced Heatmap ---
    pivot = df.pivot_table(index='weekday', columns='hour', values='minutes', aggfunc='sum', fill_value=0)
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    pivot = pivot.reindex(weekdays).fillna(0)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap='YlOrRd', cbar_kws={'label': 'Minutes'}, ax=ax, linewidths=0.5)
    ax.set_title('🌡️ Watch Time Heatmap (Weekday vs Hour)', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel('Weekday', fontsize=12, fontweight='bold')
    ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "heatmap_weekday_hour.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # --- Enhanced Monthly Trend ---
    monthly = df.groupby('month')['minutes'].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(range(len(monthly)), monthly.values, marker='o', linewidth=3, markersize=8, color=NETFLIX_RED)
    ax.fill_between(range(len(monthly)), monthly.values, alpha=0.3, color=NETFLIX_RED)
    ax.set_xticks(range(len(monthly)))
    ax.set_xticklabels(monthly.index, rotation=45, ha='right')
    ax.set_title('📈 Monthly Watch Time Trend', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Minutes Watched', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.2)
    for i, v in enumerate(monthly.values):
        ax.text(i, v + 100, f'{int(v)}', ha='center', fontweight='bold', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "monthly_trend.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # --- Binge Detection ---
    binge = df.groupby(['date', title_col]).size().reset_index(name='counts')
    binge = binge[binge['counts'] >= 3].sort_values('counts', ascending=False)
    binge.to_csv(os.path.join(OUTPUT_DIR, "binge_sessions.csv"), index=False)

    # --- Enhanced Summary Dashboard ---
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

    # Summary stats boxes
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    
    summary_text = f"""
    📊 YOUR NETFLIX VIEWING REPORT
    
    Total Watch Sessions: {total_sessions:,}  |  Total Hours: {total_hours:,}  |  Total Minutes: {total_minutes:,.0f}
    
    Most Watched: {top_by_views.index[0] if len(top_by_views)>0 else 'N/A'} ({top_by_views.values[0]} views)
    
    Highest Time Investment: {top_by_time.index[0] if len(top_by_time)>0 else 'N/A'} ({int(top_by_time.values[0])} min)
    """
    
    ax1.text(0.5, 0.5, summary_text, fontsize=11, ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor=NETFLIX_RED, alpha=0.2, pad=1),
            family='monospace', fontweight='bold')

    # Pie chart for top genres
    ax2 = fig.add_subplot(gs[1, 0])
    top5_views = top_by_views.head(5)
    colors = plt.cm.Set3(np.linspace(0, 1, len(top5_views)))
    ax2.pie(top5_views.values, labels=top5_views.index, autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('Top 5 by Views', fontsize=12, fontweight='bold')

    # Donut chart for time
    ax3 = fig.add_subplot(gs[1, 1])
    top5_time = top_by_time.head(5)
    colors = plt.cm.Set2(np.linspace(0, 1, len(top5_time)))
    wedges, texts, autotexts = ax3.pie(top5_time.values, labels=top5_time.index, autopct='%1.1f%%', colors=colors, startangle=90)
    centre_circle = plt.Circle((0,0), 0.70, fc=NETFLIX_BLACK)
    ax3.add_artist(centre_circle)
    ax3.set_title('Top 5 by Watch Time', fontsize=12, fontweight='bold')

    # Daily avg
    ax4 = fig.add_subplot(gs[2, :])
    daily = df.groupby('date')['minutes'].sum()
    ax4.bar(range(len(daily[-30:])), daily.tail(30).values, color=NETFLIX_RED, alpha=0.7)
    ax4.set_title('Last 30 Days Watch Time', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Days', fontsize=10)
    ax4.set_ylabel('Minutes', fontsize=10)
    ax4.grid(True, alpha=0.2, axis='y')

    plt.savefig(os.path.join(OUTPUT_DIR, "summary_dashboard.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # --- Save summary ---
    summary = {
        'total_sessions': total_sessions,
        'total_minutes': total_minutes,
        'total_hours': total_hours,
        'top_title_by_views': top_by_views.index[0] if len(top_by_views)>0 else None,
        'top_title_by_time': top_by_time.index[0] if len(top_by_time)>0 else None
    }
    pd.Series(summary).to_csv(os.path.join(OUTPUT_DIR, "summary.csv"))

    print("✅ Outputs written to", OUTPUT_DIR)
    print("📁 Generated files:")
    print("   - summary_dashboard.png (main overview)")
    print("   - top_by_views.png & top_by_time.png")
    print("   - heatmap_weekday_hour.png")
    print("   - monthly_trend.png")
    print("   - binge_sessions.csv")
    print("   - summary.csv\n")

if __name__ == "__main__":
    main()