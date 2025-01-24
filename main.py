import pandas as pd;
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

def get_transcript_id(gene_name):
    handle = Entrez.esearch(db="nucleotide", retmax=10, term=gene_name, idtype="acc");
    record = Entrez.read(handle);
    mRNA_accession = ""
    for entry in record["IdList"]:
        if entry.startswith("XM_"):
            mRNA_accession = entry
    return mRNA_accession;


def get_transcript_sequence(mRNA_transcript_id):
    handle = Entrez.efetch(db="nucleotide", id=mRNA_transcript_id, rettype="fasta")
    for r in SeqIO.parse(handle, "fasta"):
        return [r.seq, len(r.seq), gc_fraction(r.seq)*100];

# def get_transcript_length(transc)


def write_out(map):
    df = pd.DataFrame.from_dict(map, orient="index", columns=["Sequence", "Length", "GC Content"])

    # Reset index to move gene names into a column
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Gene Name"}, inplace=True)
    df.to_excel("./Type 2 mRNA List(_2.5).csv edited.xlsx", index=False)

def main():
    df = read_excel("./Type 2 mRNA List(_2.5).csv");
    gene_ids = get_gene_ids(df);
    gene_to_transcript = {};
    count = 0;
    for gene_name in gene_ids:
        mRNA_transcript_id = get_transcript_id(gene_name);
        transcript = get_transcript_sequence(mRNA_transcript_id);
        gene_to_transcript[gene_name] = transcript
        count += 1;
        print(count);
    print(gene_to_transcript)
    write_out(gene_to_transcript)
    print("done")

main();
