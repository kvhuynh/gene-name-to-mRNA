    df = pd.DataFrame.from_dict(data, orient="index", columns=["Sequence", "Length", "GC Content"])

    # Reset index to move gene names into a column
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Gene Name"}, inplace=True)