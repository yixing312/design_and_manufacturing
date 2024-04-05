def get_data_dict(file_path):
    with open(file_path, "r", encoding="gbk") as f:
        lines = f.readlines()
    header = lines[0].strip()  # Get the first line as the header
    lines = lines[1:]  # Remove the first line
    data = []
    for line in lines:
        values = line.strip().split("\t")
        data.append(dict(zip(header.split("\t"), values)))
    return data


def get_data_list(file_path):
    with open(file_path, "r", encoding="gbk") as f:
        lines = f.readlines()
    lines = lines[1:]  # Remove the first line
    data = []
    for line in lines:
        values = line.strip().split("\t")
        data.append(values)
    return data
