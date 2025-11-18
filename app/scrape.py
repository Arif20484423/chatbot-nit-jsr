from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json 

# ---- File types we do NOT scrape ----
FILE_EXTENSIONS = [
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".zip", ".rar", ".png", ".jpg", ".jpeg", ".gif", ".csv"
]

visited = set()

def is_file(url):
    clean = url.split("?", 1)[0].split("#", 1)[0].lower()
    return any(clean.endswith(ext) for ext in FILE_EXTENSIONS)

def is_same_domain(url, base_domain):
    return urlparse(url).netloc == base_domain

# ---- Scrape ONE PAGE (dynamic JS fully rendered) ----
def scrape_page(page, url):
    page.goto(url, timeout=60000, wait_until="networkidle")

    # Let React render everything
    page.wait_for_timeout(1500)

    # Small scroll to trigger lazy-loaded components
    for _ in range(3):
        page.mouse.wheel(0, 1500)
        page.wait_for_timeout(300)

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)

    return text, soup


# ---- MAIN CRAWLER (recursive) ----
def crawl_dynamic_site(start_url):
    base_domain = urlparse(start_url).netloc
    queue = [start_url]
    scraped = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 900})

        while queue :
            url = queue.pop(0)
            url = url.split("#")[0]   # normalize

            if url in visited:
                continue
            visited.add(url)

            # Skip external domains
            if not is_same_domain(url, base_domain):
                continue

            # Skip files (pdf/doc/images/zip)
            if is_file(url):
                print("Skipping file:", url)
                continue

            print("Scraping:", url)

            try:
                text, soup = scrape_page(page, url)

                scraped.append({
                    "url": url,
                    "text": text
                })

                # ---- Extract NEW links on this page ----
                for tag in soup.find_all("a", href=True):
                    link = tag["href"]
                    full = urljoin(url, link)
                    full = full.split("#")[0]

                    if (is_same_domain(full, base_domain)
                        and not is_file(full)
                        and full not in visited
                        and full not in queue):
                        queue.append(full)

            except Exception as e:
                print("Error:", e)

        browser.close()

    return scraped


# ------------ Usage ----------------




links = [
    "https://www.nitjsr.ac.in/",
    "https://www.nitjsr.ac.in/Institute/About_NITJSR",
    "https://www.nitjsr.ac.in/Institute/Vision_and_Mission",
    "https://www.nitjsr.ac.in/Institute/Acts_and_Statues",
    "https://www.nitjsr.ac.in/Institute/Board_of_Governers",
    "https://www.nitjsr.ac.in/Institute/Finance_Committee",
    "https://www.nitjsr.ac.in/Institute/Senate",
    "https://www.nitjsr.ac.in/Institute/Vision_and_Mission",
    "https://www.nitjsr.ac.in/Institute/Organizational_Chart",
    "https://www.nitjsr.ac.in/Institute/Ranking_and_Recognition",
    "https://www.nitjsr.ac.in/Institute/Former_Directors",
    "https://www.nitjsr.ac.in/Institute/How_to_Reach",
    "https://www.nitjsr.ac.in/Administration/Visitor",
    "https://www.nitjsr.ac.in/Administration/Chairman,_BOG",
    "https://www.nitjsr.ac.in/Administration/Director",
    "https://www.nitjsr.ac.in/Administration/deputy_director",
    "https://www.nitjsr.ac.in/Administration/Registrar",
    "https://www.nitjsr.ac.in/Administration/Deans",
    "https://www.nitjsr.ac.in/Administration/Associate_Deans",
    "https://www.nitjsr.ac.in/Administration/Head_of_Departments",
    "https://www.nitjsr.ac.in/Administration/Chief_Vigilance_Officer",
    "https://www.nitjsr.ac.in/academic/Academics",
    "https://www.nitjsr.ac.in/academic/Admissions",
    "https://www.nitjsr.ac.in/academic/People",
    "https://www.nitjsr.ac.in/academic/Departments",
    "https://www.nitjsr.ac.in/academic/Curriculum",
    "https://www.nitjsr.ac.in/academic/Student_Statistics",
    "https://www.nitjsr.ac.in/academic/Fee_Structure",
    "https://www.nitjsr.ac.in/academic/Semester_Schedule",
    "https://www.nitjsr.ac.in/academic/Ordinance",
    "https://www.nitjsr.ac.in/academic/Academic_Documents",
    "https://www.nitjsr.ac.in/Students/Placements",
    "https://www.nitjsr.ac.in/Students/News-and-Achievements",
    "https://www.nitjsr.ac.in/Students/Student-Activities",
    "https://www.nitjsr.ac.in/Students/Financial-Assistance",
    "https://www.nitjsr.ac.in/Students/Hostel-Management",
    "https://www.nitjsr.ac.in/Students/Wardens",
    "https://www.nitjsr.ac.in/Students/Anti-Ragging",
    "https://www.nitjsr.ac.in/Students/Health-and-Welfare",
    "https://www.nitjsr.ac.in/Students/Life-@NIT-JSR",
    "https://www.nitjsr.ac.in/Students/Student-Council",
    "https://www.nitjsr.ac.in/facilities/Computer_Center",
    "https://www.nitjsr.ac.in/People/Faculty",
    "https://www.nitjsr.ac.in/People/Staff",
    "https://www.nitjsr.ac.in/People/Other%20Administration",
    "https://www.nitjsr.ac.in/Tender/Active_Tenders",
    "https://www.nitjsr.ac.in/Tender/All_Tenders",
    "https://www.nitjsr.ac.in/Tender/Contact_Us",
    "https://www.nitjsr.ac.in/Tender/Useful_Links",
    "https://www.nitjsr.ac.in/Notices/Announcements",
    "https://www.nitjsr.ac.in/Notices/Office_Orders",
    "https://www.nitjsr.ac.in/Notices/Students",
    "https://www.nitjsr.ac.in/Recruitments",
    "https://www.nitjsr.ac.in/Notices/Archive_Notices",
    "https://www.nitjsr.ac.in/Cell/SC-ST_Cell",
    "https://www.nitjsr.ac.in/Cell/IPR_Cell",
    "https://www.nitjsr.ac.in/Cell/Grievance_Cell",
    "https://www.nitjsr.ac.in/Cell/Reservation_Cell",
    "https://www.nitjsr.ac.in/Cell/Publication_Cell",
    "https://www.nitjsr.ac.in/Cell/Public_Relation_Cell",
    "https://www.nitjsr.ac.in/Cell/Hindi_Cell",
    "https://www.nitjsr.ac.in/Cell/Internal_Complaints_Committee(ICC)",
    "https://www.nitjsr.ac.in/facilities/Central_Library",
    "https://www.nitjsr.ac.in/facilities/Medical_Facilities",
    "https://www.nitjsr.ac.in/facilities/Computer_Center",
    "https://www.nitjsr.ac.in/facilities/Safety_and_Security",
    "https://www.nitjsr.ac.in/facilities/Guest_House",
    "https://www.nitjsr.ac.in/facilities/Transport",
    "https://www.nitjsr.ac.in/Recruitments",
    "https://www.nitjsr.ac.in/RTI"
]

scraped_data = []
for link in links:
    scraped_data.extend(crawl_dynamic_site(link))

with open("scraped_data.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4, ensure_ascii=False)
    
print("Saved to scraped_data.json")
