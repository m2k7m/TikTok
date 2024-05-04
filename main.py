
#pip install requests bs4 countryflag

import requests,json,time,countryflag,os
from bs4 import BeautifulSoup
from datetime import datetime

def format_number(num):
    if num >= 1000000:
        return str(num // 1000000) + 'M'
    elif num >= 1000:
        return str(num // 1000) + 'K'
    else:
        return str(num)
    
class TikTok:
    def __init__(self, username: str):
        self.username = username
        self.json_data = None

        if "@" in self.username:
            self.username = self.username.replace("@", "")

        self.admin()

    def admin(self):
        self.send_request()
        self.output()

    def send_request(self):
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 GIVT"}
        r = requests.get(f"https://www.tiktok.com/@{self.username}", headers=headers)

        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            script_tag = soup.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
            script_text = script_tag.text.strip()
            self.json_data = json.loads(script_text)["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
            with open("file.json","w")as f:
                json.dump(self.json_data,f,indent=2)
        except:
            input("[X] Error : Username Not Found .")
            exit()

    def user_create_time(self):
        try:
            url_id = int(str(self.json_data["user"]["id"]))
            binary = "{0:b}".format(url_id)
            i = 0
            bits = ""
            while i < 31:
                bits += binary[i]
                i += 1
            timestamp = int(bits, 2)
            dt_object = datetime.fromtimestamp(timestamp)
            return dt_object
        except:
            return "Unknown"

    def last_change_name(self):
        if self.json_data["user"]["nickNameModifyTime"] == 0:
            return "User Never Changed Name"
        else:
            try:
                time = self.json_data["user"]["nickNameModifyTime"]
                check = datetime.fromtimestamp(int(time))
                return check
            except:
                return "Unknown"
        
    def last_change_user(self):
        if self.json_data["user"]["uniqueIdModifyTime"] == 0:
            return "User Never Changed Username"
        else:
            try:
                time = self.json_data["user"]["uniqueIdModifyTime"]
                check = datetime.fromtimestamp(int(time))
                return check
            except:
                return "Unknown"

    def see_following(self):
        try:
            check = str(self.json_data["user"]["followingVisibility"])
            if check == "1":
                return "Yes"
            return "No"
        except:
            return "Unknown"

    def output(self):
        print(f"[/] Get TikTok Info For @{self.username}..")
        time.sleep(2)
        response = ""
        if self.json_data["user"].get("uniqueId"):
            response += f"[+] Username: {self.json_data['user']['uniqueId']}\n"
        if self.json_data["user"].get("id"):
            response += f"[+] UserID: {self.json_data['user']['id']}\n"
        if self.json_data["user"].get("nickname"):
            response += f"[+] Nickname: {self.json_data['user']['nickname']}\n"
        if self.json_data["user"].get("signature"):
            response += f"[+] Bio:\n{self.json_data['user']['signature']}\n"
        if self.json_data["user"].get("verified") is not None:
            response += f"[+] Is Verified: {'Yes' if self.json_data['user']['verified'] else 'No'}\n"
        if self.json_data["user"].get("privateAccount") is not None:
            response += f"[+] Is Private: {'Yes' if self.json_data['user']['privateAccount'] else 'No'}\n"
        if self.json_data["stats"].get("followerCount"):
            response += f"[+] Followers: {format_number(self.json_data['stats']['followerCount'])}\n"
        if self.json_data["stats"].get("followingCount"):
            response += f"[+] Following: {format_number(self.json_data['stats']['followingCount'])}\n"
        if self.json_data["stats"].get("friendCount"):
            response += f"[+] Friends: {format_number(self.json_data['stats']['friendCount'])}\n"
        if self.json_data["stats"].get("heart"):
            response += f"[+] Likes: {format_number(self.json_data['stats']['heart'])}\n"
        if self.json_data["stats"].get("videoCount"):
            response += f"[+] Video Count: {format_number(self.json_data['stats']['videoCount'])}\n"
        if self.see_following():
            response += f"[+] Can See Following list: {self.see_following()}\n"
        if self.json_data["user"].get("openFavorite") is not None:
            response += f"[+] Open Favorite: {'Yes' if self.json_data['user']['openFavorite'] else 'No'}\n"
        if self.json_data["user"].get("language"):
            response += f"[+] User Language: {self.json_data['user']['language']}\n"
        if self.user_create_time() and self.user_create_time() != "Unknown":
            response += f"[+] User Create Time: {self.user_create_time()}\n"
        if self.last_change_name() and self.last_change_name() != "Unknown":
            response += f"[+] Last Time Change Nickname: {self.last_change_name()}\n"
        if self.last_change_user() and self.last_change_user() != "Unknown":
            response += f"[+] Last Time Change Username: {self.last_change_user()}\n"
        if self.json_data["user"].get("region"):
            response += f"[+] Account Region: {self.json_data['user']['region']} - {countryflag.getflag([f'{self.json_data['user']['region']}'])}\n"
        if self.json_data["user"].get("avatarLarger"):
            response += f"[+] Avatar Link: {self.json_data['user']['avatarLarger']}\n"

        print(response)
        input("[ + ] Done Sir ..")
        exit()

os.system('cls' if os.name == 'nt' else 'clear')
print("\n")
username = input("[?] Please Enter Username : ")
os.system('cls' if os.name == 'nt' else 'clear')
TikTok(username=username)
