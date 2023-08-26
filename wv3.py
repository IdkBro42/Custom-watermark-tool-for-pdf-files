
import os
from pathlib import Path
from fpdf import FPDF
import PyPDF2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Label, Button, Entry


def create_watermark(input_text, text_color=(0, 0, 0)):
    # Get desktop path
    desktop = Path.home() / "Desktop"

    # Create a watermark PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=100)

    r, g, b = text_color
    pdf.set_text_color(r, g, b)







    number_of_lines = len(input_text.split('\n'))
    text_height = number_of_lines * 0.2 * 100  
    vertical_position = (297/2) - (text_height/2)
    pdf.ln(vertical_position)

    pdf.set_fill_color(200, 200, 200) 

    pdf.multi_cell(0, 10, txt=input_text, align="C")

    watermark_filename = desktop / "watermark.pdf"
    pdf.output(watermark_filename)
    return watermark_filename

def apply_watermark(input_pdf, watermark_text):
    watermark_filename = create_watermark(watermark_text, text_color=(230, 230, 230))
    output_pdf_name = Path(input_pdf).stem + "_watermarked.pdf"
    output_pdf = Path(input_pdf).parent / output_pdf_name
    original = PyPDF2.PdfReader(input_pdf)
    pdf_watermark = PyPDF2.PdfReader(watermark_filename)
    pdf_writer = PyPDF2.PdfWriter()

    watermark_page = pdf_watermark.pages[0]
    for i in range(len(original.pages)):
        page = original.pages[i]
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    with open(output_pdf, 'wb') as output_file_handle:
        pdf_writer.write(output_file_handle)

    os.remove(watermark_filename)
    return output_pdf

def main_program():
    watermark_text = watermark_entry.get()
    input_pdf = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    if input_pdf:
        output_pdf = apply_watermark(input_pdf, watermark_text)
        messagebox.showinfo("Success!", f"Watermarked file saved as: {output_pdf}")




root = tk.Tk()
root.title("PDF Watermark App")


label = Label(root, text="Enter the watermark text:")
label.pack(pady=20)


watermark_entry = Entry(root, width=50)
watermark_entry.pack(pady=20)


apply_button = Button(root, text="Select PDF and Apply Watermark", command=main_program)
apply_button.pack(pady=20)

root.mainloop()


#working version number 3, puts a somewhat white custom watermark on the center of every page of the pdf uploaded