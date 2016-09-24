import sys, zipfile
if len(sys.argv) < 2:
    print ("Usage: python app.py <path_to_zipfile>")
    exit()

# We are going to store the code in a dict, using the filename as index
code = {}

# We are going to store the dependencies and usages in lists, in dictionaries, using the filename as index
dependencies = {}
usages = {}

# The names to look for (filename lowercase minus .ado) are stored in a list
magic_words = []

# A nice linecount variable, for the statistics
linecount = 0

# Unzip and fill code & magic_words
with zipfile.ZipFile(sys.argv[1],"r") as zip_ref:
    file_list = zip_ref.infolist()
    for i in file_list:
        if i.filename.lower().endswith(".ado"):
            magic_words.append(i.filename.lower()[:-4])
            ado_file = zip_ref.open(i.filename)
            code[i.filename] =  ado_file.readlines()
            linecount += len(code[i.filename])

            # For each file, print the number of lines
            #print(i.filename + ":" + len(code[i.filename]))

# Print some statistics
print("\nTotal files: " + str(len(code.keys())))
print("Total lines: " + str(linecount))

# Print all the magic words we are going to find
#print(magic_words)

# For each file, check the magic words
for ado_file in code.keys():
    for ado_line in code[ado_file]:
        ado_words = ado_line.strip().split()
        for ado_word in ado_words:
            try:
                ado_word_s = ado_word.decode(encoding='UTF-8')
                if ado_word_s.lower() in magic_words and ado_word_s.lower() != ado_file.lower()[:-4]:
                    #print("Found word: " + ado_word_s + " in file " + ado_file)

                    # Save dependencies
                    current_dependencies = []
                    if ado_file in dependencies.keys():
                        current_dependencies = dependencies[ado_file]

                    if ado_word_s not in current_dependencies:
                        current_dependencies.append(ado_word_s)
                        dependencies[ado_file] = current_dependencies

                    # Save usages
                    current_usages = []
                    if ado_word_s in usages.keys():
                        current_usages = usages[ado_word_s]
                    
                    if ado_file not in current_usages:
                        current_usages.append(ado_file)
                        usages[ado_word_s] = current_usages
            except:
                # Always due to some silly accent chars in the source file
                #print("Found a crazy char: " + str(ado_word) + " in file " + ado_file)
                pass

# Print the dependencies and usages + save them to file 'output.txt'
with open('output.txt', 'w') as file_out:
    for ado_file in dependencies.keys():
        #print("Dependencies for " + ado_file + ":")
        file_out.write("Dependencies for " + ado_file + ":" + "\n")
        for dep_word in dependencies[ado_file]:
            #print("\t" + str(dep_word))
            file_out.write("\t" + str(dep_word)+"\n")

    for ado_word in usages.keys():
        #print("Usages of " + ado_word + ":")
        file_out.write("Usages of " + ado_word + ":" + "\n")
        for used_file in usages[ado_word]:
            #print("\t" + str(used_file))
            file_out.write("\t" + str(used_file)+"\n")