import logging
from playwright.sync_api import sync_playwright, expect

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Клас POM для сторінки пошуку
class SearchPagePOM:
    def __init__(self, page):
        self.page = page
        self.page.goto("https://react.dev/")
        self.search_button = page.locator('//*[@id="__next"]/div[3]/nav/div/div[2]/button')
        self.search_input = page.locator('input[class="DocSearch-Input"]')
        self.search_results = page.locator('section[class="DocSearch-Hits"]')
        self.search_hit_source = page.locator('div.DocSearch-Hit-source', has_text="React APIs")

    def perform_search(self, query):
        self.search_button.click()
        self.page.wait_for_selector('input[class="DocSearch-Input"]', timeout=10000)
        self.search_input.fill(query)
        self.page.wait_for_selector('section[class="DocSearch-Hits"]', timeout=10000)

    def check_search_results(self):
        expect(self.search_hit_source).to_be_visible(timeout=10000)
        self.page.screenshot(path="react_search_results.png")

# Тест 1: Пошук у документації (POM, адаптація вашого тесту)
def test_search_react_docs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            search_page = SearchPagePOM(page)
            search_page.perform_search("useState")
            search_page.check_search_results()
            logger.info("Test search React docs with POM passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_search_error.png")
            raise
        finally:
            browser.close()

# Тест 2: Перевірка заголовка головної сторінки
def test_homepage_title():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("https://react.dev/")
            expect(page).to_have_title("React")
            page.screenshot(path="react_homepage_title.png")
            logger.info("Test homepage title passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_title_error.png")
            raise
        finally:
            browser.close()

# Тест 3: Перехід до розділу "Learn"
def test_navigate_to_learn():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("https://react.dev/")
            page.click('a[href="/learn"]')
            expect(page).to_have_url("https://react.dev/learn")
            page.screenshot(path="react_learn_page.png")
            logger.info("Test navigate to Learn passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_learn_error.png")
            raise
        finally:
            browser.close()

# Тест 4: Перевірка видимості посилання на GitHub у футері (виправлено)
def test_footer_github_link():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("https://react.dev/")
            github_link = page.locator('a[href="https://github.com/facebook/react"]')
            expect(github_link).to_be_visible(timeout=10000)
            page.screenshot(path="react_github_link.png")
            logger.info("Test footer GitHub link passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_github_error.png")
            raise
        finally:
            browser.close()

# Тест 5: Перевірка адаптивності головної сторінки
def test_homepage_responsive():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.set_viewport_size({"width": 360, "height": 640})
            page.goto("https://react.dev/")
            language_button = page.locator('//*[@id="__next"]/div[3]/nav/div/div[3]/div[3]/div[4]/a')
            expect(language_button).to_be_visible(timeout=10000)
            page.screenshot(path="react_homepage_responsive.png")
            logger.info("Test homepage responsive passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_responsive_error.png")
            raise
        finally:
            browser.close()

# Тест 6: Перехід до розділу "Reference"
def test_navigate_to_reference():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("https://react.dev/")
            page.click('//*[@id="__next"]/div[4]/main/article/div/div[1]/div[2]/a[2]')
            expect(page).to_have_url("https://react.dev/reference/react")
            page.screenshot(path="react_reference_page.png")
            logger.info("Test navigate to Reference passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_reference_error.png")
            raise
        finally:
            browser.close()

# Тест 7: Перевірка видимості кнопки пошуку
def test_search_button_visible():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("https://react.dev/")
            search_button = page.locator('//*[@id="__next"]/div[3]/nav/div/div[2]/button')
            expect(search_button).to_be_visible(timeout=10000)
            page.screenshot(path="react_search_button.png")
            logger.info("Test search button visibility passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_button_error.png")
            raise
        finally:
            browser.close()

# Тест 8: Перехід до розділу "Community"
def test_navigate_to_community():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("https://react.dev/")
            page.click('a[href="/community"]')
            expect(page).to_have_url("https://react.dev/community")
            page.screenshot(path="react_community_page.png")
            logger.info("Test navigate to Community passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_community_error.png")
            raise
        finally:
            browser.close()

# Тест 9: Перевірка валідності поля пошуку
def test_theme_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("https://react.dev/")
            page.click('//*[@id="__next"]/div[3]/nav/div/div[3]/div[3]/div[2]/button')
            expect(page.locator('html[class="paltform-win.dark"]'))
            page.screenshot(path="test_theme_button.png")
            logger.info("Test theme button validation passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_input_error.png")
            raise
        finally:
            browser.close()

# Тест 10: Перевірка видимості прикладу коду на сторінці "Learn"
def test_copy_code_snippet():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("https://react.dev/learn/react-compiler", timeout=30000)
            copy_button = page.locator('//*[@id="__next"]/div[4]/main/article/div/div[2]/div[1]/div/div[5]/div[1]/div/div[2]/button').first
            expect(copy_button).to_be_visible(timeout=10000)
            copy_button.click()
            page.screenshot(path="react_code_copied.png")
            logger.info("Test copy code snippet passed successfully.")
        except Exception as e:
            logger.error(f"Test failed: {e}")
            page.screenshot(path="react_code_copy_error.png")
            raise
        finally:
            browser.close()

# Виконання всіх тестів
if __name__ == "__main__":
    test_search_react_docs()
    test_homepage_title()
    test_navigate_to_learn()
    test_footer_github_link()
    test_homepage_responsive()
    test_navigate_to_reference()
    test_search_button_visible()
    test_navigate_to_community()
    test_theme_button()
    test_copy_code_snippet()