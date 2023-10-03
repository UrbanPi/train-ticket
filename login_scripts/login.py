import requests
def login(username="fdse_microservice", password="111111") -> str:
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
    url = base_address + "/api/v1/users/login"

    headers = {
        'Origin': url,
        'Referer': f"{base_address}/client_login.html",
    }

    data = '{"username":"' + username + '","password":"' + \
           password + '","verificationCode":"1234"}'

    # 获取cookies
    verify_url = base_address + '/api/v1/verifycode/generate'
    r = session.get(url=verify_url)
    r = session.post(url=url, headers=headers,
                     data=data, verify=False)

    if r.status_code == 200:
        data = r.json().get("data")
        token = data.get("token")
        session.headers.update(
            {"Authorization": f"Bearer {token}"}
        )
        return str(session.headers)
    else:
        print("login failed")
        return "-1"
