# Academic Research Skills — Claude Code 学术研究技能套件

[![Version](https://img.shields.io/badge/version-v3.0-blue)](https://github.com/Leooo-Huang/academic-research-skills)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

[English](README.md)

基于 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 技能系统构建的学术研究自动化套件。50+ 个 AI agent 覆盖从论文发现到终稿输出的完整流程，内置引用验证机制——每篇引用均通过 arXiv 页面实际访问确认，无法验证的论文直接丢弃。

---

## 架构

套件由五个技能模块组成，各自独立运作，也可通过 Pipeline 串联为完整流水线：

| 模块 | 版本 | Agent 数 | 职责 |
|------|------|---------|------|
| **Discovery** | v2.1 | 4 阶段 | 论文发现：Semantic Scholar + arXiv API 检索，社区信号聚合，引用图谱扩展，重要性评分 |
| **Deep Research** | v2.4 | 13 | 研究问题建模（FINER 评分）、系统文献检索、跨源综合、偏倚评估、荟萃分析 |
| **Academic Paper** | v2.4 | 12 | 结构设计、论证构建、草稿撰写、引用合规（APA/IEEE/Chicago/MLA/Vancouver）、LaTeX/PDF 排版 |
| **Paper Reviewer** | v1.4 | 5 | 模拟评审团——主编 + 3 位领域审稿人 + 魔鬼代言人，0-100 量化评分 |
| **Pipeline** | v2.8 | 调度器 | 11 阶段工作流，含两个强制完整性校验点、两轮同行评审、苏格拉底式修订辅导 |

完整流水线单次运行可产出 50-100 篇经验证论文，在阶段 2.5 和 4.5 两个检查点拦截虚假引用，最终输出可投稿论文。

---

## 安装

```bash
git clone https://github.com/Leooo-Huang/academic-research-skills.git ~/.claude/skills/academic-research-skills
```

可选——安装 Python 依赖以启用带速率控制的 API 访问：

```bash
pip install requests arxiv huggingface-hub
```

未安装 Python 时自动降级为 Claude 内置 WebFetch，功能不受影响，吞吐量降低。

---

## 使用方式

在 Claude Code 中通过自然语言触发：

- **论文发现**：`"Find papers on [主题]"` — 执行四阶段发现流程
- **完整流水线**：`"I want to write a paper on [主题]"` — 从发现到 PDF 的 11 阶段全流程
- **深度研究**：`"Research the impact of AI on [领域]"` — 13 agent 协作分析，含研究空白识别
- **论文评审**：`"Review this paper"` — 5 人模拟评审，量化评分
- **研究辅导**：`"Guide my research on [主题]"` — 苏格拉底对话 + SCR 反思协议

### 发现流程

```
阶段 A: 社区情报收集    →  X、GitHub、HuggingFace 趋势信号
阶段 B: 系统检索        →  S2 + arXiv + HF + GitHub API，200-500 篇候选
阶段 C: 逐篇验证        →  每篇论文通过 arXiv 页面访问确认
阶段 D: 引用图谱扩展    →  S2 API 正向/反向引用遍历
阶段 E: 重要性评分      →  PIS（Paper Importance Score）排序
```

**PIS 评分体系**：综合引用速度、发表场所声望、社区热度和时效衰减。权重按论文年龄动态调整——新论文侧重相关性，经典论文侧重影响力。

### 完整流水线

```
发现 → 研究 → 写作 → 验证 → 评审 → 修订 → 发表
```

11 个阶段，两个强制完整性校验点，两轮同行评审。

---

## 产出示例

完整流水线的真实产物见 [examples/showcase/](examples/showcase/)：

| 产物 | 说明 |
|------|------|
| [终稿](examples/showcase/full_paper_apa7.pdf) | APA 7.0 格式，LaTeX 排版 |
| [完整性报告](examples/showcase/integrity_report_stage2.5.pdf) | 拦截 15 条虚假引用 + 3 处统计错误 |
| [评审报告](examples/showcase/stage3_review_report.pdf) | 5 人评审团，0-100 量化评分 |
| [发表后审计](examples/showcase/post_publication_audit_2026-03-09.pdf) | 3 轮自动检查后仍发现 21/68 处问题 |

---

## 配置

**推荐模型**：Claude Opus 4.6（Max plan）。完整流水线 token 消耗可能超过 200K。

**无人值守模式**：`claude --dangerously-skip-permissions`

**可选 API Key**：

| Key | 用途 | 费用 |
|-----|------|------|
| `S2_API_KEY` | 提高 Semantic Scholar 速率限制 | 免费 |
| `OPENAI_API_KEY` | 社区情报采集（last30days 技能） | 付费 |

---

## 项目结构

```
academic-research-skills/
├── discovery/               论文发现引擎 (v2.1)
│   ├── scripts/             research_radar.py — Python API 客户端
│   └── agents/
├── deep-research/           13 agent 研究团队 (v2.4)
├── academic-paper/          12 agent 写作流水线 (v2.4)
├── academic-paper-reviewer/ 5 人模拟评审 (v1.4)
├── academic-pipeline/       11 阶段流水线调度器 (v2.8)
├── shared/                  跨模块数据合约
└── examples/showcase/       真实流水线产物
```

---

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — 非商业用途可自由使用，需注明出处。

基于 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu。
