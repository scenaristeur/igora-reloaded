import os

PDF_FOLDER_PATH ='./documentsPDF/'
PDF_TEXT_LIST = 'pdf_list.txt'


def get_folder_pdf():

    try:
        documents = [file for file in os.listdir(PDF_FOLDER_PATH) if file.endswith('.pdf')]
    except FileNotFoundError as e:
        print(e.args)
        documents = []

    return documents


def get_list_pdf():

    try:
        with open(PDF_FOLDER_PATH + PDF_TEXT_LIST, mode='r', encoding='utf-8') as f:
            lines = [line.strip('\n') for line in f]
    except FileNotFoundError as e:
        print(e.args)
        return []

    return lines


def update_list(file_names: list[str]):

    with open(PDF_FOLDER_PATH + PDF_TEXT_LIST, mode='w', encoding='UTF-8') as f:
        for name in file_names:
            f.write(f'{name}\n')

def compare_lists(list1: list[str], list2: list[str]) -> bool:

    if list1 == [] or list2 == []:
        return False

    if len(list1) != len(list2):
        return False

    result = [a == b for a, b in zip(list1, list2)]

    return all(result)

def file_exists() -> bool:

    file_list = os.listdir(PDF_FOLDER_PATH)
    if file_list == []:
        return False

    if len(file_list) == 1 and not file_list[0].endswith('.pdf'):
        return False

    return True

if __name__ == '__main__':

    print(f'folder files: {get_folder_pdf()}')
    update_list(get_folder_pdf())
    print(f'text files: {get_list_pdf()}')
    print(compare_lists(get_folder_pdf(), get_list_pdf()))
