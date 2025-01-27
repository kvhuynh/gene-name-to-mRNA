import pandas as pd;
import requests;
from Bio import Entrez, SeqIO;
from Bio.SeqUtils import gc_fraction
Entrez.email = "kvhuynh@uw.edu";

def read_excel(path):
    df = pd.read_csv(path, usecols=["Gene_ID"])
    return df;

def get_gene_ids(df):
    gene_list = []
    for gene_id in df.Gene_ID:
        gene_list.append(gene_id);
    return gene_list;

def get_flanking_regions(gene_name):
    print(gene_name)
    r = requests.get(f"https://protists.ensembl.org/Acanthamoeba_castellanii_str_neff_gca_000313135/Export/Output/Gene?db=core;flank3_display=200;flank5_display=200;g={gene_name};output=fasta;r=KB008066:138-1560;strand=feature;t=ELR14198;param=utr5;param=utr3;genomic=5_3_flanking;_format=Text");
    r = r.text;
    # Normalize line endings to "\n"
    r = r.replace("\r\n", "\n").replace("\r", "\n")
    
    # Split the input string into lines
    lines = r.strip().split("\n")
    
    # Initialize variables
    # parsed_data = []

    parsed_data = {};
    sequences = []
    current_sequence = []
    
    # parsed_data[gene_name] = []
    # Loop through each line
    for line in lines:
        if line.startswith(">"):  # If it's a header, skip it
            if current_sequence:
                sequences.append("".join(current_sequence).replace("N", ""))
                current_sequence = []  # Reset sequence for the next one
        else:  # It's a sequence line
            current_sequence.append(line.strip())
    
    # Add the last sequence
    if current_sequence:
        sequences.append("".join(current_sequence))
    return sequences;
    
def main():
    df = read_excel("./Type 2 mRNA List(_2.5).csv");
    gene_ids = get_gene_ids(df);
    flanking_bases = {};
    count = 0;
    # parsed_data = get_flanking_regions("ACA1_095890");
    # Print the cleaned output
    for gene_name in gene_ids:
        flanking_bases[gene_name] = get_flanking_regions(gene_name);

        # print(flanking_bases);
    # write_out(gene_to_transcript)
    data = [{"gene_name": gene, "upstream": values[0], "downstream": values[1]} for gene, values in flanking_bases.items()];
    # Create a DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to an Excel file
    output_file = "gene_sequences.xlsx"
    df.to_excel(output_file, index=False)
main();