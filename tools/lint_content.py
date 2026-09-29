# -*- coding: utf-8 -*-
"""内容体检：扫描 content/*.json 中的草稿残留、括号失衡、英文残留、重名城市等。
用法：D:\\Python314\\python.exe -X utf8 tools\\lint_content.py
"""
import json, os, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(BASE, "content")

ARTIFACTS = ["改为", "? 不如", "TODO", "XXX", "待补充", "？？", "??", "，。", "。，"]
# 允许出现的英文词（其余 3 连续以上字母报出，人工判断）
ALLOW = {"5a", "biang", "cnn", "musea", "pmq", "g315", "outlets", "lgbt", "k11", "t3", "pm2"}
TEXT_FIELDS_DOC = "summary tagline intro note desc stay transport fresh pitfalls souvenirs"


def walk_strings(d):
    def rec(x, path):
        if isinstance(x, str):
            yield path, x
        elif isinstance(x, dict):
            for k, v in x.items():
                yield from rec(v, path + "." + str(k))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                yield from rec(v, path + "[%d]" % i)
    yield from rec(d, "")


def main():
    issues = 0
    for f in sorted(os.listdir(CONTENT)):
        if not f.endswith(".json"):
            continue
        with open(os.path.join(CONTENT, f), encoding="utf-8-sig") as fh:
            d = json.load(fh)
        cities_seen = {}
        for path, s in walk_strings(d):
            for a in ARTIFACTS:
                if a in s:
                    print("[%s] %s 草稿残留『%s』: %s" % (f, path, a, s[:60]))
                    issues += 1
            if s.count("（") != s.count("）"):
                print("[%s] %s 括号失衡: %s" % (f, path, s[:60]))
                issues += 1
            if any(path.startswith("." + k) or ("." + k + ".") in path or (".", k) for k in
                   {"summary", "tagline", "intro", "note", "desc", "stay", "transport"}):
                for w in re.findall(r"[A-Za-z]{3,}", s):
                    if w.lower() not in ALLOW and not re.fullmatch(r"[Dd]\d+", w):
                        print("[%s] %s 英文残留『%s』: %s" % (f, path, w, s[:60]))
                        issues += 1
        for c in d.get("cities", []):
            key = c.get("name", "")
            if key in cities_seen:
                print("[%s] 城市重名: %s" % (f, key))
                issues += 1
            cities_seen[key] = 1
    print("\n体检完成，共 %d 处疑似问题" % issues)


if __name__ == "__main__":
    main()
