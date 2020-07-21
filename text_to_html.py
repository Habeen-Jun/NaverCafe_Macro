import textile

def text_to_html(text):
    html = textile.textile(text)
    return html

# s = 'hello my name is habeen Jun'
# html = textile.textile(s)
# print(html)