# Academic Research Skills — Claude Code 学术研究技能套件

[![Version](https://img.shields.io/badge/version-v3.0-blue)](https://github.com/Leooo-Huang/academic-research-skills)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Skills](https://img.shields.io/badge/skills-5-green)]()
[![Agents](https://img.shields.io/badge/agents-50+-orange)]()

[English](README.md)

> **50-100 篇验证论文。零幻觉引用。可投稿论文。一次对话完成。**

LLM 会编造看起来真实但根本不存在的引用。这个项目解决这个问题。50+ 个 AI agent 组成的技能套件，自动化学术研究全流程——从实时论文发现（每篇引用都经过验证）到可投稿论文，附带模拟同行评审。

---

## 问题

你让 Claude 帮你找论文，它编出了一堆看起来很真的引用——但这些论文根本不存在。你基于这些虚假来源写了文献综述，然后论文被直接退稿。

## 解决方案

```
你: "Find papers on robot motion retargeting"

Claude: [Phase A] 扫描 X/Twitter、GitHub、HuggingFace 社区信号...
       [Phase B] 查询 Semantic Scholar API... 找到 34 篇候选
       [Phase C] 逐篇在 arXiv 上验证... 28 篇确认存在
       [Phase D] 通过引用图谱扩展... 新增 12 篇
       [Phase E] 评分排序...

       发现完成：40 篇验证论文，0 篇幻觉引用。
       可以开始深度分析。
```

每一篇引用都通过实际访问其 arXiv 页面来验证。无法确认的论文直接丢弃——绝不猜测。

---

## 安装

```bash
git clone https://github.com/Leooo-Huang/academic-research-skills.git ~/.claude/skills/academic-research-skills
```

可选（加速论文发现）：
```bash
pip install requests arxiv huggingface-hub
```

完成。打开 Claude Code 直接使用。

---

## 你可以做什么

| 对 Claude 说 | 会发生什么 |
|-------------|----------|
| `"Find papers on [主题]"` | 从 S2 + arXiv + 社区信号中发现 50-100 篇验证论文 |
| `"I want to write a paper on [主题]"` | 运行完整 11 阶段流水线：发现 → 研究 → 写作 → 审稿 → 修订 → 发表 |
| `"Research the impact of AI on [领域]"` | 13 agent 深度研究，含缺口分析和文献综合 |
| `"Review this paper"` | 5 人模拟同行评审（主编 + 3 位审稿人 + 魔鬼代言人） |
| `"Guide my research on [主题]"` | 苏格拉底对话 + SCR 反思协议，帮你理清思路 |

---

## 完整流水线

```
发现 ──→ 研究 ──→ 写作 ──→ 验证 ──→ 评审 ──→ 修订 ──→ 发表
50-100    13 agent  12 agent  100%     5 人     回应     LaTeX
篇论文    研究团队   写作管线  引用验证  模拟评审  反馈     → PDF
```

11 个阶段。每篇引用都经过验证。两轮同行评审。零容忍虚假引用。

---

## 5 个技能，50+ 个 Agent

### 1. Discovery v2.1 — 论文发现引擎

**反幻觉核心。** Python 优先的 API 访问，内置速率控制。

| 阶段 | 目的 | 方法 |
|------|------|------|
| 社区情报 | 热点趋势、研究痛点 | last30days / WebSearch |
| 系统搜索 | 200-500 篇候选 | Python → Semantic Scholar + arXiv + HF + GitHub |
| 逐篇验证 | 这篇论文真的存在吗？ | Python → 访问每篇 arXiv 页面 |
| 引用扩展 | 它引用了谁？谁引用了它？ | Python → S2 引用图谱 API |

**评分系统**：PIS（论文重要性评分）——引用速度 + 发表场所声望 + 社区热度 + 时效衰减。权重按论文年龄自动调整：新论文看相关性，老论文看影响力。

### 2. Deep Research v2.4 — 深度研究

13 个 agent：研究问题制定（FINER 评分）、苏格拉底导师（SCR 反思协议）、系统文献检索、来源验证、跨源综合、偏倚风险评估、荟萃分析、编辑审查。

7 种模式：完整 / 快速 / 系统综述 / 苏格拉底 / 事实核查 / 文献综述 / 论文评审

### 3. Academic Paper v2.4 — 论文写作

12 个 agent：需求分析、文献策略、结构设计、论证构建、草稿撰写、引用合规（APA/IEEE/Chicago/MLA/Vancouver）、双语摘要、可视化、修订辅导、排版格式（LaTeX/DOCX/PDF）。

### 4. Academic Paper Reviewer v1.4 — 论文评审

模拟 5 人评审团：主编 + 3 位领域审稿人 + 魔鬼代言人。0-100 质量评分。决策映射：>=80 接受，65-79 小修，50-64 大修，<50 拒稿。

### 5. Academic Pipeline v2.8 — 流水线调度

11 阶段工作流调度器，含强制完整性验证（阶段 2.5 + 4.5）、两轮同行评审、苏格拉底修订辅导、协作质量评估。

---

## 为什么用 Python？

Discovery v2.1 用 Python 脚本（`research_radar.py`）替代 Claude 内置的 WebFetch 来调用 API。原因：

| | WebFetch | Python 脚本 |
|--|---------|------------|
| 速率控制 | 无法控制，429 错误缓存 15 分钟 | 指数退避（10s → 30s → 120s） |
| 请求间隔 | 无法添加延时 | 每次请求间隔 1.5s |
| 批量处理 | 一次一篇 | 一条命令验证 80 篇 |
| 错误恢复 | 卡在缓存的错误上 | 自动重试，优雅降级 |

**没有 Python？没关系。** 技能会自动降级为 WebFetch。结果一样，只是更慢，可能触发速率限制。

---

## 真实产出

查看完整流水线产出：**[examples/showcase/](examples/showcase/)**

| 产物 | 说明 |
|------|------|
| [最终论文（英文）](examples/showcase/full_paper_apa7.pdf) | APA 7.0 LaTeX 排版 |
| [完整性报告](examples/showcase/integrity_report_stage2.5.pdf) | 发现 15 个虚假引用 + 3 个统计错误 |
| [同行评审报告](examples/showcase/stage3_review_report.pdf) | 完整 5 人评审 + 0-100 评分 |
| [发表后审计](examples/showcase/post_publication_audit_2026-03-09.pdf) | 在 3 轮检查后仍发现 21/68 个问题 |

---

## 配置

**推荐模型**：Claude Opus 4.6（Max plan）。完整流水线可能超过 200K token。

**无中断运行**：`claude --dangerously-skip-permissions`

**可选 API Key**：
| Key | 用途 | 费用 |
|-----|------|------|
| `S2_API_KEY` | 提高 Semantic Scholar 速率限制 | 免费 |
| `OPENAI_API_KEY` | last30days 技能（Reddit/X/YouTube 情报） | 付费 |

---

## 项目结构

```
academic-research-skills/
├── discovery/           ← 论文发现引擎 (v2.1)
│   ├── scripts/         ← research_radar.py (Python API 客户端)
│   └── agents/
├── deep-research/       ← 13 agent 研究团队 (v2.4)
├── academic-paper/      ← 12 agent 写作流水线 (v2.4)
├── academic-paper-reviewer/ ← 5 人同行评审 (v1.4)
├── academic-pipeline/   ← 11 阶段调度器 (v2.8)
├── shared/              ← 跨技能数据合约
└── examples/showcase/   ← 真实流水线产出
```

---

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 许可

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — 非商业用途可自由分享和改编，需注明出处。

基于 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu。
