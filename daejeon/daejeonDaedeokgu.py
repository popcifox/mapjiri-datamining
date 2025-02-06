from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# 크롬 드라이버 실행
driver = webdriver.Chrome()

# 대전광역시 행정동 목록 페이지 열기
url = "https://www.daejeon.go.kr/drh/DrhContentsHtmlView.do?menuSeq=1716"
driver.get(url)
time.sleep(3)

# 대덕구 행정동 개수 가져오기
daedeokgu_count_element = driver.find_element(By.CSS_SELECTOR, "#cont-body > div > div.b_table > div > table > tbody > tr:nth-child(76) > td:nth-child(2)")
daedeokgu_count = int(daedeokgu_count_element.text.strip())

daedeokgu_list = []

# 대덕구 행정동 리스트 가져오기
for i in range(daedeokgu_count):
    if i == 0:
        dong_element = driver.find_element(By.CSS_SELECTOR, "#cont-body > div > div.b_table > div > table > tbody > tr:nth-child(77) > td:nth-child(2)")
    else:
        dong_element = driver.find_element(By.CSS_SELECTOR, f"#cont-body > div > div.b_table > div > table > tbody > tr:nth-child({i + 77}) > td:nth-child(1)")

    dong = dong_element.text.strip()
    daedeokgu_list.append(dong)

# 크롬 드라이버 종료
driver.quit()

# 데이터프레임 생성 후 CSV 저장
df = pd.DataFrame(daedeokgu_list, columns=["행정동"])
df.to_csv("대전광역시_대덕구_행정동.csv", index=False, encoding="utf-8-sig")

print("✅ 대덕구 행정동 리스트 CSV 저장 완료! (대전광역시_대덕구_행정동.csv)")
