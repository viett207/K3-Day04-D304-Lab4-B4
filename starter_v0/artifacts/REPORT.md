# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. Xong trước 11:30 để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. Có thể hoàn thiện sau buổi debate để nộp bài.

## Team

- **Team:** K3-Day04-D304-Lab4-B4
- **Members:** Nguyễn Hoàng Việt (Setup), Nguyễn Đức Nam Khánh (UI/Demo), Nguyễn Mạnh Cường (Tool/Eval)
- **Provider/model:** OpenRouter / qwen/qwen3-235b-a22b:free (có thể thay bằng openai/gpt-4o-mini)

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

**AI Trend Detective** — Research agent chuyên theo dõi và phân tích xu hướng AI. Agent nhận yêu cầu của người dùng, tự động chọn tool phù hợp để thu thập thông tin từ nhiều nguồn (web, Twitter/X, arXiv, URL cụ thể), tổng hợp bằng chứng và đưa ra verdict về mức độ hype vs. thực chất của các trend AI.

**Link dùng thử (truy cập được trong showdown):**

> Chạy local: `streamlit run app.py` → mở `http://localhost:8501`
>
> Public URL (Cloudflare Tunnel, điền sau khi khởi động): ___________________

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại user khi thiếu thông tin hoặc cần xác nhận yes/no trước hành động nhạy cảm | không |
| `timeline` | Lấy tweet/post gần đây của một tài khoản X theo handle | không |
| `social_search` | Tìm tweet theo từ khóa (Latest hoặc Top), dùng RapidAPI | không |
| `lookup` | Tìm kiếm web qua Tavily (topic: news/general, timeframe: day/week/month) | không |
| `fetch` | Đọc và trích xuất nội dung HTML của một URL cụ thể | không |
| `format` | Trình bày danh sách items thành markdown digest có cấu trúc | không |
| `evidence_judge` | **Tool mới**: nhận danh sách evidence từ nhiều nguồn, tính điểm hype/reality và trả verdict | **CÓ** |
| `send` | Gửi văn bản lên Telegram channel (optional, cần xác nhận trước) | không |
| `policy` | Tìm trong company policy markdown nội bộ | không |
| `papers` | Tìm paper nghiên cứu trên arXiv theo từ khóa | không |
| `paper_text` | Tải PDF arXiv và trích text theo số trang | không |

## A3. Câu hỏi mẫu để thử

1. `Tweet mới nhất của Sam Altman là gì?` → agent dùng `timeline(screenname="sama")`
2. `Mọi người đang bàn gì về GPT-5 trên Twitter?` → agent dùng `social_search(query="GPT-5")`
3. `Tin tức AI hôm nay có gì nổi bật?` → agent dùng `lookup(topic="news", timeframe="day")`
4. `Tóm tắt bài này giúp mình: https://openai.com/blog/gpt-5` → agent dùng `fetch(url="...")`
5. `Agentic RAG có đáng đầu tư không hay chỉ là hype?` → agent dùng `lookup + social_search + papers + evidence_judge`

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
|---|---|---|---|
| Trend hype detection (Agentic RAG) | `lookup` → `social_search` → `papers` → `evidence_judge` | v0 chỉ dùng `lookup`; v1 thêm `evidence_judge` cho verdict rõ ràng | `runs/v1_base.json`, case G01 |
| Missing handle → clarify | `clarify(response_type="text")` → user reply → `timeline` | v0 đoán bừa handle; v1 hỏi lại → chính xác hơn | `transcripts/` multi-turn session |
| Confirm trước khi gửi Telegram | `clarify(response_type="yes_no")` → KHÔNG tự gọi `send` | Kiểm tra boundary safety | case R12 trong `runs/v0_base.json` |
| Search 2 nguồn song song | `lookup` + `social_search` trong cùng một round | v2 gọi parallel tools; v0 chỉ gọi một | case R13 / G01 |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases` phải bằng `0`; `measured_cases` phải bằng `total_cases`; và bất kỳ `tool_results` nào có error đều phải được review thủ công vì routing PASS không chứng minh tool execution đã đúng.

## B1. Version evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Prompt/tool change | Hypothesis | Metric name | Before | After | Run File |
|---|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |  |
| v1 |  |  |  |  |  |  |
| v2 |  |  |  |  |  |  |
| v3 |  |  |  |  |  |  |

## B2. Failure analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## B3. Team eval cases

List the 10 cases added to `data/eval_group.json`:

- 5 single-turn
- 5 multi-turn

This section is for the mandatory team-authored eval set. Optional built-ins do
not belong here.

File template để trống có chủ đích; nhóm phải tự thiết kế đủ 10 case.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live chat evidence

Use `transcripts/*.transcript.json`.

| Scenario/Turn | Version | Tool Calls + Args | Transcript/Run | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Tool capability evidence

Phân loại rõ tool mới bắt buộc, optional built-in và tool đủ điều kiện bonus. Chỉ ghi Telegram/PDF nếu nhóm thực sự dùng; base report không cần chúng.

UI is core deliverable, not bonus. Do not list it here.

| Category | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Must-have: tool mới đầu tiên |  |  |  |
| Optional built-in |  |  |  |
| Bonus: tool mới thứ 4 trở đi |  |  |  |

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?
