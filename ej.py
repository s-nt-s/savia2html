#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bs4
from glob import glob
import sys
import re
#|Problemas para resolver
re_remove = re.compile(r"^\s*(Ejercicios para practicar|Actividades para pensar más|Encuentra el error)\s*$")
heads = ["h1", "h2", "h3", "h5", "h6"]

def get_soup(h):
    with open(h, "r") as f:
        soup = bs4.BeautifulSoup(f, "lxml")
        return soup

def get_tpt(title):
    soup = bs4.BeautifulSoup('''
<!DOCTYPE html>
<html lang="es">
	<head>
		<title>%s</title>
		<meta charset="utf-8"/>
        <!--script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script-->
        <script type="text/javascript" async src="../m/MathJax-2.7.2/MathJax.js?config=TeX-AMS_CHTML"></script>
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
        <link href="../m/theme.css" rel="stylesheet" type="text/css">
        <link href="../m/theme_ej.css" rel="stylesheet" type="text/css">
        <!--script type="text/javascript" async src="../m/ej.js"></script-->
	</head>
	<body contenteditable="true">

	</body>
</html>
	'''.strip() % (title)
        , 'lxml')
    return soup

for h in sorted(glob("out/*_-_*.html")):
    print(h)
    soup=get_soup(h)
    title = soup.find("title").get_text().strip()
    ej = get_tpt(title+" - Ejercicios")

    for ep in soup.findAll("div", text=re_remove):
        ep.extract()
    for div in soup.select("div.sm-content"):
        h1 = div.find("h1")
        span = h1.find("span")
        if span:
            span.append(". ")
        cap = h1.get_text().strip()
        if cap in ("Actividades clave", "Actividades", "Ponte a prueba"):
            if cap == "Actividades":
                h1.extract()
                for h3 in div.findAll("h3"):
                    h3.name="h1"
            ej.append(div)
        else:
            for a in div.select("div.actividades"):
                a.find("h1").string = cap
                ej.append(a)
    for e in ej.select(".exercise, .section"):
        if e.find("a"):
            e.extract()
    for i in ej.findAll(heads):
        if len(i.get_text().strip())==0:
            i.extract()
    for img in ej.findAll("img"):
        img.attrs["src"] = "../" + img.attrs["src"]

    '''
    for p in ej.findAll(heads + ["p"]):
        p.attrs["contenteditable"]="true"
    '''
    with open("out/ej/"+h[4:12]+".html", "w") as file:
        file.write(str(ej))
