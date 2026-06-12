# Run Research Experiments Skill

这是一个通用的深度学习论文实验 skill，用于让 AI agent 从公开数据集、模型基线、`M0 -> M1 -> M2 -> M3` 机制版本创新、实验记录，一直推进到中文论文初稿和英文论文初稿。

## 适用场景

- 需要至少 2 个公开数据集的论文实验。
- 需要自动查找数据集下载方式、预处理数据、转换标签和划分数据集。
- 需要在数据集预处理时生成格式化审计日志，记录解压、划分、标签转换、空标签和删除样本。
- 需要查找并复现基线模型，自动下载公开权重。
- 需要先分析改进方向，再设计创新点，避免随意修改模型。
- 需要设计 3 个有依据、有逻辑的有效创新版本：`M0` 为基线，`M1/M2/M3` 为经过筛选和验证的机制改进版本。
- 需要记录实验结果、消融分析、效率对比和失败创新点。
- 需要生成可复现实验结果图，包括训练/验证曲线、消融、效率、类别级、错误分析、数据集统计和定性结果。
- 需要所有 AI 工作都有计划、执行记录和恢复 checkpoint，防止中断后无法继续。
- 需要机器可读的项目状态和实验登记表，让换终端或换 AI 后可以继续。
- 需要在写结果和论文前检查 epoch、batch size、数据划分、输入尺寸和评估脚本是否一致。
- 需要每个论文主张都能追溯到实验结果、图表、日志、配置或引用。
- 需要每个实验项目新建独立 conda 环境，避免污染 `base` 或其它项目环境。
- 需要先写中文初稿，再基于中文稿写英文初稿，并统一专业术语。

## 核心规则

- 数据集、模型代码、实验结果、论文稿必须分目录存放。
- 创新点必须针对明确问题，且有证据、假设、机制解释和实验验证。
- 做创新前必须分析和排序改进方向，用基线错误、数据集统计、文献缺口和硬件约束决定优先尝试什么。
- 不再把创新点理解成简单的 A/B/C 叠加。`M0` 是复现基线，`M1/M2/M3` 是逐步接受的机制版本，每一步都要说明是新增、替换、细化、删除还是重新参数化了哪个内部组件。
- 纸面上的 A/B/C 只能作为简称使用，必须映射到具体的 `M1/M2/M3` 机制变化。
- 如果一个方向没有效果，AI 应该扩展候选池，尝试不同组件或阶段的改进，例如 backbone、neck、head、loss、augmentation、post-processing 或部署路径。
- 所有模型实验的 `epochs` 和 `batch size` 必须一致。
- `num_workers` 可以尽量调大，但不能超过本机 CPU、内存和磁盘吞吐能力。
- 训练不能超过本机专用显存，不能依赖共享显存、CPU offload、disk offload 或 swap。
- 数据集预处理不能静默修正或删除数据，所有异常标签、空标签、删除样本和保留样本都必须记录。
- 所有工作必须有计划、进度日志和恢复状态，换终端或中断后要能继续。
- 同时维护 `project_state.json` 和 `experiment_registry.yaml`，让 AI 和脚本能自动读取当前项目状态。
- 搜索、下载、调试和修复必须有尝试次数上限，找不到时要记录阻塞和替代方案，不能死循环。
- 每个项目必须新建专属 conda 环境，不能使用 `base`，不能复用其它项目环境。
- conda 环境本体不放入项目，只保存 `environment.yml`、显式导出文件和环境报告。
- 实验结果图必须保存原始数据、绘图脚本、PDF/SVG 矢量图和 PNG 图，不能只靠颜色区分方法。
- 写论文前必须生成实验一致性检查报告，发现不可比实验时要先修正或说明。
- 论文核心主张必须写入 `claim_evidence_matrix.md`，并映射到对应证据。
- 所有论文结果必须能追溯到日志、配置、检查点或结果文件。

## 推荐工作区结构

```text
datasets/
  raw/<dataset_name>/
  processed/<dataset_name>/
  manifests/
  scripts/
model_code/
  baselines/<baseline_name>/
  proposed/
  configs/
  scripts/
  weights/
  environment/
experiments/
  logs/
  results/
  checkpoints/
  figures/
  figure_scripts/
  reports/
  state/
paper/
  zh/
  en/
  shared/
```

## 预处理审计日志

预处理阶段必须在 `datasets/manifests/` 和 `experiments/reports/` 下生成可追溯记录：

```text
datasets/manifests/<dataset_name>_archive_manifest.csv
datasets/manifests/<dataset_name>_preprocess_log.jsonl
datasets/manifests/<dataset_name>_label_audit.csv
datasets/manifests/<dataset_name>_split_manifest.csv
experiments/reports/preprocess_report.md
```

必须记录的情况包括：

- 数据集是单个压缩包或嵌套压缩包时的解压路径、文件数量、失败文件和校验信息。
- 没有官方划分时，生成 train/val/test 的比例、随机种子和每个样本的 split。
- 标签缺失、空标签、类别错误、标注行格式错误、越界框、无效框、图片和标签不匹配。
- 预处理时自动删除、保留或修正的任何样本和标签，以及对应原因。
- 最终保留样本数、删除样本数、空标签样本数、修正标签数和未解决警告。

## 计划、恢复与防死循环

每次执行实验流水线时，都要维护以下文件：

```text
experiments/state/work_plan.md
experiments/state/resume_state.md
experiments/state/project_state.json
experiments/state/experiment_registry.yaml
experiments/logs/work_journal.jsonl
experiments/logs/search_attempts.jsonl
experiments/reports/blockers.md
```

用途如下：

- `work_plan.md`: 当前目标、阶段、任务状态、假设、约束、预计产物和下一步动作。
- `resume_state.md`: 中断或换终端后恢复用的 checkpoint，包括已完成内容、活动文件、最近成功命令、阻塞点和下一步。
- `project_state.json`: 机器可读的项目阶段、当前任务、数据集、基线、已接受版本、失败候选、硬件预算和下一步动作。
- `experiment_registry.yaml`: 机器可读的实验登记表，记录每个 screening/full run 的配置、状态、指标、产物和接受/拒绝决策。
- `work_journal.jsonl`: 每次下载、预处理、训练、评估、写作或文件修改的结构化执行记录。
- `search_attempts.jsonl`: 数据集、模型、论文、下载链接、错误修复等搜索和尝试记录。
- `blockers.md`: 超过尝试预算后仍无法解决的问题、已尝试方法、需要用户介入的动作和替代方案。

默认防死循环预算：

- 每个缺失数据集、模型或论文最多 5 次聚焦搜索。
- 每个下载源最多 3 次下载尝试。
- 同一个预处理错误最多 3 次修复尝试。
- 同一个训练或评估错误最多 3 次修复尝试。

预算耗尽后必须停止该循环，写入 `blockers.md`，并给出可行替代方案。

## 改进方向分析

在设计 `M1/M2/M3` 创新版本之前，必须先生成：

```text
experiments/reports/improvement_direction_analysis.md
experiments/reports/candidate_screening.md
```

改进方向分析要比较不同方向，例如：

- 数据增强或数据策略。
- backbone/representation。
- neck 或特征融合。
- head。
- loss 或 label assignment。
- temporal modeling、tracking 或 post-processing。
- 轻量化部署或推理优化。
- domain adaptation 或鲁棒性。

每个方向都要记录：

```text
direction | targeted problem | evidence | expected gain | novelty | implementation cost | hardware cost | risk | story fit | priority
```

原则是先试证据强、成本合理、最可能带来收益的方向。低证据方向即使看起来流行，也要先拒绝或延后。如果一个方向连续失败，AI 要更新分析并主动扩展候选池，避免在同一个方向反复微调。

快速筛选规则：

- 候选池尽量覆盖至少两个改进方向，例如 representation、fusion、loss/assignment、augmentation、post-processing 或轻量化部署。
- 每个方向默认最多筛选 3 个候选；同一候选最多修订 2 次。
- screening 阶段使用相同短 epoch、相同 batch size、相同数据子集或验证集、相同 seed policy 和相同评估脚本。
- 只有通过 screening 的候选才能进入完整 `M1/M2/M3` 实验。
- 失败候选不能删除，要写入 `candidate_screening.md` 和 `experiment_registry.yaml`。

## 实验结果作图要求

这里主要约束实验结果图，不强制规定方法结构图、模块结构图或概念示意图。

必须覆盖的实验结果图包括：

- 训练/验证曲线：`train loss`、`val loss`、mAP、Precision、Recall、Accuracy、F1 等。
- 消融实验图：`M0` Baseline、`M1`、`M2`、`M3` final method。
- 效率对比图：Params、FLOPs、FPS、Latency、显存，或 mAP vs Params/FPS/Latency。
- 类别级性能图：per-class AP、F1、Accuracy、Recall 等。
- 错误分析图：混淆矩阵，或漏检、误检、定位错误、小目标错误、遮挡错误等。
- 数据集统计图：类别分布、train/val/test 数量、目标尺寸分布、空标签统计等。
- 定性结果图：GT、Baseline、Final method 对比，成功案例和失败案例都要有。

验证曲线规则：

```text
x-axis: epoch
y-axis: loss or metric
curves: M0 baseline, M1, M2, M3 final method
source: training log / validation log / results.csv / TensorBoard / results.jsonl
style: color + linestyle + marker
preview PNG: dpi=300
final PNG: dpi=600
vector: PDF or SVG
```

统一样式要求：

- 折线图不能只靠颜色区分，必须使用不同颜色、线型和 marker。
- 柱状图不能只靠颜色区分，必要时使用 hatch 或不同边框样式。
- 折线线宽 `2.0-2.5 pt`，主曲线建议 `2.5 pt`。
- 坐标轴线宽 `1.2-1.5 pt`。
- 网格线宽 `0.6-0.8 pt`，透明度 `0.25-0.35`。
- marker 大小 `5-7 pt`。
- 柱状图边框线宽 `1.0-1.2 pt`。
- 字体大小建议：坐标轴标签 `11-12 pt`，刻度 `9-10 pt`，图例 `9-10 pt`。
- 图例不能遮挡主体，必要时放在图外；黑白打印时仍应能区分不同方法。
- epoch 很多时 marker 使用 `markevery=5` 或 `markevery=10`。

保存要求：

```text
experiments/results/curves/
experiments/results/tables/
experiments/figure_scripts/
experiments/figures/<plot_type>/
```

所有结果图必须能从原始日志、CSV、JSONL 或 TensorBoard 数据重新生成。

## 可复用模板和脚本

这个 skill 除了 `SKILL.md`，还包含项目启动模板和一致性检查脚本：

```text
templates/project_state.json
templates/experiment_registry.yaml
templates/claim_evidence_matrix.md
templates/consistency_report.md
scripts/check_experiment_consistency.py
```

启动新项目时建议复制：

```text
templates/project_state.json -> experiments/state/project_state.json
templates/experiment_registry.yaml -> experiments/state/experiment_registry.yaml
templates/claim_evidence_matrix.md -> paper/shared/claim_evidence_matrix.md
```

写最终结果表或论文前运行：

```powershell
python scripts/check_experiment_consistency.py --registry experiments/state/experiment_registry.yaml --results experiments/results/results.jsonl --output experiments/reports/consistency_report.md
```

如果报告为 `FAIL`，说明至少存在一个不可直接比较的实验配置，必须修正或明确说明后才能写入论文。

## Conda 环境隔离

每个新实验项目都必须先创建独立 conda 环境，再安装依赖、下载模型代码、预处理数据或启动训练。

推荐记录文件：

```text
model_code/environment/environment.yml
model_code/environment/conda_explicit.txt
experiments/reports/environment_report.md
```

必须记录的内容包括：

- conda 环境名，例如 `rre_<project_slug>` 或 `rre_<project_slug>_<date>`。
- 环境创建命令和激活命令。
- Python、CUDA、cuDNN、PyTorch 或其它框架版本。
- 依赖安装命令、依赖冲突和解决方式。
- 所有训练、评估、预处理和论文生成命令都应在该环境内执行。

禁止事项：

- 不能使用 `base` 环境做项目实验。
- 不能复用其它项目的 conda 环境。
- 不能把真实 conda 环境目录提交到项目或 GitHub。

## 安装到 Codex

```powershell
git clone https://github.com/xiaohuhuhuhu-code/run-research-experiments.git "$env:USERPROFILE\.codex\skills\run-research-experiments"
```

## 安装到 Claude Code

```powershell
git clone https://github.com/xiaohuhuhuhu-code/run-research-experiments.git "$env:USERPROFILE\.claude\skills\run-research-experiments"
```

如果对应目录已经存在，可以先删除旧目录，或者进入目录后执行：

```powershell
git pull
```

## 使用方式

在 Codex 或 Claude Code 中显式触发：

```text
使用 $run-research-experiments，帮我完成一个深度学习论文实验。要求至少找两个公开数据集，完成下载、预处理、基线复现，先分析改进方向并做快速筛选，再形成 M0/M1/M2/M3 机制版本实验，所有创新都要有依据、能提升、能讲成一个故事，并最后写中文初稿和英文初稿。
```

也可以根据具体研究方向补充任务：

```text
使用 $run-research-experiments，研究方向是无人机小目标检测。我的显卡是 RTX 4090 24GB，不能使用共享显存，所有模型实验 epoch 和 batch size 必须一致，并且每个项目必须新建独立 conda 环境。
```

## 文件说明

- `SKILL.md`: skill 主体规则和完整执行流程。
- `agents/openai.yaml`: Codex UI 识别用的展示元数据。
- `templates/`: 新项目可复制的状态、实验登记、一致性报告和论文证据矩阵模板。
- `scripts/check_experiment_consistency.py`: 检查实验配置一致性的无依赖 Python 脚本。
