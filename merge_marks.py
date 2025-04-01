# Merge marks1, marks2, marks3
import sys
from pathlib import Path
import pandas as pd

def entry_to_kerberos(entry_num: str):
    year = entry_num[2:4]
    dept = entry_num[4:7].lower()
    num = entry_num[7:]
    print(f"{entry_num} -> {dept}{year}{num}")
    return f"{dept}{year}{num}"

# Generate comments for hidden_tc1
def gen_comments1(df):
    comment_str = ""
    for col in df.filter(regex="cmds$").columns:
        tmp = str(col) + ": " + df[col].astype(str)
        comment_str += tmp
    comment_str += "total_1: " + df["total"].astype(str) + "\n"
    return comment_str


# Generate comments for hidden_tc1
def gen_comments2(df):
    comment_str = ""
    for col in df.filter(regex="cmds$").columns:
        # cmd: marks | time: 
        tmp = str(col) + ": " + df[col].astype(str) + " | time:" + df[f"{col}_time"].astype(str)
        comment_str += tmp
    comment_str += "total_2: " + df["total"].astype(str) + "\n"
    return comment_str


# Generate comments for hidden_tc1
def gen_comments3(df):
    comment_str = ""
    for col in df.filter(regex="cmds$").columns:
        # cmd: marks
        tmp = str(col) + ": " + df[col].astype(str)
        comment_str += tmp
    comment_str += "total_3: " + df["total"].astype(str) + "\n"
    return comment_str


def main(marks1: Path, marks2: Path, marks3: Path, output_path: Path):
    m1_df = pd.read_csv(marks1)
    m1_df["entry_no"] = m1_df["entry_no"].str.upper()
    m1_df["comments_1"] = gen_comments1(m1_df)
    m1_df = m1_df[["entry_no", "total", "comments_1"]]
    m1_df = m1_df.rename(columns={'total': 'total_1'})

    m2_df = pd.read_csv(marks2)
    m2_df["entry_no"] = m2_df["entry_no"].str.upper()
    m2_df["comments_2"] = gen_comments2(m2_df)
    m2_df = m2_df[["entry_no", "total", "comments_2"]]
    m2_df = m2_df.rename(columns={'total': 'total_2'})

    m3_df = pd.read_csv(marks3)
    m3_df["entry_no"] = m3_df["entry_no"].str.upper()
    m3_df["comments_3"] = gen_comments3(m3_df)
    m3_df = m3_df[["entry_no", "total", "comments_3"]]
    m3_df = m3_df.rename(columns={'total': 'total_3'})

    merged = m1_df.set_index('entry_no').join(m2_df.set_index('entry_no'), on="entry_no", validate="1:1")
    merged = merged.join(m3_df.set_index('entry_no'), on="entry_no")

    merged["total"] = merged["total_1"] + merged[["total_2", "total_3"]].max(axis=1)
    merged["comment"] = merged["comments_1"] + merged["comments_2"] + merged["comments_3"]
    merged.index = merged.index.map(lambda x: entry_to_kerberos(x))  # Square each value
    print(merged["total"].describe())
    print(merged)
    merged.to_csv("/home/baadalvm/final_marks.csv")



if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python marks1.csv marks2.csv marks3.csv merged_marks.csv")
        sys.exit(1)
    
    marks1 = Path(sys.argv[1])
    marks2 = Path(sys.argv[2])
    marks3 = Path(sys.argv[3])
    output_path = Path(sys.argv[4])

    main(marks1, marks2, marks3, output_path)
