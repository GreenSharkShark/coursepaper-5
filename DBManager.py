import psycopg2
from psycopg2.extensions import connection
import os
import json


postgres_pass = os.getenv('postgres_pass')


class DBManager:
    @classmethod
    def connect_to_database(cls) -> connection:
        with open('config.json') as config:
            params = json.load(config)
            connection = psycopg2.connect(port=params['port'], database=params['database'], user=params['user'], password=params['password'])
        return connection

    @staticmethod
    def get_companies_and_vacancies_count() -> None:
        connection = DBManager.connect_to_database()
        with connection.cursor() as cur:
            cur.execute(f'SELECT company_name, vacancies_count FROM companies')
            results = cur.fetchall()
            cur.close()
        return results

    @staticmethod
    def get_all_vacancies() -> None:
        connection = DBManager.connect_to_database()
        with connection.cursor() as cur:
            cur.execute(f'SELECT vacancy_name, company_name, salary_from, salary_to, url FROM vacancies '
                        f'JOIN companies ON companies.company_id = vacancies.company_id')
            results = cur.fetchall()
            cur.close()
        return results

    @staticmethod
    def get_avg_salary() -> None:
        connection = DBManager.connect_to_database()
        with connection.cursor() as cur:
            cur.execute(f'SELECT vacancy_name, company_name, salary_from, salary_to, url FROM vacancies '
                        f'JOIN companies ON companies.company_id = vacancies.company_id')
            results = cur.fetchall()
            cur.close()
        return results

    @staticmethod
    def get_vacancies_with_higher_salary() -> None:
        connection = DBManager.connect_to_database()
        with connection.cursor() as cur:
            cur.execute(f'SELECT vacancy_name, salary_from FROM vacancies '
                        f'WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)')
            results = cur.fetchall()
            cur.close()
        return results

    @staticmethod
    def get_vacancies_with_keyword(keyword: str) -> None:
        connection = DBManager.connect_to_database()
        with connection.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies "
                        f"WHERE vacancy_name LIKE '%{keyword}%'")
            results = cur.fetchall()
            cur.close()
        return results


a = DBManager()
print(a.get_avg_salary())
