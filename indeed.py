import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page():
  result = requests.get(URL)

  # html의 모든 text를 가져옴.
  # print(indeed_result.text)

  # beautifulsoup4 install
  soup = BeautifulSoup(result.text, "html.parser")

  # 해당 웹사이트를 '검사', class name = "pagination"
  pagination = soup.find("div", {"class":"pagination"})
  links = pagination.find_all('a')
  pages = []

  for link in links[:-1]:
    pages.append(int(link.string))
  # pages.append(link.find("span").string)
  # link에 string 요소가 하나만 있기 때문에 가능.

  max_page = pages[-1]  #last page nunber
  
  return max_page


def extract_job(html):
  # results : 일자리 목록, 중에서 div, class 이름이 title, 중에서 anchor를 찾고 title을
  title = html.find("div", {"class":"title"}).find("a")["title"]
  company = html.find("span", {"class":"company"})
  if company:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = company.find("a").string
    else:
      company = company.string
    company = company.strip()
  else:
    company = None

  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]

  return {
    "title": title, 
    "company": company, 
    "location":location,
    "link" : f"https://www.indeed.com/viewjob?jk={job_id}"
  }

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    # result : html 요소의 list
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs



  