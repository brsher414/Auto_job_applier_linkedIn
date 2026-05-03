# 项目改动说明

更新时间：2026-04-26

这份文档记录我们为了让这个 LinkedIn 自动投递工具更适合当前求职场景所做的改动。重点不是逐行罗列代码，而是说明每个改动解决了什么痛点。

## 1. 环境安装不稳定

痛点：

- 原项目依赖比较散，换机器或重装环境时容易漏包。
- 直接用系统 Python 跑，依赖版本不好复现。

解决：

- 增加 `pyproject.toml`，用 `uv` 管理本地环境和依赖。
- 增加 `.python-version` 和 `uv.lock`，让 Python 与依赖版本更可控。
- 在本文档中记录常用安装、校验和启动命令。

常用命令：

```powershell
uv sync
uv run python runAiBot.py
uv run python -c "from modules.validator import validate_config; print(validate_config())"
uv run python -m py_compile runAiBot.py
```

## 2. 简历不适合英文投递

痛点：

- 原始简历更偏中文场景，LinkedIn 投递外企和海外岗位时不够合适。
- 默认上传路径不是当前准备好的英文简历。

解决：

- 增加英文简历 HTML 和 PDF：
  - `resume/resume_zhibi_liu_en.html`
  - `resume/resume_zhibi_liu_en.pdf`
- 增加统一的 HTML 转 PDF 脚本：`scripts/generate_resume_pdfs.py`。
- `scripts/generate_english_resume_pdf.py` 保留为英文 PDF 生成入口，但也改为从 HTML 打印，而不是用 FPDF 重新排版。
- 将默认投递简历改为 `resume/resume_zhibi_liu_en.pdf`。
- 增加 `chinese_resume_path`，当前指向中文 PDF 简历。
- 投递时会按 JD 语言选择简历：中文 JD 用中文简历，英文或未知 JD 用英文简历。
- 如果中文 JD 被识别出来但中文简历文件不存在，会自动回退英文简历。

## 3. 搜索目标和用户背景不匹配

痛点：

- 原项目默认搜索软件工程岗位，不符合当前 Data / AI workflow 方向。
- 搜索词太散会导致轮次变长、结果噪音变大。

解决：

- 将搜索词收敛为当前更想投的方向：
  - Data Analyst
  - Business Analyst
  - Data Scientist
  - AI Agent
- 设置上海、北京优先，之后再看海外地点。
- 当前搜索轮次：
  - `Shanghai and Beijing`
  - `Overseas`
- 每个搜索轮次增加 `region` 标签：
  - 国内轮次：`china`
  - 海外轮次：`overseas`

## 4. 不用手动改配置决定投递地区

痛点：

- 之前想只投国内、只投海外或全部都投，需要手动编辑 `config/search.py`。
- 临时切换投递地区容易忘记改回去，也容易改错。

解决：

- 启动时增加地区选择弹窗：
  - China only
  - Beijing only
  - Shanghai only
  - Overseas only
  - All regions
- 支持命令行参数跳过弹窗：

```powershell
uv run python runAiBot.py --region beijing
uv run python runAiBot.py --region shanghai
uv run python runAiBot.py --region china
uv run python runAiBot.py --region overseas
uv run python runAiBot.py --region all
```

- 也支持环境变量：

```powershell
$env:AUTO_APPLY_REGION="china"; uv run python runAiBot.py
```

- 这样日常切换地区不需要再改配置文件。
- 北京单独运行会只保留 `Beijing, China`，并继续使用北京 `geoId`，避免 LinkedIn 自动解析到下属地点。

## 5. LinkedIn 的 Location filter 不可靠

痛点：

- `All filters` 里的 Location 不一定出现 Shanghai / Beijing。
- 如果只依赖筛选面板，可能根本没选上目标城市。

解决：

- 改为使用页面顶部的 Location 搜索框。
- 每个地点单独输入并搜索。
- 执行顺序是地点优先：先把顶部 Location 设为一个地点，再跑该地点下的全部搜索词。
- `All filters` 里不再动态选择 Location。
- 对上海和北京增加 LinkedIn `geoId`，避免 LinkedIn 把 `Beijing, China` 自动解析成北京下属的小地点，例如 `Xinchengzi, Beijing, China`。

## 6. 筛选条件过窄，容易漏掉合适岗位

痛点：

- 行业筛选容易误伤数据岗位，例如金融、咨询、医疗器械、互联网都可能有合适岗位。
- 工作模式筛选也会漏掉岗位，尤其 LinkedIn 标注不一定准确。

解决：

- 取消 Industry 限制：`industry = []`。
- 取消 On-site / Hybrid / Remote 限制：`on_site = []`。
- 时间窗口从 `Past week` 放宽为 `Past month`。
- 保留 `Full-time`。
- 保留经验级别：
  - Entry level
  - Associate
  - Mid-Senior level
- 重新开启 `LinkedIn Apply`，优先保证自动投递流程可控。

## 7. LinkedIn 没有可用的薪资内置筛选

痛点：

- 当前页面没有稳定的内置 Salary filter。
- 但国内岗位列表和详情顶部可能会显示 `CN¥25K/month - CN¥35K/month` 这类薪资卡片。
- 只靠关键词识别职位描述不可靠，也不符合需求。

解决：

- 内置薪资筛选设为空：`salary = []`。
- 增加 `minimum_monthly_salary_cny = 20000`。
- 程序读取 LinkedIn 页面上可见的薪资卡片文本，而不是读职位描述关键词。
- 薪资来源包括：
  - 左侧职位卡片。
  - 右侧职位详情顶部卡片。
- 只对中国岗位启用薪资过滤。
- 海外岗位不做薪资过滤。
- 没有显示薪资的岗位不会因为薪资被跳过。
- 控制台会打印原始薪资片段，方便确认程序确实读到了页面内容，例如：

```text
Visible salary card text for "Data Analyst | Example Company": CN¥25K/month - CN¥35K/month
Detected LinkedIn visible salary ceiling: 35000 CNY/month
```

## 8. 中文 LinkedIn 页面兼容成本太高

痛点：

- LinkedIn 中文页面的按钮文案、分页 aria-label、弹窗流程和英文版不一致。
- 继续维护中英文双套 UI 选择器会增加不稳定性。
- 用户已经决定把 LinkedIn 页面切换为英文版。

解决：

- 删除针对中文 LinkedIn UI 的按钮文本兼容。
- 只保留英文 UI 选择器：
  - All filters
  - Show results
  - Next / Continue
  - Review
  - Submit application
  - Done / Close
  - Discard / Cancel
- 删除中文分页 aria-label 兼容，只保留英文 `Page N`。
- 将按钮辅助函数从 `click_localized_button` 改名为 `click_labeled_button`，避免误导。

说明：

- 这不会删除中文公司黑名单，例如 `尼尔森`。
- 这也不会删除国内薪资里的 `CN¥` 解析，因为它不是中文 UI，而是薪资格式。

## 9. LinkedIn Apply 行为差异

痛点：

- 外部申请页面通常不能由这个工具继续自动填写。
- 自动投递主要依赖 LinkedIn 内部申请弹窗。
- LinkedIn 新页面筛选项已经是 `LinkedIn Apply`，不再是旧文案 `Easy Apply`。

解决：

- 增加明确配置 `linkedin_apply_only = True`。
- 筛选阶段只打开 `LinkedIn Apply`。
- `easy_apply_only` 只作为旧代码兼容别名保留，不再作为主要配置入口。
- 申请阶段也增加了内部申请弹窗检测。
- 如果识别为外部申请，会记录或跳过，不强行处理第三方网站。

## 10. Chrome / Driver 版本容易报错

痛点：

- `undetected_chromedriver` 下载的 driver 版本可能和本机 Chrome 不匹配。
- Windows 下临时 profile 参数之前拼错，可能导致 Chrome 启动异常。

解决：

- 自动检测本机 Chrome major version，并传给 `undetected_chromedriver`。
- 显式设置本机 Chrome binary path。
- 修复 Windows 临时 Chrome profile 路径，只返回路径本身，不重复拼 `--user-data-dir=...`。
- 保留 `safe_mode = True`，使用本地 `.chrome-profile` 运行时 profile。

## 11. 表单回答更贴近当前投递场景

痛点：

- 签证问题不能一律固定回答。
- 中国岗位和海外 remote 岗位的 sponsorship 逻辑不同。
- 电话区号下拉框可能需要选择 `+86`。

解决：

- 增加中国地点识别逻辑。
- 中国岗位的 sponsorship 默认按不需要处理。
- 非中国岗位的 sponsorship / visa 问题按需要 sponsorship 处理。
- 工作许可问题和 sponsorship 问题分开处理：海外岗位不会自动声明已经持有当地 work authorization / work permit。
- 遇到 `without sponsorship` 这类反向问法会自动反转 Yes/No。
- 如果表单下拉项里有 `+86`，优先选择中国区号。
- 增加日本岗位日语水平配置：`japanese_proficiency`。
- 日语水平题支持英文和日文标签识别，例如 Japanese proficiency / 日本語 / JLPT。
- 如果日语水平题无法匹配到安全选项，程序会提示手动处理，不会随机乱选。
- 增加英语水平配置：`english_proficiency`，默认 `Professional`。
- 英语水平题支持 English proficiency / English level / English fluency 等标签识别。
- 如果英语水平题无法匹配到配置选项，程序会提示手动处理，不会随机乱选。
- 增加中文/普通话水平配置：`chinese_proficiency`，默认 `Native`。
- 中文水平题支持 Chinese / Mandarin / Cantonese / 中文 / 普通话 / 粤语 等标签识别。
- 如果中文水平题无法匹配到配置选项，程序会提示手动处理，不会随机乱选。
- 对“是否曾经/当前是本公司、集团公司或其他指定公司的雇员”这类问题，默认回答 `No`。

## 12. 运行时可观察性不足

痛点：

- 之前不知道程序到底有没有读到薪资卡片。
- 筛选失败时不容易判断是页面没显示，还是解析失败。

解决：

- 增加薪资原文日志。
- 增加薪资解析结果日志。
- 没读到薪资时也明确打印：

```text
No visible CNY salary found for "...". Salary filter will not skip it.
```

## 13. 当前保留的主要策略

- 搜索地点：上海、北京优先，然后海外地点。
- 搜索词：Data Analyst / Business Analyst / Data Scientist / AI Agent。
- 时间：Past month。
- 排序：Most recent。
- 工作类型：Full-time。
- 经验：Entry level / Associate / Mid-Senior level。
- 行业：不限制。
- 工作模式：不限制。
- 申请方式：LinkedIn Apply。
- 国内薪资：可见薪资上限低于 20k/月才跳过。
- 海外薪资：不限制。
- 黑名单：保留 Nielsen / NielsenIQ / 尼尔森等。

## 14. 校验

每次主要改动后使用以下命令校验：

```powershell
uv run python -m py_compile runAiBot.py modules\validator.py config\search.py
uv run python -c "from modules.validator import validate_config; print(validate_config())"
```

期望结果：

```text
True
```

## 15. 运行时生成文件

这些是运行或测试时生成的本地文件，不属于功能改动：

- `.chrome-profile/`
- `.edge-pdf-profile/`
- 日志文件。
- 截图文件。
