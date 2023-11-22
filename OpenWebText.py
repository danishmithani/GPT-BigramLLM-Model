from tqdm import tqdm
import os
import lzma

def xz_files_in_dir(directory):
    files = []       #collecting title of each file.
    for filename in os.listdir(directory):
        if filename.endswith(".xz") and os.path.isfile(os.path.join(directory, filename)):      #to make sure if it ends with right extension and is actually a file itself and not a folder/extention of file.
            files.append(filename)
    return files

folder_path = "D:/fcc-llm-course/openwebtext"  #folder where all 20000 files are kept
output_file_train = "./Output/output_train.txt"            # If you want more than one outputs.
output_file_val = "./Output/output_val.txt" 
vocab_file = "vocab.txt"                # to save corpus of vocab. we steadily build vocab as we go through new files over time
split_files = int(input("How many files would you like to split this into?"))   # No. of output files user wants.

files = xz_files_in_dir(folder_path)

total_files = len(files)

vocab = set()

split_index = int(total_files * 0.85)
files_in_train = files[:split_index]
files_in_val = files[split_index:]

# below we open every output file (after creating it), X no. of input files in it and at the same time add unique new chars from it to vocab list.
#train_data files
for i in range(split_files):
    with open(output_file_train.format(i), "w", encoding='utf-8') as f:
        for each_file in tqdm(files_in_train, total=len(files_in_train)):
            open_file = os.path.join(folder_path, each_file)
            with lzma.open(open_file, "rt", encoding='utf-8') as inFile:
                text = inFile.read()
                f.write(text)
                chars = set(text)
                vocab.update(chars)

#validation_data files
for i in range(split_files):
    with open(output_file_val.format(i), "w", encoding='utf-8') as f:
        for each_file in tqdm(files_in_val, total=len(files_in_val)):
            open_file = os.path.join(folder_path, each_file)
            with lzma.open(open_file, "rt", encoding='utf-8') as inFile:
                text = inFile.read()
                f.write(text)
                chars = set(text)
                vocab.update(chars)



with open(vocab_file, 'w', encoding = 'utf-8') as vFile:
    for char in vocab:
        vFile.write(char + '\n')