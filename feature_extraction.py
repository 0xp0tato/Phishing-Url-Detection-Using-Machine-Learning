import ipaddress
import re
import urllib
from bs4 import BeautifulSoup
import socket
import requests
import whois
from datetime import datetime
import time
from dateutil.parser import parse as date_parse

# Calculates number of months
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

# Generate data set by extracting the features from the URL
def generate_data_set(url):

    data_set = []

    # Converts the given URL into standard format
    if not re.match(r"^https?", url):
        url = "http://" + url


    # Stores the response of the given URL
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        response = ""


    # Extracts domain from the given URL
    domain = re.findall(r"://([^/]+)/?", url)[0]
    if re.match(r"^www.",domain):
	       domain = domain.replace("www.","")

    # Requests all the information about the domain
    whois_response = whois.whois(domain)

    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })

    # Extracts global rank of the website
    try:
        global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        global_rank = -1

    # having_IP_Address
    try:
        ipaddress.ip_address(url)
        data_set.append(-1)
    except:
        data_set.append(1)

    # URL_Length
    if len(url) < 54:
        data_set.append(1)
    elif len(url) >= 54 and len(url) <= 75:
        data_set.append(0)
    else:
        data_set.append(-1)

    # Shortining_Service
    if re.findall("goo.gl|bit.ly", url):
        data_set.append(-1)
    else:
        data_set.append(1)

    # having_At_Symbol
    if re.findall("@", url):
        data_set.append(-1)
    else:
        data_set.append(1)

    # double_slash_redirecting
    if re.findall(r"[^https?:]//",url):
        data_set.append(1)
    else:
        data_set.append(-1)

    # Prefix_Suffix
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        data_set.append(-1)
    else:
        data_set.append(1)

    # having_Sub_Domain
    if len(re.findall("\.", url)) == 1:
        data_set.append(-1)
    elif len(re.findall("\.", url)) == 2:
        data_set.append(0)
    else:
        data_set.append(1)

    # SSLfinal_State
    data_set.append(-1)

    # Domain_registeration_length
    expiration_date = whois_response.expiration_date
    try:
        expiration_date = min(expiration_date)
    except:
        pass

    today = time.strftime('%Y-%m-%d')
    today = datetime.strptime(today, '%Y-%m-%d')
    registration_length = abs((expiration_date - today).days)

    if registration_length / 365 <= 1:
        data_set.append(-1)
    else:
        data_set.append(1)

    # Favicon
    try:
        if re.search(r"<link rel=\"icon\"", response.text):
            data_set.append(1)
        else:
            data_set.append(-1)
    except:
        dataset.append(-1)

    # port
    try:
        port = domain.split(":")[1]
        if port:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # HTTPS_token
    if re.findall("^https\-", url):
        data_set.append(1)
    else:
        data_set.append(-1)

    # Request_URL
    i = 0
    success = 0
    for img in soup.find_all('img', src= True):
       dots= [x.start(0) for x in re.finditer('\.', img['src'])]
       if url in img['src'] or domain in img['src'] or len(dots)==1:
          success = success + 1
       i=i+1

    for audio in soup.find_all('audio', src= True):
       dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
       if url in audio['src'] or domain in audio['src'] or len(dots)==1:
          success = success + 1
       i=i+1

    for embed in soup.find_all('embed', src= True):
       dots=[x.start(0) for x in re.finditer('\.',embed['src'])]
       if url in embed['src'] or domain in embed['src'] or len(dots)==1:
          success = success + 1
       i=i+1

    for iframe in soup.find_all('iframe', src= True):
       dots=[x.start(0) for x in re.finditer('\.',iframe['src'])]
       if url in iframe['src'] or domain in iframe['src'] or len(dots)==1:
          success = success + 1
       i=i+1

    try:
       percentage = success/float(i) * 100
    except:
        data_set.append(1)

    if percentage < 22.0 :
       dataset.append(1)
    elif((percentage >= 22.0) and (percentage < 61.0)) :
       data_set.append(0)
    else :
       data_set.append(-1)


    # URL_of_Anchor
    i = 0
    unsafe=0
    for a in soup.find_all('a', href=True):
    # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
            # there in the actual a['href']
        if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
            unsafe = unsafe + 1
        i = i + 1
        # print a['href']
    try:
        percentage = unsafe / float(i) * 100
    except:
        data_set.append(1)
    if percentage < 31.0:
        data_set.append(1)
        # return percentage
    elif ((percentage >= 31.0) and (percentage < 67.0)):
        data_set.append(0)
    else:
        data_set.append(-1)

    # Links_in_tags
    i=0
    success =0
    for link in soup.find_all('link', href= True):
       dots=[x.start(0) for x in re.finditer('\.',link['href'])]
       if url in link['href'] or domain in link['href'] or len(dots)==1:
          success = success + 1
       i=i+1

    for script in soup.find_all('script', src= True):
       dots=[x.start(0) for x in re.finditer('\.',script['src'])]
       if url in script['src'] or domain in script['src'] or len(dots)==1 :
          success = success + 1
       i=i+1
    try:
        percentage = success / float(i) * 100
    except:
        data_set.append(1)

    if percentage < 17.0 :
       data_set.append(1)
    elif((percentage >= 17.0) and (percentage < 81.0)) :
       data_set.append(0)
    else :
       data_set.append(-1)

    # SFH
    for form in soup.find_all('form', action= True):
       if form['action'] =="" or form['action'] == "about:blank" :
          data_set.append(-1)
          break
       elif url not in form['action'] and domain not in form['action']:
           data_set.append(0)
           break
       else:
             data_set.append(1)
             break

    # Submitting_to_email
    if re.findall(r"[mail\(\)|mailto:?]", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # Abnormal_URL
    if response.text == "":
        data_set.append(1)
    else:
        data_set.append(-1)

    # Redirect
    if len(response.history) <= 1:
        data_set.append(-1)
    elif len(response.history) <= 4:
        data_set.append(0)
    else:
        data_set.append(1)

    # on_mouseover
    if re.findall("<script>.+onmouseover.+</script>", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # RightClick
    if re.findall(r"event.button ?== ?2", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # popUpWidnow
    if re.findall(r"alert\(", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # Iframe
    if re.findall(r"[<iframe>|<frameBorder>]", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # age_of_domain
    try:
        registration_date = re.findall(r'Registration Date:</div><div class="df-value">([^<]+)</div>', whois_response.text)[0]
        if diff_month(date.today(), date_parse(registration_date)) >= 6:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # DNSRecord
    data_set.append(-1)

    # web_traffic
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # Page_Rank
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # Google_Index
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # Links_pointing_to_page
    number_of_links = len(re.findall(r"<a href=", response.text))
    if number_of_links == 0:
        data_set.append(1)
    elif number_of_links <= 2:
        data_set.append(0)
    else:
        data_set.append(-1)

    # Statistical_report
    data_set.append(-1)

    print (data_set)
    return data_set
