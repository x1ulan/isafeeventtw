import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

TIMES = 60
SITE_URL = "https://isafeevent.moe.edu.tw"
LOGIN_OK_SELECTOR = "button[data-href=\"/member/\"]" 

ANSWERS = [
    "NoUse", 2, 3, 2, 4, 2, 3, 1, 4, 3, 3, 2, 3,
    3, 2, 2, 3, 3, 2, 4, 2, 4, 1, 3, 2,
    4, 2, 2, 4, 2, 2, 2, 1, 2, 4, 3, 3,
    3, 4, 1, 4, 2, 2, 3, 3, 3, 2, 2, 2
]

driver = webdriver.Chrome()

try:
    driver.get(SITE_URL)
    WebDriverWait(driver, 300).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, LOGIN_OK_SELECTOR)
    )
    cookies = driver.get_cookies()
finally:
    driver.quit()

s = requests.Session()
s.headers.update({
    "Referer": SITE_URL + "/",
    "User-Agent": "Mozilla/5.0",
})

for cookie in cookies:
    s.cookies.set(
        cookie["name"],
        cookie["value"],
        domain=cookie["domain"],
        path=cookie.get("path", "/"),
    )

if not s.cookies.get("sessionid"):
    raise RuntimeError("Login failed: No sessionid found.")

csrftoken = s.cookies.get("csrftoken")
if not csrftoken:
    raise RuntimeError("Login failed: No csrftoken found.")

for i in range(TIMES):
    req = s.post(
        f"{SITE_URL}/ajax/exam/get/",
        data={
            "exam": "",
            "target": "01",
            "csrfmiddlewaretoken": csrftoken,
        },
        timeout=10,
    )
    req.raise_for_status()
    examid = req.json()["exam"]

    req2 = s.post(
        f"{SITE_URL}/ajax/exam/answer2/",
        data={
            "exam": examid,
            "csrfmiddlewaretoken": csrftoken,
            "answers": ",".join(["5"] * 16),
        },
        timeout=10,
    )
    req2.raise_for_status()

    req3 = s.get(f"{SITE_URL}/exam/do/{examid}", timeout=10)
    req3.raise_for_status()

    soup = BeautifulSoup(req3.text, "html.parser")
    questions = soup.select(".question")

    answers = []
    for q in questions:
        option = q.select_one("input[id^='q_']")
        if option is None:
            raise ValueError("Fail to get questions.")

        qid = int(option["id"].split("_")[1])
        answers.append(str(ANSWERS[qid]))

    req4 = s.post(
        f"{SITE_URL}/ajax/exam/answer/",
        data={
            "exam": examid,
            "csrfmiddlewaretoken": csrftoken,
            "answers": ",".join(answers),
        },
        timeout=10,
    )
    req4.raise_for_status()

    print(f"[{i+1:02d}] {','.join(answers)}")