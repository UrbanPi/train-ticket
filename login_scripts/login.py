import requests
def login(email="fdse_microservices@163.com", password="DefaultPassword") -> str:
    session = requests.Session()
    session.headers.update({
        # 'Proxy-Connection': 'keep-alive',
        # 'Accept': 'application/json',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Content-Type': 'application/json',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'Connection': 'keep-alive',
    })
    base_address = "http://localhost:32677"
    url = base_address + "/login"

    headers = {
        'Origin': url,
        'Referer': f"{base_address}/client_login.html",
    }

    data = '{"email":"' + email + '","password":"' + \
           password + '","verificationCode":"abcd"}'

    # get initial session
    verify_url = base_address + '/verification/generate'
    r = session.get(url=verify_url)
    r = session.post(url=url, headers=headers,
                     data=data, verify=False)

    if r.status_code == 200:
        return "\n".join(["{}: {}".format(c.name, c.value) for c in session.cookies])
    else:
        print("login failed")
        return "-1"

def login_admin(username="adminroot", password="adminroot") -> str:
    session = requests.Session()
    session.headers.update({
        # 'Proxy-Connection': 'keep-alive',
        # 'Accept': 'application/json',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Content-Type': 'application/json',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'Connection': 'keep-alive',
    })
    base_address = "http://localhost:32677"
    url = base_address + "/account/adminlogin"

    headers = {
        'Origin': url,
        'Referer': f"{base_address}/client_login.html",
    }

    data = '{"name":"' + username + '","password":"' + \
           password + '"}'

    # get initial session
    verify_url = base_address + '/verification/generate'
    r = session.get(url=verify_url)
    r = session.post(url=url, headers=headers,
                     data=data, verify=False)

    if r.status_code == 200:

        return "\n".join(["id: {}".format(r.json().get("id"))]+["{}: {}".format(c.name, c.value) for c in session.cookies])
    else:
        print("login failed")
        return "-1"
