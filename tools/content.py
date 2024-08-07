import requests
from bs4 import BeautifulSoup
import re
from readability import Readability

def convert_webpage_to_plain_text_with_bs(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text using BeautifulSoup's get_text() method
            plain_text = soup.get_text(separator=' ', strip=True)
            return plain_text
        else:
            return f"Failed to fetch content. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request Error: {e}"

def save_text_to_file(text, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(text)
        return f"Text saved to {file_name} successfully."
    except Exception as e:
        return f"Error saving text to file: {e}"

url_to_convert = 'https://www.nycresistor.com/'  # Replace with the desired URL
plain_text = convert_webpage_to_plain_text_with_bs(url_to_convert)

if plain_text:
    file_name = 'extracted_text.txt'  # Replace with your desired file name
    result = save_text_to_file(plain_text, file_name)
    print(result)
else:
    print("Failed to extract text from the webpage.")

print(plain_text)

r = Readability(plain_text)

#r.flesch_kincaid()
#r.flesch()
#r.gunning_fog()
#r.coleman_liau()
#r.dale_chall()
#r.ari()
#r.linsear_write()
#r.spache()
#r.smog()   

f = r.flesch()
print(f.score)
print(f.ease)
print(f.grade_levels)