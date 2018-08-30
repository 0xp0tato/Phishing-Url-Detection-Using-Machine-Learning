import ipaddress
import re
import urllib
from datetime import timedelta
from google import google
import phishtank
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
    today = time.strftime('%Y-%m-%d')
    today = datetime.strptime(today, '%Y-%m-%d')
    registration_length = abs((expiration_date - today).days)

    if registration_length / 365 <= 1:
        data_set.append(-1)
    else:
        data_set.append(1)

    # Favicon
    data_set.append(-1)

    # port
    try:
        port = domain.split(":")[1]
        if port:
            data_set.append(1)
        else:
            data_set.append(-1)
    except:
        data_set.append(-1)

    # HTTPS_token
    if re.findall("^https\-", domain):
        data_set.append(-1)
    else:
        data_set.append(1)

    # Request_URL
    data_set.append(-1)

    # URL_of_Anchor
    data_set.append(-1)

    # Links_in_tags
    data_set.append(-1)

    # SFH
    data_set.append(0)

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
