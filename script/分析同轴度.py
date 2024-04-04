import pandas as pd


def get_data(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    header = lines[0].strip()  # Get the first line as the header
    lines = lines[1:]  # Remove the first line
    data = []
    for line in lines:
        values = line.strip().split("\t")
        data.append(dict(zip(header.split("\t"), values)))
    csv_file_path = file_path.replace(".txt", ".csv")
    data = pd.DataFrame(data)
    data.to_csv(csv_file_path, index=False)
