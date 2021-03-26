from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# 1. Ставим запятые между элементами
text = ''
for i, contacts in enumerate(contacts_list):
    text += ",".join(contacts)
    if i + 1 < len(contacts_list):
        text += '\n'

# 2. Заменяем номера
pattern = re.compile(r'(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})')
result = re.sub(pattern, r'+7(\2)\3-\4-\5', text)
pattern = re.compile('(доб.).(\d+)')
result = re.sub(pattern, r' \1\2', result)

# 3. Ставим запятые между ФИО
pattern = re.compile('([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\,')
result = re.sub(pattern, r'\1,\2', result)
pattern = re.compile('([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\,([А-ЯЁ][а-яё]+)\,')
result = re.sub(pattern, r'\1,\2,\3', result)

# 4. Делим контакты по строкам
temporary_list = result.split('\n')


# 5. Убираем дубликаты контактов
new_list = []
already_added = set()
for person_1 in temporary_list:
    compare_list_1 = person_1.split(',')
    for person_2 in temporary_list:
        compare_list_2 = person_2.split(',')
        if compare_list_1[0] == compare_list_2[0] and compare_list_1[1] == compare_list_2[1]:
            for i in range(0, 7):
                if compare_list_1[i] == '':
                    compare_list_1[i] = compare_list_2[i]
    if (compare_list_1[0], compare_list_1[1]) not in already_added:
        new_list.append(compare_list_1)
        already_added.add((compare_list_1[0], compare_list_1[1]))

pprint(new_list)

# 6. Записываем полученный результат в формате CSV
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_list)
