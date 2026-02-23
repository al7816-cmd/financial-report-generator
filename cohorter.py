import pandas as pd
import numpy as np
import openpyxl

df = pd.read_excel('Phia Financial Model vf January.xlsx', header=4)
months = ['2025-04-01','2025-05-01','2025-06-01','2025-07-01','2025-08-01','2025-09-01','2025-10-01','2025-11-01','2025-12-01','2026-01-01']
heartbeat_cohorted = pd.DataFrame(index = months, columns = ['cohort_size','month_0','month_1','month_2','month_3','month_4','month_5','month_6','month_7','month_8','month_9'])
df.columns = df.columns.map(lambda x: x.strftime("%Y-%m-%d") if hasattr(x, "strftime") else str(x))

if __name__ == '__main__':
    for month in months:
        heartbeat_cohorted.loc[month, 'cohort_size'] = df[df['Unnamed: 1'] == 'New Successful Onboarding Users (Heartbeat)'][month].iloc[0]
        heartbeat_cohorted['month_0'] = heartbeat_cohorted['cohort_size']
    heartbeat_cohorted.to_excel('heartbeat_cohorted_output.xlsx')