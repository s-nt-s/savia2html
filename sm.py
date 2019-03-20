#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import re
from urllib.parse import urljoin, urlparse

import bs4
import requests
import yaml

tab = re.compile("^", re.MULTILINE)
sp = re.compile("\s+", re.UNICODE)

tag_concat = ['u', 'ul', 'ol', 'i', 'em', 'strong']
tag_round = ['u', 'i', 'em', 'span', 'strong', 'a']
tag_trim = ['li', 'th', 'td', 'div', 'caption', 'h[1-6]']
tag_right = ['p']
sp = re.compile("\s+", re.UNICODE)
re_piecesindex = re.compile(r"\bvar\s+piecesindex\s*=\s*(.+)\s*;?")
re_css_url = re.compile(r"\burl\(([^\)]+)\)")

re_userid = re.compile(r"\bvar\s*userid\s*=\s*'(\d+)'\s*;?")


heads = ["h1", "h2", "h3", "h4", "h5", "h6"]
block = heads + ["p", "div", "table", "article"]
inline = ["span", "strong", "b", "del"]

with open("config.yml", 'r') as stream:
    config = yaml.load(stream)

s = requests.Session()
s.headers = {
    'User-Agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

contadores = {}


def get(url):
    r = s.get(url)
    soup = bs4.BeautifulSoup(r.content, "lxml")
    return soup, r


def dwn(url, out, ext=None, ab=None):
    global contadores
    if ab:
        url = urljoin(ab, url)
    if not ext:
        path = urlparse(url).path
        ext = os.path.splitext(path)[1]
    if out not in contadores:
        contadores[out] = {}
    if ext not in contadores[out]:
        contadores[out][ext] = 1
    dest = out + ("%02d" % contadores[out][ext]) + ext
    resp = s.get(url)
    text = None
    if ext == ".css":
        if "css" not in contadores[out]:
            contadores[out]["css"] = []
        if resp.text in contadores[out]["css"]:
            return None
        contadores[out]["css"].append(resp.text)
        text = resp.text
        for m in re_css_url.findall(text):
            if len(m) > 3:
                dest2 = dwn(m, out, ab=url)
                text = text.replace(m, dest2.split("/")[-1])
        if text == resp.text:
            text = None
    with open("out/" + dest, 'wb') as fd:
        if text:
            fd.write(text.encode())
        else:
            fd.write(resp.content)
        fd.close()
    contadores[out][ext] = 1 + contadores[out][ext]
    return dest


def get_text(soup, select):
    nodes = soup.select(select)
    node = nodes[0]
    txt = sp.sub(" ", node.get_text()).strip()
    return txt


def get_tpt(title):
    soup = bs4.BeautifulSoup('''
<!DOCTYPE html>
<html lang="es">
	<head>
		<title>%s</title>
		<meta charset="utf-8"/>
        <!--script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-AMS_CHTML"></script-->
        <script type="text/javascript" async src="m/MathJax-2.7.2/MathJax.js?config=TeX-AMS_CHTML"></script>
        <script type="text/x-mathjax-config">
          MathJax.Hub.Config({
            jax: ["input/TeX","output/CommonHTML"],
            messageStyle: "none",
            showMathMenu: false,
            tex2jax: {
              inlineMath: [['$','$'], ['\\\\(','\\\\)']]
            },
            TeX: {
              extensions: ['autoload-all.js'],
              unicode: {
                fonts: "STIXGeneral, 'Arial Unicode MS'"
              }
            },
            CommonHTML: {
              scale: 100,
              matchFontHeight: false,
              mtextFontInherit: true,
              undefinedFamily: "serif"
            }
          });
        </script>
        <link href="m/theme.css" rel="stylesheet" type="text/css">
	</head>
	<body>
    <div id="netex-sm-interface" class="netex-sm-interface">
    <div id="netex-sm-subject" class="sm-subject mat_act_blue orange-lines" touch-action="pan-y">
    </div>
    </div>
	</body>
</html>
	'''.strip() % (title), 'lxml')
    return soup


def get_html(soup):
    for div in soup.findAll(["div", "p"]):
        if not div.find("img"):
            txt = div.get_text()
            txt = sp.sub("", txt)
            if len(txt) == 0:
                div.extract()
    h = str(soup)
    r = re.compile("(\s*\.\s*)</a>", re.MULTILINE | re.DOTALL | re.UNICODE)
    h = r.sub("</a>\\1", h)
    for t in tag_concat:
        r = re.compile(
            "</" + t + ">(\s*)<" + t + ">", re.MULTILINE | re.DOTALL | re.UNICODE)
        h = r.sub("\\1", h)
    for t in tag_round:
        r = re.compile(
            "(<" + t + ">)(\s+)", re.MULTILINE | re.DOTALL | re.UNICODE)
        h = r.sub("\\2\\1", h)
        r = re.compile(
            "(<" + t + " [^>]+>)(\s+)", re.MULTILINE | re.DOTALL | re.UNICODE)
        h = r.sub("\\2\\1", h)
        r = re.compile(
            "(\s+)(</" + t + ">)", re.MULTILINE | re.DOTALL | re.UNICODE)
        h = r.sub("\\2\\1", h)
    for t in tag_trim:
        r = re.compile(
            "(<" + t + ">)\s+", re.MULTILINE | re.DOTALL | re.UNICODE)
        h = r.sub("\\1", h)
        r = re.compile(
            "\s+(</" + t + ">)", re.MULTILINE | re.DOTALL | re.UNICODE)
        h = r.sub("\\1", h)
    for t in tag_right:
        r = re.compile(
            "\s+(</" + t + ">)", re.MULTILINE | re.DOTALL | re.UNICODE)
        h = r.sub("\\1", h)
        r = re.compile(
            "(<" + t + ">) +", re.MULTILINE | re.DOTALL | re.UNICODE)
        h = r.sub("\\1", h)
    r = re.compile(
        r"\s*(<meta[^>]+>)\s*", re.MULTILINE | re.DOTALL | re.UNICODE)
    h = r.sub(r"\n\1\n", h)
    r = re.compile(r"\n\n+", re.MULTILINE | re.DOTALL | re.UNICODE)
    h = r.sub(r"\n", h)
    return h


def get_curso(titulo):
    tit = titulo.split(" ")
    cap = titulo.split(" ")
    curso = "%s_%s." % (tit[1], tit[0][0])
    return curso


r = s.get(config['url'])
soup = bs4.BeautifulSoup(r.content, "lxml")
form = soup.find("form", attrs={"id": config["form"]})
data = {}
for i in form.select("input[name]"):
    n = i.attrs["name"]
    if n in config:
        data[n] = config[n]
    else:
        data[n] = i.attrs.get("value", None)
b = form.find("button")
data[b.attrs["name"]] = b.attrs["name"]

r = s.post(config['url'], data=data)

soup = bs4.BeautifulSoup(r.content, "lxml")
urls = [a.attrs["href"] for a in soup.select("a#a-book")]  # a.my_books-a")]
for url in urls:
    soup, _ = get(url)
    lib = get_text(soup, "h2.tit")
    lib = re.sub(r"\s*\. Savia$", "", lib)
    curso = get_curso(lib)
    print(lib)
    #tpt = get_tpt(lib)
    #body = tpt.find("body").find("div").find("div")
    css = []
    jss = []
    #print (url)
    urls2 = [a.attrs["href"] for a in soup.select("a.featured-a")]
    for url2 in urls2:
        soup, r = get(url2)
        num = get_text(soup, "div.num")
        tit = get_text(soup, "div.txt-content2-tit")
        flt = curso + ("%02d" % int(num))
        f_out = flt + " - " + tit
        med = "m/" + flt + "/"
        print("  %2d - %s" % (int(num), tit))
        m = re_piecesindex.search(r.text)
        piecesindex = m.group(1)
        if piecesindex.endswith(";"):
            piecesindex = piecesindex[:-1]
        piecesindex = json.loads(piecesindex)
        m = re_userid.search(r.text)
        userid = m.group(1)
        iframe = soup.find("iframe", attrs={"id": "didacticunit"})
        data = {par[0][5:]: par[1]
                for par in iframe.attrs.items() if par[0].startswith("data-")}
        uuid = data["uuid"]
        piece = piecesindex[uuid]
        courseid = data["courseid"]

        dest = "file.php/%s/%s/token/0/%s/%s/%s/%s/%s/" % (piece["modified"], piece[
                                                           "destmodified"], courseid, userid, "ext", data["piecetype"], uuid)
        dest = urljoin(url2, dest)

        tpt = get_tpt(f_out)
        body = tpt.find("body").find("div").find("div")

        if data["piecetype"] == "sm_ld_web":
            soup, r = get(dest)
            for noscript in soup.select("noscript"):
                if noscript.attrs.get("data-type", None) == "content":
                    #noscript.name = "article"
                    for img in noscript.select("img"):
                        img.attrs["src"] = urljoin(dest, img.attrs["src"])

                    for a in noscript.select("a.sm-media-button"):
                        data = {par[0][5:]: par[1] for par in a.attrs.items() if par[
                            0].startswith("data-")}
                        if "smreference" in data and data["smreference"] in piecesindex:
                            uuid = data["smreference"]
                            piece = piecesindex[uuid]
                            ext = "ext"
                            typ = piece["type"]
                            if typ == "sm_video":
                                ext = "mp4"
                            btn = "file.php/%s/%s/token/0/%s/%s/%s/%s/%s/" % (
                                piece["modified"], piece["destmodified"], courseid, userid, ext, typ, uuid)
                            btn = urljoin(url2, btn)
                            a.attrs["href"] = btn

                    body.append(noscript)
                    noscript.unwrap()
            css = [style.attrs["href"] for style in soup.select(
                "link") if style.get("href", "").endswith(".css")]
            jss = [script.attrs["src"]
                   for script in soup.select("script") if script.get("src", None)]

        if len(body.select("> *")) == 0:
            continue

        if not os.path.exists("out/" + med):
            os.makedirs("out/" + med)

        # css = { for c in list(set(css))}
        for c in css:
            link = tpt.new_tag("link")
            link.attrs["rel"] = "stylesheet"
            link.attrs["type"] = "text/css"
            link.attrs["href"] = urljoin(dest, c)
            tpt.find("head").insert(0, link)

        for div in tpt.select("div.sm_comp_js_dropdown_container"):
            div.attrs["class"] = "sm_comp_js_dropdown_container active"
            h1 = div.find("h1")
            h = tpt.new_tag("h1")
            h.attrs["class"] = h1.attrs["class"]
            h.append(h1.contents[0])
            h1.insert(0, h)
            h1.unwrap()

        # for a in tpt.findAll("a", attrs={"data-teacher-action", "true"}):
        for a in tpt.select("a[data-teacher-action=true]"):
            div = a.parent
            c = " ".join(div.attrs.get("class", []))
            if c == "sm-media-actions-dark":
                div.extract()
        for e in tpt.select("div.highlight_exercise, div.highlight"):
            divs = [p.parent for p in e.select(
                "span.sm_comp_js_show_more") if p.parent.name == "p"] + e.select("div.sm_js_show_content")
            prs = e.find("h1")
            if prs and sp.sub(" ", prs.get_text()).strip() == "Problema resuelto":
                divs.append(prs)
            if len(divs) > 0:
                c = " ".join(div.attrs.get("class", []))
                c = re.sub(r"highlight_?", "", c)
                e.attrs["class"] = c
                for d in divs:
                    d.extract()

        for l in tpt.select("link"):
            link = l.attrs["href"]
            if link.startswith("http"):
                dest = dwn(link, med)
                if dest:
                    l.attrs["href"] = dest
                else:
                    l.extract()

        for img in tpt.findAll(["img"]):  # , "script"]):
            link = img.attrs.get("src", None)
            if link and link.startswith("http"):
                dest = dwn(link, med)
                img.attrs["src"] = dest

        for l in tpt.select("a"):
            link = l.attrs["href"]
            if link and link.startswith("http") and "/sm_ofimatico/" in link:
                dest = dwn(link, med, ext=".pdf")
                l.attrs["href"] = dest

        html = get_html(tpt)
        f_out = f_out.replace(" ", "_") + ".html"
        with open("out/" + f_out, "w") as file:
            file.write(html)
