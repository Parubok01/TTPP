from playwright.sync_api import sync_playwright

class BrowserFactory:
    @staticmethod
    def get_browser(browser_type="chromium", headless=True):
        playwright = sync_playwright().start()

        if browser_type == "chromium":
            return playwright, playwright.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            return playwright, playwright.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            return playwright, playwright.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")