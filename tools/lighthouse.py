import requests
import json

# Lighthouse function
def lighthouse(url):
    # Results to be returned
    audits_list = []

    # URL for PageSpeed Insights API
    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    # Parameters
    params = {
        "url": url,
        "key": "AIzaSyC654yxAByvvhpEIhk-ibGjjyeZxLw5iJ0",
        "strategy": "mobile",
    #    "category": ["performance", "accessibility", "best-practices", "seo" "pwa"]
        "category": ["seo"]
        }

    report = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if report.status_code == 200:
        # Save the report to a JSON file
        with open("lighthouse_report.json", "w") as json_file:
            json.dump(report.json(), json_file)
            print("Report saved as lighthouse_report.json")

    # Accessing more keys under a specific category and printing their values
    #    pwa = report.json()["lighthouseResult"]["categories"]["pwa"]
    #    print("Category Title:", pwa["title"])
    #    print("Category Description:", pwa["description"])
    #    print("Category Score:", pwa["score"] * 100)
    # Add more keys as needed

    # Accessing more keys under a specific category and printing their values
        seo = report.json()["lighthouseResult"]["categories"]["seo"]
        print("Category Title:", seo["title"])
        print("Category Description:", seo["description"])
        print("Category Score:", seo["score"] * 100)

    # Accessing more keys under a specific category and printing their values
        metadescription = report.json()["lighthouseResult"]["audits"]["meta-description"]
        print("Audit Title:", metadescription["title"])
        print("Audit Description:", metadescription["description"])
        print("Audit Result:", metadescription["score"] * 100)

        # Accessing more keys under a specific category and appending their key-value pairs to the list
        audits = report.json()["lighthouseResult"]["audits"]

        for audit_key, audit_value in audits.items():
            # Create a dictionary to hold the key-value pair for this audit
            audit_dict = {}

            # Add key-value pairs to the dictionary
            audit_dict["Audit ID"] = audit_value["id"]
            audit_dict["Audit Title"] = audit_value["title"]
            # Check if the "score" key exists and if it's not None before multiplying by 100
            if "score" in audit_value and audit_value["score"] is not None:
                audit_dict["Audit Result"] = audit_value["score"] * 100
            else:
                audit_dict["Audit Result"] = 0

            # Append the dictionary to the list
            audits_list.append(audit_dict)

        # Print the list
        for audit_info in audits_list:
            print("Audit ID:", audit_info["Audit ID"])
            print("Audit Title:", audit_info["Audit Title"])
            print("Audit Result:", audit_info["Audit Result"])

        # Accessing more keys under a specific category and printing their values
    #    best_practices = report.json()["lighthouseResult"]["categories"]["best-practices"]
    #    print("Category Title:", best_practices["title"])
    #    print("Category Description:", seo["description"])
    #    print("Category Score:", best_practices["score"] * 100)

    # Accessing more keys under a specific category and printing their values
    #    performance = report.json()["lighthouseResult"]["categories"]["performance"]
    #    print("Category Title:", performance["title"])
    #    print("Category Description:", seo["description"])
    #    print("Category Score:", performance["score"] * 100)

    # Accessing more keys under a specific category and printing their values
    #    accessibility = report.json()["lighthouseResult"]["categories"]["accessibility"]
    #    print("Category Title:", accessibility["title"])
    #    print("Category Description:", accessibility["description"])
    #    print("Category Score:", accessibility["score"] * 100) 
            
        return audits_list

    else:
        print("Failed to fetch the report. Status code:", report.status_code)

    #print(report.json()["lighthouseResult"]["i18n"]["rendererFormattedStrings"]["varianceDisclaimer"])