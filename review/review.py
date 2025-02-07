from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

def get_restaurant_review_tags(driver, restaurant_name):
    """
    가게 상세보기 페이지에서 태그 정보를 가져오는 함수.
    """
    try:
        print(f"▶ {restaurant_name}의 태그 크롤링 시작...")

        # `view_likepoint` 안에 있는 모든 `chip_likepoint` 요소 가져오기
        tag_elements = driver.find_elements(By.CLASS_NAME, "chip_likepoint")

        for tag in tag_elements:
            try:
                tag_name = tag.find_element(By.CLASS_NAME, "txt_likepoint").text.strip()  # 태그 이름 (예: "맛")
                tag_count = tag.find_element(By.CLASS_NAME, "num_likepoint").text.strip()  # 태그 숫자 (예: "7")

                restaurant_tag_data.append([restaurant_name, tag_name, tag_count])

            except Exception as e:
                print(f"❌ 태그 크롤링 실패: {e}")

        print(f"✅ {restaurant_name} 태그 크롤링 완료! ({len(tag_elements)}개)")

    except Exception as e:
        print(f"❌ {restaurant_name} 태그 크롤링 실패:", e)


def get_restaurant_review_details(driver, restaurant_name):
    """
    가게 상세보기 페이지에서 개별적인 리뷰 정보를 가져오는 함수.
    """

def get_restaurant_info(driver, button, index):
    """
    가게 상세보기 페이지에서 가게 정보를 가져오는 함수.
    """

    try:
        print(f"▶ {index + 1}번째 가게 상세보기 클릭 중...")

        driver.execute_script("window.open(arguments[0].href, '_blank');", button)

        driver.switch_to.window(driver.window_handles[-1])

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "place_details")))

        try:
            name = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/h2').text.strip()
        except:
            name = "정보 없음"

        try:
            rating = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div[2]/a[1]/span[1]').text.strip()
        except:
            rating = "정보 없음"

        try:
            review_count = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div[2]/a[2]/span').text.strip()
        except:
            review_count = "정보 없음"

        restaurant_info_data.append([name, rating, review_count])

        print(f"✅ {index + 1}번째 가게 크롤링 완료: {name} (⭐ {rating}, 리뷰 {review_count}개)")

        # ✅ 태그 정보 크롤링 추가
        get_restaurant_review_tags(driver, name)
        get_restaurant_review_details(driver, name)

        driver.close()

        driver.switch_to.window(driver.window_handles[0])

        time.sleep(1)

    except Exception as e:
        print(f"❌ {index + 1}번째 가게 크롤링 실패:", e)


# 크롬 드라이버 실행
driver = webdriver.Chrome()

url = "https://map.kakao.com"
driver.get(url)

input_tag = driver.find_element(By.ID, "search.keyword.query")

search_query = "대전 장대동 짜장면"
input_tag.send_keys(search_query)
input_tag.send_keys(Keys.RETURN)

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "placelist")))
time.sleep(3)

detail_buttons = driver.find_elements(By.CLASS_NAME, "moreview")

print(f"✅ 검색된 가게 수: {len(detail_buttons)}개")

restaurant_info_data = []
restaurant_tag_data = []
restaurant_review_data = []

# 테스트 모드로 2개만 실행
for idx, button in enumerate(detail_buttons[:2]):
    get_restaurant_info(driver, button, idx)

driver.quit()

df_restaurant = pd.DataFrame(restaurant_info_data, columns=["이름", "평점", "리뷰 수"])
df_restaurant.to_csv("카카오_맛집_데이터.csv", index=False, encoding="utf-8-sig")

df_tags = pd.DataFrame(restaurant_tag_data, columns=["가게 이름", "태그 이름", "태그 수"])
df_tags.to_csv("카카오_태그_데이터.csv", index=False, encoding="utf-8-sig")

print("📄 CSV 파일 저장 완료: 카카오_맛집_데이터.csv")
print("📄 CSV 파일 저장 완료: 카카오_태그_데이터.csv")