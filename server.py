from mcp.server.mcpserver import MCPServer
import pandas as pd
mcp = MCPServer("expense-budget")

df = None

@mcp.tool()
def load_activities(csv_path: str) -> str:
    """ Reads the csv file"""
    global df
    df = pd.read_csv(csv_path)
    return f"Loaded {len(df)} rows"

@mcp.tool()
def get_column_names():
    """ Gets Column names"""
    return list(df.columns)

@mcp.tool()
def total_run_distance() -> float:
    runs= df[df['Activity Type'] == 'Run']
    total = runs['Distance'].sum()
    return float(total)

@mcp.tool()
def weekly_distance() -> dict:
    """Total run distance per week."""
    runs = df[df["Activity Type"] == "Run"].copy()
    runs["Activity Date"] = pd.to_datetime(runs["Activity Date"])
    weekly = runs.groupby(pd.Grouper(key="Activity Date", freq="W"))["Distance"].sum()
    return {str(week.date()): float(km) for week, km in weekly.items()}

@mcp.tool()
def longest_run() -> dict:
    runs = df[df["Activity Type"] == "Run"].copy()
    index = runs['Distance'].idxmax()
    row =  runs.loc[index]
    return {"date": str(row["Activity Date"]), "distance": float(row["Distance"])}

@mcp.tool()
def injury_risk():
    """Flag weeks where run distance exceeded the prior 4-week average by more than 30%."""
    runs = df[df["Activity Type"] == "Run"].copy()
    runs["Activity Date"] = pd.to_datetime(runs["Activity Date"])
    weekly = runs.groupby(pd.Grouper(key="Activity Date", freq="W"))["Distance"].sum()
    baseline = weekly.rolling(4).mean().shift(1)
    flagged = weekly[(weekly > baseline * 1.3) & (baseline > 5)]
    return {str(d.date()): float(km) for d, km in flagged.items()}

@mcp.tool()
def predict_race_time(distance_km: float):
    """Predict race time (minutes) for a target distance in km.
Uses the Riegel formula on your fastest run of 5 km or more.""" 
    runs = df[(df['Activity Type'] == 'Run') & (df['Distance'] >= 5)]
    pace = runs['Moving Time'] / runs['Distance']
    best = runs.loc[pace.idxmin()]
    new_time = best['Moving Time'] * (distance_km/best['Distance']) ** 1.06
    return float(new_time/60)




    

    


@mcp.tool()
def pong():
    """Reply with pong to check the server is alive."""
    return "pong"

if __name__ == "__main__":
    mcp.run()


