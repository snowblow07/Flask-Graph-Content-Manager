# Import libraries for Goole Lighthouse
import requests
import json

# Import libraries for seoAnalyzer
from seoanalyzer import analyze

# Import libraries for readability
from bs4 import BeautifulSoup
import re
from readability import Readability

# Lighthouse function
def lighthouse(url_string):
    
    # URL for PageSpeed Insights API
    url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    # Set API parameters
    params = {
        "url" : url_string,
        "key" : "YOUR_API_KEY_HERE",
        "strategy" : "mobile",
        "category" : ["performance", "accessibility", "best-practices", "seo", "pwa"]
    }
    lh_report = requests.get(url, params=params)

    # Check response expected 200
    if lh_report.status_code == 200:
    # Save the report to a JSON file
        with open("pagespeed_report.json", "w") as json_file:
            json.dump(lh_report.json(), json_file)
            print("Report saved as pagespeed_report.json")

        # Accessing more keys under a specific category and printing their values
        pwa = lh_report.json()["lighthouseResult"]["categories"]["pwa"]
        print("Category Title:", pwa["title"])
        print("Category Description:", pwa["description"])
        print("Category Score:", pwa["score"] * 100)
        # Add more keys as needed

        # Accessing more keys under a specific category and printing their values
        seo = lh_report.json()["lighthouseResult"]["categories"]["seo"]
        print("Category Title:", seo["title"])
        print("Category Description:", seo["description"])
        print("Category Score:", seo["score"] * 100)

        # Accessing more keys under a specific category and printing their values
        best_practices = lh_report.json()["lighthouseResult"]["categories"]["best-practices"]
        print("Category Title:", best_practices["title"])
        print("Category Score:", best_practices["score"] * 100)

        # Accessing more keys under a specific category and printing their values
        performance = lh_report.json()["lighthouseResult"]["categories"]["performance"]
        print("Category Title:", performance["title"])
        print("Category Score:", performance["score"] * 100)

        # Accessing more keys under a specific category and printing their values
        accessibility = lh_report.json()["lighthouseResult"]["categories"]["accessibility"]
        print("Category Title:", accessibility["title"])
        print("Category Description:", accessibility["description"])
        print("Category Score:", accessibility["score"] * 100) 

    else:
        print("Failed to fetch the report. Status code:", lh_report.status_code)

# seoAnalyzer function     
def seoAnalyzer(url_string):
    output = analyze(url_string)
    # Generate report
    seo_report = analyze(url_string)
    # save report as json
    with open("seoAnalyze.json", "w") as json_file:
        json.dump(output, json_file)
        print("Report saved as seoAnalyze.json")
    print(output)

# Readibility function
# Convert webpage to plain text
def convert_webpage_to_plain_text_with_bs(domain):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/94.0.4606.81 Safari/537.36'
        }
        response = requests.get(domain, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text using BeautifulSoup's get_text() method
            plain_text = soup.get_text(separator=' ', strip=True)
            return plain_text
        else:
            return f"Failed to fetch content. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request Error: {e}"
# Save text to file
def save_text_to_file(text, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(text)
        return f"Text saved to {file_name} successfully."
    except Exception as e:
        return f"Error saving text to file: {e}"
# Execute Readibility Function
def content_analyze(domain):
    url_to_convert = domain  # Replace with the desired URL
    plain_text = convert_webpage_to_plain_text_with_bs(url_to_convert)
    if plain_text:
        file_name = 'extracted_text.txt'  # Replace with your desired file name
        result = save_text_to_file(plain_text, file_name)
        print(result)
    else:
        print("Failed to extract text from the webpage.")
    #print(plain_text)
    r = Readability(plain_text)
    f = r.flesch()
    print(f.score)
    print(f.ease)
    print(f.grade_levels)

# Get user input
domain = input("type the url: ")

# Function calls

#LIGHTHOUSE
#lighthouse(domain)

#SEOANALYZER
#seoAnalyzer(domain)

#CONTENT ANALYZER
#content_analyze(domain)