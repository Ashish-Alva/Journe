import pandas as pd

# ============================================
# READ EXCEL FILE
# ============================================
file_path = "Book1.xlsx"

# Read without headers
df = pd.read_excel(file_path, header=None)

# ============================================
# GET COUNTRY ROW & FILL EMPTY VALUES
# ============================================
country_row = df.iloc[0].fillna(method='ffill')

# Get date row
date_row = df.iloc[1]

# ============================================
# CREATE COLUMN NAMES
# ============================================
new_columns = ["MEASURE"]

for i in range(1, len(df.columns)):

    country = str(country_row[i]).strip()

    # Convert date
    date_value = pd.to_datetime(date_row[i])

    # Month name
    month = date_value.strftime("%b").upper()

    # Short country name
    short_country = country[:3].upper()

    # Example: IND_JAN
    col_name = f"{short_country}_{month}"

    new_columns.append(col_name)

# ============================================
# REMOVE FIRST 2 ROWS
# ============================================
data = df.iloc[2:].reset_index(drop=True)

# Keep only required columns
data = data.iloc[:, :len(new_columns)]

# Assign new columns
data.columns = new_columns

# ============================================
# CREATE FINAL OUTPUT
# ============================================
final_output = []

for _, row in data.iterrows():

    measure = row["MEASURE"]

    for col in data.columns[1:]:

        country, month = col.split("_")

        value = row[col]

        if pd.isna(value):
            continue

        final_output.append({
            "MEASURE": measure,
            "COUNTRY": country,
            "MONTH": month,
            "VALUE": value
        })

# ============================================
# FINAL DATAFRAME
# ============================================
final_df = pd.DataFrame(final_output)

# ============================================
# PRINT OUTPUT
# ============================================
print(final_df)

# ============================================
# SAVE OUTPUT
# ============================================
final_df.to_excel("output.xlsx", index=False)

print("\nOutput saved as output.xlsx")