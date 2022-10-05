from pathlib import Path
from glob import glob
import pandas as pd

# totalise measure tables
for f in set(glob("output/measure_gp_consultations_by_*.csv")) - set(
    glob("output/*_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv")
):
    demographic = Path(f).stem.replace("measure_gp_consultations_by_", "")
    df = pd.read_csv(f)
    df.groupby(demographic)[["gp_consultation_count", "population"]].sum().to_csv(
        f.replace(demographic, f"{demographic}_total")
    )

# overall summary statistics
df = pd.read_csv("output/measure_gp_consultations.csv")

dfg = df.groupby("date")[["gp_consultation_count", "population"]].agg(
    ["sum", "describe"]
)

dfg.columns = [
    f"{c[0]}_sum"
    if c[1] in ["gp_consultation_count", "population"]
    else f"{c[0]}_{c[1]}"
    for c in zip(dfg.columns.get_level_values(0), dfg.columns.get_level_values(2))
]

dfg.to_csv("output/overall_summary.csv")
