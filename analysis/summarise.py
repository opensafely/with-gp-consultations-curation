from pathlib import Path
from glob import glob
import pandas as pd

# totalise measure tables
for f in glob("output/measure_gp_consultations_by_*[a-z].csv"):
    demographic = Path(f).stem.replace("measure_gp_consultations_by_", "")
    df = pd.read_csv(f)
    f_out = Path(f.replace(demographic, f"{demographic}_total"))
    f_out = Path(f_out.parts[0], "tables", f_out.parts[1])
    df.groupby(demographic)[["gp_consultation_count", "population"]].sum().to_csv(f_out)

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

dfg.to_csv("output/tables/overall_summary.csv")
