import requests
from bs4 import BeautifulSoup

base_url = "https://gitstar-ranking.com/repositories"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept_Encoding': 'gzip, deflate, sdch, br', 'Accept_Language':'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

repo_data = []

def add_data(item):
    repo_data.append(item)

def examine_repos(repos_collected):
    github_repo_api = "https://api.codetabs.com/v1/loc/?github="

    for found_repo in repos_collected:
        url = github_repo_api + found_repo
        print("\nRepo : "+ url[40:])
        page = requests.get(url).json()
        if "Error" in page:
            print("#### Large Repo ####")
            print(page)
        else:
            print(page[-1])

def parse_page(url):
    
    page = requests.get(url, headers=headers)
    
    if page.status_code == requests.codes.ok:
        soup = BeautifulSoup(page.content, 'html5lib')
        for repo in soup.find_all(class_='list-group-item paginated_item'):
            repo = repo.get('href')
            add_data(repo[1:])
            #print(repo[1:])

        next_page_text = soup.find('ul', class_='pagination').find_all()[-1].get("rel") 
        #print(next_page_text)

        if next_page_text == ['next']:
            next_page_url = soup.find('ul', class_='pagination').find_all()[-1].get("href")
            #print(next_page_url)
            next_page_url = "https://gitstar-ranking.com"+ next_page_url
            parse_page(next_page_url)
        else:
            examine_repos(repo_data) #print("### Yay! It finished!! ###")
    
print("Working on it...")
parse_page(base_url)
