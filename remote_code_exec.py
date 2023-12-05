import urllib.request

href = "https://gist.githubusercontent.com/tertek/31de3bc933f756137ed4c529cc41543c/raw/7e95a4f54be91da6d30c6562b7f59ab453b04cc2/remote-odk.py"

with urllib.request.urlopen(href) as url:
    r = url.read()
    s = r.decode('ascii')

ldict = {}
exec(s, globals(), ldict)

output = ldict['output']