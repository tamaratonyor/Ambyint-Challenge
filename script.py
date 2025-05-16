import csv
import random
from faker import Faker
from datetime import datetime

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

def generate_cast():
    return ', '.join([fake.name() for _ in range(random.randint(4, 8))])

def generate_director():
    return fake.name() if random.random() > 0.1 else ''  # 10% chance of no director

def generate_description():
    return fake.sentence(nb_words=20)

def generate_entry(index):
    show_id = f"s{index}"
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
today_str = datetime.now().strftime('%Y-%m-%d')
file_name = f"dbt_project/src/tests/netflix_titles_{today_str}.csv"

# Write CSV with header
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'show_id', 'type', 'title', 'director', 'cast', 'country',
        'date_added', 'release_year', 'rating', 'duration',
        'listed_in', 'description'
    ])
    for i in range(1, 101):  # generate 100 rows
        writer.writerow(generate_entry(i))

print(f"CSV file '{file_name}' generated successfully.")
