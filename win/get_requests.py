import requests
from cookies.get_cookies import main


def get_projects_url(pattern:str="rdp") -> list:
    url = "https://media108.cloudflareaccess.com/apps/data"

    headers = {
        'Cookie': main()
    }

    response = requests.get(url, headers=headers)

    return [i['domain'] for i in response.json()['apps'] if pattern in i['domain'].lower()]


print(get_projects_url())
