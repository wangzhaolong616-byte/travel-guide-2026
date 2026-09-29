# 📖 01 · GitHub 使用指南

本指南面向想**使用、更新、部署**这个仓库的人。即使你从没用过 GitHub，跟着做也能上手。

---

## 1. 这个仓库是怎么建起来的（了解即可）

本项目使用 GitHub 官方命令行工具 **gh CLI** 完成：

1. 在本机安装便携版 gh CLI 与 Git（无需管理员权限，绿色解压即用）
2. `gh auth login --web` 设备授权：gh 给出一个一次性验证码，用户在 github.com/login/device 输入并授权
3. `git init` 初始化本地仓库 → 提交全部文件 → `gh repo create --public --source . --push` 一键建公开仓库并推送
4. 通过 GitHub API 开启 Pages：`gh api repos/OWNER/REPO/pages -f "source[branch]=main" -f "source[path]=/"`

> 你不需要重复以上步骤，但如果想在自己电脑复刻一套，按这个顺序即可。

## 2. 获取仓库的三种方式

| 方式 | 操作 | 适合 |
|---|---|---|
| 在线浏览 | 打开仓库网页，点进任意文件直接看 | 偶尔查看 |
| 下载 ZIP | 仓库页绿色 `Code` 按钮 → `Download ZIP` | 拿走源码，不要更新 |
| Clone | `git clone https://github.com/OWNER/travel-guide-2026.git` | 长期使用/参与更新 ✅ |

## 3. 最常用的操作：更新一个省份的内容

以"修改四川内容"为例：

```bash
# 1. 进入仓库目录（本机克隆的位置）
cd travel-guide-2026

# 2. 用任意编辑器打开 content/sichuan.json，修改内容
#    （注意保持 JSON 格式合法，规范见根目录 SPEC.md）

# 3. 校验格式是否正确（需要 Python 3.10+）
python tools/check_json.py

# 4. 重新构建单文件 HTML（同时更新离线版与在线版入口）
python build.py

# 5. 提交并推送
git add .
git commit -m "更新四川内容：补充xx景点"
git push
```

推送后 GitHub Pages 会在 **约 1 分钟内自动重新部署**，刷新在线版即可看到更新。

## 4. 不装任何工具：用 GitHub 网页版直接改

1. 打开仓库 → 进入 `content/` → 点击要改的 JSON 文件
2. 点右上角 **铅笔图标**（Edit this file）登录后即可编辑
3. 改完点右上角 **Commit changes**，填写一句修改说明（如"补充洛阳汉服体验"）
4. ⚠️ 网页版改完 JSON 后，**还需在网页上改 `index.html` 和 `中国旅行宝典2026.html` 才能让在线版生效**——这两个文件是构建产物，网页改 JSON 不会自动重建。所以推荐本地跑 `build.py`，或提 Issue 请维护者重建。

## 5. GitHub Pages 是怎么工作的

- Pages 从 **main 分支根目录** 读取 `index.html` 作为网站首页
- 访问地址：`https://用户名.github.io/travel-guide-2026/`
- 每次 `git push` 到 main，GitHub 自动重新构建部署，约 1 分钟生效
- 查看部署状态：仓库页 **Actions** 标签 → `pages build and deployment` 工作流
- 如需手动开关：仓库 **Settings → Pages**

## 6. 提 Issue 与 Pull Request

- **发现问题**（内容错误、功能 bug）：仓库页 → Issues → New issue，写清"哪个省份/哪个功能 + 期望 vs 实际"
- **贡献内容**：Fork 仓库 → 自己的副本里修改 → 发起 Pull Request，写清改了什么。维护者合并后自动上线

## 7. 常用命令速查

```bash
git status                 # 看当前改动
git pull                   # 拉取云端最新
git add .                  # 暂存全部改动
git commit -m "说明"        # 提交
git push                   # 推送到 GitHub（触发 Pages 部署）
git log --oneline -10      # 看最近10次提交
```

> 💡 Windows 用户推荐配合 GitHub Desktop（图形界面）使用，上面的命令行操作它全都能点出来。
