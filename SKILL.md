---
name: run-research-experiments
description: Use when an AI coding/research agent needs to run an end-to-end deep learning paper experiment involving public dataset discovery/download, dataset preprocessing, structured preprocessing audit logs, resumable work plans, anti-loop safeguards, per-project conda isolation, label conversion, train/val/test splits, baseline model selection, pretrained weight download, improvement direction analysis, model innovation, ablation experiments, failed-improvement iteration, experiment logging, Chinese manuscript drafting, English manuscript drafting, terminology consistency, grammar polishing, and reproducible research artifacts.
---

# Run Research Experiments

## Overview

Use this skill to drive a complete research workflow from datasets to manuscript. The core rule is evidence first: every dataset, baseline, innovation, metric, and paper claim must be traceable to a source file, command, log, or measured result.

Default to a general deep learning workflow. If the task is computer vision, detection, tracking, segmentation, action recognition, or UAV/drone research, specialize the dataset search, metrics, and baselines for that task.

## Operating Rules

- Use at least two public datasets unless the user explicitly narrows the task.
- Search the web for current official dataset pages, papers, download links, licenses, and citation requirements. Do not invent download URLs.
- Download datasets and pretrained models automatically when public access permits it. If access requires login, form approval, manual license acceptance, or a private token, stop and give the user the exact action needed.
- Keep failed ideas in the experiment log under `experiments/`. Only promote effective innovations into the final method and paper narrative.
- Never write paper results before the corresponding experiments exist. Do not fabricate tables, curves, ablations, or comparisons.
- Every innovation must have a documented rationale: the baseline/dataset problem it targets, the evidence showing that problem exists, the hypothesis for improvement, and the experiment that verifies it.
- Innovations `A`, `B`, and `C` must form a coherent research story. They can be progressive internal refinements, complementary modules, or a mix of both, but they must answer the same research problem rather than become unrelated tricks.
- Module-based innovation is allowed. Modules may improve different parts of the system, such as backbone, neck, head, loss, assignment, augmentation, post-processing, or deployment path, but each module must have evidence, a clear interface, an expected effect, and measured validation.
- Do not force all innovations into one direction if evidence shows diminishing returns. If one path stalls, broaden the candidate pool across different model components or training/inference stages.
- Before implementing innovations, analyze and rank improvement directions from evidence. Do not change the model randomly; target the most likely failure sources first to find effective innovations faster.
- Treat local hardware as a hard constraint. Before training, detect or confirm GPU model, dedicated VRAM, CPU, RAM, and disk space. Do not exceed dedicated GPU memory, and do not rely on shared GPU memory, CPU offload, disk offload, or swap to make an experiment fit.
- Keep `epochs` and `batch size` identical for all model experiments, including baseline, intermediate improved methods, final method, and external comparison baselines. If one method cannot fit the planned batch size, lower the common batch size for all methods.
- Dataset preprocessing must produce structured audit logs. Archive extraction, generated splits, label conversion, invalid labels, empty labels, file deletion, file retention, and sample filtering must be recorded; never silently fix or drop data.
- Every substantial task must have a written plan, progress log, and resume checkpoint so another terminal or agent can continue without starting over.
- Use explicit search/retry budgets to prevent dead loops. If a dataset, model, paper, download, or bug fix cannot be found or solved within the budget, stop, log the blocker, and present alternatives.
- Every project must use a newly created, project-specific conda environment. Do not install dependencies into `base`, do not reuse another project's environment, and do not mix package state across projects.
- Prefer reproducible scripts, configs, manifests, and JSONL/CSV logs over manual notes.
- Use fixed seeds, versioned dependencies, and consistent evaluation settings across baseline and improved models.

## Workspace Layout

Create or reuse this structure when the repo has no stronger convention. Keep the four artifact groups separate: datasets, model code, experiment outputs, and paper drafts.

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
  reports/
  state/
paper/
  zh/
  en/
  shared/
```

Do not mix these categories. Dataset archives and processed labels stay under `datasets/`; source code, configs, and weights stay under `model_code/`; metrics, logs, checkpoints, plots, and ablation outputs stay under `experiments/`; manuscript files stay under `paper/`.

Maintain these records:

- `experiments/reports/dataset_sources.md`: dataset name, task, official page, paper, license, download URL, access date, citation.
- `experiments/reports/preprocess_report.md`: split policy, label mapping, ignored labels, image/video counts, class counts, integrity checks.
- `experiments/state/work_plan.md`: phase plan, task status, assumptions, decisions, and next actions.
- `experiments/state/resume_state.md`: latest checkpoint for restarting after interruption or switching terminals.
- `experiments/logs/work_journal.jsonl`: structured log of actions, commands, artifacts, results, and next steps.
- `experiments/logs/search_attempts.jsonl`: structured log of searches, download attempts, failures, and fallback decisions.
- `experiments/reports/blockers.md`: unresolved blockers, exhausted retry budgets, user actions needed, and safe alternatives.
- `model_code/environment/environment.yml`: reproducible conda environment specification.
- `model_code/environment/conda_explicit.txt`: explicit package export when available for exact environment reconstruction.
- `experiments/reports/environment_report.md`: conda environment name, creation commands, Python/CUDA/PyTorch versions, installed packages, and activation instructions.
- `datasets/manifests/<dataset_name>_archive_manifest.csv`: archive path, extraction target, extracted files, checksum if available, and extraction errors.
- `datasets/manifests/<dataset_name>_preprocess_log.jsonl`: structured event log for extraction, split generation, label conversion, filtering, deletion, and retention.
- `datasets/manifests/<dataset_name>_label_audit.csv`: invalid labels, empty labels, corrected labels, dropped labels, and reasons.
- `datasets/manifests/<dataset_name>_split_manifest.csv`: sample id/path, split, split source, seed, and reason.
- `experiments/reports/experiment_matrix.md`: baseline, improved method after A, improved method after A then B, final improved method after A then B then C, comparison methods, datasets, metrics, seeds, status.
- `experiments/results/results.jsonl`: one line per run with command, config, git SHA, seed, hardware, metrics, checkpoint, log path.
- `experiments/reports/improvement_direction_analysis.md`: baseline weaknesses, evidence, candidate directions, scores, priorities, and selected improvement path.
- `experiments/reports/candidate_screening.md`: lightweight screening plan and results for candidate modules/mechanisms before full experiments.
- `experiments/reports/innovation_audit.md`: accepted and rejected innovations with evidence.
- `experiments/reports/innovation_story.md`: problem evidence, A/B/C rationale, logical relationship, and paper narrative.
- `experiments/reports/hardware_budget.md`: GPU/VRAM, CPU/RAM, disk, allowed batch/image/model settings, and memory safety margin.
- `paper/shared/terminology.md`: Chinese term, English term, abbreviation, first-use rule.
- `paper/zh/`: Chinese outline, manuscript draft, tables, figure captions, and revision notes.
- `paper/en/`: English outline, manuscript draft, tables, figure captions, and revision notes.

## Planning, Resume, And Loop Guards

Before substantial work, create or update `experiments/state/work_plan.md`.

The plan must include:

- Objective and current phase.
- Assumptions and constraints.
- Task list with statuses: `pending`, `in_progress`, `done`, `blocked`, or `rejected`.
- Expected artifacts and their paths.
- Current search/retry budgets.
- Next concrete action.

During work, append to `experiments/logs/work_journal.jsonl` after each meaningful action, command, file change, download, preprocessing step, training run, evaluation, or writing pass. Each entry should include:

```text
timestamp | phase | action | command_or_source | input | output | artifact_paths | status | next_step
```

Update `experiments/state/resume_state.md` after each phase, before any long-running download/training/evaluation, after any failure, and before ending a session. It must contain the current goal, completed work, active files, last successful command, running or pending commands, blockers, and the exact next action.

When resuming after an interruption or switching terminals:

1. Read `experiments/state/resume_state.md`, `experiments/state/work_plan.md`, `experiments/logs/work_journal.jsonl`, `experiments/results/results.jsonl`, and relevant reports before acting.
2. Continue from the next incomplete task instead of repeating completed downloads, preprocessing, training, or writing.
3. Verify existing artifacts before reusing them. If an artifact is missing or corrupt, log the reason before regenerating it.

Anti-loop rules:

- Set a budget before open-ended search or debugging. Default: at most 5 focused search queries/pages per missing dataset/model/paper, 3 download attempts per source, 3 retries for the same preprocessing error, and 3 retries for the same training/evaluation failure.
- Log every attempt in `experiments/logs/search_attempts.jsonl` or `experiments/logs/work_journal.jsonl`.
- If the budget is exhausted, stop that loop, write the issue to `experiments/reports/blockers.md`, summarize what was tried, and propose safe alternatives such as another dataset, another baseline, a smaller model, a different mirror, or a request for user-provided access.
- Do not keep changing keywords, mirrors, parameters, or code indefinitely without a new hypothesis.
- Prefer a documented blocker over unbounded searching that wastes time and compute.

## Conda Environment Isolation

Before installing dependencies, downloading model code that installs packages, preprocessing data, or running experiments, create a new conda environment for the project.

Rules:

- Use a project-specific name such as `rre_<project_slug>` or `rre_<project_slug>_<date>`.
- Do not use `base` for project work.
- Do not reuse another project's conda environment.
- Do not install packages globally or into an unrelated shared environment.
- Keep all training, evaluation, preprocessing, and paper-generation commands inside the project environment.
- If a baseline repository recommends its own environment, merge the needed dependencies into the project environment unless isolation is impossible. If separate environments are unavoidable, document why and keep experiment comparisons reproducible.

Record:

- Environment creation command.
- Python version.
- CUDA/cuDNN/PyTorch or framework versions.
- Package installation commands.
- Any dependency conflicts and how they were resolved.
- Activation command and expected environment name.

Export:

```text
model_code/environment/environment.yml
model_code/environment/conda_explicit.txt
experiments/reports/environment_report.md
```

Do not commit or copy the actual conda environment directory into the project. Store only the environment specifications and reports.

## Phase 1: Dataset Discovery

For each candidate public dataset:

1. Verify relevance to the target task, scene, sensor, label type, and evaluation protocol.
2. Prefer official project pages, benchmark pages, paper repositories, institutional mirrors, Kaggle/Hugging Face pages with clear provenance, or publisher-linked repositories.
3. Record license, citation, download size, annotation format, class definitions, train/val/test protocol, and any usage restrictions.
4. Select at least two datasets with complementary value, such as main benchmark plus cross-domain validation, or easy/standard dataset plus difficult/small-object/low-light/occlusion dataset.
5. If no suitable public dataset is fully downloadable, present the nearest valid alternatives and explain the access blocker.

Before preprocessing, create a dataset decision note explaining why the selected datasets are suitable and how they support the paper's experimental claims.

## Phase 2: Download And Preprocess

Download raw data into `datasets/raw/` and never modify it in place. Preprocess into `datasets/processed/`.

Before preprocessing, create formatted logs under `datasets/manifests/`. Prefer JSONL for event logs and CSV for tabular manifests. Each preprocessing event log entry should include:

```text
timestamp | dataset | stage | source_path | target_path | sample_id | split | action | reason | before | after | status
```

For every dataset:

- If the dataset is one archive or has nested archives, log extraction paths, extracted file counts, failed files, and checksums when available.
- Verify archive checksums or at least file counts after extraction.
- Convert labels to the training framework format, keeping a source-to-target class map.
- Validate every label file and record missing labels, empty labels, invalid class ids, malformed rows, invalid boxes/masks/keypoints, out-of-bounds coordinates, duplicate annotations, unreadable images, and image-label mismatches.
- Never silently delete samples or labels. If preprocessing drops a file, drops a label, keeps an empty-label sample, or removes an empty-label sample because the framework cannot use it, write a log entry with the exact reason.
- Preserve ignored/difficult/crowd labels according to the benchmark protocol.
- Split data into train/val/test using the official split when available. If no official split exists, create a deterministic split with a fixed seed and document the ratio.
- For datasets with no direct split, write `datasets/manifests/<dataset_name>_split_manifest.csv` so every sample's generated split can be audited and reproduced.
- Check for leakage, especially duplicate frames, near-duplicate videos, shared sequences, or same-scene images across train/test.
- Produce a small visual sanity check: sample images with labels overlaid, class distribution, object-size distribution when relevant.
- Write dataset config files used by training, such as YAML/JSON paths and class names.
- Summarize preprocessing actions in `experiments/reports/preprocess_report.md`, including total samples kept, labels kept, empty-label samples, corrected labels, dropped samples, dropped labels, and unresolved warnings.

Do not start model training until preprocessing has a written report in `experiments/reports/` and basic visual/label checks pass.

## Hardware Budget

Before any training run, write `experiments/reports/hardware_budget.md`.

Record:

- GPU model and dedicated VRAM, such as RTX 4090 with 24 GB VRAM when that is the available card.
- CPU model, system RAM, disk free space, CUDA/cuDNN/PyTorch or framework versions.
- Maximum allowed image size, common batch size, common epoch count, workers, precision, gradient accumulation, and model scale.
- A safety margin below dedicated VRAM. For a 24 GB card, target memory usage should stay below about 22 GB unless the user explicitly approves otherwise.

Rules:

- Do not enable shared GPU memory, CPU offload, disk offload, swap-based training, or model sharding that spills to system memory unless the user explicitly asks for it.
- If a run risks exceeding dedicated VRAM, reduce batch size, input resolution, model size, number of workers, cache policy, or use mixed precision and gradient accumulation.
- When reducing batch size for memory safety, update the shared experiment configuration and rerun/compare all affected methods with the same batch size.
- Tune `num_workers` upward when possible to improve throughput, but keep it within CPU core count, RAM, disk bandwidth, and data-loader stability. Run a short data-loader smoke test before long training.
- Run a short smoke test before long training to confirm memory usage, speed, and data loading behavior.
- Monitor GPU memory during training. If training begins paging into shared memory or slows dramatically because VRAM is exceeded, stop the run, record the issue, and revise the configuration.
- Prefer a smaller reproducible experiment over a larger run that depends on memory spillover and takes much longer.

## Phase 3: Baseline Selection

Search for baselines from the target task's recent literature and widely used open-source implementations.

Baseline selection rules:

- Include one primary baseline that is easy to reproduce and strong enough to be credible.
- Include additional comparison baselines when feasible, especially classic, lightweight, real-time, or state-of-the-art families relevant to the paper.
- Prefer official repositories, released pretrained weights, maintained packages, and models with published metrics on the selected datasets.
- Record model version, repository URL, commit/tag, weight URL, license, expected input size, parameters, FLOPs, FPS/latency, and published metrics.
- Download pretrained weights automatically when public. Keep weights under `model_code/weights/` and record their source.

Reproduce the primary baseline before adding innovations. If reproduced metrics are far from published or expected values, debug data processing, evaluation protocol, image size, training schedule, and dependency versions before claiming a new method.

## Phase 4: Improvement Direction Analysis

Before designing A/B/C, write `experiments/reports/improvement_direction_analysis.md`. The goal is to quickly identify the most promising innovation directions instead of randomly modifying the model.

Use evidence from:

- Baseline error analysis: class-wise metrics, object-size metrics, confusion cases, missed detections, false positives, temporal errors, or deployment bottlenecks.
- Dataset statistics: class imbalance, target size distribution, scene conditions, occlusion, blur, illumination, domain gap, label noise, or empty-label prevalence.
- Literature gaps: what recent papers improve, what they ignore, and which ideas are feasible on the selected datasets.
- Hardware budget: whether the direction fits local VRAM, runtime, parameter, FLOP, and training-time constraints.
- Paper story: whether the direction helps build a coherent method and convincing motivation.

Score each candidate direction before implementation:

```text
direction | targeted problem | evidence | expected gain | novelty | implementation cost | hardware cost | risk | story fit | priority
```

Recommended directions to compare:

- Data or augmentation strategy.
- Backbone/representation.
- Neck or feature fusion.
- Detection/classification head.
- Loss function or label assignment.
- Temporal modeling or tracking/post-processing.
- Lightweight deployment or inference optimization.
- Domain adaptation or robustness.

Rules:

- Select candidates with strong evidence and reasonable cost first.
- Prefer directions that can be tested with short screening runs before full training.
- Reject or postpone low-evidence directions even if they sound fashionable.
- If all top-ranked candidates fail, update the analysis and deliberately broaden the search space instead of repeatedly tweaking the same idea.
- Write `experiments/reports/candidate_screening.md` with the screening plan, quick results, and decision for each candidate.

Do not proceed to final A/B/C design until the improvement direction analysis identifies why those directions are likely to be effective.

## Phase 5: Innovation Design

Define at least three candidate innovations, named `A`, `B`, and `C`. Each must have:

- A source of evidence for the problem, such as baseline error analysis, literature gap, dataset statistics, qualitative failures, metric weakness, latency bottleneck, or deployment constraint.
- A clear hypothesis tied to a known weakness of the baseline or dataset.
- A minimal implementation plan.
- A mechanism explanation describing why the change should address that weakness.
- A statement of what internal part or module of the method is being changed, such as backbone representation, neck fusion, detection head, loss, assignment strategy, temporal modeling, augmentation policy, post-processing, or deployment path.
- A relationship note explaining how it relates to the other accepted innovations. `B` and `C` may address remaining limitations after earlier steps, or they may be complementary modules that solve different evidence-backed weaknesses of the same baseline.
- A module interface note when the innovation is modular: where it connects, what tensor/data flow it changes, what extra cost it adds, and what failure mode it is expected to fix.
- Expected effect on accuracy, robustness, speed, parameters, FLOPs, or memory.
- A risk note explaining how it could fail.
- A measurable acceptance criterion.

Good innovation categories include architecture modules, feature fusion, attention, loss functions, label assignment, data augmentation, temporal modeling, lightweight deployment changes, domain adaptation, post-processing, or training strategy. Avoid cosmetic changes that cannot be isolated experimentally.

Design `A`, `B`, and `C` with enough breadth to avoid getting stuck in one narrow direction. It is acceptable to build modules, replace modules, or combine modules when the evidence supports doing so. What is not acceptable is blind stacking: adding modules only because they sound useful, without a targeted problem, interface explanation, cost analysis, and validation.

Before committing to final A/B/C, create a candidate pool across at least two different improvement directions when feasible, such as representation, fusion, loss/assignment, augmentation, temporal modeling, post-processing, or lightweight deployment. Run lightweight screening within the hardware and anti-loop budgets, then select the strongest validated and most coherent set.

Before implementing A/B/C, write `experiments/reports/innovation_story.md` with this structure:

```text
Observed problem:
Evidence:
Research hypothesis:
A rationale:
B rationale:
C rationale:
How A -> B -> C forms one coherent method:
What mechanism or module changes at each step:
Why the selected modules/refinements are complementary:
Expected verification:
Risks and fallback ideas:
```

The story must be understandable in the paper's introduction and method sections. If the three innovations cannot be explained as one coherent answer to the research problem, redesign them before running the full ablation. A coherent answer may be a progressive chain, a complementary module set, or a hybrid of both.

## Phase 6: Experiment Loop

Run experiments in this required order:

```text
Baseline
Improved method after A
Improved method after A then B
Final improved method after A then B then C
```

For each step:

1. Train with the same data split, schedule, epoch count, batch size, image size, seed policy, and evaluation script unless the user explicitly approves a change.
2. Evaluate on every selected dataset or use one dataset for screening and another for final validation if compute is limited.
3. Record metrics, training curves, confusion/error analysis, qualitative examples, speed, parameters, FLOPs, and hardware.
4. Compare against the immediately previous accepted model and the original baseline.
5. Accept the innovation only if the primary metric improves meaningfully and trade-offs remain acceptable.
6. After accepting each innovation, update `experiments/reports/innovation_story.md` so the rationale and measured evidence stay aligned.
7. Keep every run within the documented hardware budget. Configuration changes made to fit VRAM must be applied consistently to baseline and improved methods.
8. Record `epochs`, `batch size`, `num_workers`, precision, gradient accumulation, and measured throughput for each run. `num_workers` may be tuned for throughput, but `epochs` and `batch size` must remain fixed across model experiments.

Use labels like `A`, `A then B`, and `A then B then C` only as shorthand in tables. In implementation and writing, describe the actual module or mechanism change, not just which letters were added.

Default acceptance guideline:

- Detection/segmentation: primary metric improves by at least 0.3 to 0.5 percentage points, or improves a difficult subset while preserving the main metric.
- Classification/action recognition: top metric improves by at least 0.5 percentage points, or improves robustness/generalization.
- Real-time systems: accuracy may stay similar only if latency, model size, or FPS improves substantially.

If an innovation does not improve:

- Do not hide it. Log it as rejected or under revision.
- Diagnose likely causes using loss curves, class-wise metrics, object-size metrics, qualitative errors, and overfitting/underfitting signals.
- Revise the idea, replace it with a better candidate, and rerun the affected step.
- Continue until there are three accepted innovations or until compute/data constraints make that impossible. If impossible, document the constraint and keep the strongest validated subset.

## Phase 7: Ablation And Comparison

After the final improved method is accepted, run final ablations:

- Baseline
- Improved method after A
- Improved method after A then B
- Final improved method after A then B then C
- Targeted diagnostic checks only when needed to explain a mechanism or module interaction. Do not present arbitrary `A/B/C` permutations as the main paper story, but do run targeted interaction checks when modules may help or interfere with each other.
- Comparison against selected external baselines under the same evaluation protocol.
- Cross-dataset validation on at least two public datasets.
- Efficiency comparison: parameters, FLOPs, FPS/latency, memory when relevant.

Use the same metric names and decimal precision across all tables. Mark the best and second-best values only after verifying the numbers come from logs.

## Phase 8: Reporting Results

Produce these artifacts before writing the paper:

- Main result table across datasets.
- Ablation table for the mechanism steps: after A, after A then B, and final method after A then B then C.
- Efficiency table.
- Training/evaluation curves when useful.
- Qualitative figure showing typical success and failure cases.
- Error analysis grouped by class, object size, scene type, occlusion, lighting, or other task-relevant factors.
- Reproducibility checklist with environment, commands, seeds, configs, checkpoints, and hardware.

Every number in every paper table must link back to `experiments/results/results.jsonl`, a training log, evaluation output, or a generated report.

## Phase 9: Chinese Manuscript Draft

Write the Chinese draft first, grounded in measured results. Store Chinese outlines, drafts, tables, captions, and revision notes under `paper/zh/`.

Recommended structure:

- 标题
- 摘要
- 关键词
- 引言
- 相关工作
- 方法
- 实验设置
- 实验结果与消融分析
- 讨论
- 结论
- 参考文献占位或已核验引用

Chinese writing rules:

- Keep the problem, motivation, method, and experimental evidence aligned.
- Explain A, B, and C as a coherent method, not three unrelated tricks.
- For each innovation, state the targeted problem, supporting evidence, design motivation, and verified effect.
- Explain what part of the method was changed at each step, including module placement and data flow when a module is introduced.
- Present A/B/C in a smooth logical order, such as problem diagnosis -> candidate module/mechanism screening -> selected complementary improvements -> final robust method.
- Use precise claims: say where the method improves, on which dataset, under which metric.
- Do not claim state-of-the-art unless the comparison table truly supports it.
- Include limitations and failure cases when they affect interpretation.

## Phase 10: English Manuscript Draft

Translate and rewrite from the approved Chinese draft; do not independently invent new claims. Store English outlines, drafts, tables, captions, and revision notes under `paper/en/`.

Before writing English, build `paper/shared/terminology.md`:

```text
中文术语 | English term | Abbreviation | First-use style | Notes
```

English writing rules:

- Keep terminology, abbreviations, dataset names, model names, and metric names consistent.
- Use standard academic phrasing for the target field.
- Preserve the same logical order as the Chinese draft unless English readability requires local restructuring.
- Check grammar, subject-verb agreement, article usage, tense, and parallel structure.
- Use past tense for completed experiments and present tense for general truths or method descriptions.
- Ensure every numerical claim matches the final verified tables.

## Completion Checklist

Do not report the work as complete until these are true:

- `experiments/state/work_plan.md`, `experiments/state/resume_state.md`, and `experiments/logs/work_journal.jsonl` are current enough for another agent or terminal to continue.
- Search/retry budgets were followed, and exhausted loops are documented in `experiments/reports/blockers.md`.
- A new project-specific conda environment was created, used for all project commands, documented, and exported.
- At least two public datasets are selected, sourced, downloaded where permitted, and documented.
- Datasets, model code, experiment outputs, and paper drafts are stored in their required folders.
- Preprocessing is complete, deterministic, and visually sanity-checked.
- Structured preprocessing logs exist for archive extraction, split generation, label validation, label conversion, empty labels, dropped/kept samples, and unresolved warnings.
- Hardware budget is documented, and no accepted run relies on shared GPU memory or memory offload.
- Epoch count and batch size are identical across all accepted model experiments; any batch-size reduction was applied to every compared method.
- `num_workers` is tuned within the local hardware budget and recorded for each run.
- The primary baseline is reproduced or the reproduction gap is explained and fixed as far as possible.
- Improvement directions were analyzed, scored, screened when feasible, and documented before final innovation design.
- At least three innovations were attempted, with accepted/rejected status recorded.
- Baseline, improved method after A, improved method after A then B, and final improved method experiments are logged.
- Only validated improvements appear as final innovations.
- Every final innovation has a documented problem, evidence, rationale, mechanism, and measured effect.
- A/B/C are evidence-backed mechanism or module improvements with a coherent relationship, not arbitrary modules that were simply stacked or permuted.
- The final A/B/C method has a coherent story that can be explained in the introduction, method, and ablation sections, whether the story is progressive, modular-complementary, or hybrid.
- Final results are traceable to logs/configs/checkpoints.
- Chinese draft exists before English draft.
- English terminology matches the Chinese draft and terminology table.
- The final response names the key artifacts and any unresolved constraints.
