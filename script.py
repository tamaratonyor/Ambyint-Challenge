import csv
import random
from faker import Faker
from datetime import datetime
import snowflake.connector
from snowflake.connector.errors import Error as SnowflakeError
import os

fake = Faker()

show_types = ['Movie', 'TV Show']
ratings = ['TV-MA', 'R', 'PG-13', 'PG', 'G', 'TV-14']
durations_movie = [f"{random.randint(70, 130)} min" for _ in range(20)]
durations_tv = [f"{random.randint(1, 6)} Seasons" for _ in range(20)]
genres = [
    "Dramas", "Comedies", "Horror Movies", "International Movies", 
    "TV Dramas", "TV Sci-Fi & Fantasy", "Independent Movies", 
    "Action & Adventure", "Documentaries", "International TV Shows"
]
countries = ['United States', 'Brazil', 'Mexico', 'Singapore', 'Canada', 'India', 'France']
config = {
        'user': os.environ['SF_USER'],
        'password': os.environ['SF_PASSWORD'],
        'account': os.environ['SF_ACCOUNT'],
        'warehouse': os.environ['SF_WAREHOUSE'],
        'database': os.environ['SF_DATABASE'],
        'schema': os.environ['SF_SCHEMA'],
}

def generate_cast():
    return ', '.join([fake.name() for _ in range(random.randint(4, 8))])

def generate_director():
    return fake.name() if random.random() > 0.1 else ''  # 10% chance of no director

def generate_description():
    return fake.sentence(nb_words=20)

def get_max_show_id():
    try:
        print("Connecting...")
        conn = snowflake.connector.connect(**config)

        conn.cursor().execute(f"USE DATABASE {config['database']}")
        conn.cursor().execute(f"USE SCHEMA {config['schema']}")

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT MAX(TO_NUMBER(REGEXP_SUBSTR(show_id, '[1-9][0-9]*'))) AS max_show_id
                FROM NETFLIX_TITLES;
            """)
            result = cursor.fetchone()
            if result and result[0] is not None:
                return int(result[0])
            else:
                print("⚠️ No matching show_id values found.")

    except SnowflakeError as e:
        print("❌ Snowflake error:", e)
    except Exception as e:
        print("❌ General error:", e)
    finally:
        if conn:
            conn.close()

def generate_entry(show_id):
    show_id = f"s{show_id}"
    type_ = random.choice(show_types)
    title = fake.word().capitalize() + (":" + str(random.randint(1, 99)) if random.random() < 0.2 else '')
    director = generate_director()
    cast = generate_cast()
    country = random.choice(countries)
    date_added = fake.date_between(start_date="-5y", end_date="today").strftime("%B %d, %Y")
    release_year = random.randint(2000, 2024)
    rating = random.choice(ratings)
    duration = random.choice(durations_tv if type_ == 'TV Show' else durations_movie)
    listed_in = ', '.join(random.sample(genres, k=random.randint(1, 3)))
    description = generate_description()

    return [
        show_id, type_, title, director, cast, country, date_added,
        release_year, rating, duration, listed_in, description
    ]

# Use today's date to name the file
today_str = datetime.now().strftime('%Y_%m_%d')
file_name = f"dbt_project/src/seeds/netflix_titles_{today_str}.csv"

# Write CSV with header
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'show_id', 'type', 'title', 'director', 'cast', 'country',
        'date_added', 'release_year', 'rating', 'duration',
        'listed_in', 'description'
    ])
    max_show_id = get_max_show_id()
    for i in range(1, 101):  # generate 100 rows
        writer.writerow(generate_entry(show_id=max_show_id + 1))
        max_show_id+=1

print(f"CSV file '{file_name}' generated successfully.")
