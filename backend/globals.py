import sys
import psycopg2
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uszipcode import SearchEngine as search
from datetime import datetime, timedelta
from job import Job

# GLOBALS

db = ''
c = ''
conn = None
cur = None

# add scraper filenames for a whitelist, run all of them if empty
active_scrapers = []

# EXCEPTIONS


class Error(Exception):
    '''Base class for exceptions in the parser'''
    pass


class ParseError(Error):
    '''Exception raised for error in parsing for jobs

    Attributes:
        url -- expression where the error occured
        msg -- explanation of the error
    '''

    def __init__(self, url, msg):
        self.url = url
        self.msp = msg


class LocationError(Error):
    '''Exception raised for error in job location

    Attributes:
        url -- expression where the error occured
        msg -- explanation of the error
    '''

    def __init__(self, url, msg):
        self.url = url
        self.msp = msg


# FUNCTIONS


def error_handler(error_msg):
    print error_msg
    exit()


def print_vars(job_class):
    print "Title: ", job_class.title
    print "Summary: ", job_class.summary
    print "Location: ", job_class.location
    print "Zip Code: ", job_class.zip_code
    print "Post Date: ", job_class.post_date
    print "Full or Part-Time: ", job_class.full_or_part
    print "Salary: ", job_class.summary
    print "Information: ", job_class.info_link


def create_tables():
    global cur
    global conn
    commands = ('''
    CREATE TABLE IF NOT EXISTS test_regions (
        id SERIAL,
        name TEXT UNIQUE NOT NULL,
        PRIMARY KEY (id)
    )
    ''', '''
    CREATE TABLE IF NOT EXISTS test_organizations (
        id SERIAL,
        name TEXT UNIQUE NOT NULL,
        url TEXT NOT NULL,
        logo TEXT,
        mission TEXT,
        description TEXT,
        street TEXT,
        suite TEXT,
        city TEXT,
        state TEXT,
        zip TEXT,
        latitude TEXT,
        longitude TEXT,
        phone TEXT,
        PRIMARY KEY (id)
    )
    ''', '''
    CREATE TABLE IF NOT EXISTS test_organizations_regions (
        organization_id INTEGER REFERENCES organizations (id),
        region_id INTEGER REFERENCES regions (id)
    )
    ''', '''
    CREATE TABLE IF NOT EXISTS jobs (
        id SERIAL,
        date DATE,
        job_title VARCHAR,
        job_summary VARCHAR,
        job_location VARCHAR,
        job_zip_code VARCHAR,
        job_post_date DATE,
        full_or_part VARCHAR,
        salary VARCHAR,
        info_link VARCHAR,
        organization_id INTEGER REFERENCES organizations (id),
        PRIMARY KEY (id)
    )
    ''')
    try:
        for command in commands:
            cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def drop_tables():
    global cur
    global conn
    commands = ('''
        DROP TABLE IF EXISTS jobs
    ''', '''
        DROP TABLE IF EXISTS test_organizations
    ''', '''
        DROP TABLE IF EXISTS test_regions
    ''', '''
        DROP TABLE IF EXISTS test_organizations_regions
    ''')
    try:
        for command in commands:
            cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def print_organization(organization_name, curr, total):
    sys.stdout.write(str(curr) + '/' + str(total) + ': ')
    sys.stdout.write(organization_name)
    sys.stdout.flush()


def print_insert_progress():
    sys.stdout.write('.')
    sys.stdout.flush()


def print_organization_end(insert_count):
    sys.stdout.write('(' + str(insert_count) + ')')
    sys.stdout.write('\n')
    sys.stdout.flush()
    # print('Inserted ' + str(globals.insert_count) + ' job(s).')


def print_id_name():
    sql = '''
    SELECT id, name
    FROM organizations    
    ORDER BY name ASC
    '''
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for r in result:
            print(r)
    except:
        print("didnt work")


def insert_job(values):
    sql = '''
    INSERT INTO jobs (job_title, organization_id, date, job_summary, job_location, job_zip_code, job_post_date, full_or_part, salary, info_link)
    VALUES (%s, (SELECT id FROM organizations WHERE name = %s), current_date, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    '''
    try:
        # print(values)
        cur.execute(sql, values)
        # print(cur.fetchone()[0])
        print_insert_progress()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def job_insert(job):
    """
        Insert an instance of the Job class in the Jobs table.
    """

    sql = '''
    INSERT INTO jobs (job_title, organization_id, date, job_summary, job_location, job_zip_code, job_post_date, full_or_part, salary, info_link)
    VALUES (%s, %s, current_date, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    '''
    try:
        cur.execute(sql, (job.title, job.organization_id, job.summary,
                          job.location, job.zip_code, job.post_date,
                          job.full_or_part, job.salary, job.info_link))
        print_insert_progress()
        return 1
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 0


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    return soup


def get_javascript_soup(url):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.implicitly_wait(10)
    driver.get(url)
    innerHTML = driver.execute_script("return document.body.innerHTML")
    driver.quit()
    return BeautifulSoup(innerHTML, "lxml")


def get_javascript_soup_delayed(url, dynamicElement):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, dynamicElement)))
    finally:
        innerHTML = driver.execute_script("return document.body.innerHTML")
        driver.quit()
        return BeautifulSoup(innerHTML, "lxml")


def get_javascript_soup_delayed_and_click(url, dynamicElement):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, dynamicElement)))
    finally:
        element.click()
        innerHTML = driver.execute_script("return document.body.innerHTML")
        driver.quit()
        return BeautifulSoup(innerHTML, "lxml")


def update_db(job_class):
    insert_job(
        (job_class.title, job_class.organization_name, job_class.summary,
         job_class.location, job_class.zip_code, job_class.post_date,
         job_class.full_or_part, job_class.salary, job_class.info_link))


def date_ago(timeLength, timeUnit):
    timeUnit = timeUnit.strip().lower()
    today = datetime.today()
    if timeUnit[:3] == 'day':
        return today - timedelta(days=timeLength)
    elif timeUnit[:5] == 'month':
        return today - timedelta(days=30 * timeLength)
    elif timeUnit[:4] == 'year':
        return today - timedelta(days=365 * timeLength)


def clean_location(string):
    return string.split(',')[0].strip()


# def clean_location(string):
#    if string.split(',')[-1].strip() == 'CA':
#        return string.split(',')[0].strip()
#    else:
#        raise LocationError(string, 'Location not in California')


def city_to_zip(location):
    # remove ending 'county' in location
    tokens = location.split()
    if tokens[-1].lower() == 'county':
        location = ' '.join(tokens[:-1])

    return int(search().by_city_and_state(location, 'CA')[0].zipcode)


def zip_to_city(cityzip):
    return search().by_zipcode(cityzip).major_city


def select_organization_id_by_name(name):
    global cur
    cur.execute("SELECT id from organizations WHERE name=%s", [name])

    rows = cur.fetchall()
    if len(rows) == 0:
        print('organization doesn\'t exist: %s' % name)
    return rows[0][0]


def delete_jobs_by_organization(organization_name):
    query = '''
    DELETE FROM jobs
    WHERE organization_id = (
        SELECT id FROM organizations WHERE name = %s
    ) AND is_user_created = false
    '''
    try:
        cur.execute(query, [organization_name])
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
