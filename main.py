
from bs4 import BeautifulSoup
from datetime import datetime

import requests
import json
import re

def format_numbers(num: int) -> str:
    if num >= 1000000:
        return str(num // 1000000) + 'M'
    elif num >= 1000:
        return str(num // 1000) + 'K'
    else:
        return str(num)
    
def TikTok(username: str) -> None:
    """Get TikTok account info

    Parameters:
        username (``str``):
            pass username with or without "@" or pass link.
    """

    match = re.search(r'@([^/?#]+)', username)
    username = match.group(1)

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 GIVT"}
    r = requests.get(f"https://www.tiktok.com/@{username}", headers=headers)

    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        script_tag = soup.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
        script_text = script_tag.text.strip()
        json_data = json.loads(script_text)["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
    except:
        input("[X] Error : Username Not Found .")
    
    user = json_data["user"]
    
    url_id = int(user["id"])
    binary = "{0:b}".format(url_id)
    i = 0
    bits = ""
    while i < 31:
        bits += binary[i]
        i += 1
    timestamp = int(bits, 2)
    creation_date = datetime.fromtimestamp(timestamp)

    nickNameModifyTime = user.get("nickNameModifyTime", "Never")
    last_change_name = "Never" if nickNameModifyTime == 0 else datetime.fromtimestamp(nickNameModifyTime)

    uniqueIdModifyTime = user.get("uniqueIdModifyTime", "Never")
    last_change_username = "Never" if uniqueIdModifyTime == 0 else datetime.fromtimestamp(uniqueIdModifyTime)

    print(f"[/] Get TikTok Info For @{username}..")
    response = (
        f"[+] Username: {user.get('uniqueId')}\n"
        f"[+] UserID: {url_id}\n"
        f"[+] Nickname: {user.get('nickname')}\n"
        f"[+] Bio:\n{user.get('signature')}\n"
        f"[+] Is Verified: {'Yes' if user.get('verified') else 'No'}\n"
        f"[+] Is Private: {'Yes' if user.get('privateAccount') else 'No'}\n"
        f"[+] Followers: {format_numbers(json_data['stats']['followerCount'])}\n"
        f"[+] Following: {format_numbers(json_data['stats']['followingCount'])}\n"
        f"[+] Friends: {format_numbers(json_data['stats']['friendCount'])}\n"
        f"[+] Video Count: {format_numbers(json_data['stats']['videoCount'])}\n"
        f"[+] Likes: {format_numbers(json_data['stats']['heart'])}\n"
        f"[+] Can See Following List: {"Yes" if user.get("followingVisibility", "Unknown") == 1 else "No"}\n"
        f"[+] Open Favorite: {'Yes' if user.get('openFavorite') else 'No'}\n"
        f"[+] User Language: {user.get('language')}\n"
        f"[+] User Create Time: {creation_date}\n"
        f"[+] Last Time Change Nickname: {last_change_name}\n"
        f"[+] Last Time Change Username: {last_change_username}\n"
        f"[+] Account Region: {user.get('region')}\n"
        f"[+] Avatar Link: {user.get('avatarLarger')}\n"
    )

    print(response)
    input("[ + ] Done Sir ..")

print("\n")
username = input("[?] Enter a username or link: ")
print("\n")
TikTok(username=username)
