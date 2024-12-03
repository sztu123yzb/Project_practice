import requests
from bs4 import BeautifulSoup
import time
import re

header = {
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    "Cookie" : "douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; SEARCH_RESULT_LIST_TYPE=%22single%22; ttwid=1%7CB5ulWjCvn0LN5Yk2Y8iY48KcuLe0nqmbAxIB9cvKO54%7C1729578383%7Cc1aa8631525e0caa6fa6853065bac6f243c364b64848c6b63725451e8232e235; UIFID_TEMP=60b2ef133e5e740633c50bb923c1ddfcacd13dfeee1bbba287269d01840b457b98fc38691e625398deeeca68c7ed0302f23237c95289f2217e0a1161eff2bfffffd2f2ac87d88a6012312f13f3392648; s_v_web_id=verify_m2k2babx_qqebsJ4f_0r0s_497F_Ay1s_fd73LHWwBis5; hevc_supported=true; dy_swidth=1920; dy_sheight=1080; passport_csrf_token=ce0a440e7f40136173c740f2e3be9c77; passport_csrf_token_default=ce0a440e7f40136173c740f2e3be9c77; fpk1=U2FsdGVkX1+bKsufy2quW04ze8Q8EdanUYivMrUsL2IsoESHeYMtZdxGhGtYMhoJSIOONF+Rktt58qCfwvH2VA==; fpk2=16453d6e2683b8800ded2a27c7f595d9; bd_ticket_guard_client_web_domain=2; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; UIFID=60b2ef133e5e740633c50bb923c1ddfcacd13dfeee1bbba287269d01840b457b28314fed13e6ad4a6a8b22e1792981299ea9eda45ce768577f0b4a100c638e411a76097b59ebca840c7592a3e6eb3d4803de9cc7eea24e1eef9e142841cf62b03a52c400a8aa97673c92f984c2d93b4074e2a548cd8c114a580790f4b25c4a713f8115dd18824f9fa492460ce048daa6e96b63ce193fe75ae0a03024173df452; passport_assist_user=Cj3dLsIWOUzjSn1oV0Rb7NBssVV27i-V8MYz9MmsBu451udcjnxiShIivOL-kIWq2tA9e1spUbcH5gCP84kFGkoKPPiNoMnfLze9EypcAcUyl5rYxbB1zQXdJvFT2QKG65xGoboFo-2DpIkQlB8cVrb7PqCodhJYvXb8NZh-LxDttd8NGImv1lQgASIBA-rPmyw%3D; n_mh=f-DHyxN2w4F7D6ijxfcO6RtuPMT0RwO99xG4vAe2vc0; sso_uid_tt=22a0184ca1638a4944a2e9fad8f6b0c5; sso_uid_tt_ss=22a0184ca1638a4944a2e9fad8f6b0c5; toutiao_sso_user=c30c45cf6ae41f683333b804994841bc; toutiao_sso_user_ss=c30c45cf6ae41f683333b804994841bc; sid_ucp_sso_v1=1.0.0-KGQ3MmE2MTNmZmIxN2E1MDEzNzIxMWMwMDc0NTQyYTNmNjQ4ZjlhYTQKHwiw7Yui9wIQtMvduAYY7zEgDDCV-L7ZBTgGQPQHSAYaAmxmIiBjMzBjNDVjZjZhZTQxZjY4MzMzM2I4MDQ5OTQ4NDFiYw; ssid_ucp_sso_v1=1.0.0-KGQ3MmE2MTNmZmIxN2E1MDEzNzIxMWMwMDc0NTQyYTNmNjQ4ZjlhYTQKHwiw7Yui9wIQtMvduAYY7zEgDDCV-L7ZBTgGQPQHSAYaAmxmIiBjMzBjNDVjZjZhZTQxZjY4MzMzM2I4MDQ5OTQ4NDFiYw; passport_auth_status=591922250ec06ab8257932a44de26423%2C; passport_auth_status_ss=591922250ec06ab8257932a44de26423%2C; uid_tt=14e50079f9fca2a3cd3962c022346943; uid_tt_ss=14e50079f9fca2a3cd3962c022346943; sid_tt=0ac2c6b1fd45b2545b0de8ec56db8a9d; sessionid=0ac2c6b1fd45b2545b0de8ec56db8a9d; sessionid_ss=0ac2c6b1fd45b2545b0de8ec56db8a9d; is_staff_user=false; SelfTabRedDotControl=%5B%5D; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=86c3c4e8a5ee140a39a06c08c72fc3bf; __security_server_data_status=1; sid_guard=0ac2c6b1fd45b2545b0de8ec56db8a9d%7C1729586618%7C5183997%7CSat%2C+21-Dec-2024+08%3A43%3A35+GMT; sid_ucp_v1=1.0.0-KDBmZTU2Y2VmNjQzZWQ4OTI0ZTMzYjJiZjAwY2YxMTFjNjdmOTg2OTgKGQiw7Yui9wIQusvduAYY7zEgDDgGQPQHSAQaAmhsIiAwYWMyYzZiMWZkNDViMjU0NWIwZGU4ZWM1NmRiOGE5ZA; ssid_ucp_v1=1.0.0-KDBmZTU2Y2VmNjQzZWQ4OTI0ZTMzYjJiZjAwY2YxMTFjNjdmOTg2OTgKGQiw7Yui9wIQusvduAYY7zEgDDgGQPQHSAQaAmhsIiAwYWMyYzZiMWZkNDViMjU0NWIwZGU4ZWM1NmRiOGE5ZA; store-region=cn-gd; store-region-src=uid; publish_badge_show_info=%220%2C0%2C0%2C1729586621320%22; WallpaperGuide=%7B%22showTime%22%3A1729588189171%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A10%2C%22cursor2%22%3A2%7D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAxAtIdSiYersl06vKx88aTtrs6OmhlDi9BQmiFZ5b1nQ%2F1729612800000%2F0%2F1729588192516%2F0%22; download_guide=%223%2F20241022%2F0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; pwa2=%220%7C0%7C2%7C0%22; __ac_nonce=06719d81b00806ed95777; __ac_signature=_02B4Z6wo00f01CX9fhgAAIDB-YThrpBWUjwl3XqAAG5t1d; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; csrf_session_id=0408556e32e1307c1c3fac116361e865; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAxAtIdSiYersl06vKx88aTtrs6OmhlDi9BQmiFZ5b1nQ%2F1729785600000%2F0%2F1729746973288%2F0%22; strategyABtestKey=%221729746973.314%22; biz_trace_id=3aa9dac7; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSExoSmNUMDBGcVdGWW9HZ0I1UXhVNTFoMnJDTWFKVXE2TlVVbjFRQ1BiVWdpbk5nUHo2ekQrSlB4Smh2c0VFdXNBeUVwQ2lwR1E1NlExYmd3blE5dUE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; odin_tt=bb5b52071ebbf8523fd8cd728da871b39fe1396707ad4629538a261ce4088e8d5727f36cc9f299b58b7d015ac14beb19f0a1ff0816c58e6a2bf0666184eef50d; IsDouyinActive=false; passport_fe_beating_status=false"
}

def getnote():
    text = input()
    url_p = re.search(r'https?://\S+', text)
    if url_p:
        url = url_p.group(0)
        print(url)

        try:
            response = requests.get(url,allow_redirects=True,proxies={"http": None, "https": None})
            url_final = response.url
            print("重定向后的连接:",url_final)
            # return url_final
        except requests.exceptions.RequestException as e:
            print("请求过程中出现错误：",e)
            # return None
    else:
        print("未找到URL")
        # return None
    r = requests.get(url_final,headers=header)
    r.encoding = "utf-8"
    s_code = r.status_code
    print(r.status_code)
    d = r.text
    #print(d)
    soup = BeautifulSoup(d,"html.parser")
    if "xiaohongshu.com" in url_final:
        tags = soup.find_all("meta",attrs={'name': 'og:image'})
        for tag in tags:
            img_src = tag["content"]
            print(img_src)
            # down4(img_src)
    else:
        tags = soup.find_all("img",class_="VPaAoQLs")
        for tag in tags:
            img_src = tag["src"]
            print(img_src)
            # down4(img_src)


# def down4(shuchu):
#     print(time.time())
#     fileName = "./image/" + str(int(time.time() * 1000)) + ".jpg"
#     r = requests.get(shuchu, headers=header)
#     f = open(fileName, "wb")
#     f.write(r.content)
#     f.close()

if __name__ == "__main__":
    getnote()
#0.51 TlC:/ 02/01 z@g.OX 幸福就好 何必在意其他 https://v.douyin.com/iSqcdXkN/ 复制此链接，打开Dou音搜索，直接观看视频！
#31 【我的澳洲醫生男友  - 黃奶油是博士奇 | 小红书 - 你的生活指南】 😆 rG3al4M69bcd82t 😆 https://www.xiaohongshu.com/discovery/item/642828fe000000001101397d?source=webshare&xhsshare=pc_web&xsec_token=ABRFQvko_98iJTUa8RsRfhgu7TtYWTKKHqDQShd6Thgaw=&xsec_source=pc_share
