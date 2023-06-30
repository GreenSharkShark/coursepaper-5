CREATE TABLE companies(
    company_id serial primary key NOT NULL,
    company_name varchar(255),
    company_descriptiom text,
    vacancies_count smallint
);

CREATE TABLE vacancies(
    company_id serial REFERENCES companies(company_id) NOT NULL,
    vacancy_id_from_hh int UNIQUE,
    vacancy_name varchar(255),
    vacamcy_description text,
    salary_from int,
    salary_to int,
    city varchar(255),
    url varchar(500)
);
