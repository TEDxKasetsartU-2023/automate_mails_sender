def html2list(html):
    _open = "{{"
    _close = "}}"

    data = html.split("\n")
    data = [line.strip() for line in data]
    data = [line.split(_open)[1] for line in data if len(line.split(_open)) > 1]
    data = [line.split(_close)[0] for line in data if len(line.split(_close)) > 1]
    return data

def dictSubHtml(html, dct):
    _open = "{{"
    _close = "}}"

    for k, v in dct.items():
        html = html.replace(_open + k + _close, v)
    
    return html

if __name__ == "__main__":
    with open("template.html", "rt") as f:
        print(html2list(f.read()))