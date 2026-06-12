---
name: run-research-experiments
description: Use when an AI coding/research agent needs to run an end-to-end deep learning paper experiment involving public dataset discovery/download, preprocessing audit logs, resumable plans, anti-loop safeguards, per-project conda isolation, baseline reproduction, evidence-based mechanism innovation, fast candidate screening, M0-M3 ablations, experiment consistency checks, result figures, bilingual manuscript drafting, claim-evidence tracing, and reproducible artifacts.
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
- Use mechanism versions instead of blind letter stacking: `M0` is the reproduced baseline, `M1`, `M2`, and `M3` are accepted method versions. Paper labels such as `A`, `B`, and `C` may be used only after they map to concrete `M1/M2/M3` mechanism changes.
- Each step from `M1` to `M3` must specify whether it adds, replaces, refines, removes, or re-parameterizes an internal component. Later steps may revise earlier modules; they do not need to simply append more blocks.
- Module-based innovation is allowed. Modules may improve different parts of the system, such as backbone, neck, head, loss, assignment, augmentation, post-processing, or deployment path, but each module must have evidence, a clear interface, an expected effect, and measured validation.
- Do not force all innovations into one direction if evidence shows diminishing returns. If one path stalls, broaden the candidate pool across different model components or training/inference stages.
- Before implementing innovations, analyze and rank improvement directions from evidence. Do not change the model randomly; target the most likely failure sources first to find effective innovations faster.
- Before full training, run a fast candidate screening protocol when compute permits. Screen multiple evidence-backed candidates cheaply, promote only promising candidates to full `M1/M2/M3` experiments, and stop or broaden the direction when the screening budget is exhausted.
- Treat local hardware as a hard constraint. Before training, detect or confirm GPU model, dedicated VRAM, CPU, RAM, and disk space. Do not exceed dedicated GPU memory, and do not rely on shared GPU memory, CPU offload, disk offload, or swap to make an experiment fit.
- Keep `epochs` and `batch size` identical for all model experiments, including baseline, intermediate improved methods, final method, and external comparison baselines. If one method cannot fit the planned batch size, lower the common batch size for all methods.
- Dataset preprocessing must produce structured audit logs. Archive extraction, generated splits, label conversion, invalid labels, empty labels, file deletion, file retention, and sample filtering must be recorded; never silently fix or drop data.
- Every substantial task must have a written plan, progress log, and resume checkpoint so another terminal or agent can continue without starting over.
- Maintain both human-readable and machine-readable state: `work_plan.md` and `resume_state.md` for humans, plus `project_state.json` and `experiment_registry.yaml` for agents and scripts.
- Use explicit search/retry budgets to prevent dead loops. If a dataset, model, paper, download, or bug fix cannot be found or solved within the budget, stop, log the blocker, and present alternatives.
- Every project must use a newly created, project-specific conda environment. Do not install dependencies into `base`, do not reuse another project's environment, and do not mix package state across projects.
- Experimental result figures must be reproducible from logged data. Save the raw plot data, plotting script, vector export, and PNG export; do not create figures from hand-edited numbers.
- Before final reporting or manuscript drafting, run an experiment consistency check for epochs, batch size, data split, evaluation script, input size, seeds, and hardware-relevant settings.
- Every important paper claim must be traceable through `paper/shared/claim_evidence_matrix.md` to a metric, table, figure, log, config, checkpoint, or external citation.
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
  figure_scripts/
  reports/
  state/
paper/
  zh/
  en/
  shared/
```

Do not mix these categories. Dataset archives and processed labels stay under `datasets/`; source code, configs, and weights stay under `model_code/`; metrics, logs, checkpoints, plots, and ablation outputs stay under `experiments/`; manuscript files stay under `paper/`.

## Reusable Skill Resources

When starting a new project, copy these templates from this skill into the project workspace before running long tasks:

- `templates/project_state.json` -> `experiments/state/project_state.json`
- `templates/experiment_registry.yaml` -> `experiments/state/experiment_registry.yaml`
- `templates/claim_evidence_matrix.md` -> `paper/shared/claim_evidence_matrix.md`
- `templates/consistency_report.md` -> `experiments/reports/consistency_report.md` if a blank report is needed before running checks.

Before final tables or manuscript claims, run the consistency checker from the project root:

```text
python <skill_dir>/scripts/check_experiment_consistency.py --registry experiments/state/experiment_registry.yaml --results experiments/results/results.jsonl --output experiments/reports/consistency_report.md
```

If the script reports `FAIL`, fix the experiment configuration mismatch or document why the affected runs cannot be compared before using those results in the paper.

Maintain these records:

- `experiments/reports/dataset_sources.md`: dataset name, task, official page, paper, license, download URL, access date, citation.
- `experiments/reports/preprocess_report.md`: split policy, label mapping, ignored labels, image/video counts, class counts, integrity checks.
- `experiments/state/work_plan.md`: phase plan, task status, assumptions, decisions, and next actions.
- `experiments/state/resume_state.md`: latest checkpoint for restarting after interruption or switching terminals.
- `experiments/state/project_state.json`: machine-readable project phase, active task, accepted method versions, blockers, and next action.
- `experiments/state/experiment_registry.yaml`: machine-readable list of planned, running, completed, failed, accepted, and rejected runs.
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
- `experiments/reports/experiment_matrix.md`: `M0` baseline, `M1`, `M2`, `M3`, comparison methods, datasets, metrics, seeds, status, and whether each method is screening-only or full-run.
- `experiments/results/results.jsonl`: one line per run with command, config, git SHA, seed, hardware, metrics, checkpoint, log path.
- `experiments/reports/improvement_direction_analysis.md`: baseline weaknesses, evidence, candidate directions, scores, priorities, and selected improvement path.
- `experiments/reports/candidate_screening.md`: lightweight screening plan and results for candidate modules/mechanisms before full experiments.
- `experiments/reports/innovation_audit.md`: accepted and rejected innovations with evidence.
- `experiments/reports/innovation_story.md`: problem evidence, `M1/M2/M3` rationale, mechanism changes, logical relationship, and paper narrative.
- `experiments/reports/consistency_report.md`: pre-reporting audit of shared epochs, batch size, split, input size, evaluation script, seeds, and hardware-relevant settings.
- `experiments/reports/hardware_budget.md`: GPU/VRAM, CPU/RAM, disk, allowed batch/image/model settings, and memory safety margin.
- `experiments/results/curves/`: raw curve data used for training/validation plots.
- `experiments/results/tables/`: raw tabular data used for ablation, efficiency, class-wise, error-analysis, and dataset-statistic plots.
- `experiments/figure_scripts/`: plotting scripts that regenerate experimental result figures.
- `experiments/figures/`: exported experimental result figures, grouped by plot type.
- `paper/shared/claim_evidence_matrix.md`: each manuscript claim mapped to evidence files, result ids, figures, tables, or citations.
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

Also update `experiments/state/project_state.json` and `experiments/state/experiment_registry.yaml` whenever phase, run status, accepted method version, blocker, or next action changes. Prefer copying the templates from this skill's `templates/` directory when starting a new project.

`project_state.json` must include:

```text
project_id | current_phase | active_task | datasets | baseline | method_versions | accepted_versions | rejected_candidates | hardware_budget | blockers | next_action | last_updated
```

`experiment_registry.yaml` must include one entry per screening or full run:

```text
run_id | method_version | run_type | dataset | seed | config | epochs | batch_size | input_size | eval_script | status | metrics | artifacts | decision
```

When resuming after an interruption or switching terminals:

1. Read `experiments/state/project_state.json`, `experiments/state/experiment_registry.yaml`, `experiments/state/resume_state.md`, `experiments/state/work_plan.md`, `experiments/logs/work_journal.jsonl`, `experiments/results/results.jsonl`, and relevant reports before acting.
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

Before designing `M1/M2/M3`, write `experiments/reports/improvement_direction_analysis.md`. The goal is to quickly identify the most promising innovation directions instead of randomly modifying the model.

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

### Fast Candidate Screening

Use screening to find effective innovations faster without burning full training time.

Screening rules:

- Build a candidate pool across at least two improvement directions when feasible, such as representation, fusion, loss/assignment, augmentation, temporal modeling, post-processing, or lightweight deployment.
- For each direction, try only evidence-backed candidates with a stated hypothesis and expected metric effect.
- Use the same screening budget for comparable candidates: same subset, same short epoch count, same batch size, same seed policy, same input size, and same evaluation script.
- Default budget: at most 3 candidates per direction and at most 2 revision attempts for the same candidate. If all candidates in a direction fail, stop that direction and broaden the search.
- Promote a candidate to full experiments only if it improves the screening metric, fixes a diagnosed failure mode, or improves efficiency without unacceptable accuracy loss.
- Record every screened candidate in `experiments/reports/candidate_screening.md` and `experiments/state/experiment_registry.yaml`, including rejected candidates.

Do not proceed to final `M1/M2/M3` design until the improvement direction analysis and candidate screening identify why the selected mechanisms are likely to be effective.

## Phase 5: Innovation Design

Define at least three accepted method versions: `M1`, `M2`, and `M3`. `M0` is always the reproduced baseline. Each method version must have:

- A source of evidence for the problem, such as baseline error analysis, literature gap, dataset statistics, qualitative failures, metric weakness, latency bottleneck, or deployment constraint.
- A clear hypothesis tied to a known weakness of the baseline or dataset.
- A minimal implementation plan.
- A mechanism explanation describing why the change should address that weakness.
- A statement of what internal part or module of the method is being changed, such as backbone representation, neck fusion, detection head, loss, assignment strategy, temporal modeling, augmentation policy, post-processing, or deployment path.
- An operation type: `add`, `replace`, `refine`, `remove`, or `re-parameterize`.
- A relationship note explaining how it relates to the other accepted versions. `M2` and `M3` may address remaining limitations after earlier steps, replace a weak part of `M1`, refine an accepted module, or add complementary mechanisms that solve different evidence-backed weaknesses of the same baseline.
- A module interface note when the innovation is modular: where it connects, what tensor/data flow it changes, what extra cost it adds, and what failure mode it is expected to fix.
- Expected effect on accuracy, robustness, speed, parameters, FLOPs, or memory.
- A risk note explaining how it could fail.
- A measurable acceptance criterion.

Good innovation categories include architecture modules, feature fusion, attention, loss functions, label assignment, data augmentation, temporal modeling, lightweight deployment changes, domain adaptation, post-processing, or training strategy. Avoid cosmetic changes that cannot be isolated experimentally.

Design `M1`, `M2`, and `M3` with enough breadth to avoid getting stuck in one narrow direction. It is acceptable to build modules, replace modules, refine modules, remove harmful parts, or combine complementary modules when the evidence supports doing so. What is not acceptable is blind stacking: adding modules only because they sound useful, without a targeted problem, interface explanation, cost analysis, and validation.

Before committing to final `M1/M2/M3`, create a candidate pool across at least two different improvement directions when feasible, such as representation, fusion, loss/assignment, augmentation, temporal modeling, post-processing, or lightweight deployment. Run lightweight screening within the hardware and anti-loop budgets, then select the strongest validated and most coherent version sequence.

Before implementing `M1/M2/M3`, write `experiments/reports/innovation_story.md` with this structure:

```text
Observed problem:
Evidence:
Research hypothesis:
M1 change, operation type, and rationale:
M2 change, operation type, and rationale:
M3 change, operation type, and rationale:
How M0 -> M1 -> M2 -> M3 forms one coherent method:
What mechanism or module changes at each step:
Why the selected modules/refinements are complementary:
Expected verification:
Risks and fallback ideas:
```

The story must be understandable in the paper's introduction and method sections. If the three accepted versions cannot be explained as one coherent answer to the research problem, redesign them before running the full ablation. A coherent answer may be a progressive chain, a complementary module set, a replacement/refinement sequence, or a hybrid of these.

## Phase 6: Experiment Loop

Run experiments in this required order:

```text
M0 Baseline
M1 accepted mechanism version
M2 accepted mechanism version
M3 final accepted mechanism version
```

For each step:

1. Train with the same data split, schedule, epoch count, batch size, image size, seed policy, and evaluation script unless the user explicitly approves a change.
2. Evaluate on every selected dataset or use one dataset for screening and another for final validation if compute is limited.
3. Record metrics, training curves, confusion/error analysis, qualitative examples, speed, parameters, FLOPs, and hardware.
4. Compare against the immediately previous accepted model and the original baseline.
5. Accept the method version only if the primary metric improves meaningfully, a diagnosed failure mode is fixed, or an efficiency objective improves with acceptable trade-offs.
6. After accepting each method version, update `experiments/reports/innovation_story.md`, `experiments/state/project_state.json`, and `experiments/state/experiment_registry.yaml` so the rationale and measured evidence stay aligned.
7. Keep every run within the documented hardware budget. Configuration changes made to fit VRAM must be applied consistently to baseline and improved methods.
8. Record `epochs`, `batch size`, `num_workers`, precision, gradient accumulation, and measured throughput for each run. `num_workers` may be tuned for throughput, but `epochs` and `batch size` must remain fixed across model experiments.

Use labels like `A`, `B`, and `C` only as optional paper shorthand after they map to concrete versions such as `M1: replace neck fusion`, `M2: refine assignment loss`, or `M3: add post-processing calibration`. In implementation and writing, describe the actual mechanism change, not just which letters were added.

Default acceptance guideline:

- Detection/segmentation: primary metric improves by at least 0.3 to 0.5 percentage points, or improves a difficult subset while preserving the main metric.
- Classification/action recognition: top metric improves by at least 0.5 percentage points, or improves robustness/generalization.
- Real-time systems: accuracy may stay similar only if latency, model size, or FPS improves substantially.

If an innovation does not improve:

- Do not hide it. Log it as rejected or under revision.
- Diagnose likely causes using loss curves, class-wise metrics, object-size metrics, qualitative errors, and overfitting/underfitting signals.
- Revise the idea, replace it with a better candidate, remove the harmful part, or re-parameterize the mechanism, then rerun the affected step.
- Continue until there are three accepted innovations or until compute/data constraints make that impossible. If impossible, document the constraint and keep the strongest validated subset.

## Phase 7: Ablation And Comparison

After the final improved method is accepted, run final ablations:

- `M0` baseline.
- `M1` accepted mechanism version.
- `M2` accepted mechanism version.
- `M3` final accepted mechanism version.
- Targeted diagnostic checks only when needed to explain a mechanism or module interaction. Do not present arbitrary permutations as the main paper story, but do run targeted interaction checks when mechanisms may help or interfere with each other.
- Comparison against selected external baselines under the same evaluation protocol.
- Cross-dataset validation on at least two public datasets.
- Efficiency comparison: parameters, FLOPs, FPS/latency, memory when relevant.

Use the same metric names and decimal precision across all tables. Mark the best and second-best values only after verifying the numbers come from logs.

Before writing result tables or paper claims, generate `experiments/reports/consistency_report.md`. The report must pass or explicitly explain every mismatch in epochs, batch size, data split, input size, evaluation script, seed policy, precision, gradient accumulation, and hardware-relevant settings.

## Phase 8: Reporting Results

Produce these artifacts before writing the paper:

- Main result table across datasets.
- Ablation table for the mechanism versions: `M0`, `M1`, `M2`, and `M3`.
- Efficiency table.
- Training/validation curves.
- Qualitative result figures showing typical success and failure cases.
- Class-wise performance figures when labels/classes exist.
- Dataset-statistic figures that support preprocessing, problem diagnosis, or improvement direction analysis.
- Error analysis grouped by class, object size, scene type, occlusion, lighting, or other task-relevant factors.
- Reproducibility checklist with environment, commands, seeds, configs, checkpoints, and hardware.
- Claim-evidence matrix mapping each manuscript claim to supporting result files, tables, figures, logs, configs, checkpoints, or citations.

Every number in every paper table must link back to `experiments/results/results.jsonl`, a training log, evaluation output, or a generated report.

Before manuscript drafting, create `paper/shared/claim_evidence_matrix.md` with:

```text
claim_id | manuscript_section | claim_text | evidence_type | evidence_path | result_id_or_citation | status | notes
```

### Experimental Result Figure Requirements

These requirements apply to experimental result figures only. Method architecture diagrams, module diagrams, conceptual illustrations, and model-flow figures may be designed separately according to the paper story.

Required experimental result figures:

- Training/validation curves: train loss, validation loss, and task metrics such as mAP50, mAP50-95, Precision, Recall, Accuracy, F1, IoU, or other task-specific metrics.
- Ablation result figure: `M0` baseline, `M1`, `M2`, and `M3` final method.
- Efficiency comparison figure: parameters, FLOPs, FPS, latency, memory, or scatter plots such as metric vs Params, metric vs FPS, or metric vs Latency.
- Class-wise performance figure: per-class AP, F1, Accuracy, Recall, or task-relevant class metric.
- Error-analysis figure: confusion matrix for classification, or detection/segmentation error types such as missed detection, false positive, localization error, small-object error, occlusion error, or label-noise-related error.
- Dataset-statistic figure: class distribution, train/val/test counts, target-size distribution, empty-label samples, or other preprocessing statistics.
- Qualitative result figure: GT, baseline prediction, and final method prediction, including both success cases and failure cases.

Training/validation curve rules:

```text
x-axis: epoch
y-axis: loss or metric
curves: M0 baseline, M1, M2, M3 final method
source: training log, validation log, results.csv, TensorBoard log, or experiments/results/results.jsonl
style: color + linestyle + marker
preview export: PNG at dpi=300
final raster export: PNG at dpi=600
vector export: PDF or SVG
```

- Curves in the same plot must use the same epoch count, batch size, data split, validation set, and evaluation script.
- Do not compare curves from different training schedules unless the figure explicitly explains the difference and the user approved it.
- If smoothing is used, state the smoothing window and preserve the raw curve data. Do not show only a smoothed curve without traceable raw data.
- Mark best epoch or final epoch when useful, but do not crop the curve to only the favorable segment.
- If multiple random seeds are used, plot the mean and use a shaded band for standard deviation.
- For many epochs, use `markevery=5` or `markevery=10` so markers remain readable.

Figure style rules:

- Do not distinguish methods by color alone. Use color plus linestyle plus marker for lines, and color plus hatch or edge style for bars.
- Suggested line styles: `M0` baseline = solid + circle marker, `M1` = dashed + square marker, `M2` = dash-dot + triangle marker, `M3` final = dotted + diamond marker.
- Line width: 2.0 to 2.5 pt. Use 2.5 pt for primary curves and 2.0 pt for auxiliary curves.
- Axis spine width: 1.2 to 1.5 pt.
- Grid width: 0.6 to 0.8 pt with alpha 0.25 to 0.35.
- Marker size: 5 to 7 pt.
- Bar edge line width: 1.0 to 1.2 pt.
- Recommended font sizes: axis labels 11 to 12 pt, ticks 9 to 10 pt, legend 9 to 10 pt, subplot titles 11 to 12 pt.
- Legends must use full method names or clear stage names, not only `A`, `B`, `C`, or bare `M1/M2/M3`.
- Legends must not cover the main data. Place them outside the axes or above the plot when needed.
- Figures must remain interpretable in black-and-white printing.

Export and reproducibility rules:

- Save raw plot data under `experiments/results/curves/` or `experiments/results/tables/`.
- Save plotting scripts under `experiments/figure_scripts/`.
- Save exported figures under `experiments/figures/<plot_type>/`.
- Export every paper-ready experimental result figure as PDF or SVG plus PNG.
- Use `dpi=300` for preview PNG and `dpi=600` for final raster PNG.
- Every figure must document data source, plotting script, export path, dpi, and format in the work journal or figure report.
- Do not hide failed innovation curves or failed diagnostic plots; keep them in experiment records even if they are not used in the final paper.

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
- Explain `M1`, `M2`, and `M3` as a coherent method evolution, not three unrelated tricks.
- For each innovation, state the targeted problem, supporting evidence, design motivation, and verified effect.
- Explain what part of the method was changed at each step, including module placement and data flow when a module is introduced.
- Present the method versions in a smooth logical order, such as problem diagnosis -> candidate module/mechanism screening -> selected mechanism change -> refinement/replacement -> final robust method.
- Use precise claims: say where the method improves, on which dataset, under which metric.
- Do not claim state-of-the-art unless the comparison table truly supports it.
- Include limitations and failure cases when they affect interpretation.
- Link each major claim to `paper/shared/claim_evidence_matrix.md` before writing the final Chinese or English draft.
### Chinese Small-Paper Writing And Formatting Rules

Use these rules when the user asks for a Chinese SCI/EI-style small paper or asks to polish a Chinese manuscript according to prior preferences:

- Drafting route: produce a Chinese draft first, revise the Chinese manuscript against the user's structural and formatting requirements, then polish or translate. Do not jump directly to an English manuscript when the user asks for a Chinese first version.
- Template matching: if the user provides a sample Word document, inspect its fonts, heading levels, caption style, paragraph spacing, table style, reference style, and page layout before generating the new manuscript. Match the sample unless the user gives a newer explicit formatting rule.
- Title pattern: use “一种基于……的……方法” when the paper is method-oriented. The title must name the core mechanism and the target task directly.
- Abstract: target about 400 Chinese characters. Sentence 1 states the research meaning. Sentence 2 states the concrete problem and “本文提出了一种基于……的……方法”. Then state implementation, measured effect, and significance. Do not include detailed hardware model names, formula symbols, inequalities, or over-specific abbreviations in the abstract.
- Keywords: use five keywords ordered from broad background to specific technology.
- Introduction: write research meaning, current methods, research gaps that this paper actually addresses, this paper’s work, and manuscript structure. Citations should be distributed across the first two paragraphs, cited one by one, and should not be reused later in Related Work unless unavoidable.
- Related Work: organize from large background to concrete task in about three paragraphs, about 300 Chinese characters per paragraph when the journal format permits. Each paragraph should correspond to verified references and should not overuse old literature.
- Claims: use declarative academic prose. Do not advertise, overstate novelty, claim state-of-the-art without evidence, use emotional adjectives, use story-like phrasing, use unnecessary quotation marks, or raise gaps that the method/experiments do not address.
- Methods: explain the system top-down from input to output. Define variables once, keep notation consistent across equations, tables, figures, and text, and provide formulas for model outputs, fusion, gating, and decision rules when applicable.
- Experiments: every table/figure needs one analysis paragraph. Include ablation, efficiency, and failure/degradation analysis when supported by logs. Do not fabricate experiments; if an experiment cannot be added, state the limitation.
- Tables: use three-line tables. Center cell content horizontally and vertically, remove paragraph indents inside cells, keep decimal places consistent by applying one decimal-place rule per metric column, and adjust widths so cells do not break into one- or two-character lines. Any variable, metric symbol, subscript, superscript, Greek letter, or formula-like expression inside a table must be inserted as a Word/MathType-compatible equation object, not typed as plain text.
- Figures: draw manuscript diagrams as PPT sketches or editable PPT source first, then export images at 600 dpi or higher and insert the exported images into Word; keep the PPT source with the manuscript package for later editing. Use differentiated colors/shapes, orthogonal arrows, no arrow-through-text, no overlapping lines, no text overflow, and figure text large enough to remain readable after Word insertion and PDF export. If a specialized diagram tool or skill is available, consider it for deep-learning/model architecture diagrams. Variables and formulas in PPT diagrams should use MathType/Office equation objects before export whenever feasible.
- Equations: use Word/MathType-compatible equation objects when generating DOCX. This applies to display equations, inline variables in body text, table cells, figure labels, and captions when they contain formula symbols. Put display equation numbers on the right, use single line spacing around equations, captions, and figure/table labels when needed for complete display, and verify in exported PDF that subscripts and symbols are complete. Audit physiological variable notation and subscripts explicitly; for peripheral blood oxygen saturation, use `SpO_2` or `\mathrm{SpO}_2` consistently, not `SPO2`, `Sp02`, or mixed forms.
- Word formatting: body Chinese font is 宋体小四, English font is Times New Roman 小四. Captions and references use 五号. First-level headings such as 引言、相关工作、方法与材料、实验分析、结论、参考文献 should have no first-line indent; second-level headings such as 3.1 and 4.1 should also have no indent. Keep each figure with its caption on the same page and each table with its caption on the same page by using keep-with-next/page-break controls. Do not insert spaces between adjacent Chinese and English/numeric terms in body text unless required by the target journal or a style guide.
- Citations and references: cite in order without skipped numbers; avoid ranges longer than three references, and prefer individual citations. Use superscript citation markers linked to the reference list. In DOCX, references must use real Word automatic numbering, not hand-typed `[1]` text. Add bookmarks or equivalent anchors on numbered reference items so each in-text citation can jump to the corresponding reference. Target 30 references when the user requests a standard small-paper reference set. Verify every reference against Crossref, publisher pages, or PDFs, and ensure titles match publisher/PDF metadata rather than AI-generated variants. Prefer recent five-year journal papers, CAS Q2 or above when feasible, fewer OA/MDPI/conference references, GB/T 7714 style, no DOI in the final reference list, page range or article number when available, hanging indent of two Chinese characters, justified alignment, and reference paragraph line spacing set to exactly 20 pt. Download legally available PDFs when possible and produce a manifest for unavailable or access-restricted PDFs.
- Revision loop: after the first complete draft, simulate at least three reviewers with at least three comments each, including content, experiment, and formatting issues. Revise according to feasible comments. Add experiments only when existing data/logs support them; otherwise state why the experiment cannot be added.
- File hygiene: after producing the final package, remove temporary lock files and clearly obsolete drafts, or move old versions into an archive folder. Do not delete source data, verified references, scripts, or user-provided files.
- Final QA: export DOCX to PDF, render or visually inspect pages, and check headings, duplicate numbering, table layout, decimal-place consistency, figure/caption and table/caption same-page placement, figure text readability, equation completeness, variable subscripts, reference 20 pt line spacing, reference numbering, citation jump links, typos, and Chinese-English spacing. For DOCX structure, verify that formula-like content is stored as equation objects, reference entries are real numbered-list paragraphs, manual reference-number paragraphs are absent, citation anchors resolve to reference bookmarks, and exported PDF retains link annotations when citation jumps are required. Check that title numbering, figure numbering, table numbering, and reference numbering are not duplicated. After QA, report any remaining limits such as inaccessible reference PDFs or experiments that could not be added from existing data.

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
- `experiments/state/project_state.json` and `experiments/state/experiment_registry.yaml` are current enough for another agent or script to resume.
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
- `M0`, `M1`, `M2`, and `M3` experiments are logged.
- Only validated improvements appear as final innovations.
- Every final innovation has a documented problem, evidence, rationale, mechanism, and measured effect.
- `M1/M2/M3` are evidence-backed mechanism or module improvements with a coherent relationship, not arbitrary modules that were simply stacked or permuted.
- Each accepted version records whether it adds, replaces, refines, removes, or re-parameterizes an internal mechanism.
- The final `M0 -> M1 -> M2 -> M3` story can be explained in the introduction, method, and ablation sections, whether the story is progressive, modular-complementary, replacement/refinement-based, or hybrid.
- `experiments/reports/consistency_report.md` verifies shared epochs, batch size, data split, input size, evaluation script, seed policy, and hardware-relevant settings.
- Final results are traceable to logs/configs/checkpoints.
- `paper/shared/claim_evidence_matrix.md` links major Chinese and English manuscript claims to evidence.
- Chinese draft exists before English draft.
- English terminology matches the Chinese draft and terminology table.
- The final response names the key artifacts and any unresolved constraints.
