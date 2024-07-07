import PyPDF2

pdf = open("Python.pdf", "rb")
text = PyPDF2.PdfReader(pdf).getPage(22)
print(text)