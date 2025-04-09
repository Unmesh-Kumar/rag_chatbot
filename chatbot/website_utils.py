import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from collections import deque

from .constants import SUPPORT_SITE_URL, SUPPORT, HTML_PARSER, NEWLINE, P_TAG,\
LI_TAG, H1_TAG, H2_TAG, H3_TAG, A_TAG, HREF_TAG, SITE_REQUEST_TIMEOUT, \
SITE_REQUEST_RETRIES, SITE_REQUEST_BACKOFF

def get_all_support_links(base_url=SUPPORT_SITE_URL, max_pages=10000):
   visited = set()
   to_visit = deque([base_url])
   all_links = []

   while to_visit and len(visited) < max_pages:
      url = to_visit.popleft()
      print(f"visiting url: {url}")
      url = urldefrag(url)[0].rstrip('/')
      if url in visited or SUPPORT not in url:
         continue
      visited.add(url)

      try:
         res = requests.get(url, timeout=10)
         soup = BeautifulSoup(res.text, HTML_PARSER)
         all_links.append(url)

         for a_tag in soup.find_all(A_TAG, href=True):
            link = urljoin(url, a_tag[HREF_TAG])
            link = urldefrag(link)[0].rstrip('/')
            if link.startswith(base_url) and link not in visited:
               to_visit.append(link)

      except Exception as e:
         print(f"Failed to fetch {url}: {e}")
         continue

   return all_links

def extract_text_from_url(url, retries=SITE_REQUEST_RETRIES, backoff=SITE_REQUEST_BACKOFF):
   for attempt in range(retries):
      try:
         response = requests.get(url, timeout=SITE_REQUEST_TIMEOUT)
         response.raise_for_status()
         soup = BeautifulSoup(response.content, HTML_PARSER)
         texts = [tag.get_text(separator=' ', strip=True) for tag in soup.find_all([P_TAG, LI_TAG, H1_TAG, H2_TAG, H3_TAG])]
         return NEWLINE.join(texts)
      except requests.exceptions.Timeout:
         print(f"Timeout while fetching {url} (attempt {attempt + 1}/{retries})")
      except requests.exceptions.RequestException as e:
         print(f"Failed to fetch {url}: {e}")
         break  # skipping retries on non-timeout errors
      time.sleep(backoff * (attempt + 1))
   
   print(f"Giving up on {url}")
   return ""