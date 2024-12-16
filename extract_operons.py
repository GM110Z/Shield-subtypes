import pandas as pd
import sys
# Load the tables into pandas DataFrames
table1 = sys.argv[1]
table2 = sys.argv[2]

table1 = pd.read_csv(table1)  # PHORIFIC output
table2 = pd.read_csv(table2)  #Table with Nuccore and Protein ID from Flags/Deltablast/etna 

# Step 1: Add a new column to table1 based on matching nuccore_id and Protein_ID from table2
# Check if each combination of 'nuccore_id' and 'Protein_ID' in table1 exists in table2
table1['Operon'] = table1.apply(lambda row: 'ShdA' if (row['nuccore_id'], row['Protein_ID']) in table2.values else '', axis=1)

# Step 2: Now, group rows by nuccore_id and operon_number, labeling the operons
# We first filter the rows that have 'ShdA' in the 'Operon' column
shda_rows = table1[table1['Operon'] == 'ShdA']

# Create a new list to store results
operon_results = []

# For each ShdA row, find matching rows with the same nuccore_id and operon_number
for _, shda_row in shda_rows.iterrows():
    nuccore_id = shda_row['nuccore_id']
    operon_number = shda_row['operon_number']
    
    # Find other rows with the same nuccore_id and same operon_number
    matching_rows = table1[(table1['nuccore_id'] == nuccore_id) & (table1['operon_number'] == operon_number)]
    
    # Append the matching rows with the 'Operon' column (e.g., 'Operon1', 'Operon2' etc.)
    for idx, row in matching_rows.iterrows():
        operon_label = f"Operon{operon_number}"
        operon_results.append(row.tolist() + [operon_label])

# Create the final DataFrame for operon matches
columns = table1.columns.tolist() + ['Operon Label']
operon_table = pd.DataFrame(operon_results, columns=columns)

# Save the final table to a new CSV file
operon_table.to_csv('operon_results.csv', index=False)

print("Process completed and results saved to 'operon_results.csv'")
