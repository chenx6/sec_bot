from aiohttp import ClientSession

ANQUANKE_DOMAIN = 'https://api.anquanke.com'


async def search_anquanke_vuln(text: str, exp=False) -> str:
    async with ClientSession() as session:
        params = {
            's': text,
            'c': '',
            'field': '',
            'start': '',
            'end': '',
            'platform': ''
        }
        response = await session.get(ANQUANKE_DOMAIN + '/data/v1/search/vul',
                                     params=params)
        json = await response.json()
        if json['total_count'] == 0:
            return ''
        vulns = []
        for vuln in json['data']:
            data = f'''漏洞名称：{vuln["name"].strip()}
漏洞编号：{vuln["cve"]}
漏洞描述：{vuln["description"].strip()}'''
            if exp:
                data += f'\nExp:\n{vuln["exp"]}'
            vulns.append(data)
        return '\n'.join(vulns)
