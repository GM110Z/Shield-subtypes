import os
import pandas as pd
import requests
import subprocess
import sys

def fetch_sequences(wp_ids, output_file):
    """Fetch FASTA sequences for a list of WP IDs and save to a file."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "protein",
        "rettype": "fasta",
        "id": ",".join(wp_ids),
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        with open(output_file, "w") as f:
            f.write(response.text)
    else:
        raise Exception(f"Failed to fetch sequences. HTTP status: {response.status_code}")

def find_dominant_protein(fasta_file, keyword):
    """Identify a protein in the FASTA file with the given keyword in its header."""
    dominant_protein = None
    with open(fasta_file, "r") as f:
        for line in f:
            if line.startswith(">") and keyword in line:
                dominant_protein = line.split()[0][1:]  # Extract protein ID from header
                break
    if not dominant_protein:
        raise Exception(f"No protein with keyword '{keyword}' found in {fasta_file}.")
    return dominant_protein

def run_cblaster(input_fasta, output_dir, comment, dominant_protein):
    """Run cblaster with the given input FASTA and save results to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{comment}_cblaster_results.json")
    cblaster_cmd = [
        "cblaster",
        "search",
        "-q", input_fasta,
        "-o", output_file,
        "-mi", "20",
        "-mc", "20",
        "-mh", "3",
        "-g", "70",
        "-r", dominant_protein
    ]
    subprocess.run(cblaster_cmd, check=True)

def main():
    # Load the table into a Pandas DataFrame
    table_file = sys.argv[1] # Replace with your table file path
    df = pd.read_csv(table_file, sep="\t")

    # Group by `nuccore_id` and `Comment`
    grouped = df.groupby(["nuccore_id", "Comment"])

    for (nuccore_id, comment), group in grouped:
        if pd.isna(comment):
            continue  # Skip rows with no comment

        # Get WP IDs from the group
        wp_ids = group["Protein_ID"].tolist()

        # Define file paths
        fasta_file = f"{nuccore_id}_{comment}_sequences.fasta"
        output_dir = comment.replace(" ", "_")

        # Ensure clean slate for each operon
        if os.path.exists(fasta_file):
            os.remove(fasta_file)

        # Fetch FASTA sequences
        print(f"Fetching sequences for WP IDs: {wp_ids}")
        fetch_sequences(wp_ids, fasta_file)

        # Find the dominant protein with the keyword "DUF2130"
        print(f"Searching for dominant protein with keyword 'DUF2130' in {fasta_file}")
        try:
            dominant_protein = find_dominant_protein(fasta_file, "DUF2130")
            print(f"Dominant protein found: {dominant_protein}")
        except Exception as e:
            print(f"Error finding dominant protein: {e}")
            continue  # Skip to the next operon

        # Run cblaster
        print(f"Running cblaster for comment: {comment}")
        try:
            run_cblaster(fasta_file, output_dir, comment, dominant_protein)
        except subprocess.CalledProcessError as e:
            print(f"Error running cblaster: {e}")
            continue  # Skip to the next operon

        # Clean up FASTA file after processing
        if os.path.exists(fasta_file):
            os.remove(fasta_file)

        print(f"Completed processing for operon: {comment}\n")

if __name__ == "__main__":
    main()
