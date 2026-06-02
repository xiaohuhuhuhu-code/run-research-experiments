# Run Research Experiments Skill

这是一个通用的深度学习论文实验 skill，用于让 AI agent 从公开数据集、模型基线、机制递进式创新点、实验记录，一直推进到中文论文初稿和英文论文初稿。

## 适用场景

- 需要至少 2 个公开数据集的论文实验。
- 需要自动查找数据集下载方式、预处理数据、转换标签和划分数据集。
- 需要在数据集预处理时生成格式化审计日志，记录解压、划分、标签转换、空标签和删除样本。
- 需要查找并复现基线模型，自动下载公开权重。
- 需要设计 3 个有依据、有逻辑、非简单堆叠的创新点。
- 需要记录实验结果、消融分析、效率对比和失败创新点。
- 需要先写中文初稿，再基于中文稿写英文初稿，并统一专业术语。

## 核心规则

- 数据集、模型代码、实验结果、论文稿必须分目录存放。
- 创新点必须针对明确问题，且有证据、假设、机制解释和实验验证。
- A/B/C 不能是独立模块堆叠或排列组合，必须是递进式内部机制改进。
- 所有模型实验的 `epochs` 和 `batch size` 必须一致。
- `num_workers` 可以尽量调大，但不能超过本机 CPU、内存和磁盘吞吐能力。
- 训练不能超过本机专用显存，不能依赖共享显存、CPU offload、disk offload 或 swap。
- 数据集预处理不能静默修正或删除数据，所有异常标签、空标签、删除样本和保留样本都必须记录。
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
experiments/
  logs/
  results/
  checkpoints/
  figures/
  reports/
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
使用 $run-research-experiments，帮我完成一个深度学习论文实验。要求至少找两个公开数据集，完成下载、预处理、基线复现、三个递进式创新点实验，并最后写中文初稿和英文初稿。
```

也可以根据具体研究方向补充任务：

```text
使用 $run-research-experiments，研究方向是无人机小目标检测。我的显卡是 RTX 4090 24GB，不能使用共享显存，所有模型实验 epoch 和 batch size 必须一致。
```

## 文件说明

- `SKILL.md`: skill 主体规则和完整执行流程。
- `agents/openai.yaml`: Codex UI 识别用的展示元数据。
