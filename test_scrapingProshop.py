from dataclasses import asdict
import unittest
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import scrapingProshop

class TestScrape(unittest.TestCase):

    def test_getnextpage(self):
        url = 'https://www.proshop.dk'
        page_ten = 'https://www.proshop.dk/?s=ASUS&pn=10'
        s = HTMLSession()
        request = s.get(page_ten)
        soup = BeautifulSoup(request.text, 'html.parser')
        next_button = '/?s=ASUS&pn=11'
        page_eleven = url + next_button
        result = scrapingProshop.getnextpage(soup)
        self.assertEqual(result, page_eleven)
        

if __name__ == '__main__':
    unittest.main()


    