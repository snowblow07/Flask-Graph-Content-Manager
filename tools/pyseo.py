from seoanalyzer import analyze
import json

site = "https://www.nytimes.com/2024/01/11/us/politics/us-houthi-missile-strikes.html"

output = analyze(site)

with open("seoAnalyze.json", "w") as json_file:
    json.dump(output, json_file)
    print("Report saved as seoAnalyze.json")

print(output)
