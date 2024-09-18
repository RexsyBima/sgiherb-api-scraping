from curl_cffi import requests
from models import SgiherbProduct
from bs4 import BeautifulSoup
from db.models import SgiherbSqlAlchemyItem
from db import session
import pandas as pd
import time
from datetime import datetime


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_item(id: int | str):
    resp = requests.get(
        f"https://sg.iherb.com/ugc/api/product/v2/{id}", impersonate="chrome"
    )
    if resp.status_code == 200:
        data_dict: dict = resp.json()
        if "brandLogoUrl" in data_dict:
            del data_dict["brandLogoUrl"]
        item = SgiherbProduct(**data_dict)
        return item
    else:
        raise Exception(
            f"Failed to get item with id: {id}, status code is {resp.status_code}"
        )


def get_html(url: str):
    resp = requests.get(url, impersonate="chrome")
    if resp.status_code == 200:
        return BeautifulSoup(resp.text, "html.parser")
    else:
        raise Exception(
            f"Failed to get item with url: {url}, status code is {resp.status_code}"
        )


def get_max_page(soup: BeautifulSoup):
    max_page: BeautifulSoup = soup.find_all("a", class_="pagination-link")[-1]
    max_page = int(max_page.get_text())
    return max_page


def save_xlsx():  # query ke sqlalchemy/database
    all_db_items = session.query(SgiherbSqlAlchemyItem).all()

    all_db_items = [item.__dict__ for item in all_db_items]
    for item in all_db_items:
        del item["_sa_instance_state"]
        del item["no"]
    all_db_items = [SgiherbProduct(**item) for item in all_db_items]
    df = pd.DataFrame(all_db_items)
    df.to_excel(f"output-{get_current_date()}.xlsx", index=False)


def save_item_to_db(item: SgiherbProduct):
    dbitem = SgiherbSqlAlchemyItem(**item.__dict__)
    session.add(dbitem)
    session.commit()


def scrape_product_ids_urls(soup: BeautifulSoup):
    card_table: BeautifulSoup = soup.find(
        "div", class_="products product-cells clearfix"
    )
    product_ids_urls: list[BeautifulSoup] = card_table.find_all("a")
    product_ids_urls = [
        (item["data-product-id"], item["href"])
        for item in product_ids_urls
        if item.has_attr("data-product-id") and item.has_attr("href")
    ]
    return product_ids_urls


def check_product_not_exist(id: id):
    product_exist = session.query(SgiherbSqlAlchemyItem).filter_by(id=id).first()
    if product_exist:
        return False
    else:
        return True


if __name__ == "__main__":
    soup = get_html("https://sg.iherb.com/new-products")
    max_p = get_max_page(soup)
    for p in range(1, max_p + 1):
        print(f"accessing page : {p}")
        soup = get_html(f"https://sg.iherb.com/new-products?p={p}")
        product_ids_urls = scrape_product_ids_urls(soup)
        for id, url in product_ids_urls:
            print(f"scraping url = {url}")
            if check_product_not_exist(id):
                item = get_item(id)
                print(item)
                save_item_to_db(item)
                time.sleep(3)
            else:
                print(f"product with id = {id} already exist")
    session.close()


#    item = get_item(143194)
#    print(item)
