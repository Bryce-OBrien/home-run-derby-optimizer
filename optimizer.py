import pandas as pd
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpBinary, LpStatus


def optimize_balanced(df, budget_cap=163, team_size=8):
    """
    Balanced optimizer: maximize total HRs of all 8 selected players.
    """
    prob = LpProblem("HRD_Balanced", LpMaximize)

    x_vars = {row['player_name']: LpVariable(f"select_{row['player_name']}", cat=LpBinary)
              for _, row in df.iterrows()}

    prob += lpSum(x_vars[name] * df.loc[df['player_name'] == name, 'hr_projection'].values[0] for name in x_vars)
    prob += lpSum(x_vars[name] * df.loc[df['player_name'] == name, 'cost_to_draft'].values[0] for name in x_vars) <= budget_cap
    prob += lpSum(x_vars[name] for name in x_vars) == team_size

    prob.solve()

    selected = [name for name in x_vars if x_vars[name].varValue == 1]
    df_team = df[df['player_name'].isin(selected)].copy()
    df_team = df_team.sort_values(by='hr_projection', ascending=False).reset_index(drop=True)

    total_cost = df_team['cost_to_draft'].sum()
    total_hr_projection = df_team['hr_projection'].sum()

    return df_team, total_cost, total_hr_projection, LpStatus[prob.status]


def optimize_top_7(df, budget_cap=163, team_size=8, top_k=7):
    """
    Top-heavy optimizer: only the top 7 HRs among the 8 selected players count.
    """
    prob = LpProblem("HRD_Top_7_of_8", LpMaximize)

    x_vars = {row['player_name']: LpVariable(f"select_{row['player_name']}", cat=LpBinary)
              for _, row in df.iterrows()}
    y_vars = {row['player_name']: LpVariable(f"count_{row['player_name']}", cat=LpBinary)
              for _, row in df.iterrows()}

    prob += lpSum(y_vars[name] * df.loc[df['player_name'] == name, 'hr_projection'].values[0] for name in y_vars)
    prob += lpSum(x_vars[name] * df.loc[df['player_name'] == name, 'cost_to_draft'].values[0] for name in x_vars) <= budget_cap
    prob += lpSum(x_vars[name] for name in x_vars) == team_size
    prob += lpSum(y_vars[name] for name in y_vars) == top_k

    for name in x_vars:
        prob += y_vars[name] <= x_vars[name]

    prob.solve()

    selected = [name for name in x_vars if x_vars[name].varValue == 1]
    df_team = df[df['player_name'].isin(selected)].copy()
    df_team = df_team.sort_values(by='hr_projection', ascending=False).reset_index(drop=True)

    total_cost = df_team['cost_to_draft'].sum()
    top_hr_total = sum(
        df.loc[df['player_name'] == name, 'hr_projection'].values[0]
        for name in y_vars if y_vars[name].varValue == 1
    )

    return df_team, total_cost, top_hr_total, LpStatus[prob.status]
