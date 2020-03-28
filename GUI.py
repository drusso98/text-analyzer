import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Combobox
from tabulate import tabulate
import functions

window = tk.Tk()
window.geometry("800x800")
window.title("Text Analyzer")
window.grid_columnconfigure(0, weight=1)


def print_report(name, text):
    # create a .doc file where to save the report of the analysis
    name = name + ".txt"
    report = open(name, "w")
    print("writing the report...\n")
    report.write("ANALYSIS REPORT\n")
    report.write("_______________\n")
    report.write("\n")
    report.write("number of sentences: {}\n".format(functions.sentence_count(text)))
    report.write("number of words: {}\n".format(functions.word_count(text)))
    report.write("number of characters(no spaces): {}\n".format(functions.char_count_nospace(text)))
    report.write("\n")

    report.write("most common words distribution:\n\n\t")
    commonw = functions.words_distribution(text)
    report.write('\n\t'.join('{} {}'.format(x[0], x[1]) for x in commonw))

    report.write("\n\n")

    report.write("most common words' length distribution:\n\n\t")
    commonwl = functions.words_length_distribution(text)
    report.write('\n\t'.join('{} {}'.format(x[0], x[1]) for x in commonwl))

    report.write("\n\n")

    report.write("deviation standard: {}\n".format(functions.standard_dev(text)))
    report.write("lexical density: {}\n\n".format(functions.lexical_density(text)))

    report.write("Automated Readability Index (ARI): {}\n".format(functions.ARI(text)))

    report.write("\ncompare the score to the following guide.\n\n")

    report.write(tabulate([["SCORE", "AGE", "GRADE LEVEL"],
                           ["1", "5-6", "Kindergarten"],
                           ["2", "6-7", "First/Second Grade"],
                           ["3", "7-9", "Third Grade"],
                           ["4", "9-10", "Fourth Grade"],
                           ["5", "10-11", "Fifth Grade"],
                           ["6", "11-12", "Sixth Grade"],
                           ["7", "12-13", "Seventh Grade"],
                           ["8", "13-14", "Eighth Grade"],
                           ["9", "14-15", "Ninth Grade"],
                           ["10", "15-16", "Tenth Grade"],
                           ["11", "16-17", "Eleventh Grade"],
                           ["12", "17-18", "Twelfth grade"],
                           ["13", "18-24", "College student"],
                           ["14", "24++", "Professor"]
                           ], headers="firstrow", tablefmt="psql"))

    report.write("\n\nEND.")
    report.close()


def open_file():
    # opening file dialog and saving file's path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # opening the selected file
    file = open(file_path)
    text = file.read()
    file.close()
    textWidget.insert(1.0, text)
    return text


welcome_label = tk.Label(window,
                         text="Upload and analyze your english text: ",
                         font=("Helvetica", 15))
welcome_label.grid(row=0, column=0)

upload_btn = tk.Button(text="upload", command=open_file)
upload_btn.grid(row=2, column=0, pady=10)

textWidget = tk.Text()
textWidget.grid(row=3, column=0, padx=10)

v = ["tokenization", "tokenization (stop words)", "stemming", "lemmatisation", "counter", "words length distribution", "words distribution", "POS tagging", "lexical density", "ARI"]
combo = Combobox(window, values=v)


def callback(eventObject):
    print(combo.get())
    if combo.get() == 'tokenization':
        option_label = tk.Label(window, text=combo.get(),  font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.token(textWidget.get(1.0,tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=10)
        display.insert(tk.END, 'DESCRIPTION: Tokenization is the process of breaking down text document apart in Tokens.\n\n')
        for x in output:
            display.insert(tk.END, '- ' + x + '\n')

    elif combo.get() == 'tokenization (stop words)':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.del_stopwords(textWidget.get(1.0, tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=10)
        display.insert(tk.END, 'DESCRIPTION: Tokenization is the process of breaking down text document apart in Tokens. '
                               'Stop words - usually the most common words in a language - are filtered out before or after processing of a text.\n\n')
        for x in output:
            display.insert(tk.END, '- ' + x + '\n')

    elif combo.get() == 'stemming':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.stemming(textWidget.get(1.0, tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=10)
        display.insert(tk.END, 'DESCRIPTION: Stemming redunces inflected words to their word stem, base or root form.\n\n')
        for x in output:
            display.insert(tk.END, '- ' + x + '\n')

    elif combo.get() == 'lemmatisation':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.lemmas(textWidget.get(1.0, tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=10)
        display.insert(tk.END, 'DESCRIPTION: Lemmatisation is the algorithmic process of determining the lemma of a word based on its intended meaning.\n\n')
        for x in output:
            display.insert(tk.END, '- ' + x + '\n')

    elif combo.get() == 'counter':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        words = functions.word_count(textWidget.get(1.0, tk.END))
        sentences = functions.sentence_count(textWidget.get(1.0, tk.END))
        ch_count = functions.char_count_spaces(textWidget.get(1.0, tk.END))
        ch_count_nsp = functions.char_count_nospace(textWidget.get(1.0, tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=10)
        display.insert(tk.END, 'Number of words: ' + str(words) + '\n')
        display.insert(tk.END, 'Number of sentences: ' + str(sentences) + '\n')
        display.insert(tk.END, 'Number of characters (spaces included): ' + str(ch_count) + '\n')
        display.insert(tk.END, 'Number of characters (spaces excluded): ' + str(ch_count_nsp) + '\n')

    elif combo.get() == 'words length distribution':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.words_length_distribution(textWidget.get(1.0, tk.END))
        media = functions.arithmetic_mean(textWidget.get(1.0, tk.END))
        dev_standard = functions.standard_dev(textWidget.get(1.0, tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=2)
        display.insert(tk.END, 'most common 10:\n')
        for x in output:
            display.insert(tk.END, '- ' + str(x[0]) + ':' + str(x[1]) + '\n')
        display.insert(tk.END, 'arithmetic mean : ' + str(media) + '\n')
        display.insert(tk.END, 'standard deviation : ' + str(dev_standard))

    elif combo.get() == 'words distribution':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.words_distribution(textWidget.get(1.0, tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=2)
        display.insert(tk.END, 'most common 10:\n')
        for x in output:
            display.insert(tk.END, '- ' + str(x[0]) + ':' + str(x[1]) + '\n')

    elif combo.get() == 'POS tagging':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.pos_tagging(textWidget.get(1.0, tk.END))
        print(output)
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=10)
        display.insert(tk.END, 'DESCRIPTION: Part-of-speech tagging is the process of marking up a word in a text (corpus) as corresponding to a particular part of speech.\n\n')
        for x in output:
            display.insert(tk.END, '- ' + str(x[0]) + ':' + str(x[1]) + '\n')

    elif combo.get() == 'lexical density':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.lexical_density(textWidget.get(1.0, tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=10)
        display.insert(tk.END, 'DESCRIPTION: Lexical density estimates the linguistic complexity in a written or spoken composition from the functional words (grammatical units) and content words (lexical units, lexemes).\n\n')
        display.insert(tk.END, 'Lexical density is: ' + str(output) + '\n')

    elif combo.get() == 'ARI':
        option_label = tk.Label(window, text=combo.get(), font=("Helvetica", 12))
        option_label.grid(row=5, column=0)
        output = functions.ARI(textWidget.get(1.0, tk.END))
        display = tk.Text(window, width=80, height=10)
        display.grid(row=6, column=0, padx=10)
        display.insert(tk.END, 'DESCRIPTION: The Automated Readability Index (ARI) is a readability test for English texts, designed to gauge the understandability of a text.\n\n')
        display.insert(tk.END, 'Automated Readability Index is: ' + str(output) + '\n')


combo.grid(row=4, column=0, pady=10)
combo.current(1)
combo.set("choose an action")
combo.bind("<<ComboboxSelected>>", callback)

report_label = tk.Label(window, text="Insert the name of the report you want to create:")
report_label.grid(row=7, column=0)
report_name = tk.Entry(window,width=30)
report_name.grid(row=8, column=0, pady=10)
report_btn = tk.Button(text="print a report", command = lambda: print_report(report_name.get(),textWidget.get(1.0,tk.END)))
report_btn.grid(row=9, pady=2)

window.mainloop()


