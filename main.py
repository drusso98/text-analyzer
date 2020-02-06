import functions
import tkinter as tk
from tkinter import filedialog
from tabulate import tabulate

print("choose the text you want to analize:\n")
#opening file dialog and saving file's path
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

#opening the selected file
file = open(file_path)
text = file.read()
file.close()

# create a .doc file where to save the report of the analysis
print("write the name of the file in which you want to save the report:\n")
name = input()
name = name+".txt"
report = open(name, "w")

print("writing the report...\n")
report.write("ANALYSIS REPORT\n")
report.write("_______________\n")
report.write("\n")
report.write("file path chosen: " + file_path + "\n")
report.write("\n")
report.write("number of sentences: {}\n" .format(functions.sentence_count(text)))
report.write("number of words: {}\n" .format(functions.word_count(text)))
report.write("number of characters(no spaces): {}\n" .format(functions.char_count_nospace(text)))
report.write("\n")

report.write("most common words distribution:\n\n\t")
commonw = functions.words_distribution(text)
report.write('\n\t'.join('{} {}'.format(x[0],x[1]) for x in commonw))

report.write("\n\n")

report.write("most common words' length distribution:\n\n\t")
commonwl = functions.words_length_distribution(text)
report.write('\n\t'.join('{} {}'.format(x[0],x[1]) for x in commonwl))

report.write("\n\n")

report.write("deviation standard: {}\n" .format(functions.standard_dev(text)))
report.write("lexical density: {}\n\n" .format(functions.lexical_density(text)))

report.write("Automated Readability Index (ARI): {}\n" .format(functions.ARI(text)))

report.write("\ncompare the score to the following guide.\n\n")

report.write(tabulate([["SCORE","AGE","GRADE LEVEL"],
                       ["1","5-6","Kindergarten"],
                       ["2","6-7","First/Second Grade"],
                       ["3","7-9","Third Grade"],
                       ["4","9-10","Fourth Grade"],
                       ["5","10-11","Fifth Grade"],
                       ["6","11-12","Sixth Grade"],
                       ["7","12-13","Seventh Grade"],
                       ["8", "13-14","Eighth Grade"],
                       ["9", "14-15","Ninth Grade"],
                       ["10", "15-16","Tenth Grade"],
                       ["11", "16-17","Eleventh Grade"],
                       ["12", "17-18","Twelfth grade"],
                       ["13", "18-24","College student"],
                       ["14", "24++","Professor"]
                       ], headers="firstrow", tablefmt="psql"))

report.write("\n\nEND.")
report.close()
