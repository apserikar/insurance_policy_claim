files_processed = {}

def write_json(file_name, output):

    write_header = False
    data = [str(x) for x in output.values()]
    
    if file_name not in files_processed:
        write_header = True
        files_processed[file_name] = True
        hdr = [x for x in output.keys()]
    
    if write_header:
        write_file_header(file_name, hdr)
        write_file_data(file_name, data)
    else:
        write_file_data(file_name, data)

def write_file_header(file_name, data):
    data_out = ",".join(data)
    with open(file_name, "w") as f:
        f.write(data_out + "\n")

def write_file_data(file_name, data):
    data_out = ",".join(data)
    with open(file_name, "a") as f:
        f.write(data_out + "\n")


