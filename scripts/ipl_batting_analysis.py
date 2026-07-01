# ============================================================
# IPL Batting Analysis — Pandas Script (FIXED)
# Author: Kalyankar Mythlesh
# Dataset: IPL ball-by-ball data (2008–2025)


import pandas as pd
import matplotlib
matplotlib.use('Agg')  # headless-safe backend
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. LOAD DATA ─────────────────────────────────────────────
df = pd.read_csv('IPL.csv', low_memory=False)
print(f"Dataset shape: {df.shape}")
print(f"Seasons covered: {sorted(df['season'].dropna().unique())}\n")

# ── 2. TOTAL RUNS PER BATSMAN ────────────────────────────────
total_runs = df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False)
print("Top 10 Run Scorers:")
print(total_runs.head(10))
print()

# ── 3. DISMISSALS ────────────────────────────────────────────
dismissals = (
    df[df['player_out'].notna() & (df['player_out'] != '')]
    .groupby('player_out')
    .size()
    .rename('dismissals')
)

# ── 4. BATTING AVERAGE (raw, unfiltered) ─────────────────────
# Average = total runs / times dismissed
batting_avg_raw = (total_runs / dismissals).dropna().rename('batting_avg')

# Qualified view used only for the Top 10 print/chart (min 20 dismissals)
batting_avg_qualified = batting_avg_raw[dismissals >= 20].sort_values(ascending=False)
print("Top 10 Batting Averages (min 20 dismissals):")
print(batting_avg_qualified.head(10).round(2))
print()

# ── 5. STRIKE RATE (raw, unfiltered) ─────────────────────────
# Strike rate = (runs / balls faced) * 100
# (excludes wides AND no-balls — wrong denominator for a batting stat)
balls_faced = df.groupby('batter')['balls_faced'].sum().rename('balls_faced')
strike_rate_raw = ((total_runs / balls_faced) * 100).rename('strike_rate')

# Qualified view used only for the Top 10 print/chart (min 200 balls)
strike_rate_qualified = strike_rate_raw[balls_faced >= 200].sort_values(ascending=False)
print("Top 10 Strike Rates (min 200 balls faced):")
print(strike_rate_qualified.head(10).round(2))
print()

# ── 6. INNINGS PLAYED ────────────────────────────────────────
# so Super Over appearances are counted as separate innings.
innings = (
    df.assign(_match_innings=df['match_id'].astype(str) + '_' + df['innings'].astype(str))
    .groupby('batter')['_match_innings']
    .nunique()
    .rename('innings')
)

# ── 7. COMBINED STATS TABLE ──────────────────────────────────
stats_df = pd.DataFrame({
    'batter': total_runs.index,
    'total_runs': total_runs.values
})
stats_df = (
    stats_df
    .merge(batting_avg_raw, left_on='batter', right_index=True, how='left')
    .merge(strike_rate_raw, left_on='batter', right_index=True, how='left')
    .merge(innings, left_on='batter', right_index=True, how='left')
    .merge(dismissals, left_on='batter', right_index=True, how='left')
    .merge(balls_faced, left_on='batter', right_index=True, how='left')
)

# Most played season per batter
season_data = (
    df.groupby('batter')['year']
    .agg(lambda x: x.mode()[0])
    .reset_index()
    .rename(columns={'year': 'most_active_year'})
)
stats_df = stats_df.merge(season_data, on='batter', how='left')

# Save to CSV for Power BI
stats_df.to_csv('ipl_batting_stats_v2.csv', index=False)
print(f"Saved ipl_batting_stats_v2.csv — {len(stats_df)} batters\n")

# ── 8. VISUALIZATIONS ────────────────────────────────────────
sns.set_theme(style='whitegrid')
fig, axes = plt.subplots(1, 3, figsize=(20, 7))
fig.suptitle('IPL Batting Analysis Dashboard', fontsize=18, fontweight='bold', y=1.02)

# Chart 1 — Top 10 Run Scorers
top10_runs = total_runs.head(10)
axes[0].barh(top10_runs.index[::-1], top10_runs.values[::-1], color='steelblue')
axes[0].set_title('Top 10 Run Scorers', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Total Runs')

# Chart 2 — Top 10 Batting Averages (qualified)
top10_avg = batting_avg_qualified.head(10)
axes[1].barh(top10_avg.index[::-1], top10_avg.values[::-1], color='seagreen')
axes[1].set_title('Top 10 Batting Averages\n(min 20 dismissals)', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Batting Average')

# Chart 3 — Top 10 Strike Rates (qualified)
top10_sr = strike_rate_qualified.head(10)
axes[2].barh(top10_sr.index[::-1], top10_sr.values[::-1], color='darkorange')
axes[2].set_title('Top 10 Strike Rates\n(min 200 balls)', fontsize=13, fontweight='bold')
axes[2].set_xlabel('Strike Rate')

plt.tight_layout()
plt.savefig('ipl_batting_dashboard.png', dpi=150, bbox_inches='tight')
print("Chart saved as ipl_batting_dashboard.png")
