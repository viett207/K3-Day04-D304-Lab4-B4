from pathlib import Path
text = """# AI Trend Detective — Kế hoạch phân công công việc (3 người)

## Tổng quan

File này chia công việc lab thành ba vai trò và giải thích rõ mỗi thành viên cần làm gì. Mục tiêu là thực hiện theo thứ tự:

1. Setup & preflight
2. Baseline v0 + UI
3. v1 + tool mới
4. Team eval = v2
5. Ra demo cuối

Mỗi người có phần việc chính, nhưng vẫn phải phối hợp chặt chẽ và review chéo để đảm bảo artifact nhất quán.

---

## Vai trò trong team

- **Nguyễn Hoàng Việt — Setup & Baseline lead**
- **Nguyễn Đức Nam Khánh — UI / Demo lead**
- **Nguyễn Mạnh Cường — Tool + Eval lead**

Bạn có thể thay bằng tên thật nếu muốn.

---

## Nguyễn Hoàng Việt: Setup & Baseline lead

### Trách nhiệm

- Cài và kiểm tra môi trường Python.
- Cấu hình `.env` và credential của provider.
- Chạy kiểm tra preflight provider.
- Xây prompt và tool baseline cho `v0`.
- Chạy baseline eval và thu bằng chứng.
- Cập nhật `artifacts/version_log.csv` cho `v0`.

### Kết quả cần đạt

- Hướng dẫn thiết lập `.env` trong repo (không commit `.env`).
- Nội dung `artifacts/system_prompt.md` cho baseline.
- Khai báo tool baseline trong `artifacts/tools.yaml`.
- Kết quả chạy `python run_eval.py --version v0` và file run JSON.
- Tổng hợp số liệu baseline.

### Công việc

1. Tạo file `.env` từ `./.env.example`.
   - Điền API key provider dùng.
   - Điền `TAVILY_API_KEY` và `RAPIDAPI_KEY` nếu cần.

2. Cài dependencies Python:
   ```powershell
   cd starter_v0
   python -m venv .venv
   .\\.venv\\Scripts\\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Chạy preflight:
   ```powershell
   python scripts/preflight_provider.py --provider openrouter
   ```
   - Nếu dùng provider khác thì đổi tham số.
   - Sửa lỗi provider nếu có.

4. Viết `artifacts/system_prompt.md`.
   - Tập trung mission AI Trend Detective.
   - Định nghĩa rõ quy tắc gọi tool.

5. Xác nhận `artifacts/tools.yaml` có ít nhất 5 tool core.
   - `clarify`, `lookup`, `social_search`, `timeline`, `fetch`, `format`.
   - Chưa thêm tool mới.

6. Chạy baseline eval:
   ```powershell
   python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json
   ```

7. Lưu run file và ghi số liệu.
   - Thêm dòng `v0` vào `artifacts/version_log.csv`.
   - Ghi tên file run JSON.

### Ghi chú

- Nguyễn Hoàng Việt không chỉnh team eval cases giai đoạn này.
- Baseline cần đủ ổn định để hỗ trợ UI và version sau.

---

## Nguyễn Đức Nam Khánh: UI / Demo lead

### Trách nhiệm

- Tạo UI Streamlit `app.py`.
- Hiển thị trace tool, version và transcript.
- Kiểm tra UI chạy cục bộ.
- Chuẩn bị tài liệu demo và báo cáo.

### Kết quả cần đạt

- `starter_v0/app.py` chạy được.
- `requirements.txt` có `streamlit>=1.30.0`.
- UI hiển thị:
  - yêu cầu người dùng
  - phản hồi cuối của agent
  - tool rounds và tool events
  - version artifact
  - file transcript đã lưu
- Nội dung demo trong `artifacts/REPORT.md` phần A.

### Công việc

1. Thêm Streamlit nếu cần:
   - Mở `requirements.txt`, thêm `streamlit>=1.30.0`.

2. Tạo file `starter_v0/app.py`.
   - Dùng lại `run_model_tool_loop` từ `chat.py`.
   - Cho phép chọn provider, version, và model override.
   - Hiển thị tool calls và tool results.
   - Lưu transcript vào `transcripts/`.

3. Chạy app cục bộ:
   ```powershell
   streamlit run app.py
   ```
   - Xác nhận mở được `http://localhost:8501`.

4. Test UI với một câu hỏi thử.
   - Xác nhận trace tool xuất hiện.
   - Xác nhận transcript file được tạo.

5. Chuẩn bị nội dung `artifacts/REPORT.md` phần A.
   - Mô tả mission, danh sách tool, câu hỏi mẫu, và kịch bản demo.

### Ghi chú

- UI là deliverable bắt buộc.
- Nếu Streamlit không chạy được, có thể dùng Flask/Gradio nhưng vẫn giữ tính năng tương đương.

---

## Nguyễn Mạnh Cường: Tool + Eval lead

### Trách nhiệm

- Thêm tool mới của nhóm.
- Cập nhật `tools/__init__.py` và `artifacts/tools.yaml`.
- Viết 10 case team eval vào `data/eval_group.json`.
- Chạy `v1` và `v2`.
- Hỗ trợ tạo transcript và bằng chứng báo cáo.

### Kết quả cần đạt

- Folder tool mới và tài liệu.
- Khai báo tool mới cập nhật.
- `data/eval_group.json` có 10 case.
- Kết quả chạy `run_eval.py` cho `v1` và `v2`.
- Bằng chứng team eval và tool mới.

### Công việc

1. Chọn tên và thiết kế tool mới.
   - Gợi ý: `evidence_judge` hoặc `trend_verdict`.
   - Tool nhận evidence và trả scores/verdict.

2. Tạo folder tool mới:
   - `tools/evidence_judge/TOOL.md`
   - `tools/evidence_judge/tool.py`

3. Đăng ký tool:
   - Thêm import và mapping trong `tools/__init__.py`.
   - Thêm khai báo tool vào `artifacts/tools.yaml`.

4. Viết logic trong `tool.py`.
   - Tính điểm evidence và trả JSON.
   - Giữ đơn giản nhưng có ý nghĩa.

5. Viết case eval trong `data/eval_group.json`.
   - 5 case single-turn.
   - 5 case multi-turn.
   - Mỗi case có `phase: "B"`, `failure_type`, `expect`, `metadata.what_it_tests`.
   - Phản ánh ý tưởng Trend Detective.

6. Chạy đường dẫn tool mới.
   - Sau baseline, chạy `v1` base eval.
   - Sau đó chạy `v2` group eval.

7. Ghi `v1` và `v2` vào `artifacts/version_log.csv`.
   - Ghi prompt/tool thay đổi, giả thuyết, metric before/after, và file run.

### Ghi chú

- Giữ tên tool đồng bộ giữa `artifacts/tools.yaml`, `tools/__init__.py`, và case eval.
- File eval nhóm phải phản ánh ý tưởng Trend Detective.

---

## Phối hợp chung

### Chia sẻ và review

- Dùng cùng một branch và cập nhật tiến độ thường xuyên.
- Review chéo trước khi commit.
- Giữ `artifacts/system_prompt.md` và `artifacts/tools.yaml` đồng bộ.
- Kiểm tra mỗi thay đổi bằng eval hoặc app test.

### Sync hàng ngày gợi ý

1. Nguyễn Hoàng Việt báo baseline và số liệu `v0`.
2. Nguyễn Đức Nam Khánh xác nhận UI chạy và trace hiển thị.
3. Nguyễn Mạnh Cường chia tool mới và case eval.
4. Thống nhất mọi thay đổi prompt/tool.

### Sở hữu file

- `Nguyễn Hoàng Việt`: `artifacts/system_prompt.md`, baseline `v0`, preflight, `artifacts/version_log.csv`.
- `Nguyễn Đức Nam Khánh`: `app.py`, UI trace, `requirements.txt`, báo cáo `artifacts/REPORT.md`.
- `Nguyễn Mạnh Cường`: `tools/evidence_judge`, `tools/__init__.py`, `artifacts/tools.yaml`, `data/eval_group.json`, `run_eval` team eval.

---

## Checklist demo cuối

Mỗi thành viên xác nhận một artifact:

- Nguyễn Hoàng Việt: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`
- Nguyễn Đức Nam Khánh: `streamlit run app.py` chạy và UI hiển thị trace.
- Nguyễn Mạnh Cường: `python run_eval.py --provider openrouter --version v2 --suite group --eval-cases data/eval_group.json`

Sau đó chuẩn bị demo chung:

- Case baseline thể hiện v0.
- Case v1 thể hiện tool mới.
- Case v2 team eval thể hiện Trend Detective.
- Scenario live UI từ `app.py`.

---

## Cách dùng file này

1. Gán tên thật cho mỗi thành viên.
2. Theo thứ tự công việc từng phần.
3. Cập nhật file nếu vai trò thay đổi.

Chúc nhóm hoàn thành tốt — kế hoạch này theo đúng workflow bạn yêu cầu và làm rõ công việc cho team 3 người.
"@
[System.IO.File]::WriteAllText('TEAM_TASKS.md', $txt, [System.Text.Encoding]::UTF8)
