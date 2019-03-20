#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bs4
from glob import glob
import sys
import re

#|Problemas para resolver
re_remove = re.compile(r"^\s*(Ejercicios para practicar|Actividades para pensar más|Encuentra el error)\s*$")
re_difi1 = re.compile(r'^\s*[●○]{3}\s*$')
re_difi2 = re.compile(r'\(\s*<span class="dificultad">[●○]{3}</span>\s*\)')
heads = ["h1", "h2", "h3", "h5", "h6"]

def get_soup(h):
    with open(h, "r") as f:
        soup = bs4.BeautifulSoup(f, "lxml")
        return soup

def add_class(n, cl):
    c = n.attrs.get("class", "")
    if isinstance(c, str):
        c = (c + " "+cl).strip()
    else:
        c.append(cl)
    n.attrs["class"]=c

def get_tpt(title):
    soup = bs4.BeautifulSoup('''
<!DOCTYPE html>
<html lang="es">
	<head>
		<title>%s</title>
		<meta charset="utf-8"/>
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
        <script type="text/javascript" async src="../m/ej.js"></script>
	</head>
	<body>
        <div>
        <h1 contenteditable="true">Escriba aquí el título de la ficha</h1>
        <p contenteditable="true">Escriba aquí la descripción de la ficha</p>
        </div>
        <div contenteditable="true">
        </div>
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
    body = ej.findAll("div")[-1]

    for ep in soup.findAll("div", text=re_remove):
        ep.extract()
    for div in soup.select("div.sm-content"):
        h1 = div.find("h1")
        span = h1.find("span")
        if span:
            span.append(". ")
        cap = h1.get_text().strip()
        if cap in ("Actividades clave", "Ponte a prueba"):
            continue
        if cap in ("Actividades clave", "Actividades", "Ponte a prueba"):
            if cap == "Actividades":
                h1.extract()
                for h3 in div.findAll("h3"):
                    h3.name="h1"
            body.append(div)
        else:
            for a in div.select("div.actividades"):
                a.find("h1").string = cap
                body.append(a)
    for e in body.select(".exercise, .section"):
        if e.find("a"):
            e.extract()
    for i in body.findAll(heads):
        if len(i.get_text().strip())==0:
            i.extract()
        else:
            add_class(i, "phide")

    for img in body.findAll("img"):
        img.attrs["src"] = "../" + img.attrs["src"]

    for e in body.select("div.exercise"):
        n = e.select("div.sm-exercise-number")[0]
        n.attrs["contenteditable"]="false"
        n = n.get_text().strip()
        add_class(e, "e"+n)

    for s in body.findAll("span", text=re_difi1):
        p = s.previous_sibling
        n = s.next_sibling
        if not p or not n:
            continue
        if p.string.strip().endswith("(") and n.string.strip().startswith(")"):
            nt = ej.new_tag("span")
            nt.string = s.string.strip()
            nt.attrs["class"]="dificultad"
            s.replace_with(nt)

    with open("out/ej/"+h[4:], "w") as file:
        ej = str(ej)
        ej = re_difi2.sub("", ej)
        file.write(ej)
