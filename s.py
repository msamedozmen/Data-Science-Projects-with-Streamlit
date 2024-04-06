import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

base_url = "https://books.toscrape.com/"

def extract_books_from_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    book_containers = soup.find_all("article", class_="product_pod")
    book_names = [book.h3.a["title"] for book in book_containers]
    return category_url.split("/")[-2], book_names  
if __name__ == "__main__":
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    category_links = [base_url + a["href"] for a in soup.find_all("a", href=lambda href: href and "/category/books/" in href)]

    with Pool() as pool:
        results = pool.map(extract_books_from_category, category_links)

    # Create dictionary from results
    category_books = dict(results)

    print(category_books)