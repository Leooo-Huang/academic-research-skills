# AI + 机器人研究全栈工作流

> 方向：AI 大模型 + 机器人
> 工具栈：academic-research-skills + claude-scientific-skills(research-lookup) + AI-Research-SKILLs(Orchestra)
> 原则：每个阶段 MECE、零重叠、每个工具只做它不可替代的事

---

## 架构总览

```
阶段 0          阶段 1          阶段 2          阶段 3          阶段 4          阶段 5
社区情报 ──────→ 文献调研 ──────→ 实验工程 ──────→ 论文写作 ──────→ 投稿策略 ──────→ 审稿修订
(发现方向)      (穷举论文)       (跑实验)        (写论文)        (选会议)        (回应审稿)
    ▲                                                                │
    └──────────────────── 持续监控（贯穿全程）─────────────────────────┘
```

### 工具职责边界（MECE）

| 来源 | 只负责 | 不负责 |
|------|--------|--------|
| X / Reddit / HuggingFace / GitHub | 社区情报 + 趋势嗅探 | 穷举检索 |
| Semantic Scholar + arXiv API | 穷举检索 + 引用图谱 | 分析、写作 |
| research-lookup (Perplexity) | 跨领域 AI 辅助发现 | 穷举检索 |
| deep-research 13-agent | 文献深度分析 | 检索、实验 |
| Orchestra 86 skills | ML 实验工程 | 检索、写作 |
| academic-research 12-agent | 论文写作 | 检索、实验 |
| Venue 分析框架 | 投稿选择 | 写作、实验 |
| academic-research 审稿系统 | 审稿修订 | 其他一切 |

---

## 安装

```bash
# 1. academic-research-skills（分析 + 写作 + 审稿）
git clone https://github.com/Imbad0202/academic-research-skills.git ~/.claude/skills/academic-research-skills

# 2. 只从 claude-scientific-skills 拿 research-lookup（AI 辅助检索）
git clone --depth 1 https://github.com/K-Dense-AI/claude-scientific-skills.git /tmp/css
cp -r /tmp/css/scientific-skills/research-lookup ~/.claude/skills/research-lookup
rm -rf /tmp/css

# 3. AI-Research-SKILLs（实验工程）
npx @orchestra-research/ai-research-skills
# 选装：Model Architecture, Fine-Tuning, Distributed Training, Optimization,
#       Inference & Serving, Multimodal, Post-Training, Agents, MLOps, Evaluation
# 不装：ML Paper Writing, Research Ideation, Autoresearch

# 4. 直接 API 访问（文献检索主力）
uv pip install semanticscholar arxiv

# 5. 配置 API Key（research-lookup 需要）
# PARALLEL_API_KEY=你的key
# OPENROUTER_API_KEY=你的key
# S2_API_KEY=你的key（可选，提高 Semantic Scholar rate limit）
```

---

## 阶段 0：社区情报

### 目标
在正式文献调研之前，用社区信号发现研究方向、热点趋势和未被论文覆盖的实践洞察。

### 为什么需要这一步
- 论文有 3-12 个月的滞后（写作→投稿→审稿→发表）
- X/Reddit 上的讨论往往领先论文 6-12 个月
- 社区的痛点和失败经验不会出现在论文里，但对选题至关重要
- 研究证明：被 X 上影响力账号推荐的论文，中位引用数高 2-3 倍

### 流程

```
步骤 A ─→ 步骤 B ─→ 步骤 C ─→ 步骤 D
信息源配置  趋势扫描   社区深挖   方向锁定
```

#### 步骤 A：信息源配置（一次性设置）

**X/Twitter 必关注账号**：

| 类别 | 账号 | 价值 |
|------|------|------|
| **论文策展人** | @_akhaliq (AK, HuggingFace) | 最快的论文推送，几小时内覆盖新 arXiv |
| **论文策展人** | @arankomatsuzaki | 另一个主要策展人，覆盖面互补 |
| **机器人/Embodied AI** | Jim Fan (NVIDIA) | GR00T/Cosmos，embodied AI 前沿 |
| **机器人学习** | Pieter Abbeel (UC Berkeley) | RL + 机器人，也主持 The Robot Brains 播客 |
| **基础模型** | Andrej Karpathy | 深度技术帖，arxiv-sanity 作者 |
| **AI 批判性思考** | Yann LeCun (Meta) | 对 AI 趋势的清醒评估 |
| **机器人现实主义** | Rodney Brooks | 对机器人炒作 vs 现实的理性评估 |
| **实验室** | MIT CSAIL, Google DeepMind, NVIDIA Research, Toyota Research Institute | 研究发布 |

**关键 hashtag**：`#robotics` `#embodiedAI` `#VLA` `#reinforcementlearning` + 会议标签 `#CoRL` `#ICRA` `#NeurIPS` `#ICLR`

**Reddit 必关注**：

| 子版块 | 价值 |
|--------|------|
| r/MachineLearning | 论文讨论、最诚实的社区评价 |
| r/robotics | 硬件+软件+研究，定期 Showcase |
| r/reinforcementlearning | RL 算法、环境、论文 |
| r/LocalLLaMA | 本地部署实践，量化经验 |

**论文发现工具**：

| 工具 | 用途 | 频率 |
|------|------|------|
| [HuggingFace Trending Papers](https://huggingface.co/papers/trending) | 社区投票的热门论文 | 每日 |
| [Papers With Code](https://paperswithcode.com/) | 论文+代码+SOTA排行榜 | 每周 |
| [Connected Papers](https://www.connectedpapers.com/) | 可视化引用网络 | 按需 |
| [arxiv-sanity-lite](https://github.com/karpathy/arxiv-sanity-lite) | 个性化 arXiv 推荐 | 每日 |
| arXiv RSS (cs.RO, cs.AI, cs.LG, cs.CV) | 原始新论文流 | 每日 |
| Semantic Scholar Research Feeds | AI 驱动的个性化推荐 | 每日 |
| Google Scholar Alerts | 关键词/作者/引用 提醒 | 自动 |

**HuggingFace 机器人生态**：

| 资源 | 说明 |
|------|------|
| [LeRobot](https://huggingface.co/lerobot) | HF 官方机器人项目，模型+数据集+工具 |
| SmolVLA | 小型 VLA 模型，单 GPU 可训练 |
| RoboMIND | 107K 真实世界演示轨迹，479 个任务 |
| 机器人数据集 | 2024→2025 从 1,145 增长到 26,991，最大类别 |

**Newsletter（每周 30 分钟）**：

| 名称 | 受众 | 重点 |
|------|------|------|
| AlphaSignal | 180K+ | GitHub 趋势 + ML/硬件 |
| Import AI (Jack Clark) | 研究者 | 政策+研究，每周 |
| The Batch (Andrew Ng) | 通用 | AI 新闻精选 |

**播客（通勤/运动时听）**：

| 播客 | 主持人 | 与你相关的原因 |
|------|--------|--------------|
| The Robot Brains | Pieter Abbeel | 直接相关：机器人+AI 顶级研究者访谈 |
| MLST | Tim Scarfe | 深度技术讨论，认知科学+AI |
| Lex Fridman Podcast | Lex Fridman | AI/机器人长访谈 |

**GitHub 监控**：

| 来源 | 方法 |
|------|------|
| [GitHub Trending](https://github.com/trending) | 按语言/时间筛选 |
| [Embodied AI Paper TopConf](https://github.com/Songwxuan/Embodied-AI-Paper-TopConf) | ICLR/NeurIPS/ICML/RSS/CoRL/ICRA/IROS/CVPR 的 embodied AI 论文 |
| [Embodied AI Paper List](https://github.com/HCPLab-SYSU/Embodied_AI_Paper_List) | 综合列表 |
| Star 增长速度 | 几天内从 0 到几千 stars = 趋势形成 |

---

#### 步骤 B：趋势扫描（每周 1 小时）

**日常扫描（5-10 分钟/天）**：
1. @_akhaliq + @arankomatsuzaki 的推文
2. HuggingFace Trending Papers
3. arXiv-sanity 或 arXiv RSS

**每周深度（30 分钟/周）**：
1. 1-2 个 Newsletter（AlphaSignal + Import AI）
2. Reddit r/MachineLearning 本周 top posts
3. GitHub Trending 机器人/AI 相关

**做什么**：
1. 记录高讨论量的主题（likes > 1K 或 comments > 100）
2. 标记跨平台出现的相同概念（X + Reddit + GitHub 同时讨论 = 强信号）
3. 注意社区的**痛点**和**失败报告**——这些是论文不会告诉你的

**输出**：`community/weekly_signals.md`

```markdown
## Week of 2026-03-16

### 强信号（多平台交叉）
- VLA scaling laws：Jim Fan 发推 + r/MachineLearning 讨论 + 3篇新 arXiv
  → 可能是下一个重要方向

### 社区痛点
- "sim-to-real transfer for dexterous manipulation still sucks"
  → r/robotics 多人抱怨，可能是研究 gap

### 新工具/数据集
- OpenClaw: 9K→60K stars in days
  → 值得关注的新框架

### 值得深读的论文
- [paper_id] 被 5+ 独立研究者引用讨论
```

---

#### 步骤 C：社区深挖

**当步骤 B 发现强信号时**：

1. **X 深度分析**：
   - 找到原始讨论帖，追踪引用链
   - 看谁在讨论——如果是领域大佬在认真讨论而非简单转发，信号更强
   - 专家 quote-tweet 中的批评意见 = 该方向的真实挑战

2. **Reddit 深挖**：
   - r/MachineLearning 的论文讨论帖——评论区比论文更诚实
   - 复现尝试帖——揭示论文没说的实际困难
   - "What is the state of X?" 帖——社区对当前现状的综合评估

3. **GitHub 验证**：
   - 有代码的论文 vs 没代码的论文——有代码的可信度更高
   - Star 数 + Fork 数 + Issue 活跃度 = 实际使用程度
   - 看 Issues 里的 bug 报告——揭示方法的真实局限

---

#### 步骤 D：方向锁定

**综合步骤 B+C 的信号，回答三个问题**：

```
1. 什么方向在升温？
   → 社区讨论量上升 + 新论文增多 + 新工具出现

2. 什么问题还没解决？
   → 社区反复抱怨 + 论文声称解决但社区不买账

3. 我能做什么差异化贡献？
   → 结合自己的背景（AI 大模型 + 机器人）找交叉点
```

**输出**：`community/direction_candidates.md`——列出 3-5 个候选方向，每个标注信号强度和信心度

**质量门控**：
- 每个候选方向必须有来自至少 2 个不同平台的信号支撑
- 不能只看一个大 V 的推文就定方向
- 候选方向进入阶段 1 的正式文献调研后才最终确认

---

## 阶段 1：文献调研

### 目标
穷举相关论文，零遗漏，过程可审计可复现。

### 流程

```
步骤 A ─→ 步骤 B ─→ 步骤 C ─→ 步骤 D ─→ 步骤 E ─→ 步骤 F
问题定义   多源检索   去重合并   引用链追踪  PRISMA筛选  输出报告
```

#### 步骤 A：研究问题定义 + 检索策略设计

**工具**：deep-research → Research Question Agent + Research Architect Agent

**做什么**：
1. 用 PICO/SPIDER 框架精确定义研究问题
2. 拆解为多组布尔检索式
3. 定义纳入/排除标准
4. 选择目标数据库

**输出示例**：
```
研究问题：
  如何利用视觉语言模型提升机器人抓取的泛化能力？

检索式矩阵：
  组1: ("vision language model" OR "VLM" OR "multimodal LLM")
       AND ("robot*" OR "manipulation" OR "embodied")
       AND ("grasp*" OR "pick and place")

  组2: ("foundation model" OR "large language model")
       AND ("robotic manipulation" OR "dexterous")
       AND ("generalization" OR "zero-shot" OR "few-shot")

  组3: ("CLIP" OR "GPT-4V" OR "LLaVA" OR "RT-2")
       AND ("robot*")

纳入标准：
  - 2020年后发表
  - 同行评审或 arXiv 预印本
  - 涉及真实机器人实验或高保真仿真

排除标准：
  - 纯 NLP/CV 无机器人应用
  - Workshop 短文（< 4页）
  - 非英文
```

**质量门控**：检索式必须由至少 2 个独立的概念维度交叉，避免过宽或过窄。

---

#### 步骤 B：多源并行检索

**工具**：三个来源并行

| 来源 | 职责 | 查什么 | 预期量级 |
|------|------|--------|---------|
| **Semantic Scholar API** | 主力穷举 | 用步骤A的布尔检索式 | 200-500 篇 |
| **arXiv API** | 补最新预印本 | 最近 6 个月，同样关键词 | 50-100 篇 |
| **research-lookup** | 补盲区 | 自然语言描述研究问题 | 10-20 篇 |

**Semantic Scholar 检索要点**：
```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()

# 每组检索式分别查
results = sch.search_paper(
    query="vision language model robot grasping",
    year="2020-2026",
    fields=["title", "abstract", "citationCount", "venue", "year",
            "authors", "externalIds", "tldr"],
    limit=500
)

# 按引用数排序，快速定位高影响力论文
results_sorted = sorted(results, key=lambda x: x.citationCount, reverse=True)
```

**arXiv 检索要点**：
```python
import arxiv

search = arxiv.Search(
    query='cat:cs.RO AND (abs:"vision language" OR abs:"VLM") AND abs:"grasp"',
    max_results=100,
    sort_by=arxiv.SortCriterion.SubmittedDate
)
```

**research-lookup 查询**：
```
"What are the latest approaches combining vision-language models
 with robotic manipulation? Focus on grasping and dexterous tasks."
```

**质量门控**：三个来源的结果必须有交叉（至少 20% 重叠），如果完全不重叠说明检索策略有问题。

---

#### 步骤 C：去重 + 合并

**做什么**：
1. 按 DOI / arXiv ID 去重
2. 合并为统一格式的文献库
3. 标记每篇论文的来源（哪些数据库找到的）

**输出**：`literature/all_papers.csv`

| DOI | 标题 | 年份 | 引用数 | 来源 | venue |
|-----|------|------|--------|------|-------|
| 10.xxx | ... | 2024 | 150 | SS+arXiv | CoRL |

**质量门控**：记录去重前后的数量，写入 PRISMA 流程图。

---

#### 步骤 D：引用链追踪（防遗漏的关键步骤）

**工具**：Semantic Scholar API 的引用图谱

**做什么**：
1. 取步骤 C 中引用数 top 20 的论文
2. 对每篇做双向追踪：
   - **前向引用**（谁引用了这篇？）→ 找到后续跟进工作
   - **后向引用**（这篇引用了谁？）→ 找到奠基性工作
3. 新发现的论文如果符合纳入标准，加入文献库

```python
# 前向引用
citations = sch.get_paper_citations(paper_id, limit=100)

# 后向引用
references = sch.get_paper_references(paper_id, limit=100)
```

**为什么必须做这步**：
- 关键词检索永远有盲区（术语变体、新造词）
- 引用链能找到关键词搜不到但学术社区公认重要的论文
- 这是系统综述方法论的标准步骤

**质量门控**：引用链追踪应新增 10-30% 的论文。如果新增 < 5%，检查是否遗漏了重要的种子论文。

---

#### 步骤 E：PRISMA 筛选

**工具**：deep-research → Synthesis Agent + Risk of Bias Agent + Devil's Advocate Agent

**流程**：
```
步骤 D 的完整文献库
    │
    ▼
初筛（标题 + 摘要）
    │ 排除明显不相关的
    │ 记录排除原因和数量
    ▼
复筛（全文阅读）
    │ 精确判断是否符合纳入标准
    │ 记录排除原因和数量
    ▼
质量评估
    │ Risk of Bias Agent 评估每篇论文的偏倚风险
    │ Devil's Advocate 挑战纳入/排除决策
    ▼
最终文献库（50-100 篇核心论文）
```

**PRISMA 流程图**：
```
数据库检索: ___ 篇 (SS: ___, arXiv: ___, research-lookup: ___)
                    │
去重后: ___ 篇      │ 去重移除: ___ 篇
                    │
初筛后: ___ 篇      │ 初筛排除: ___ 篇 (原因: ___)
                    │
引用链新增: ___ 篇
                    │
复筛后: ___ 篇      │ 复筛排除: ___ 篇 (原因: ___)
                    │
最终纳入: ___ 篇
```

**质量门控**：PRISMA 流程图必须完整，每一步的数字必须可追溯。

---

#### 步骤 F：综合分析报告

**工具**：deep-research → Synthesis Agent + Meta-Analysis Agent + Socratic Mentor Agent

**做什么**：
1. **主题聚类**：将论文按方法/任务/贡献类型分组
2. **趋势分析**：按年份画出各方法的论文数量变化
3. **Gap 识别**：Socratic Mentor 引导式提问，找出文献中的空白
4. **研究定位**：明确你的研究在现有工作中的位置

**输出**：`literature/survey_report.md`

**质量门控**：Devil's Advocate Agent 审查报告，挑战每一个"gap"是否真的存在。

---

## 阶段 2：实验工程

### 目标
实验可复现、结果可信、流程自动化。

### 流程

```
步骤 A ─→ 步骤 B ─→ 步骤 C ─→ 步骤 D ─→ 步骤 E
实验设计   环境搭建   训练迭代   评估验证   结果归档
```

#### 步骤 A：实验设计

**工具**：Orchestra → Evaluation skill + Model Architecture skill

**做什么**：
1. 定义研究假设（从阶段 1 的 Gap 出发）
2. 设计实验变量：
   - **自变量**：你要测试的方法/参数
   - **因变量**：评估指标（成功率、泛化性、推理速度）
   - **控制变量**：固定的条件（数据集、硬件、随机种子）
3. 定义 baseline 对比方案
4. 预估所需算力和时间

**输出**：`experiments/experiment_design.md`

```markdown
假设：在机器人抓取任务中，VLM 指导的抓取策略比纯视觉方法泛化性更好

自变量：
  - 方法 A：我们的 VLM-guided 方法
  - 方法 B：纯视觉 baseline (GraspNet)
  - 方法 C：Language-only baseline (SayCan)

因变量：
  - 已见物体抓取成功率 (%)
  - 未见物体抓取成功率 (%)（泛化性核心指标）
  - 推理延迟 (ms)

控制变量：
  - 数据集：ACRONYM + 自采集 50 个物体
  - 硬件：Franka Emika Panda
  - 随机种子：42, 123, 456（三次重复）
  - 训练 epoch：统一 100
```

**质量门控**：实验设计必须支持统计显著性检验（至少 3 次重复实验）。

---

#### 步骤 B：环境搭建

**工具**：Orchestra → MLOps skill + Distributed Training skill

**做什么**：
1. 环境管理：用 Docker/conda 锁定所有依赖版本
2. 数据版本管理：DVC 或 git-lfs 管理数据集
3. 实验追踪：W&B / MLflow 配置
4. 代码结构：

```
experiments/
├── configs/          # 所有超参数配置（YAML）
├── data/             # 数据处理脚本
├── models/           # 模型定义
├── scripts/
│   ├── train.py      # 训练入口
│   ├── eval.py       # 评估入口
│   └── ablation.py   # 消融实验
├── results/          # 自动保存的结果
├── Dockerfile        # 环境锁定
└── requirements.txt  # 依赖锁定（uv pip freeze）
```

**质量门控**：
- `Dockerfile` 必须能从零复现环境
- 所有超参数必须在 config 文件中，不能硬编码在代码里
- 随机种子必须可设置

---

#### 步骤 C：训练迭代

**工具**：Orchestra 按需选用

| 任务 | 用哪个 skill |
|------|-------------|
| 微调 VLM | Fine-Tuning (LoRA/QLoRA/Unsloth) |
| 多卡训练 | Distributed Training (DeepSpeed/FSDP) |
| 加速推理 | Optimization (FlashAttention) |
| 多模态融合 | Multimodal |
| RLHF 对齐 | Post-Training |

**训练循环**：
```
config v1 → 训练 → W&B 记录 → 评估 → 分析结果
    │                                      │
    │          不满意                        │
    │◄─────── 调整 config ◄────────────────┘
    │
    │          满意
    ▼
冻结 config，进入正式评估
```

**质量门控**：
- 每次训练的 config 必须自动保存到 W&B
- loss 曲线必须收敛（不收敛则停下排查，不要继续）
- 中间 checkpoint 定期保存

---

#### 步骤 D：评估验证

**工具**：Orchestra → Evaluation skill

**做什么**：
1. **主实验**：所有方法在相同条件下评估
2. **消融实验**：逐一移除你方法的关键组件，验证每个组件的贡献
3. **统计检验**：t-test / Wilcoxon 检验显著性，报告 p-value 和置信区间
4. **失败案例分析**：手动检查失败样本，归纳失败模式

**输出**：`experiments/results/`

```
results/
├── main_results.csv          # 主实验数据
├── ablation_results.csv      # 消融实验数据
├── statistical_tests.md      # 统计检验结果
├── failure_analysis.md       # 失败案例分析
└── figures/                  # 生成的图表
    ├── comparison_bar.pdf
    ├── ablation_table.pdf
    └── qualitative_examples.pdf
```

**质量门控**：
- 所有对比必须有 p-value（p < 0.05 才能声称"显著"）
- 消融实验必须覆盖你方法的每个核心模块
- 必须有失败案例分析（审稿人一定会问）

---

#### 步骤 E：结果归档

**做什么**：
1. 所有模型权重保存到持久存储
2. 所有实验 config 归档
3. 写一份可复现指南：`experiments/REPRODUCE.md`
4. 验证复现性：在干净环境中从 `Dockerfile` 开始重跑，确认结果一致

**质量门控**：另一个人（或你自己换台机器）能只看 `REPRODUCE.md` 复现出 ±1% 以内的结果。

---

## 阶段 3：论文写作

### 目标
符合顶会/顶刊标准的完整论文，逻辑严密、图表专业。

### 流程

```
步骤 A ─→ 步骤 B ─→ 步骤 C ─→ 步骤 D ─→ 步骤 E
故事线     初稿      图表      引用      内审
```

#### 步骤 A：故事线设计

**工具**：deep-research → Socratic Mentor Agent

**在写任何文字之前**，先确定：

```
1. 一句话概括贡献：
   "我们提出了 XXX，它是第一个 YYY 的方法，在 ZZZ 上达到了 SOTA。"

2. 核心叙事线：
   问题（为什么重要）
   → 现有方法的局限（为什么现在的不行）
   → 我们的洞察（为什么我们的方法能解决）
   → 方法（怎么做的）
   → 结果（效果如何）
   → 意义（对领域的影响）

3. 目标读者：
   - 主审稿人可能是哪个方向的？
   - 他们最关心什么？
   - 他们可能提出什么质疑？
```

**质量门控**：故事线必须通过"电梯测试"——30 秒内能向非专家解释清楚你做了什么、为什么重要。

---

#### 步骤 B：初稿生成

**工具**：academic-research-skills → 12-agent 写作团队

**分工**：

| Agent | 职责 | 关键要求 |
|-------|------|---------|
| Introduction Agent | 引言 | 三段式：大背景→具体问题→我们的贡献 |
| Literature Agent | 相关工作 | 不是罗列论文，是按主题组织+指出不足 |
| Methods Agent | 方法 | 数学符号一致、足够复现的细节 |
| Results Agent | 实验结果 | 先说 setup 再说 results，表格先于文字 |
| Discussion Agent | 讨论 | 局限性必须诚实，不要回避 |
| Conclusion Agent | 结论 | 不重复摘要，强调 insight 和 future work |
| Abstract Agent | 摘要 | 最后写（等其他部分定稿后） |

**写作原则**：
- 每段一个论点，首句就是论点（topic sentence）
- 段与段之间有逻辑连接词
- 被动语态少用（"We propose" > "It is proposed"）
- 避免模糊表述（"significantly better" → "12.3% higher"）

**质量门控**：Editor-in-Chief Agent 检查全文一致性（术语、符号、时态、人称）。

---

#### 步骤 C：图表制作

**原则**：图表是审稿人最先看的东西，必须独立可读。

**要求**：
1. **Figure 1**（方法概览图）：不看正文也能大致理解你的方法
2. **定量结果表**：加粗最优、下划线次优、标注统计显著性
3. **定性对比图**：并排展示你的方法 vs baseline 的输出
4. **消融实验表**：清晰展示每个组件的贡献
5. **所有图**：矢量格式（PDF），字体 ≥ 8pt，colorblind-friendly 配色

**质量门控**：
- 每张图都有完整的 caption（不需要看正文就能理解）
- 打印成黑白后信息不丢失（不能只靠颜色区分）

---

#### 步骤 D：引用管理

**工具**：academic-research-skills → References Agent

**做什么**：
1. 所有引用使用 BibTeX
2. 验证每条引用的完整性（作者、标题、年份、venue、页码/DOI）
3. 检查自引比例（< 20%）
4. 确保引用了目标 venue 近 2 年的论文（审稿人可能就是这些作者）

**质量门控**：
- 零 "et al." 错误
- 零格式不一致（会议名称、缩写统一）
- 引用数量合理（顶会论文通常 30-60 篇）

---

#### 步骤 E：内部审查

**工具**：deep-research → Devil's Advocate Agent

**在提交审稿之前**：
1. Devil's Advocate 逐段挑战：
   - 这个 claim 有实验支撑吗？
   - 这个对比公平吗？
   - 这个 limitation 你承认了吗？
2. 检查常见被拒原因：
   - [ ] 贡献不够新（和已有工作差异不明确）
   - [ ] 实验不够强（缺 baseline / 缺消融 / 缺统计检验）
   - [ ] 写作不清楚（方法描述不足以复现）
   - [ ] 相关工作遗漏（漏引了重要论文）

**质量门控**：Devil's Advocate 的所有质疑都必须有回应或修改，不能无视。

---

## 阶段 4：投稿策略

### 目标
选择最匹配的 venue，最大化录用概率和影响力。

### 为什么需要单独一个阶段
- 同一篇论文投不同会议，录用概率可以相差 3 倍
- 错误的 venue 选择 = 浪费 3-6 个月审稿周期
- venue 的审稿人池决定了你需要怎么写和强调什么

### 流程

```
步骤 A ─→ 步骤 B ─→ 步骤 C ─→ 步骤 D
Venue 全景  匹配分析   时间规划   格式适配
```

#### 步骤 A：Venue 全景图

**AI + 机器人领域 Venue 数据库**：

##### Tier 1 机器人专属会议（最高声望）

| 会议 | 录用率 | 投稿量 | 周期 | 特点 |
|------|--------|--------|------|------|
| **RSS** | 28-33% | ~600 | 1月底截稿→4月通知→7月开会 | 单 track，最精选，理论深度+真机实验 |
| **CoRL** | ~28-30% | ~670+ | 6月截稿→8月通知→11月开会 | **你的方向最佳 venue**，VLA/机器人学习专属 |

##### Tier 2 机器人旗舰会议（大规模）

| 会议 | 录用率 | 投稿量 | 周期 | 特点 |
|------|--------|--------|------|------|
| **ICRA** | ~39% | 4,000+ | 9月截稿→1月通知→5-6月开会 | 最广覆盖，IEEE RAS 旗舰，7000+参会 |
| **IROS** | ~43-48% | 2,000+ | 3月截稿→6月通知→10月开会 | 与 ICRA 互补，偏系统 |

##### AI/ML 顶会（接受机器人论文）

| 会议 | 录用率 | 投稿量 | 与你的相关性 | 关键要求 |
|------|--------|--------|-------------|---------|
| **ICLR** | ~32% | 11,500+ | **极高** — 2026 年收到 164 篇 VLA 论文 | ML 贡献必须强 |
| **NeurIPS** | ~24.5% | 21,500+ | 高 — embodied AI workshop 很强 | ML 理论深度 |
| **ICML** | ~27% | 12,000+ | 中 — RL/优化理论 | 理论贡献 |
| **CVPR** | ~22% | 13,000+ | 高 — 越来越多真机器人论文 | 视觉方法必须强 |
| **ECCV** | ~28% | 8,500+ | 中 — 视觉+操作 | 双年（偶数年） |
| **AAAI** | ~18% | 23,000+ | 中 — 规划/推理 | 越来越卷 |

##### 期刊

| 期刊 | 影响因子 | 审稿周期 | 最适合 |
|------|---------|---------|--------|
| **Science Robotics** | 19-26 | 3-6 月 | 突破性成果，广泛影响 |
| **T-RO** (IEEE Trans. Robotics) | 10-12 | ~6 月 | 深度技术贡献 |
| **IJRR** | 7.5-9 | 3-6+ 月 | 基础算法、理论、系统 |
| **RA-L** | 5-6 | **3 月首次决定** | 快速发表 + 可在 ICRA/IROS 报告 |

##### 关键 Workshop（战略性使用）

| Workshop | 所属会议 | 用途 |
|----------|---------|------|
| Embodied World Models for Decision Making | NeurIPS | 测试早期想法 |
| Foundation Models Meet Embodied Agents | CVPR | 提前获得领域反馈 |
| Safely Leveraging VL Foundation Models in Robotics | ICRA | 针对性反馈 |
| Robot Learning Workshop | ICLR | VLA 方向预投 |

> **Workshop 策略**：Workshop 论文通常是非存档的，不阻止后续投正式会议。用 workshop 获取反馈，改进后投正式会议。

---

#### 步骤 B：论文-Venue 匹配分析

**按贡献类型匹配**：

| 你的论文贡献类型 | 最佳 Venue | 次选 |
|----------------|-----------|------|
| 新 VLA 架构/方法 | ICLR, CoRL | NeurIPS |
| 新学习算法 + 理论 | NeurIPS, ICML | ICLR |
| 新算法 + 真机器人演示 | CoRL, RSS | ICRA |
| 视觉/感知方法用于机器人 | CVPR, CoRL | ECCV |
| 操作/抓取系统 | RSS, CoRL | ICRA, RA-L |
| 大规模系统论文 | ICRA, T-RO | IJRR |
| Benchmark / 数据集 | NeurIPS (Datasets), CoRL | ICRA |

**匹配决策矩阵**：

对每个候选 venue，回答以下问题并打分：

```
1. 主题匹配度（0-10）
   该 venue 近 2 年是否发表过你这个方向的论文？
   → 去 venue 官网搜关键词，数数录用论文数量

2. 方法论匹配度（0-10）
   该 venue 的审稿人期望什么类型的贡献？
   → 理论 vs 系统 vs 实验 vs 综合

3. 竞争强度（0-10，越低越好）
   该方向在这个 venue 的竞争有多激烈？
   → 如果 ICLR 收到 164 篇 VLA，你的需要足够突出

4. 审稿人友好度（0-10）
   你的故事线和写作风格是否适合这个社区？
   → ML 社区 vs 机器人社区的审美差异

5. 时间线可行性（0-10）
   从现在到截稿，时间够吗？
   → 留至少 2 周的 buffer
```

**总分 = 加权求和**，阈值 > 30 才考虑投稿。

---

#### 步骤 C：投稿时间规划

**2025-2026 关键截稿日历**：

| 截稿时间 | Venue | 通知时间 | 开会时间 |
|---------|-------|---------|---------|
| 2025.06 | CoRL 2025 | 2025.08 | 2025.11 |
| 2025.09 | ICRA 2026 / ICLR 2026 | 2026.01 | 2026.05-06 |
| 2025.10 | ICLR 2026 | 2026.01 | 2026.04-05 |
| 2026.01 | RSS 2026 | 2026.04 | 2026.07 (Sydney) |
| 2026.03 | IROS 2026 | 2026.06 | 2026.09 (Pittsburgh) |
| 随时 | RA-L | 投稿后 3 个月 | 可选 ICRA/IROS 报告 |

**反向排期（从截稿日倒推）**：

```
截稿日 - 8周：阶段 2 实验必须完成
截稿日 - 6周：阶段 3 步骤 A-B 完成（故事线+初稿）
截稿日 - 4周：阶段 3 步骤 C-D 完成（图表+引用）
截稿日 - 2周：阶段 3 步骤 E 完成（内审）
截稿日 - 1周：格式化 + 最终检查
截稿日 - 1天：最终通读，提交
```

**会议 vs 期刊决策**：

| 选会议当… | 选期刊当… |
|-----------|----------|
| 结果时效性强（VLA 领域变化极快） | 需要更大篇幅（>8页） |
| 需要社区曝光和社交 | 合并多个会议级贡献为一篇 |
| 快速建立发表记录 | 冲击 tenure/升职评审 |
| 想通过 talk/poster 获取反馈 | 工作深度足够发期刊 |

**混合策略（推荐）**：
1. 先投 RA-L（3 个月出结果）+ 选 ICRA/IROS 报告 → 同时拿期刊发表+会议报告
2. 精选版投 CoRL/RSS → 拿顶会声望
3. 扩展版投 T-RO/IJRR → 存档完整版本

---

#### 步骤 D：格式适配

**不同 venue 的格式和风格差异**：

| 维度 | ML 会议 (ICLR/NeurIPS) | 机器人会议 (CoRL/RSS) | 机器人旗舰 (ICRA/IROS) |
|------|----------------------|---------------------|---------------------|
| 审稿人关心什么 | ML 方法新颖性、理论支撑 | 方法+真机实验 | 系统完整性、工程贡献 |
| 实验期望 | SOTA 对比、大规模 ablation | 真机+仿真、泛化性测试 | 系统演示、实际可用性 |
| 写作风格 | 偏数学、定理证明 | 平衡理论和实践 | 偏工程描述 |
| 页数限制 | 通常 9-10 页 | 8 页 | 6-8 页 |
| 引用风格 | ML 社区论文 | 机器人+ML 交叉 | 机器人社区论文 |
| 补充材料 | 附录不限 | 通常有限制 | 视频演示加分 |

**适配检查清单**：
- [ ] 页数符合目标 venue 限制
- [ ] 引用了目标 venue 近 2 年的相关论文
- [ ] 实验设置符合该社区的期望标准
- [ ] 写作风格匹配（ML 偏理论 vs 机器人偏实践）
- [ ] 使用该 venue 的 LaTeX 模板
- [ ] 补充材料（视频、代码、数据）按要求准备

**质量门控**：
- 投稿前必须读该 venue 近 2 年至少 5 篇与你方向最相关的录用论文
- 对照它们的结构、深度、写作风格调整你的论文
- 引用中该 venue 近 2 年论文的比例 ≥ 15%

---

## 阶段 5：审稿修订

### 目标
系统性回应审稿意见，每条都有理有据。

### 流程

```
步骤 A ─→ 步骤 B ─→ 步骤 C ─→ 步骤 D
意见分类   逐条回应   修改论文   复审验证
```

#### 步骤 A：审稿意见分类

**工具**：academic-research-skills → Editor-in-Chief Agent

**分类矩阵**：

| 类型 | 处理方式 | 优先级 |
|------|---------|--------|
| 事实性错误 | 立即修正 | P0 |
| 缺少实验 | 补实验（回阶段 2） | P0 |
| 方法质疑 | 详细解释或补充证据 | P1 |
| 写作问题 | 改写 | P2 |
| 超出范围 | 礼貌说明 + 列为 future work | P3 |

---

#### 步骤 B：逐条回应

**工具**：academic-research-skills → 5 人审稿团（反向使用：站在作者角度回应）

**回应模板**：

```
## Reviewer 1, Comment 3

> [原文引用审稿人的意见]

**回应**：感谢审稿人的建议。[具体回应]

**修改**：我们在第 X 节做了以下修改：[具体描述改了什么]
         修改内容用蓝色标注在修订稿中。
```

**原则**：
- 每条意见都要回应，即使不同意也要解释原因
- 不同意时用数据/文献支撑，不能只说"我们认为"
- 补充实验的结果必须包含具体数字
- 态度要专业尊重，即使审稿人明显理解错了

---

#### 步骤 C：修改论文

**做什么**：
1. 根据步骤 B 的回应，修改论文对应段落
2. 所有修改用颜色标注（LaTeX: `\textcolor{blue}{新内容}`）
3. 如果需要补实验，回到阶段 2 的步骤 D
4. 更新引用（如果审稿人要求补引）

---

#### 步骤 D：复审验证

**工具**：academic-research-skills → Devil's Advocate Agent + Editor-in-Chief Agent

**做什么**：
1. Devil's Advocate 模拟审稿人再审：
   - 之前的问题是否真正解决了？
   - 修改是否引入了新问题？
   - 回应信是否有逻辑漏洞？
2. Editor-in-Chief 检查修订稿整体一致性
3. 确认所有修改都在回应信中提到了

**质量门控**：复审通过后才提交修订稿。

---

## 附录 A：各阶段文件结构

```
robo_retargeting/
├── research-workflow.md            # 本文件
│
├── community/                      # 阶段 0：社区情报
│   ├── weekly_signals.md           # 每周趋势信号
│   ├── direction_candidates.md     # 候选研究方向
│   └── sources_config.md           # 信息源配置记录
│
├── literature/                     # 阶段 1：文献调研
│   ├── search_queries.md           # 检索策略
│   ├── raw/                        # 原始检索结果
│   │   ├── semantic_scholar.csv
│   │   ├── arxiv.csv
│   │   └── research_lookup.md
│   ├── all_papers.csv              # 去重合并后
│   ├── citation_tracking.md        # 引用链追踪记录
│   ├── prisma_flowchart.md         # PRISMA 流程图
│   └── survey_report.md            # 综合分析报告
│
├── experiments/                    # 阶段 2：实验工程
│   ├── experiment_design.md        # 实验设计
│   ├── configs/                    # 超参数配置
│   ├── data/                       # 数据处理
│   ├── models/                     # 模型定义
│   ├── scripts/                    # 训练/评估脚本
│   ├── results/                    # 实验结果
│   │   ├── main_results.csv
│   │   ├── ablation_results.csv
│   │   ├── statistical_tests.md
│   │   ├── failure_analysis.md
│   │   └── figures/
│   ├── Dockerfile                  # 环境复现
│   └── REPRODUCE.md                # 复现指南
│
├── paper/                          # 阶段 3：论文写作
│   ├── main.tex                    # 论文主文件
│   ├── sections/                   # 各章节
│   ├── figures/                    # 图表（PDF 矢量）
│   ├── tables/                     # 表格
│   ├── references.bib              # BibTeX
│   └── supplementary/              # 补充材料
│
├── venue/                          # 阶段 4：投稿策略
│   ├── venue_analysis.md           # Venue 匹配分析
│   ├── scoring_matrix.md           # 打分矩阵
│   ├── timeline.md                 # 投稿时间规划
│   └── format_checklist.md         # 格式适配清单
│
└── review/                         # 阶段 5：审稿修订
    ├── reviewer_comments.md        # 原始审稿意见
    ├── response_letter.md          # 逐条回应
    ├── revision_diff.tex           # 修改标注版
    └── rebuttal_checklist.md       # 复审清单
```

---

## 附录 B：质量门控清单

每个阶段结束前必须通过的检查：

### 阶段 0 完成标准
- [ ] 信息源已配置（X 关注列表 + Reddit 订阅 + Newsletter）
- [ ] 至少扫描 2 周的社区动态
- [ ] 候选方向有 ≥ 2 个平台的交叉信号支撑
- [ ] 候选方向已记录在 direction_candidates.md

### 阶段 1 完成标准
- [ ] PRISMA 流程图完整，每步数字可追溯
- [ ] 引用链追踪覆盖 top 20 高被引论文
- [ ] Devil's Advocate 审查通过
- [ ] 明确识别出至少 1 个研究 Gap
- [ ] 综合报告覆盖所有主要方法流派

### 阶段 2 完成标准
- [ ] 所有实验至少 3 次重复
- [ ] 所有对比有统计检验 (p < 0.05)
- [ ] 消融实验覆盖每个核心模块
- [ ] 有失败案例分析
- [ ] REPRODUCE.md 验证通过

### 阶段 3 完成标准
- [ ] 故事线通过电梯测试
- [ ] 所有 claim 有实验/引用支撑
- [ ] 图表独立可读（caption 完整）
- [ ] 引用格式一致且完整
- [ ] Devil's Advocate 所有质疑已回应
- [ ] 页数/格式符合目标 venue 要求

### 阶段 4 完成标准
- [ ] Venue 打分矩阵总分 > 30
- [ ] 反向排期时间可行（截稿前 ≥ 2 周 buffer）
- [ ] 读过目标 venue 近 2 年 ≥ 5 篇相关录用论文
- [ ] 引用中目标 venue 论文占比 ≥ 15%
- [ ] LaTeX 模板和格式已适配
- [ ] 补充材料（视频/代码/数据）已准备

### 阶段 5 完成标准
- [ ] 每条审稿意见都有回应
- [ ] 所有修改在回应信中标注
- [ ] 修订稿修改处用颜色标注
- [ ] 复审模拟通过
- [ ] 无新引入的一致性问题

---

## 附录 C：持续监控系统

贯穿所有阶段的后台任务，不属于任何单一阶段。

### 日常（5-10 分钟）
- [ ] @_akhaliq + @arankomatsuzaki 推文扫描
- [ ] HuggingFace Trending Papers
- [ ] arXiv RSS (cs.RO, cs.LG)

### 每周（30 分钟）
- [ ] Newsletter 阅读（AlphaSignal + Import AI）
- [ ] Reddit r/MachineLearning top posts
- [ ] GitHub Trending 机器人/AI 项目
- [ ] 更新 `community/weekly_signals.md`

### 每月
- [ ] Semantic Scholar Research Feeds 校准
- [ ] Google Scholar Alerts 结果审查
- [ ] 检查目标 venue 的新 CFP（Call for Papers）
- [ ] 检查竞争对手实验室的新发表

### 会议季（截稿前 2 个月）
- [ ] 目标 venue 的往年 Best Paper 分析
- [ ] OpenReview / CMT 上的往年审稿意见模式分析
- [ ] 调整论文的写作风格和重点以匹配 venue
