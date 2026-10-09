
import pandas as pd

# Load CSV file
df = pd.read_csv("dataset.csv")

# Delete rows containing 3 or more "-" values
df = df[df.eq("-").sum(axis=1) < 3]

# Save cleaned dataset
df.to_csv("cleaned_dataset.csv", index=False)

print("Cleaning completed!")
print("Remaining rows:", len(df))
print("Saved to cleaned_dataset.csv")