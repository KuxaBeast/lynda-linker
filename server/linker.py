import string
import requests
from bs4 import BeautifulSoup
import youtube_dl
import sys
from http import cookiejar

class LyndaAuth(object):
  def __init__(self, cookies="lynda.txt"):
    self.cookies = cookies

  def lyndaLogin(self, org, card_num, card_pin):
    login_url = "https://www.lynda.com/portal/sip?org=" + org
    s = requests.session()

    s.cookies = cookiejar.MozillaCookieJar()

    response = s.get(login_url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    seasurf = soup.find("input", {"type": "hidden", "id": "seasurf"}).attrs["value"]
    # print(seasurf)

    response = s.post(login_url, {"libraryCardNumber": card_num, "libraryCardPin": card_pin, "libraryCardPasswordVerify": None, "org": org, "currentView": "login", "seasurf": seasurf})
    print("Cookies are restored.", file=sys.stderr)
    s.cookies.save(self.cookies)
    #print(response.text)
    #print(s.cookies)

  def loginStatus(self):
    cjar = cookiejar.MozillaCookieJar(self.cookies)
    cjar.load()
    for cookie in cjar:
      if cookie.name == "LyndaLoginStatus":
        if cookie.value != "Member-Logged-In":
          print("Tryin' to restore cookies.", file=sys.stderr)
          return False
        return True


class LyndaLinker(object):
  def __init__(self, cookies="lynda.txt"):
    self.cookies = cookies

  def lyndaDownload(self, courseid, videoid, quality):
    ydl_opts = { "cookiefile": self.cookies, "format": quality, "skip_download": True, "no_warnings": True }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      data = ydl.extract_info('https://www.lynda.com/path/video/' + courseid + '/' + videoid + '.html', download=False)
      #print("URL TO RETURN: " + data["url"])
      return data["url"]
      #ydl.download([url])

  def checkUrl(self, url):
    # try:
    #   url.index("https://www.lynda.com/")
    # except:
    #   return False

    split_url = url.split('/')
    try:
      if split_url[0] != 'https:' and split_url[2] != 'www.lynda.com':
        return False

      int(split_url[5])
      spl0 = split_url[6].split('.')[0].split('-')
      int(spl0[0])
      int(spl0[1])
    except:
      return False
    return True

  # deprecated
  def parseUrl(self, url):
    if self.checkUrl(url):
      split_url = url.split('/')
      return [split_url[5], split_url[6].split('.')[0]]
    else:
      print("Address not valid", file=sys.stderr)
      return None
    
  def get_link(self, courseid, videoid, qual = None):
    qual_opts = {
      "360": "best[height=360]",
      "540": "best[height=540]",
      "720": "best[height=720]"
    }

    org = "organisation.org"
    lib_card_num = "yournum"
    lib_card_pin = "yourpin"

    try:
      quality = qual_opts[qual]
    except:
      quality = "best"

    #print(qual)

    auth = LyndaAuth(self.cookies)

    for i in range(2):
      if not auth.loginStatus():
        auth.lyndaLogin(org, lib_card_num, lib_card_pin)
      try:
        return self.lyndaDownload(courseid, videoid, quality)
      except youtube_dl.utils.DownloadError:
        print("Download fucked up, but tryin' to repair.", file=sys.stderr)
