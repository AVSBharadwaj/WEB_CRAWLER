import re
import requests
from urllib.parse import urlparse 
class crawler(object):
    def __init__(self,start_url):
        self.start_url = start_url
        self.vis=set()
    def getHtml(self,url):
        try:
            html=requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')
    def getLinks(self,url):
        html=self.getHtml(url)
        
        parsed=urlparse(url)
        
        base=f"{parsed.scheme}://{parsed.netloc}"
        
        links=re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''',html)   

        for i,link in enumerate(links):
            if not urlparse(link).netloc:
                link_base=base+link
                links[i]=link_base

        return set(filter(lambda x:'mailto' not in x,links))

    def extract_info(self,url):
        html=self.getHtml(url)

        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)
        return dict(meta)

    def crawl(self,url):
        for link in self.getLinks(url):
            if link in self.vis:
                continue
            self.vis.add(link)

            info=self.extract_info(link)
            print(f"""Link: {link}  Description: {info.get('description')} Keywords: {info.get('keywords')}    
            """) 

            self.crawl(link)



    def start(self):
        self.crawl(self.start_url)


if __name__=="__main__":
    crawl=crawler("https://google.com")

    crawl.start()