import pdfplumber

class TextConverter():
    # Step 1: Extract text from the PDF
    @staticmethod
    def pdf_to_text(pdfpath, output_text_file_path):
        pdf_path = pdfpath
        all_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:  # You can increase the range for full book
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
        with open(output_text_file_path, 'w') as file:
            file.write(all_text)
        return all_text
    
    def read_from_text_file(text_file_path:str):
        with open(text_file_path, 'r') as file:
            all_text = file.read()
        return all_text