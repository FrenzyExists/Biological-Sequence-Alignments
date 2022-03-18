import sys
import csv
import os

def load_data():
    if len(sys.argv) <= 1:
        print("""
Usage: wush [FILE]... [PARAMS]
Compares two sequences. this help print appears when no file is specified

Optional parameters.
[match score number] [mismatch score number] [gap score] 
        """)
        exit()
    try:
        file = open(sys.argv[1], 'r')
        data = csv.reader(file)
    except:
        print("invalid path or file")
        exit()
    return data

def score(n1, n2):
    if n1 == n2:
        return match_score
    else:
        return mismatch_score

def needleman_wunsch(a: str, b: str, d):
    len_a, len_b = len(a), len(b)

    F = [[0 for j in range(len_b+1)] for i in range(len_a+1)]

    for i in range(0, len_a + 1):
        F[i][0] = d * i
    for j in range(0, len_b + 1):
        F[0][j] = d * j

    for i in range(1, len_a + 1):
        for j in range(1, len_b+1):
            F[i][j] = max(
                F[i - 1][j - 1] + score(a[i - 1], b[j - 1]),
                F[i][j - 1] + d,
                F[i - 1][j] + d,
            )

    alignment_a, alignment_b = "", ""

    while len_a > 0 or len_b > 0:
    
        if len_a > 0 and len_b > 0 and F[len_a][len_b] == F[len_a-1][len_b-1] + score(a[len_a-1], b[len_b-1]):
            alignment_a = a[len_a-1] + alignment_a
            alignment_b = b[len_b-1] + alignment_b
            len_a -= 1
            len_b -= 1
        elif len_a > 0 and F[len_a][len_b] == F[len_a - 1][len_b] + d:
            alignment_a = a[len_a-1] + alignment_a
            alignment_b = "-" + alignment_b
            len_a -= 1
        else:
            alignment_a = "-" + alignment_a
            alignment_b = b[len_b-1] + alignment_b
            len_b -= 1
    
    return ["".join(i for i in [alignment_a, " ", alignment_b]), F[-1][-1]]

if __name__ == "__main__":
    data = load_data()
    
    try:
        output = sys.argv[2]
    except:
        os.makedirs('./output', exist_ok=True)
        output = './output/results.csv'

    try:
        match_score = int(sys.argv[3])
    except:
        match_score = 1

    try:
        mismatch_score = int(sys.argv[4])
    except:
        mismatch_score = -1
    
    try:
        gap_penalty = int(sys.argv[5])
    except:
        gap_penalty = -2
        
    with open (output, 'w', newline='') as output_csv:
        out = csv.writer(output_csv, delimiter=",")        
        m = next(data) + ['alignment_text', 'score']
        out.writerow(m)

        for row in data:
            row += needleman_wunsch(row[0], row[1], gap_penalty)
            out.writerow(row)
        output_csv.close()
