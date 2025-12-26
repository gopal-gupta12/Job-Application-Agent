import requests # for http requests
from bs4 import BeautifulSoup  # for HTML parsing

FAKE_JOBS_URL = "https://realpython.github.io/fake-jobs" # Constant holding URL of a demo job board Real Python for scrapping practices.

# Scraps a demo jobs page and return a list of job dicts . Each dict has title, company, url, desciption.
def scrape_fake_jobs() -> list[dict]:
    response = requests.get(FAKE_JOBS_URL, timeout= 10) # Sends get requests to the page , timeout prevents hanging forever.
    response.raise_for_status() # Raises exception instead of failing when server returns 404,500.

    soup = BeautifulSoup(response.text, "html.parser")  # Parses the HTML into a tree so can search elements.

    result_container = soup.find(id = "ResultsContainer") 
    jobs: list[dict] = []
    
# Iterating over each job card. Class name is taken to inspecting the HTML.
    for card in result_container.find_all("div", class_ = "card-content"):
        title_element = card.find("h2", class_="title")
        company_element = card.find("h3", class_="company")
        description_element = card.find("p", class_="description")
        link_element = card.find("a", string="Apply")
          
        # skips malformed card to avoid crashing.
        if not (title_element and company_element and description_element and link_element):
            continue

        job_dictionary = {
            "title": title_element.get_text(strip=True),
            "company": company_element.get_text(strip=True),
            "description": description_element.get_text(strip=True),
            "url": link_element['href'],
        }

        jobs.append(job_dictionary)

    return jobs