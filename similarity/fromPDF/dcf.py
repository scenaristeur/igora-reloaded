import os

PDF_FOLDER_PATH ='./documentsPDF/'


def get_folder_pdf():

    try:
        documents = [file for file in os.listdir(PDF_FOLDER_PATH) if file.endswith('.pdf')]
    except FileNotFoundError as e:
        print(e.args)
        documents = []

    return documents


def get_list_pdf():

    with open(PDF_FOLDER_PATH + 'pdf_list.txt', mode='r', encoding='UTF-8') as f:
        lines = [line for line in f]

    return lines


def update_list(file_names: list[str]):
    
    with open(PDF_FOLDER_PATH + 'pdf_list.txt', mode='w', encoding='UTF-8') as f:
        for name in file_names:
            f.write(name)

def compare_lists(list1: list[str], list2: list[str]) -> bool:

    if len(list1) != len(list2):
        return False

    result = [a == b for a, b in zip(list1, list2)]

    return result

if __name__ == '__main__':

    print(f'folder files: {get_folder_pdf()}')
    update_list(get_folder_pdf())
    print(f'text files: {get_list_pdf()}')
