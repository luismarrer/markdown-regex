import re

def parse_markdown(md_text: str) -> str:
    html = md_text

    # h1 to h6
    html = re.sub(r'###### (.*)', r'<h6>\1</h6>', html)
    html = re.sub(r'##### (.*)', r'<h5>\1</h5>', html)
    html = re.sub(r'#### (.*)', r'<h4>\1</h4>', html)
    html = re.sub(r'### (.*)', r'<h3>\1</h3>', html)
    html = re.sub(r'## (.*)', r'<h2>\1</h2>', html)
    html = re.sub(r'# (.*)', r'<h1>\1</h1>', html)

    # bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # italic
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'\_(.*?)\_', r'<em>\1</em>', html)

    # code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)

    
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)


    return html