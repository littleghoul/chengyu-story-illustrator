# 成语水墨图文卡 `chengyu-story-illustrator`

一个面向公务员考试言语理解与表达学习的 Codex skill：先核对成语释义、来源、用法和易错点，再规划画面并生成水墨国风成语学习卡片。

## 功能

- 将成语学习目标提炼为一个清晰的视觉记忆钩子
- 优先检索百度汉语，核对释义、拼音、来源、用法和常见误用
- 按古代故事、现代寓意、辨析提醒三类场景选择画法
- 约束图像生成只产出无文字主图，避免中文错字
- 使用 Pillow 脚本确定性叠加标题、拼音、释义、来源和易错提醒

## 安装

将本目录复制到 Codex skill 目录，并保持目录名为 `chengyu-story-illustrator`：

```text
~/.codex/skills/chengyu-story-illustrator/
```

Windows 默认位置通常是：

```text
C:\Users\<用户名>\.codex\skills\chengyu-story-illustrator\
```

也可以将仓库作为 skill 目录直接使用，只要 Codex 能发现其中的 `SKILL.md`。

## 使用

在 Codex 中提出类似请求：

```text
使用 $chengyu-story-illustrator，制作“首当其冲”的公考成语学习卡片。
```

skill 会先核对资料，再生成无文字主图，并用 `scripts/compose_card.py` 叠加准确中文文案。

## 本地排版脚本

依赖 Python 3.10+ 和 Pillow：

```bash
python -m pip install Pillow
python scripts/compose_card.py \
  --input <无文字主图.png> \
  --output <最终卡片.png> \
  --idiom "首当其冲" \
  --pinyin "shǒu dāng qí chōng" \
  --meaning "最先受到攻击或遭遇灾难。" \
  --source "未查到稳定来源，本卡以现代用法为准。" \
  --warning "不是第一个主动行动，也不是冲锋在前。"
```

脚本会优先使用 Windows 微软雅黑或 Linux Noto CJK 字体；如未找到中文字体，可通过 `--font` 指定字体文件。

## 目录

```text
.
├── SKILL.md
├── agents/openai.yaml
├── assets/icon.png
├── references/card-template.md
├── scripts/compose_card.py
├── LICENSE
└── README.md
```

## 资料与责任边界

skill 只要求对公开词典内容进行核对、概括和改写，不应复制长段落。来源、释义或用法无法稳定核实时，应保留不确定性或省略来源，不虚构典故细节。生成图片中的中文由本地排版脚本绘制，最终交付前仍应逐字校对。

## 贡献

欢迎提交触发描述、学习流程、模板和排版脚本方面的改进。请保持 skill 的核心约束：准确释义优先、一个画面只服务一个核心语义、图像与文字分离生成。
