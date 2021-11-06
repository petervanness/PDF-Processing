# PDF-Processing
Functions for parsing and searching PDFs

# Overview
The general idea of these programs is to run a control+F on a bunch of PDFs from a webpage or in a folder, with multiple search terms. This repository contains a couple simple programs for programmatic searching for text in PDFs, generally several at a time. 

PDF_to_Text.py is one of the base functions and converts PDFs to string readable by Python, relying on the very helpful PDFMiner package.

PDF_Text_Search.py is another base function that searches the parsed PDF text for user-specified keywords and returns a pandas dataframe with the references to the keywords and corresponding file paths/URLs.

The URL_PDF_Search jupyter notebook includes very high level instructions because that version was intended to be distributed on Google Colab to non-coding folks. 

folder_pdf_search.py utilizes the above functions to run searches of PDFs through a local folder.

## Important Caveats
1. The false-negative rate should be about the same as Control+F, so if opening each of these documents and Ctrl+F-ing through would be precise enough for your purposes, this should do about as well as that, but faster and more easily. 

2. There will be some false positives. It is using computer vision, and occasionally of fuzzy scans, so sometimes it will return screwy things like blanks or bizarre characters or visually similar but unwanted results (e.g. it seems to mistake the dots in i's as periods sometimes). The idea isn't for the program to read for you but to identify at a high rate portions of documents that could be of interest, so hopefully it can do that in spite of these irregularities.

4. There are occasionally PDFs which the program can't open (PDF urls with spaces throw it off, for example), which is frustrating. The output at the bottom of the page will tell you which files were not read. As time permits, these issues will be ironed out.

The search is not case-sensitive.

---

