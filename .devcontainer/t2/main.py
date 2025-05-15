import PyPDF2
def extract_text_from_pdf(pdf_path):
    text = ""
        with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                        for page in reader.pages:
                                    text += page.extract_text() + "\n"
                                            return text
                                            # Example usage
                                            pdf_file_path = "/content/caa50098-1fb4-4251-996e-324a25560f9e_250514_223047.PDF"
                                            extracted_text = extract_text_from_pdf(pdf_file_path)
                                            print(len(extracted_text))