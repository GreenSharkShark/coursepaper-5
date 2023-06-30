import psycopg2
import os


postgres_pass = os.getenv('postgres_pass')


class DBManager:
    @staticmethod
    def get_companies_and_vacancies_count() -> None:
        connection = psycopg2.connect(port=5433, database='hh_vacancies', user='ZhorikZeniuk', password=postgres_pass)
        with connection.cursor() as cur:
            cur.execute(f'SELECT company_name, vacancies_count FROM companies')
            results = cur.fetchall()
            cur.close()
        return results

    @staticmethod
    def get_all_vacancies() -> None:
        connection = psycopg2.connect(port=5433, database='hh_vacancies', user='ZhorikZeniuk', password=postgres_pass)
        with connection.cursor() as cur:
            cur.execute(f'SELECT vacancy_name, company_name, salary_from, salary_to, url FROM vacancies '
                        f'JOIN companies ON companies.company_id = vacancies.company_id')
            results = cur.fetchall()
            cur.close()
        return results

    @staticmethod
    def get_avg_salary() -> None:
        connection = psycopg2.connect(port=5433, database='hh_vacancies', user='ZhorikZeniuk', password=postgres_pass)
        with connection.cursor() as cur:
            cur.execute(f'SELECT vacancy_name, company_name, salary_from, salary_to, url FROM vacancies '
                        f'JOIN companies ON companies.company_id = vacancies.company_id')
            results = cur.fetchall()
            cur.close()
        return results

    @staticmethod
    def get_vacancies_with_higher_salary() -> None:
        connection = psycopg2.connect(port=5433, database='hh_vacancies', user='ZhorikZeniuk', password=postgres_pass)
        with connection.cursor() as cur:
            cur.execute(f'SELECT vacancy_name, salary_from FROM vacancies '
                        f'WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)')
            results = cur.fetchall()
            cur.close()
        return results

    @staticmethod
    def get_vacancies_with_keyword(keyword: str) -> None:
        connection = psycopg2.connect(port=5433, database='hh_vacancies', user='ZhorikZeniuk', password=postgres_pass)
        with connection.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies "
                        f"WHERE vacancy_name LIKE '%{keyword}%'")
            results = cur.fetchall()
            cur.close()
        return results
