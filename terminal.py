DEFAULT_CODE = "print(int(input())*(300000000**2))"

def get_headers(username, password):
    from seleniumwire import webdriver
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    play_url = "https://fp-leic.fe.up.pt/play"
    authentication_url = "https://wayf.up.pt/idp/profile/SAML2/Redirect/SSO?execution=e1s2"

    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #options.add_argument('--disable-gpu')
    #options.add_argument("--remote-debugging-pipe")

    service = Service(log_output="nul", service_args=["--log-level=OFF"])

    driver = webdriver.Edge(options=options, service=service)
    driver.get(play_url)

    WebDriverWait(driver, 60).until(
        EC.url_to_be(authentication_url)
    )

    driver.find_element("id", "username").send_keys(username)
    driver.find_element("id", "password").send_keys(password)
    driver.find_element("id", "btnLogin").click()

    WebDriverWait(driver, 60).until(
        EC.url_to_be(play_url)
    )

    for request in driver.requests[::-1]:
        if request.url == play_url:
            headers = request.headers

            driver.close()

            return headers


def run_code(code, headers):
    import requests

    submission_url = "https://fp-leic.fe.up.pt/play/py01/einstein"

    payload = {"code": code}

    response = requests.post(submission_url, headers=headers, data=payload)

    return response.text


def get_code_for_cmd(cmd):
    script = f"import subprocess\nprint(subprocess.run('{cmd}', capture_output=True, text=True, shell=True).stdout.strip())"
    return script
    

def get_output(html):
    from lxml import etree

    xpath = "/html/body/div[2]/table[1]/tbody/tr[1]/td[3]/code"

    dom = etree.HTML(html)
    return dom.xpath(xpath)[0].text.strip("'").replace("\\n", "\n")


if __name__ == "__main__":
    from getpass import getpass

    username = input("Username:")
    password = getpass(prompt="Password:")
    print("Getting request headers...")
    HEADERS = get_headers(username, password)

    while True:
        cmd = input(">>>")
        html = run_code(get_code_for_cmd(cmd), HEADERS)
        print(get_output(html))
        print("")