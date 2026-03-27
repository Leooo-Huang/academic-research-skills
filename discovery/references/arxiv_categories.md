# arXiv Category Codes — AI, Robotics, and Related Fields

Use these codes to refine WebSearch queries in Phase 1. Append as additional search terms to improve precision.

Example: `site:arxiv.org "robotic grasping" cs.RO 2025`

---

## Core Categories for AI + Robotics Research

| Code | Full Name | Use When |
|------|-----------|---------|
| **cs.RO** | Robotics | Robot motion, manipulation, navigation, HRI, embodied AI |
| **cs.AI** | Artificial Intelligence | General AI, planning, knowledge representation, reasoning |
| **cs.LG** | Machine Learning | Deep learning, RL, generalization, optimization, theory |
| **cs.CV** | Computer Vision | Image/video understanding, 3D perception, object detection |
| **cs.CL** | Computation and Language | NLP, LLMs, language grounding, VLMs |
| **cs.MA** | Multiagent Systems | Multi-robot coordination, swarm robotics, MARL |
| **cs.NE** | Neural and Evolutionary Computing | Neural architectures, evolutionary methods |
| **cs.SY** | Systems and Control | Control theory, optimal control, model predictive control |
| **eess.SY** | Systems and Control (EE) | Signal processing, control systems (EESS mirror) |

---

## Extended Categories

| Code | Full Name | Use When |
|------|-----------|---------|
| **cs.HC** | Human-Computer Interaction | HRI, user studies, interface design |
| **cs.GR** | Graphics | Simulation, rendering, synthetic data |
| **cs.MM** | Multimedia | Audio-visual learning, multimodal |
| **stat.ML** | Machine Learning (Statistics) | Probabilistic ML, Bayesian methods |
| **math.OC** | Optimization and Control | Trajectory optimization, convex optimization |
| **eess.SP** | Signal Processing | Sensor fusion, tactile sensing |

---

## Topic → Category Mapping (AI/Robotics)

| Research Topic | Primary Category | Secondary |
|---------------|-----------------|-----------|
| Robot manipulation / grasping | cs.RO | cs.CV, cs.LG |
| Legged locomotion | cs.RO | cs.SY, cs.LG |
| Navigation / SLAM | cs.RO | cs.CV |
| Sim-to-real transfer | cs.RO | cs.LG |
| Imitation learning / LfD | cs.LG | cs.RO |
| Reinforcement learning for robots | cs.LG | cs.RO |
| Vision-language models | cs.CV | cs.CL, cs.LG |
| Large language models for robotics | cs.CL | cs.RO, cs.AI |
| Diffusion models (policy/generation) | cs.LG | cs.CV, cs.RO |
| Foundation models | cs.LG | cs.AI, cs.CL |
| Multi-robot systems | cs.MA | cs.RO |
| Human-robot interaction | cs.RO | cs.HC |
| Transformer architectures | cs.LG | cs.CV, cs.CL |
| 3D perception / point clouds | cs.CV | cs.RO |
| Tactile sensing | cs.RO | eess.SP |
| Safe / constrained RL | cs.LG | cs.SY |
| Model predictive control | cs.SY | cs.RO |

---

## Top Venues by Topic

Use venue names as additional search terms in Q3 queries.

### Robotics Conferences
- **ICRA** — IEEE International Conference on Robotics and Automation
- **IROS** — IEEE/RSJ International Conference on Intelligent Robots and Systems
- **CoRL** — Conference on Robot Learning
- **RSS** — Robotics: Science and Systems
- **HRI** — ACM/IEEE International Conference on Human-Robot Interaction

### Robotics Journals
- **RA-L** — IEEE Robotics and Automation Letters
- **T-RO** — IEEE Transactions on Robotics
- **IJRR** — International Journal of Robotics Research
- **Science Robotics**

### AI / ML Conferences
- **NeurIPS** — Neural Information Processing Systems
- **ICML** — International Conference on Machine Learning
- **ICLR** — International Conference on Learning Representations
- **CVPR** — Computer Vision and Pattern Recognition
- **ICCV** — International Conference on Computer Vision
- **ECCV** — European Conference on Computer Vision
- **AAAI** — Association for the Advancement of Artificial Intelligence

### LLM / Foundation Model
- **ACL** — Association for Computational Linguistics
- **EMNLP** — Empirical Methods in Natural Language Processing
- **NAACL** — North American Chapter of the ACL

---

## arXiv Search URL Patterns

Direct arXiv search (use in Q1 fallback):
```
https://arxiv.org/search/?query={keywords}&searchtype=all&start=0
```

Category-filtered search:
```
https://arxiv.org/search/?query={keywords}&searchtype=all&category={cs.RO}
```

Recent papers in category (last 30 days):
```
https://arxiv.org/list/{cs.RO}/recent
```

These URLs can be fetched via WebFetch for more structured results than WebSearch when needed.
