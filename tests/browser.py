"""Run against a local server or the production container stack."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
if __name__=="__main__":
    base=os.getenv("BASE_URL","http://localhost:8000")
    out=Path("test-results");out.mkdir(exist_ok=True)
    with sync_playwright() as runner:
        browser=runner.chromium.launch(executable_path=os.getenv("CHROME_PATH"))
        page=browser.new_page(viewport={"width":1440,"height":960})
        page.goto(base);page.get_by_role("button",name="Skip",exact=True).click()
        page.locator("#theme").select_option("day");page.reload()
        expect(page.locator("html")).to_have_attribute("data-theme","day")
        expect(page.locator(".boot")).to_be_hidden()
        page.screenshot(path=out/"desktop.png")
        page.locator('.dock a[aria-label="Projects"]').click()
        page.locator('a.project').first.click()
        expect(page.get_by_role("heading",name="LabQuest",exact=True)).to_be_visible()
        page.goto(base+"/#about")
        page.get_by_role("button",name="Notebook").focus()
        expect(page.locator(".workspace [aria-live]")).to_contain_text("Linux")
        page.get_by_role("button",name="Python",exact=True).click()
        expect(page.locator(".layer").last).to_contain_text("API and data")
        page.locator("#theme").select_option("night")
        expect(page.locator("html")).to_have_attribute("data-theme","night")
        page.goto(base+"/blog");page.get_by_role("searchbox").fill("Linux")
        expect(page.locator("#results")).to_contain_text("published")
        phone=browser.new_page(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,reduced_motion="reduce")
        phone.goto(base);expect(phone.locator(".boot")).to_be_hidden()
        assert phone.evaluate("document.documentElement.scrollWidth<=innerWidth")
        expect(phone.locator("#scene img")).to_be_attached()
        phone.screenshot(path=out/"mobile.png")
        browser.close()
