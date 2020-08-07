import re
def convert_url(url):
    menuidmatch = re.search('menuid=\d{4}',url)
    clubidmatch = re.search('clubid=\d{8}', url)
    menuid = menuidmatch[0].split('=')[1]
    clubid = clubidmatch[0].split('=')[1]
    return 'https://cafe.naver.com/ca-fe/cafes/'+clubid+'/menus/'+menuid+'/articles/write?boardType=L'


print(convert_url('https://cafe.naver.com/4uloveme?iframe_url=/ArticleList.nhn%3Fsearch.clubid=23465858%26search.menuid=1513%26search.boardtype=L'))