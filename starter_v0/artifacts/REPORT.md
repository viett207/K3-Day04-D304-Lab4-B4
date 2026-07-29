# Day 04 Lab v2 Report — AI Trend Detective

## Team

- Team: K3-Day04-D304-Lab4-B4
- Members: Nguyễn Hoàng Việt, Nguyễn Đức Nam Khánh, Nguyễn Mạnh Cường
- Phân chia công việc ở TEAM_TASKS.md
- UI: Streamlit (`app.py`)
- Provider/model: OpenRouter + `openai/gpt-4o-mini` was used for the saved v0 transcripts. Gemini 2.5 Flash was configured for live testing, but its Google project returned `403 PERMISSION_DENIED`; this is a provider/project-access issue, not a valid evaluation result.

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

AI Trend Detective là research agent giúp đánh giá một xu hướng AI là cơ hội thực tế hay chỉ là hype. Agent thu thập evidence từ web, mạng xã hội, tài khoản cụ thể và paper; sau đó tổng hợp điểm Evidence, Hype, Adoption và Risk để đưa ra verdict có cấu trúc.

**Link dùng thử:** chạy cục bộ bằng `streamlit run app.py`, sau đó mở `http://localhost:8501`.

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại khi yêu cầu thiếu phạm vi hoặc thông tin cần thiết. | Không |
| `lookup` | Tìm tin và thông tin web về xu hướng AI. | Không |
| `social_search` | Tìm thảo luận trên X/Twitter theo từ khóa. | Không |
| `timeline` | Lấy các bài đăng gần đây của một tài khoản X/Twitter. | Không |
| `fetch` | Đọc nội dung từ một URL cụ thể. | Không |
| `papers` | Tìm research paper liên quan. | Không |
| `paper_text` | Lấy text từ paper arXiv. | Không |
| `evidence_judge` | Chấm Evidence, Hype, Adoption, Risk; trả verdict và phương pháp tính điểm. | **Có** |
| `format` | Chuyển evidence thành markdown digest. | Không |
| `policy` | Tìm trong tài liệu policy nội bộ. | Không |
| `send` | Gửi nội dung sau khi có xác nhận. | Không |

## A3. Câu hỏi mẫu để thử

1. `Xem 5 tweet mới nhất của Sam Altman về AI trend, sau đó đánh giá mức độ hype.`
2. `Agentic RAG năm 2026 có đáng để làm đồ án hay chỉ là hype? Hãy nêu evidence và rủi ro.`
3. `Tôi muốn đánh giá AI cho marketing tại Việt Nam; chỉ tập trung vào social media.`
4. `Tóm tắt bài viết này và nói liệu nó có cho thấy hype AI không: <URL>.`
5. `Trend AI gần đây, tôi nên đầu tư vào cái nào?` — agent cần hỏi lại phạm vi trước khi tìm kiếm.

## A4. Kịch bản demo đã chuẩn bị

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
|---|---|---|---|
| Câu hỏi mơ hồ: `abcd là gì?` | `clarify` với `response_type: text` | v0 xác nhận thông tin còn thiếu thay vì tự đoán. | `transcripts/v0_openrouter_20260729T123500.transcript.json` |
| Kiểm tra tài khoản cụ thể | `timeline(screenname="sama", limit=5)` | v2 có case G03 kiểm tra chọn đúng tool và đúng handle. | Chạy lại từ UI với RapidAPI key. |
| Đánh giá Agentic RAG | `lookup` → `social_search` → `papers` → `evidence_judge` | v1 thêm bước chấm điểm có thể giải thích thay vì chỉ tóm tắt nguồn. | Chạy lại sau khi cấu hình các key nghiên cứu. |
| Đánh giá URL | `fetch` → `evidence_judge` | v2 có G10 để kiểm tra URL cụ thể không bị định tuyến nhầm sang search. | Chạy case G10 trong group eval. |

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version evidence

Run group eval mới nhất đã được lưu trong `runs/v3_B_group_openrouter_20260729T213621199396.json`.
Kết quả evaluation:

- `total_cases`: 10
- `measured_cases`: 10
- `provider_error_cases`: 0
- `passed_cases`: 3
- `case_accuracy`: 0.3
- `tool_routing_accuracy`: 0.3
- `argument_accuracy`: 0.3
- `multiturn_accuracy`: 0.0
- `failure_counts`: {"wrong_tool": 6, "out_of_scope": 1}
- `observed_mismatch_counts`: {"missing_tool_call": 2, "wrong_arg_value": 4, "unexpected_tool_call": 1}

| Version | Prompt/tool change | Hypothesis | Metric name | Result | Run File |
|---|---|---|---:|---:|---|
| v0 | Baseline prompt và core tools. | Agent xử lý được yêu cầu research cơ bản. | `case_accuracy` | 0.3 | `runs/v3_B_group_openrouter_20260729T213621199396.json` |
| v1 | Thêm `evidence_judge`, đăng ký trong tool registry và `tools.yaml`. | Điểm số minh bạch giúp kết luận trend nhất quán hơn. | `tool_routing_accuracy` | 0.3 | `runs/v3_B_group_openrouter_20260729T213621199396.json` |
| v2 | Thêm `eval_group.json`: 10 case gồm 5 single-turn và 5 multi-turn. | Đo routing, đối số và khả năng giữ ngữ cảnh đa lượt. | `multiturn_accuracy` | 0.0 | `runs/v3_B_group_openrouter_20260729T213621199396.json` |

Lưu ý: kỹ thuật này đã cho thấy metrics nhưng còn một số tool execution error (ví dụ thiếu `TAVILY_API_KEY`, RapidAPI 403) nên cần sửa trước khi dùng các số liệu này để quyết định cuối cùng.

## B2. Failure analysis

Kết quả run đã cho thấy các lỗi chính sau:

- 6 case `wrong_tool`, 1 case `out_of_scope`.
- 2 trường hợp `missing_tool_call`.
- 4 trường hợp `wrong_arg_value`.
- 1 trường hợp `unexpected_tool_call`.

Các nguyên nhân quan sát được:

- Model gọi `clarify` khi test kỳ vọng thu thập evidence (ví dụ G01), dẫn đến routing mismatch.
- Một số case gọi `lookup` nhưng vẫn bị lỗi runtime do thiếu `TAVILY_API_KEY` trong môi trường, nên evidence không được tạo ra.
- Case multi-turn đôi khi thiếu bước `evidence_judge` sau khi thu thập thông tin.

Ví dụ cụ thể từ run:

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| G01_trend_hype_vs_reality | `wrong_tool` | `clarify` | Missing expected evidence calls (`lookup`, `social_search`, `papers`, `evidence_judge`) | Sửa prompt/rules để không hỏi lại nếu case đủ rõ ràng; điều chỉnh expected behavior nếu clarify hợp lệ. |
| G04_multi_turn_add_example | `wrong_tool` | `lookup(query='AI startup Vietnam', topic='news', timeframe='month', max_results=5)` | Wrong query phrasing and missing `social_search`/`evidence_judge`; web search also failed due missing API key | Cập nhật prompt để dùng chính xác query text; thiết lập `TAVILY_API_KEY` và rerun. |
| G05_request_summary | `wrong_tool` | `lookup`, `papers`, `social_search` | Missing expected `evidence_judge`; arg mismatch on query/timeframe | Thêm rule bắt buộc `evidence_judge` sau collection và chuẩn hóa timeframe. |

## B3. Team eval cases

`data/eval_group.json` có 10 case: 5 single-turn và 5 multi-turn, và đã được chạy trong `runs/v3_B_group_openrouter_20260729T213621199396.json`.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01 | Phân biệt Agentic RAG có evidence hay hype. | `lookup`, `social_search`, `papers`, `evidence_judge` | FAIL (`wrong_tool`) |
| G02 | Yêu cầu đầu tư quá rộng. | `clarify` trước khi tìm kiếm | PASS |
| G03 | Bài đăng từ tài khoản cụ thể. | `timeline(sama, 5)` | PASS |
| G04 | Giữ ngữ cảnh startup Việt qua hai lượt. | `lookup`, `social_search`, `evidence_judge` | FAIL (`wrong_tool`) |
| G05 | Tóm tắt trend AI agent trong ngữ cảnh vận hành. | `lookup`, `evidence_judge` | FAIL (`wrong_tool`) |
| G06 | Rủi ro AI-generated content cho startup truyền thông. | `lookup`, `social_search`, `evidence_judge` | FAIL (`wrong_tool`) |
| G07 | Thu hẹp chủ đề marketing sang Việt Nam/social media. | `lookup`, `social_search`, `evidence_judge` | FAIL (`wrong_tool`) |
| G08 | Câu hỏi suy đoán ngoài phạm vi research trend. | Không gọi tool | FAIL (`out_of_scope`) |
| G09 | Scope doanh nghiệp vừa và nhỏ chưa đủ rõ. | `clarify` | PASS |
| G10 | Đánh giá một URL cụ thể. | `fetch`, `evidence_judge` | FAIL (`wrong_tool`) |

## B4. Live chat evidence

| Scenario/Turn | Version | Tool Calls + Args | Transcript/Run | Outcome |
|---|---|---|---|---|
| `elon musk là ai` | v0 | Không gọi tool | `transcripts/v0_openrouter_20260729T123219.transcript.json` | Agent trả lời trực tiếp; đây chỉ là smoke test, không phải evidence cho khả năng research trend. |
| `abcd là gì` | v0 | `clarify(question=..., response_type="text")` | `transcripts/v0_openrouter_20260729T123500.transcript.json` | Agent chuyển sang trạng thái `waiting_for_user`, đúng boundary khi thiếu thông tin. |

## B5. Tool capability evidence

| Category | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Must-have: tool mới đầu tiên | `tools/evidence_judge/tool.py`, `tools/evidence_judge/TOOL.md` | Chấm bốn chiều và trả `scoring_method` để giải thích trọng số. | Chỉ đánh giá evidence đã có; reject số âm hoặc dữ liệu sai kiểu. |
| Optional built-in | `tools/timeline/tool.py`, `tools/social_search/tool.py` | Hỗ trợ truy vấn X/Twitter qua RapidAPI. | Cần `RAPIDAPI_KEY`; kết quả API lỗi phải được review, không coi là evidence. |
| Optional built-in | `tools/lookup/tool.py` | Tìm web bằng Tavily. | Cần `TAVILY_API_KEY`; không có key thì không được coi tool execution thành công. |

## B6. Reflection

- `system_prompt.md` phù hợp cho routing rule: hỏi rõ scope, lấy evidence trước khi kết luận, dùng `evidence_judge` sau thu thập dữ liệu và không bịa URL.
- `tools.yaml` phù hợp để nêu schema, kiểu đối số và mô tả ngắn cho model. `evidence_judge` đã được cập nhật mô tả về các score và phương pháp chấm có thể kiểm chứng.
- Lỗi provider, thiếu API key, quota hoặc `tool_results.error` cần review thủ công; routing PASS không đồng nghĩa tool đã chạy thành công.
- Bước tiếp theo là khôi phục quyền Gemini project hoặc dùng provider khả dụng, cấu hình Tavily để chạy đầy đủ group eval, sau đó lưu `runs/*.json` và cập nhật metric thật vào `version_log.csv` và B1–B3.

## B7. Latest run (auto-generated)

Run vừa thực hiện: `runs/v3_B_group_openrouter_20260729T213621199396.json` (generated_at: 2026-07-29T21:36:21).

Summary metrics (from run file):

- `total_cases`: 10
- `measured_cases`: 10
- `provider_error_cases`: 0
- `passed_cases`: 3
- `case_accuracy`: 0.3
- `tool_routing_accuracy`: 0.3
- `argument_accuracy`: 0.3
- `multiturn_accuracy`: 0.0
- `failure_counts`: {"wrong_tool": 6, "out_of_scope": 1}
- `observed_mismatch_counts`: {"missing_tool_call": 2, "wrong_arg_value": 4, "unexpected_tool_call": 1}

Notes:
- Metrics are available and were added to this report, but several tool executions returned runtime errors (e.g. missing `TAVILY_API_KEY`, RapidAPI 403). Those tool-level errors should be fixed and runs re-done to obtain fully trustworthy evidence.
- Per-case details are saved inside the run JSON; consider exporting `results` to CSV for further post-mortem.

