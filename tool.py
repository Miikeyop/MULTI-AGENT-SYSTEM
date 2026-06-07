from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from rich import print
import requests
from bs4 import BeautifulSoup


tavily=TavilySearch(max_results=5)

@tool
def web_search(query:str)->str:
    """search the web for recent and reliable information on the topic. Returns title URL and small snippet"""
    result=tavily.invoke({"query":query})
    out=[]
    for r in result["results"]:
        out.append(
            f"title:{r['title']} \n URL:{r['url']} \n content:{r['content'][:300]}"
        )
    return "\n\n".join(out)

@tool
def scrape_url(url:str)->str:
    """"Scrape and return the clean ccontent for bettern understandin"""
    try:
        req=requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        soup=BeautifulSoup(req.text,"html.parser")
        
        for tag in soup(['script','style','nav','footer']):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"Error scraping the url: {str(e)}"
    

    


