# -*- coding: utf-8 -*-
"""校验旅行宝典省份JSON文件。
用法：
  D:\\Python314\\python.exe -X utf8 tools\\check_json.py            # 校验content目录全部
  D:\\Python314\\python.exe -X utf8 tools\\check_json.py 文件1 文件2  # 校验指定文件
"""
import json, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(BASE, "content")
REGIONS = {"华北", "东北", "华东", "华中", "华南", "西南", "西北", "港澳台"}
GRADES = {"顶流必去", "黑马新贵", "小众宝藏"}
TOPSIGHT_TYPES = {"世界遗产", "5A景区", "自然奇观", "人文古迹", "小众秘境", "主题乐园"}
REQUIRED = ["name", "region", "emoji", "grade", "tagline", "summary", "tags", "bestSeason",
            "suggestedDays", "budget", "cities", "signatureFood", "topSights", "experiences",
            "souvenirs", "routes", "transport", "pitfalls", "fresh"]


def warn(msg):
    print("  [警告]", msg)


def err(msg, errs):
    errs.append(msg)
    print("  [错误]", msg)


def check_file(path):
    errs = []
    disp = os.path.basename(path)
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            d = json.load(f)
    except Exception as e:
        err("JSON解析失败: %s" % e, errs)
        return errs
    if not isinstance(d, dict):
        err("顶层不是对象", errs)
        return errs
    for k in REQUIRED:
        if k not in d:
            err("缺少字段 %s" % k, errs)
    if d.get("region") not in REGIONS:
        err("region非法: %s" % d.get("region"), errs)
    if d.get("grade") not in GRADES:
        err("grade非法: %s" % d.get("grade"), errs)
    for k in ("tagline", "summary", "bestSeason", "suggestedDays", "budget", "transport"):
        v = d.get(k)
        if not isinstance(v, str) or not v.strip():
            err("%s 应为非空字符串" % k, errs)
    if isinstance(d.get("summary"), str) and len(d["summary"]) < 100:
        warn("summary不足100字（要求120-180）")
    for k in ("tags", "souvenirs", "pitfalls", "fresh"):
        v = d.get(k)
        if not isinstance(v, list) or not v:
            err("%s 应为非空列表" % k, errs)
    cities = d.get("cities")
    if not isinstance(cities, list) or len(cities) < 3:
        err("cities应至少3个", errs)
    else:
        for c in cities:
            if not isinstance(c, dict):
                err("cities元素应为对象", errs)
                continue
            for ck in ("name", "intro", "sights", "food"):
                if ck not in c:
                    err("城市[%s]缺少 %s" % (c.get("name"), ck), errs)
            if len(c.get("sights") or []) < 3:
                warn("城市[%s] sights少于3条" % c.get("name"))
            if len(c.get("food") or []) < 3:
                warn("城市[%s] food少于3条" % c.get("name"))
    for k, lo in (("signatureFood", 6), ("topSights", 8), ("experiences", 4)):
        v = d.get(k)
        if isinstance(v, list) and len(v) < lo:
            warn("%s 仅%d条(建议>=%d)" % (k, len(v), lo))
    for s in d.get("topSights") or []:
        if isinstance(s, dict) and s.get("type") not in TOPSIGHT_TYPES:
            warn("topSights类型异常: %s" % s.get("type"))
    for r in d.get("routes") or []:
        if not isinstance(r, dict) or "title" not in r or "days" not in r:
            warn("routes条目缺 title/days")
    print("%s %s 城市%d 美食%d 景点%d 体验%d" % (
        "OK  " if not errs else "FAIL", disp,
        len(d.get("cities") or []), len(d.get("signatureFood") or []),
        len(d.get("topSights") or []), len(d.get("experiences") or [])))
    return errs


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = [os.path.join(CONTENT, f) for f in sorted(os.listdir(CONTENT)) if f.endswith(".json")]
    total = 0
    for p in files:
        total += len(check_file(p))
    print("\n共%d个文件, 错误%d处" % (len(files), total))
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
