from bs4 import BeautifulSoup
import requests
import pypdfium2 as pdfium

website = "https://web.stanford.edu/~jurafsky/slp3/"

hault = 0

for chapter in range(2, 50):
    pdf_page = f"https://web.stanford.edu/~jurafsky/slp3/{chapter}.pdf"

    pdf = []
    
    response = requests.get(pdf_page)

    if response.status_code == 200:
        with open(f"{chapter}.pdf", "wb") as file:
            file.write(response.content)
            print(f"PDF of chapter {chapter} downloaded successfully.")
            hault = 0
            pdf = pdfium.PdfDocument(f"{chapter}.pdf")
    else:
        hault += 1
        if hault == 2:
            print("Finished!")
            break

    for page_num in range(len(pdf)):
        page = pdf.get_page(page_num)
        # (l, b, r, t)
        page.set_trimbox(75, 25, 500, 715)
        page.set_cropbox(75, 50, 500, 715)
        page.gen_content()

    if pdf:
        pdf.save(f"{chapter}.pdf")

# content = response.text

# soup = BeautifulSoup(content, 'lxml')
