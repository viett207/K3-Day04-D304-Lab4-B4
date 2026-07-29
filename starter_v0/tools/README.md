# Tool Folder Contract

Each tool lives in its own folder:

```text
tools/<tool_name>/
  TOOL.md   # frontmatter + human notes
  tool.py   # self-contained implementation
```

`tools/__init__.py` is the registry. `agent.py`, `chat.py`, and `run_eval.py`
import `TOOL_FUNCTIONS` from that registry.

## Frontmatter Fields

Every `TOOL.md` uses the same fields:

```yaml
---
name: tool_name
track: core | bonus
kind: live_api | local_formatter | local_knowledge | action | control
provider: Provider name if any
requires_env: [ENV_VAR]
inputs: [arg_name]
outputs: [field_name]
side_effect: false | true | local_file_write
requires_confirmation: true   # only for write/action tools
---
```

Core tools are enough to pass the base lab. `track: bonus` means optional or
extension-only; it does not automatically earn bonus points. If its declaration
stays in `tools.yaml`, the model can still see it and core routing may change.

---

## Tool List

| Tool Name | Track | Kind | ENV Required | Description |
|-----------|-------|------|-------------|-------------|
| `clarify` | core | control | — | Hỏi lại user khi thiếu thông tin hoặc cần xác nhận (yes_no / text) |
| `timeline` | core | live_api | `RAPIDAPI_KEY` | Lấy tweet gần đây của một tài khoản theo handle |
| `social_search` | core | live_api | `RAPIDAPI_KEY` | Tìm tweet theo từ khóa (Latest hoặc Top) |
| `lookup` | core | live_api | `TAVILY_API_KEY` | Tìm kiếm web (news / general), hỗ trợ timeframe |
| `fetch` | core | live_api | — | Đọc nội dung HTML của một URL cụ thể |
| `format` | core | local_formatter | — | Trình bày danh sách items thành markdown digest |
| `send` | bonus | action | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | Gửi văn bản lên Telegram channel (cần xác nhận) |
| `policy` | bonus | local_knowledge | — | Tìm trong company policy markdown nội bộ |
| `papers` | bonus | live_api | — | Tìm paper trên arXiv theo từ khóa |
| `paper_text` | bonus | local_knowledge | — | Tải PDF arXiv và trích text theo số trang |
| `evidence_judge` | core | local_formatter | — | Nhận danh sách evidence và trả scores/verdict (tool mới của team) |

---

## Cách thêm tool mới

1. Tạo folder `tools/<tool_name>/`
2. Tạo `TOOL.md` với frontmatter đầy đủ
3. Tạo `tool.py` với hàm chính (phải return `dict[str, Any]`)
4. Thêm import và mapping vào `tools/__init__.py`:
   ```python
   from tools.<tool_name>.tool import <function_name>
   # Trong TOOL_FUNCTIONS dict:
   "<tool_name>": <function_name>,
   ```
5. Thêm declaration vào `artifacts/tools.yaml` với `name`, `description`, và `parameters`
6. Sync tên tool với `data/eval_base.json`, `data/eval_group.json`, và `artifacts/system_prompt.md`
7. Smoke-test: `python -c "from tools import TOOL_FUNCTIONS; print(TOOL_FUNCTIONS.keys())"`

> **Quan trọng**: Tên tool phải khớp chính xác giữa `tools.yaml`, `TOOL_FUNCTIONS`, và các file eval.
> Dùng `tools/_shared.py` cho code dùng chung (HTTP helpers, rate limiters, formatters).
