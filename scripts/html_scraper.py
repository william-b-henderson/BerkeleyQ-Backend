from bs4 import BeautifulSoup


def get_wait_time(filename):
    with open(filename) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        wait_time_div = soup.find_all("div", "alert alert-success alert-dismissable fade in")[0]
        wait_time = wait_time_div.h4.strong.text
        return wait_time
