import requests
import json
import argparse

API_KEY = "YOUR API KEY"
PDL_URL = "https://api.peopledatalabs.com/v5/person/enrich"

def mainFun(link, email):
    if args.email and args.link :
        PARAMS = {
            "api_key": API_KEY,
            "profile": [link],
                "min_likelihood": 6,
            "email" : [f"{email}"]}
        
    elif args.email and not args.link:
        PARAMS = {
            "api_key": API_KEY,
            "email" : [f"{email}"]}

    elif not args.email and args.link:
        PARAMS = {
            "api_key": API_KEY,
            "profile": [link], 
               "min_likelihood": 6}
        
    else:
        print("Invalid search")
        return 

    json_response = requests.get(PDL_URL, params=PARAMS).json()
    if json_response["status"] == 200:
        record = json_response['data']

        print(
            record['work_email'],
            record['full_name'],
            record['job_title'],
            record['job_company_name']
        )

        print(f"Successfully enriched profile with PDL data.")

        with open(f"{record['full_name']}.jsonl", "w") as out:
            out.write(json.dumps(record) + "\n")
    else:
        print("Enrichment unsuccessful. See error and try again.")
        print("error:", json_response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieves data')
    parser.add_argument('-l', '--link', help='Linkedin profile link',)
    parser.add_argument('-e', '--email', help='Email format option', action='store_true')
    args = parser.parse_args()

    if args.email:
        mainFun(args.link, 'e' if args.email else 'l')
    else:
        mainFun(args.link, '')

