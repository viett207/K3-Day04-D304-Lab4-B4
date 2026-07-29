# AI Trend Detective — Kế hoạch phân công công việc (3 người)

## Overview

This file divides the lab work into three roles and explains exactly what each member should do. The goal is to follow the workflow you requested:

1. Setup & preflight
2. Baseline v0 + UI
3. v1 + new tool
4. Team eval = v2
5. Final demo

Each member should own a primary area but collaborate closely, review each other's work, and keep the artifact state consistent.

---

## Team roles

- **Nguyễn Hoàng Việt — Setup & Baseline lead**
- **Nguyễn Đức Nam Khánh — UI / Demo lead**
- **Nguyễn Mạnh Cường — Tool + Eval lead**

You can replace these labels with actual names.

---

## Member Nguyễn Hoàng Việt: Setup & Baseline lead

### Responsibilities

- Install and verify environment.
- Configure `.env` and provider credentials.
- Run preflight provider checks.
- Build the baseline `v0` prompt + tool declarations.
- Run baseline evaluation and collect baseline evidence.
- Keep `artifacts/version_log.csv` updated for `v0`.

### Deliverables

- `.env` setup instructions in the repo (not committed).
- `artifacts/system_prompt.md` baseline content.
- `artifacts/tools.yaml` baseline declarations.
- `run_eval.py --version v0` output and run JSON evidence.
- Baseline metrics summary.

### Tasks

1. Create `.env` based on `./.env.example`.
   - Set provider key for whichever service you will use.
   - Set `TAVILY_API_KEY` and `RAPIDAPI_KEY` if needed for web/social tools.

2. Install Python dependencies if not already installed:
   ```bash
   cd starter_v0
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Run the preflight check:
   ```bash
   python scripts/preflight_provider.py --provider openrouter
   ```
   - If using another provider, change the provider flag.
   - Fix any provider issues before moving on.

4. Write baseline `artifacts/system_prompt.md`.
   - Focus on AI Trend Detective mission.
   - Make clear routing rules for the baseline tool set.

5. Confirm `artifacts/tools.yaml` contains at least 5 core tools.
   - `clarify`, `lookup`, `social_search`, `timeline`, `fetch`, `format` are good.
   - Do not add the new tool yet.

6. Run baseline eval:
   ```bash
   python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json
   ```

7. Save the run file and note the metrics.
   - Add a `v0` row in `artifacts/version_log.csv`.
   - Record the run JSON filename.

### Notes

- `Nguyễn Hoàng Việt` should not change team eval cases yet.
- Baseline should be stable enough to support the UI and later versions.

---

## Member Nguyễn Đức Nam Khánh: UI / Demo lead

### Responsibilities

- Create Streamlit UI entrypoint `app.py`.
- Display tool trace, version info, and transcript metadata.
- Verify UI works locally.
- Prepare demo artifacts and the final report format.

### Deliverables

- `starter_v0/app.py` working Streamlit app.
- `requirements.txt` includes `streamlit>=1.30.0`.
- UI behavior showing:
  - user request
  - final agent response
  - tool rounds and tool events
  - artifact version label
  - saved transcript file path
- Demo notes and scenarios in `artifacts/REPORT.md` Part A.

### Tasks

1. Add Streamlit dependency if missing:
   - Open `requirements.txt` and add `streamlit>=1.30.0`.

2. Create `starter_v0/app.py`.
   - Reuse `run_model_tool_loop` from `chat.py`.
   - Allow selecting provider, version, and model override.
   - Show live tool calls and results in the UI.
   - Save transcripts to `transcripts/`.

3. Run the app locally:
   ```bash
   streamlit run app.py
   ```
   - Confirm it opens at `http://localhost:8501`.

4. Test the UI with a simple agent request.
   - Confirm the trace appears.
   - Confirm transcript file is created.

5. Prepare `artifacts/REPORT.md` Part A content.
   - Add the agent mission, tool list, sample questions, and demo scenarios.

### Notes

- UI is a core deliverable, not optional.
- If Streamlit is unavailable, use a simple Flask/Gradio fallback, but keep the same contract.

---

## Member Nguyễn Mạnh Cường: Tool + Eval lead

### Responsibilities

- Add the new team tool.
- Update `tools/__init__.py` and `artifacts/tools.yaml`.
- Write the team evaluation cases in `data/eval_group.json`.
- Run `v1` and `v2` evaluations.
- Help produce final demo transcripts and report evidence.

### Deliverables

- New tool implementation directory and docs.
- Updated tool declarations and prompt if needed.
- `data/eval_group.json` with 10 cases.
- `run_eval.py` results for `v1` and `v2`.
- Evidence for team eval and new tool.

### Tasks

1. Choose the new tool name and design.
   - Suggested: `evidence_judge` or `trend_verdict`.
   - The tool should take gathered evidence and return scores/verdict.

2. Create new tool folder:
   - `tools/evidence_judge/TOOL.md`
   - `tools/evidence_judge/tool.py`

3. Register the tool:
   - Add the new import and function mapping in `tools/__init__.py`.
   - Add the tool declaration into `artifacts/tools.yaml`.

4. Implement basic logic in `tool.py`.
   - Score evidence and return structured JSON.
   - Keep it simple but meaningful.

5. Create team eval cases in `data/eval_group.json`.
   - 5 single-turn queries.
   - 5 multi-turn conversations.
   - Each with `phase: "B"`, `failure_type`, `expect`, and `metadata.what_it_tests`.
   - Test the new trend analysis concept.

6. Run the new tool path.
   - After baseline, run `v1` on base eval to validate new tool usage.
   - Then run `v2` on group eval.

7. Add `v1` and `v2` entries into `artifacts/version_log.csv`.
   - Document the prompt/tool change, hypothesis, metric before/after, and run file.

### Notes

- Keep tool names synchronized across `artifacts/tools.yaml`, `tools/__init__.py`, and eval expectations.
- The team eval file should be original and reflect your Trend Detective concept.

---

## Cross-team coordination

### Shared work and review

- Use the same branch and share progress often.
- Review each others changes before commit.
- Keep `artifacts/system_prompt.md` and `artifacts/tools.yaml` in sync.
- Validate every change by re-running the relevant eval or app test.

### Suggested daily sync

1. Nguyễn Hoàng Việt reports baseline status and `v0` metrics.
2. Nguyễn Đức Nam Khánh confirms UI works and shows the trace.
3. NNguyễn Mạnh Cường shares tool implementation and eval cases.
4. Agree on any prompt/tool wording changes together.

### File ownership summary

- `Nguyễn Hoàng Việt`: `artifacts/system_prompt.md`, baseline `v0`, preflight checks, `artifacts/version_log.csv`.
- `Nguyễn Đức Nam Khánh`: `app.py`, UI trace display, `requirements.txt`, demo writeup in `artifacts/REPORT.md`
- `NNguyễn Mạnh Cường`: `tools/evidence_judge`, `tools/__init__.py`, `artifacts/tools.yaml`, `data/eval_group.json`, `run_eval` for team eval.

---

## Final demo checklist

Each member should verify one demo artifact:

- Nguyễn Hoàng Việt: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`
- Nguyễn Đức Nam Khánh: `streamlit run app.py` works and UI shows tool trace.
- NNguyễn Mạnh Cường: `python run_eval.py --provider openrouter --version v2 --suite group --eval-cases data/eval_group.json`

Then prepare a final joint demo with:

- A baseline case showing v0 behavior.
- A v1 improvement showing the new tool in action.
- A v2 team eval case demonstrating the Trend Detective concept.
- A live UI scenario from `app.py`.

---

## How to use this file

1. Assign actual names to Nguyễn Hoàng Việt, B, C.
2. Follow the step order in each section.
3. Update the file if roles shift or if the team decides a different split is better.

Good luck — this plan follows your exact workflow and makes the lab execution clear for a 3-person team.