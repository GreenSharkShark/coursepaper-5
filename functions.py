import requests
import psycopg2
import os
from DBManager import DBManager

postgres_pass = os.getenv('postgres_pass')
id_list: list = ['1858119', '672796', '796835', '3011921', '5036338', '1035627', '2676727', '4525306', '1231878',
                 '746783']


def get_vacancies_info_by_id(company_id) -> list[str]:
    vacancies_url = "https://api.hh.ru/vacancies"
    params = {'employer_id': company_id, 'per_page': 100}
    all_vacancies = []

    page = 0
    while True:
        params['page'] = page
        response = requests.get(vacancies_url, params=params)
        if response.status_code == 200:
            vacancies_data = response.json()
            vacancies_list = vacancies_data.get("items", [])

            if len(vacancies_list) == 0:
                break

            all_vacancies.extend(vacancies_list)
            page += 1
        else:
            print("Ошибка при получении списка вакансий")
            break

    return all_vacancies


def get_company_info_by_id(company_id_list: list[str]) -> list:
    companys_info = []
    for company_id in company_id_list:
        company_url = f"https://api.hh.ru/employers/{company_id}"
        response = requests.get(company_url)
        if response.status_code == 200:
            company_data = response.json()
            companys_info.append(company_data)
        else:
            print("Ошибка при получении информации о компании")
            return None
    return companys_info


def save_data_to_vacamcies_table(vacancies_info_list: list) -> None:
    conn = DBManager.connect_to_database()
    for vacancy in vacancies_info_list:
        cur = conn.cursor()
        employer = vacancy['employer']['name']
        vacancy_id_from_hh = vacancy['id']  # Использую для проверки дублирования вакансий
        vacancy_name = vacancy['name']
        vacancy_description = vacancy['snippet']['responsibility']
        try:
            salary_from = vacancy['salary']['from']
            salary_to = vacancy['salary']['to']
        except TypeError:
            salary_from = None
            salary_to = None
        city = vacancy['area']['name']
        url = vacancy['employer']['alternate_url']
        cur.execute(
            f"INSERT INTO vacancies(company_id, vacancy_id_from_hh, vacancy_name, vacamcy_description, salary_from, salary_to, city, url)"
            f"VALUES ((SELECT company_id FROM companies WHERE company_name = %s), %s, %s, %s, %s, %s, %s, %s)",
            (employer, vacancy_id_from_hh, vacancy_name, vacancy_description, salary_from, salary_to, city, url))
        conn.commit()
        cur.close()
    conn.close()


def save_data_to_companies_table(companies_info_list: list[str]) -> None:
    conn = DBManager.connect_to_database()
    for company in companies_info_list:
        cur = conn.cursor()
        company_name = company['name']
        company_description = company['description']
        vacancies_count = company['open_vacancies']
        cur.execute(f"INSERT INTO companies(company_name, company_descriptiom, vacancies_count)"
                    f"VALUES (%s, %s, %s)",
                    (company_name, company_description, vacancies_count))
        conn.commit()
        cur.close()
    conn.close()
