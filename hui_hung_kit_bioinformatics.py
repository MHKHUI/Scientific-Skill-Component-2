# -*- coding: utf-8 -*-
"""HUI Hung Kit Bioinformatics

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1up44DQDmB4NQTcujIO9lGH0-KGtJBHsa

# BMS11603 Scientific Skills Component 1

# Bioinformatics Exercise

### Student name: HUI Hung Kit
### Student ID: 40740267
### Date: 02-12-2024

## Excerise Contents

_1. **Introduction**_

_2.	**Data Cleaning and Quality Control Summary**_

_3.	**Sequence Analysis**_

_4.	**Notebook Organization and Reproducibility**_

_5.	**Reflection**_

## Reference links

[Markdown Preview](https://markdownlivepreview.com/)

[HKUSPACE](https://hkuspace.hku.hk)

[Markdown to PDF Online](https://www.markdowntopdf.com/)

[Bioinformatics, PMID: 11976246](https://pmc.ncbi.nlm.nih.gov/articles/PMC1122955/)

[A brief history of bioinformatics, doi: 10.1093/bib/bby063](https://doi.org/10.1093/bib/bby063)

## 1. **Introduction**

### Overview of bioinformatics data skills and significance.

The definition of _Bioinformatics_ according to A Bayat, 2002 stated this is the application of tools of computation and analysis to capture and interpret the biological data, it integrates the Computer Science and Biological Science, with using mathematics and statistics techniquies to manage and analyze the data obtained from different biological studies.

#### Background

The modern bioinformatics have a big dump after the invention of NGS to generate thousands of data for analysis. As it generates massive data.  However, the Bioinformatics are coming from the 50 years ago (Jeff Gauthier, et al, Volume 20, Issue 6, November 2019, Pages 1981–1996), from the discovery of DNA, invention of Sanger Sequencing and also popularization of computer.  Scientist well use the computer programming to work on the DNA sequence to generate and interpret the data.

#### Skills

Bioinformaticist shall be focusing on the molecular biology to generate the data; the computer scientist to analysis the data; the analyst shall be manulipate the data to suggestion various hypothesis, statistical hypothesis and test the truth or false.

#2. **Data Cleaning and Quality Control Summary**#

*i) Frist of all, we need to install the Library (Biostrings) and run the script.  The installation script shall be obtained from https://bioconductor.org/packages/release/bioc/html/Biostrings.html*
"""

if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("Biostrings")

"""*ii) Then we have to run the Biogenerics package*"""

# @title
library(Biostrings)

"""**##### DATA CLEANING #####**

*iii)	Load the provided SARS-CoV-2 FASTA file (20 sequences, each 29,903 bp) from Github (https://github.com/Koohoko/HKU_Space_Data_handling_bioinformatics_lessons_2024/blob/main/sequence_data/selected_seqs.fasta) into the Colab notebook.*
"""

readDNAStringSet("https://raw.githubusercontent.com/Koohoko/HKU_Space_Data_handling_bioinformatics_lessons_2024/refs/heads/main/sequence_data/selected_seqs.fasta")

"""iv) *Keep sequences with coverage over 85% (counting only A, C, T, and G bases).*

*Manually calculate the proportion of A, C, T, G in the sequences*

*Try to extract one sequence and print it*
"""

seq1 <- seqs[[1]]
print(seq1)
seq1_char <- as.character(seq1)
print(seq1_char)
seq1_char_list <- strsplit(seq1_char, "")
print(seq1_char_list)
seq1_char_table <- table(seq1_char_list)
print(seq1_char_table)

"""*v) Repeat the above steps for all the sequences and run*"""

seqs_char <- lapply(seqs, as.character)
seqs_char_list <- lapply(seqs_char, strsplit, "")
seqs_char_table <- lapply(seqs_char_list, table)
print(seqs_char_table)

"""*vi) Run to calculate the proportion of A, C, T, G in each sequence*"""

seqs_char_table_prop <- lapply(seqs_char_table, function(x) x/sum(x))
print(seqs_char_table_prop)

"""*vii) Then run to calculate the summed proportion of A, C, T, G in all the sequences*"""

seqs_char_table_prop_actg <- lapply(seqs_char_table_prop, function(x) sum(x[names(x) %in% c("A", "C", "T", "G")]))
print(seqs_char_table_prop_actg)
print(seqs_char_table_prop_actg[seqs_char_table_prop_actg<0.85])
print(seqs[seqs_char_table_prop_actg<0.85])

"""*Viii) Using a built-in function to calculate the proportion of A, C, T, G in the sequences*"""

seqs_nt_count <- alphabetFrequency(seqs)
print(seqs_nt_count)
seqs_nt_prop <- seqs_nt_count/rowSums(seqs_nt_count)
print(seqs_nt_prop)

"""*ix) Way 1 to calculate*"""

seqs_nt_prop_actg_1 <- apply(seqs_nt_prop, 1, function(x) sum(x[names(x) %in% c("A", "C", "T", "G")]))
print(seqs_nt_prop_actg_1)

"""*x) Way 2 to calculate*"""

seqs_nt_prop_df <- as.data.frame(seqs_nt_prop)
seqs_nt_prop_actg_2 <- (seqs_nt_prop_df$A + seqs_nt_prop_df$C + seqs_nt_prop_df$T + seqs_nt_prop_df$G)
print(seqs_nt_prop_actg_2)

"""*xi) Then we run to compare the two ways*"""

print(seqs_nt_prop_actg_1 - seqs_nt_prop_actg_2)
(seqs_nt_prop_actg_1 - seqs_nt_prop_actg_2)<0.00000000001

"""*xii) keeping sequences with at least 85% of A, C, T, G*"""

seqs_filtered <- seqs[seqs_nt_prop_actg_1 >= 0.85]
print(seqs_filtered)

"""#*After proceed the above script, Total 17 seqeunces are at least 85% of A, C, G and T.*#

#3. **SEQUENCE ANALYSIS**
############# 1. Calculate GC content for each of two randomly selected sequences.
############# 2. Extract the spike gene region (positions 21,563 to 25,384) for both sequences.
############# 3. Calculate the codon usage for one of the extracted sequences.

*i) Calculate GC content for each of two randomly selected sequences*
"""

set.seed(2024)
seqs_sample <- sample(seqs_filtered, 2)
seqs_sample_nt_count <- alphabetFrequency(seqs_sample)
print(seqs_sample_nt_count)
seqs_sample_nt_count_df <- as.data.frame(seqs_sample_nt_count)
seqs_sample_nt_count_df$length <- rowSums(seqs_sample_nt_count)
seqs_sample_nt_count_df$GC <- seqs_sample_nt_count_df$G + seqs_sample_nt_count_df$C
seqs_sample_nt_count_df$GC_content <- seqs_sample_nt_count_df$GC/seqs_sample_nt_count_df$length

print(names(seqs_sample))
print(seqs_sample_nt_count_df$GC_content)
print(paste0("GC content of sequence ", names(seqs_sample)[1], ": ", seqs_sample_nt_count_df$GC_content[1]))
print(paste0("GC content of sequence ", names(seqs_sample)[2], ": ", seqs_sample_nt_count_df$GC_content[2]))

"""*ii) Extract the spike gene region (positions 21,563 to 25,384) for both sequences*"""

spike_gene <- subseq(seqs_sample, start=21563, end=25384)
print(spike_gene)

"""*iii) Calculate the codon usage for one of the extracted sequences*"""

set.seed(20241107)
spike_gene_selected <- spike_gene[sample(1:2, 1)]
length(spike_gene_selected)
width(spike_gene_selected)

"""#*After run the above script, the codon number for the spike gene from extracted sequence is 3822.*#

#4. **Notebook Organization and Reproducibility**

The Colab notebook is very useful as a platform to run the script to perform many statistical analysis; before has these efficient tools, scientist need to analyse the sequence results manually.  After the popularity of sanger sequencing and NGS afterwards, the manual works may not be possible to handle the hundreds gigabytes data.

The Colab notebook, we shall be able to program the font style and size to welll organize the notebook.  Such as it is separating the Scripts and Text.  Also it is appliable to use the "markdown" language to make the notebook presentable.

In Colab platform, we shall be read the codes and reproduce the scripts so that the we share be sharing our codes and scripts to other partners (coworkers), we shall share the link to other partners, he/she shall read the codes and even copy the scripts for generating the data.

The running scripts shall be using different programming language such as R or Python.  In our project, we are using R language as it shall provide different libraries and tools shall be applied and utilize in our data analysis and visualization.  R language can be interchangeable to Python to replace to use of spreadsheet to handle data.

#5. **Reflection**

Colab notebook links to other platform such as Github for other people to comment and review the codes and scripts.  Github is a repository hosting service providing a web-based graphical interface for interacting between collaborators.

Colab is also user friendly as you just need to plug the script into and it can run the script and “print” the results.  You also don’t need to install the extra program as the project we are working, we just need to install Library (Biostrings) and run the Biogenerics package.  

Finally Colab is developed by Googles and so that you shall save the files in Cloud instead of your local harddisk, you shall open the file and edit anywhere.  Unless you need extra spaces, you could pay to extend the storage size.
"""