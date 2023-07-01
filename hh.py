import requests 
import csv


num_of_pages = [i for i in range(int(input('Задайте глубину поиска в страницах: ')))] # Задаем глубину поиска (сколько страниц будет просмотрено)
vacancie_name = input('Вакансия должная содержать...: ') # Задаем ключ для поиска
area = input("Введите нормер региона, в котором ищете работу: ") # Краснодар - 53*

pages = []

for num_of_page in num_of_pages: # итерируемся по страницам
    ls_page = requests.get('https://api.hh.ru/vacancies', params={'text': vacancie_name,
                                                                  'area': area,
                                                                  'page': str(num_of_page),
                                                                  'per_page': '50',
                                                                  'only_with_salary': 'true'}).json()['items']
    pages.append(ls_page)



smooth_ls = [ls for sublist in pages for ls in sublist]

with open('expl.csv', 'w', encoding='utf-8-sig', newline='') as file: # открываем файл для записи
    writer = csv.writer(file, delimiter=';')
    writer.writerow([ # Устанавливаем заголовки
        "Название вакансии", "Зарплата минимальная", "Зарплата максимальная", 
        "Gross", "Статус вакансии", "Ссылка на вакансию", "Имя работодателя",
        "Ссылка на профиль работодателя", "Требования", "Суть работы",
        "Адрес работодателя"
    ]) 
    for vacancie in smooth_ls: # итерируемся по каждой найденной вакансии
        vacancie_name = vacancie['name']
        vacancie_salary = [value for key, value in vacancie['salary'].items() if key != 'currency']
        type_ = vacancie['type']['name']
        vacancie_url = vacancie['alternate_url']
        employer_name = vacancie['employer']['name']
        try:
            employer_url = vacancie['employer']['alternate_url']
        except:
            employer_url = '' # на случай отсутствия ссылки на сайт работодателя
        requirement = vacancie['snippet']['requirement']
        responsibility = vacancie['snippet']['responsibility']
        try:
            adress = [value for key, value in vacancie['address'].items() if key == 'raw'][0] 
        except:
            adress = '' # на случай не отсутствия адреса работодателя
        flatten = vacancie_name, *vacancie_salary, type_, vacancie_url, employer_name, employer_url, requirement, responsibility, adress # размещаем значения по соответствующим столбцам
        writer.writerow(flatten) # производим запись в файл, при повторной записи обязательно закрыть книгу