import urllib.request

from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, source):
        self.source = source
        self.final_array = []

    def get_final_data(self) -> list:
        if self.source == 'excelsior':
            page = 0
            titles = []
            descriptions = []
            anchors = []
            while page < 5:
                data = urllib.request.urlopen(
                f'https://www.excelsior.com.mx/ultima-hora?page={page}').read().decode()
                soup = BeautifulSoup(data, 'html.parser')
                titles += soup.find_all('span', class_='ultima-hora-title')
                descriptions += soup.find_all('span', class_='ultima-hora-summary')
                anchors += soup.select(
                    'div.widget-content2.ultima-hora-content-wrapper > ul > li > a')
                page += 1
            if len(titles) == len(descriptions) and len(titles) == len(anchors):
                for i in range(len(titles)):
                    self.final_array.append({
                        "content": descriptions[i].text,
                        "reference": "https://" + anchors[i].get('href')[2:]
                    })
                return self.final_array
            return []
        elif self.source == 'milenio':
            data = urllib.request.urlopen(
                'https://www.milenio.com/ultima-hora').read().decode()
            soup = BeautifulSoup(data, 'html.parser')
            titles = soup.find_all('div', class_='title')
            descriptions = soup.find_all('div', class_='summary')
            anchors = soup.select('div.title-container > div.title > a')
            if len(titles) == len(descriptions) and len(titles) == len(anchors):
                for i in range(len(titles)):
                    self.final_array.append({
                        "content": descriptions[i].text.replace('\n', ''),
                        "reference": "https://www.milenio.com" + anchors[i].get('href')
                    })
                return self.final_array
            return []
        elif self.source == '20minutos':
            page = 1
            titles = []
            descriptions = []
            anchors = []
            while page < 5:
                data = urllib.request.urlopen(
                f'https://www.20minutos.com.mx/minuteca/ciudad-de-mexico/{page}/').read().decode()
                soup = BeautifulSoup(data, 'html.parser')
                titles += soup.select('div.media-content > header > h1 > a')
                descriptions += soup.find_all('div', class_="media-intro")
                anchors += soup.select('div.media-content > header > h1 > a')
                page += 1
            if len(titles) == len(descriptions) and len(titles) == len(anchors):
                for i in range(len(titles)):
                    self.final_array.append({
                        "content": descriptions[i].text.replace('\n', '').strip(),
                        "reference": anchors[i].get('href')
                    })
                return self.final_array
        else:
            return []