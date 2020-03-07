from bs4 import BeautifulSoup
import requests


class Session:
    def __init__(self, login, password):
        self.session = requests.Session()
        self.auth(login, password)
    
    def auth(self, login, password):
        response = self.session.post('https://informatics.mccme.ru/login/index.php', {
            'username': login,
            'password': password
        })

        html = response.content.decode()
        if 'Вы не прошли идентификацию' in html:
            if 'неверный логин или пароль' in html:
                raise Exception('вы не прошли идентификацию: неверный логин или пароль')
            
            raise Exception('вы не прошли идентификацию')
    
    def get_standings(self, contest_id, group_id):
        response = self.session.get('https://informatics.mccme.ru/py/monitor', params={
            'contest_id': contest_id,
            'group_id': group_id
        })

        html = response.content.decode()
        soup = BeautifulSoup(html, 'html.parser')

        with open('w.html', 'w', encoding='utf8') as f:
            f.write(str(soup))
        
        columns = []
        rows = []

        table = soup.find('table')

        tr_els = table.findAll('tr')
        for k, row in enumerate(tr_els):
            cells = []

            for cell in row.findAll('td'):
                if a_el := cell.find('a'):
                    content = a_el.encode_contents().decode()
                else:
                    content = cell.encode_contents().decode()

                cells.append(content.strip())
            
            if k == 0:
                columns = cells
            elif k == len(tr_els) - 1:
                continue
            else:
                rows.append(dict(zip(columns, cells)))
        
        return rows


session = Session('<login>', '<password>')
print(session.get_standings(50145, 14276))