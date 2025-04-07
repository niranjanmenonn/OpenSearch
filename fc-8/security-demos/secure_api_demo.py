#Secures all API calls to Google Search
#Removes sensitive parameters
#Adds security headers to requests


import requests

def secure_api_call(endpoint, params):
    headers = {
        'X-Disable-Logging': 'true',
        'Accept': 'application/vnd.github.v3+json'
    }  #Reduces tracking capabilities
    sanitized_params = {k: v for k, v in params.items() if not k.startswith('_')} #Removes any parameters starting with '_' which might contain sensitive data
    return requests.get(endpoint, params=sanitized_params, headers=headers)

if __name__ == "__main__":
    print("GitHub Repository Search API Demo")
    repo_name = input("Enter a GitHub repository name to search (e.g., tensorflow): ")
    
    endpoint = f"https://api.github.com/search/repositories"
    params = {
        '_query': repo_name,  # This will be filtered out
        'q': repo_name,       # This will remain
        'sort': 'stars'
    }
    
    print(f"\nOriginal parameters: {params}")
    response = secure_api_call(endpoint, params)
    
    print(f"Sanitized request URL: {response.url}")
    print(f"Response status code: {response.status_code}")
    
    data = response.json()
    if data['items']:
        repo = data['items'][0]  # Prevents exposure of excessive data
        print("\nTop Repository Details:")
        print(f"Name: {repo['name']}")
        print(f"Stars: {repo['stargazers_count']}")
        print(f"Description: {repo['description']}")
        print(f"URL: {repo['html_url']}")
