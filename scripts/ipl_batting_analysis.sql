-- ============================================================
-- IPL Batting Analysis — SQL Queries (FIXED)
-- Author: Kalyankar Mythilesh 
-- Dataset: IPL ball-by-ball data (2008–2025)
-- Note: Load ipl_batting_stats_v2.csv into your SQL database
--       (SQLite / MySQL / PostgreSQL all work)
-- ============================================================


-- ── 1. TOP 10 RUN SCORERS ────────────────────────────────────
SELECT
    batter,
    total_runs,
    innings,
    dismissals
FROM ipl_batting_stats
ORDER BY total_runs DESC
LIMIT 10;


-- ── 2. TOP 10 BATTING AVERAGES ───────────────────────────────
-- Only include batters with at least 20 dismissals
SELECT
    batter,
    ROUND(batting_avg, 2) AS batting_avg,
    total_runs,
    dismissals
FROM ipl_batting_stats
WHERE dismissals >= 20
ORDER BY batting_avg DESC
LIMIT 10;


-- ── 3. TOP 10 STRIKE RATES ───────────────────────────────────
-- players (e.g. a bowler who hit one six off three balls)
-- can't top the leaderboard.
SELECT
    batter,
    ROUND(strike_rate, 2) AS strike_rate,
    total_runs,
    balls_faced
FROM ipl_batting_stats
WHERE strike_rate IS NOT NULL
  AND balls_faced >= 200
ORDER BY strike_rate DESC
LIMIT 10;


-- ── 4. BEST ALL-ROUNDERS ─────────────────────────────────────
-- Players who rank high in BOTH average AND strike rate
SELECT
    batter,
    total_runs,
    ROUND(batting_avg, 2)  AS batting_avg,
    ROUND(strike_rate, 2)  AS strike_rate,
    innings
FROM ipl_batting_stats
WHERE dismissals >= 20
  AND strike_rate >= 130
  AND batting_avg >= 30
ORDER BY batting_avg DESC, strike_rate DESC
LIMIT 10;


-- ── 5. MOST CONSISTENT BATTERS ───────────────────────────────
-- High average with high innings count = consistent over career
SELECT
    batter,
    innings,
    ROUND(batting_avg, 2) AS batting_avg,
    total_runs
FROM ipl_batting_stats
WHERE innings >= 50
  AND dismissals >= 20
ORDER BY batting_avg DESC
LIMIT 10;


-- ── 6. RUNS PER INNINGS (EFFICIENCY) ─────────────────────────
SELECT
    batter,
    total_runs,
    innings,
    ROUND(CAST(total_runs AS FLOAT) / innings, 2) AS runs_per_innings,
    ROUND(batting_avg, 2) AS batting_avg
FROM ipl_batting_stats
WHERE innings >= 30
ORDER BY runs_per_innings DESC
LIMIT 10;


-- ── 7. SUMMARY STATISTICS ────────────────────────────────────
SELECT
    COUNT(*)                        AS total_batters,
    SUM(total_runs)                 AS total_ipl_runs,
    ROUND(AVG(batting_avg), 2)      AS avg_batting_avg,
    ROUND(AVG(strike_rate), 2)      AS avg_strike_rate,
    MAX(total_runs)                 AS highest_run_scorer_runs,
    ROUND(MAX(batting_avg), 2)      AS highest_batting_avg,
    ROUND(MAX(strike_rate), 2)      AS highest_strike_rate
FROM ipl_batting_stats
WHERE dismissals >= 20;
