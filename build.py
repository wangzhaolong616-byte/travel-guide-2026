# -*- coding: utf-8 -*-
"""把 content/*.json 注入 template.html，生成单文件《中国旅行宝典2026.html》。
用法：D:\\Python314\\python.exe -X utf8 build.py
"""
import json, os, shutil, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(BASE, "content")

ORDER = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江",
         "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东",
         "河南", "湖北", "湖南",
         "广东", "广西", "海南",
         "重庆", "四川", "贵州", "云南", "西藏",
         "陕西", "甘肃", "青海", "宁夏", "新疆",
         "香港", "澳门", "台湾"]
REGION_ORDER = ["华北", "东北", "华东", "华中", "华南", "西南", "西北", "港澳台"]
GRADE_RANK = {"顶流必去": 0, "黑马新贵": 1, "小众宝藏": 2}

CALENDAR = [
    {"m": 1, "t": "冰雪童话 × 暖冬逃离", "d": "冰雪大世界正当季；三亚开启暖气自由；香港延续新年气氛。", "ps": ["黑龙江", "吉林", "海南", "香港"]},
    {"m": 2, "t": "春节年味地图", "d": "西安大唐不夜城灯会、山西社火、潮汕英歌舞、福州游神，年味各不相同。", "ps": ["陕西", "山西", "广东", "福建"]},
    {"m": 3, "t": "花季序章", "d": "婺源油菜花海、林芝桃花沟、无锡鼋头渚樱花、武汉大学早樱渐次盛开。", "ps": ["江西", "西藏", "江苏", "湖北"]},
    {"m": 4, "t": "国色与江南", "d": "洛阳牡丹进入全盛，黄山春色初醒，平潭蓝眼泪初现，明前龙井正鲜。", "ps": ["河南", "安徽", "浙江", "福建"]},
    {"m": 5, "t": "初夏节奏", "d": "伊犁花季启幕，东江湖晨雾如仙境，大理进入『有风』的季节。", "ps": ["新疆", "湖南", "云南"]},
    {"m": 6, "t": "草原与海风", "d": "呼伦贝尔返青，青海湖环湖正美，黄果树进入丰水期，万宁冲浪最佳。", "ps": ["内蒙古", "青海", "贵州", "海南"]},
    {"m": 7, "t": "避暑内卷之王", "d": "门源油菜花铺成金色大地，甘南草原花开，六盘水19℃夏天，崇礼上山避暑。", "ps": ["青海", "甘肃", "贵州", "河北"]},
    {"m": 8, "t": "高原蜜月季", "d": "暑期进藏窗口，稻城亚丁盛开，独库公路全盛，香格里拉松茸上市。", "ps": ["西藏", "四川", "新疆", "云南"]},
    {"m": 9, "t": "初秋第一抹金", "d": "喀纳斯迎来初秋，九寨沟水色渐深，阿尔山层林尽染，张家界云海多发。", "ps": ["新疆", "四川", "内蒙古", "湖南"]},
    {"m": 10, "t": "金秋顶流 · 黄金周", "d": "额济纳胡杨最黄的21天，敦煌金秋，盘锦红海滩进入高潮，香山红叶渐染。", "ps": ["内蒙古", "甘肃", "辽宁", "北京"]},
    {"m": 11, "t": "晚秋与温泉", "d": "腾冲银杏村金黄满地，塔川秋色入画，桂林海洋乡银杏，澳门大赛车轰鸣。", "ps": ["云南", "安徽", "广西", "澳门"]},
    {"m": 12, "t": "冰雪回归", "d": "冰雪大世界新季开园，长白山粉雪开板，三亚避寒启程，香港圣诞氛围拉满。", "ps": ["黑龙江", "吉林", "海南", "香港"]},
]


def main():
    data = []
    for f in sorted(os.listdir(CONTENT)):
        if not f.endswith(".json"):
            continue
        with open(os.path.join(CONTENT, f), encoding="utf-8-sig") as fh:
            item = json.load(fh)
        item["py"] = f[:-5]
        data.append(item)

    idx = {n: i for i, n in enumerate(ORDER)}
    data.sort(key=lambda d: (REGION_ORDER.index(d["region"]),
                             idx.get(d["name"], 99),
                             GRADE_RANK.get(d["grade"], 9)))

    names = {d["name"] for d in data}
    missing = [n for n in ORDER if n not in names]
    if missing:
        print("缺失省份:", "、".join(missing))
        sys.exit(1)
    extra = [n for n in names if n not in ORDER]
    if extra:
        print("多余省份:", "、".join(extra))
        sys.exit(1)

    ncities = sum(len(d.get("cities") or []) for d in data)
    ndis = sum(len(c.get("districts") or []) for d in data for c in d.get("cities") or [])
    nitems = 0
    for d in data:
        nitems += len(d.get("signatureFood") or []) + len(d.get("topSights") or []) + \
                  len(d.get("experiences") or []) + len(d.get("souvenirs") or [])
        for c in d.get("cities") or []:
            nitems += len(c.get("sights") or []) + len(c.get("food") or []) + len(c.get("districts") or [])

    with open(os.path.join(BASE, "template.html"), encoding="utf-8") as fh:
        tpl = fh.read()
    assert "__DATA__" in tpl and "__CALENDAR__" in tpl, "模板缺占位符"
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    assert "</script" not in payload.lower(), "数据中含脚本结束符"
    html = tpl.replace("__CALENDAR__", json.dumps(CALENDAR, ensure_ascii=False)) \
              .replace("__DATA__", payload)
    out = os.path.join(BASE, "中国旅行宝典2026.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    shutil.copyfile(out, os.path.join(BASE, "index.html"))
    print("省份%d 城市%d 区县板块%d 条目%d 大小%dKB" % (len(data), ncities, ndis, nitems, len(html) // 1024))
    print("已同步离线版与 index.html（在线版入口）")

    for cand in [os.path.join(os.path.expanduser("~"), "Desktop"),
                 os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
                 os.path.join(os.path.expanduser("~"), "OneDrive", "桌面")]:
        if os.path.isdir(cand):
            shutil.copyfile(out, os.path.join(cand, "中国旅行宝典2026.html"))
            print("已复制到:", cand)
            break


if __name__ == "__main__":
    main()
