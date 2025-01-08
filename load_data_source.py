def LoadDataSource(filepath):
    with open(filepath,'r') as file:
        data=file.readlines()

    urls=[]
    for line in data:
        line=line.strip()
        line=line[1:-2]
        urls.append(line)

    return urls