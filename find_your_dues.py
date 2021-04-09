import PyPDF2

pdf_file = open('no_dues.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)


def find_defaulter(registration_number):
    for i in range(0, 100):
        page = pdf_reader.getPage(i)
        text = page.extractText().split()
        if registration_number in text:
            index = text.index(registration_number)
            last_index = len(text) - 1
            serial_number = text[index-2]
            serial_number = int(serial_number)
            next_number = serial_number+1
            defaulter_contents = list()
            while text[index] != str(next_number):
                defaulter_contents.append(text[index])
                if index == last_index:
                    break
                index += 1
            count = 0
            j = 0
            for content in defaulter_contents:
                if j == len(defaulter_contents)-1:
                    if not total_due:
                        total_due = defaulter_contents[defaulter_contents.index(content)]
                elif content.isnumeric() and count == 2:
                    print('\n')
                    count += 1
                    total_due = defaulter_contents[defaulter_contents.index(content)-1]
                elif content.isnumeric():
                    print('\n')
                    count += 1
                print(content, end=" ")
                j += 1
            print(f'\nYour Total Due is {total_due}!')
            return
    print('You are a Good Boy')


registration_number = input('Enter your Registration Number')
find_defaulter(registration_number)
