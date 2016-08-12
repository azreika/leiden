import re

input_gene = "DYSF"

gene_vep_file = open("../dat/" + input_gene + ".vep.txt")
lines = [line.rstrip('\n').split('\t') for line in gene_vep_file]
gene_vep_file.close()

i = 0
while lines[i][0][0]=='#':
    i+=1

col_names = lines[i-1]
col_names[0] = col_names[0][1:]
rows = lines[i:]
#print col_names
extra_index = col_names.index("Extra")

output_file = open("../dat/" + input_gene + "_final_output.txt", "w")
concise_file = open("../dat/" + input_gene + "_concise_output.txt", "w")
var_name_ind = col_names.index("Uploaded_variation")
location_ind = col_names.index("Location")
conseq_ind = col_names.index("Consequence")

first_row_out = ("%s\t%s\t%s\t%s\n")%("Uploaded_variation", "Location", "Consequence", "Allele_frequency")

concise_file.write(first_row_out)
output_file.write(first_row_out)

for line in rows:
    extra_data = line[col_names.index("Extra")].split(';')
    freq_data = next((x.split('=')[1] for x in extra_data if "ExAC_Adj_MAF=" in x), None)

    add_to_concise = True
    #get the actual change from freq_data - TODO: CHECK THIS WITH HIMANSHU
    var_name = line[var_name_ind]
    if '>' in var_name and freq_data:
        tmp_freq_data = freq_data.replace(',', ':')
        new_base = var_name[-1]
        res_list = tmp_freq_data.split(':')
        try:
            main_ind = res_list.index(new_base)
            freq_data = "%.9f"%(float(res_list[main_ind+1]))
        except:
            freq_data = "No relevant ExAC data"
            add_to_concise = False

    #print line[var_name_ind], line[location_ind], line[conseq_ind], freq_data
    if freq_data == None:
        freq_data = "No ExAC data for variant"
        add_to_concise = False

    row_to_add = ("%s\t%s\t%s\t%s\n")%(line[var_name_ind], line[location_ind], line[conseq_ind], freq_data)
    output_file.write(row_to_add)
    if add_to_concise:
        concise_file.write(row_to_add)
    #output_file.write("%s\t%s\t%s\t%s\t%s\t%s

output_file.close()
concise_file.close()
