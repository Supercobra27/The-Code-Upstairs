from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("Transcript W25.pdf")
print(result.text_content)