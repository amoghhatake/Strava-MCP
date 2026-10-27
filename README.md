# Strava MCP Server

A Python MCP server that lets Claude analyze your Strava running data in plain English.

## Tools

1. `load_activities`: load your Strava `activities.csv`
2. `get_column_names`: list the columns in the file
3. `total_run_distance`: total km across all runs
4. `weekly_distance`: run distance per week
5. `longest_run`: your longest run with its date
6. `injury_risk`: flag weeks where mileage jumped more than 30% above the prior 4-week average
7. `predict_race_time`: predict race time for a target distance using the Riegel formula

## Setup

1. Export your data from Strava (Settings -> My Account > Download or Delete Your Account -> Request Your Archive) and keep `activities.csv`.
2. Install dependencies: `pip install -r requirements.txt`
3. Test it: `mcp dev server.py`

## Claude Desktop config

Add this under `mcpServers` in `claude_desktop_config.json`, using your own path:

{
"mcpServers": {
"strava": {
"command": "python",
"args": ["C:\\path\\to\\server.py"]
}
}
}

Fully quit and reopen Claude Desktop afterwards.

## Example prompts

1.  "Load my activities from C:\path\to\activities.csv"
2.  "Which weeks had a risky jump in mileage?"
3.  "What was my longest run?"
4.  "Predict my half marathon time"

## Notes

- Expects Strava's column names (Activity Type, Distance, Activity Date, Moving Time).
- Your CSV stays local and is excluded by `.gitignore`.
