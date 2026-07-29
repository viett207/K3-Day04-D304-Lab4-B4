## Ý tưởng đề xuất số 1: **AI Trend Detective**

> Một “thám tử AI” điều tra xem một công nghệ đang thật sự bùng nổ hay chỉ là hype.

### Ví dụ người dùng hỏi

> “Agentic RAG có thật sự đáng làm cho đồ án tốt nghiệp không, hay chỉ đang được quảng cáo quá mức?”

Agent sẽ:

1. Tìm thông tin tổng quan trên web.
2. Tìm bài đăng gần đây trên mạng xã hội.
3. Tìm bài nghiên cứu liên quan.
4. Phân tích mức độ đồng thuận và mâu thuẫn.
5. Chấm điểm:

   * **Hype Score**
   * **Research Evidence Score**
   * **Industry Adoption Score**
   * **Risk Score**
6. Đưa ra kết luận:

```text
VERDICT: PROMISING BUT OVERHYPED

Hype Score: 86/100
Research Evidence: 64/100
Industry Adoption: 71/100
Risk: 58/100
```

## Vì sao ý tưởng này dễ nhưng cực kỳ ấn tượng?

Bạn tận dụng gần như toàn bộ tool có sẵn:

* `lookup`: tìm web.
* `social_search`: tìm thảo luận xã hội.
* `timeline`: xem quan điểm của một tài khoản.
* `fetch`: đọc bài cụ thể.
* `papers`: tìm nghiên cứu.
* `format`: tạo báo cáo.

Bạn chỉ cần viết thêm **một tool mới rất dễ**:

```text
trend_verdict
```

Tool này không cần API mới. Nó chỉ nhận dữ liệu đã thu thập và tính điểm theo công thức đơn giản.

Ví dụ input:

```json
{
  "web_evidence_count": 8,
  "paper_count": 5,
  "positive_social_posts": 14,
  "negative_social_posts": 6,
  "real_product_examples": 4
}
```

Output:

```json
{
  "hype_score": 78,
  "evidence_score": 72,
  "adoption_score": 65,
  "risk_score": 41,
  "verdict": "Promising but still overhyped"
}
```

Không cần xây ML, không cần train model, không cần database phức tạp.

---

# Điểm “ảo ma” nhất: **Evidence Battle Mode**

UI chia màn hình thành hai nhân vật:

### 🔵 AI Optimist

Tìm bằng chứng chứng minh công nghệ rất tiềm năng.

### 🔴 AI Skeptic

Tìm bằng chứng phản biện, rủi ro, hạn chế và dấu hiệu hype.

Sau đó một agent thứ ba:

### ⚖️ AI Judge

Tổng hợp bằng chứng và đưa ra phán quyết cuối cùng.

Thực tế phía dưới bạn vẫn có thể dùng **một agent loop duy nhất**, chỉ thay đổi cách trình bày kết quả. Không cần xây multi-agent thật.

UI hiển thị:

```text
┌────────────────────┬────────────────────┐
│ AI OPTIMIST        │ AI SKEPTIC         │
│                    │                    │
│ ✓ Nhiều paper mới  │ ⚠ Ít ứng dụng thật │
│ ✓ Community mạnh   │ ⚠ Benchmark yếu    │
│ ✓ Startup đầu tư   │ ⚠ Chi phí cao      │
└────────────────────┴────────────────────┘

             ⚖️ FINAL VERDICT
       “Promising, but not mature yet”
```

Cảm giác rất “multi-agent debate”, nhưng code vẫn đơn giản.

---

# Tool mới đề xuất

## `evidence_judge`

### Chức năng

Nhận danh sách evidence, phân loại và tính verdict.

### Schema đơn giản

```yaml
name: evidence_judge
description: >
  Use this tool only after collecting multiple pieces of evidence
  from web, social media or research papers. It scores evidence
  strength, detects conflicting claims and returns a final verdict.

parameters:
  topic:
    type: string
  positive_evidence:
    type: array
    items:
      type: string
  negative_evidence:
    type: array
    items:
      type: string
  paper_count:
    type: integer
    default: 0
  real_world_examples:
    type: integer
    default: 0
```

### Logic

```python
def evidence_judge(
    topic,
    positive_evidence,
    negative_evidence,
    paper_count=0,
    real_world_examples=0
):
    positive = len(positive_evidence)
    negative = len(negative_evidence)

    evidence_score = min(
        100,
        paper_count * 12 +
        real_world_examples * 10 +
        positive * 4
    )

    hype_score = min(
        100,
        max(0, positive * 8 - paper_count * 5 - real_world_examples * 6)
    )

    risk_score = min(100, negative * 12)

    if evidence_score >= 75 and risk_score < 50:
        verdict = "Strong Opportunity"
    elif evidence_score >= 50:
        verdict = "Promising but Uncertain"
    else:
        verdict = "Mostly Hype"

    return {
        "topic": topic,
        "evidence_score": evidence_score,
        "hype_score": hype_score,
        "risk_score": risk_score,
        "verdict": verdict
    }
```

Tool mới chỉ khoảng 30–50 dòng code nhưng demo rất có chiều sâu.

---

# Kịch bản demo xuất sắc nhất

## Câu hỏi demo chính

> “Điều tra xem AI Agent có thực sự thay thế được workflow truyền thống trong năm 2026 không.”

## Luồng demo

### V0 — Agent ngây thơ

Agent chỉ gọi `lookup`, lấy vài bài rồi kết luận ngay.

Sai ở:

* Chỉ dùng một nguồn.
* Không tìm paper.
* Không kiểm tra mạng xã hội.
* Không phân tích evidence đối lập.
* Kết luận quá tự tin.

### V1 — Sửa routing

Thêm rule:

```text
For trend validation, collect evidence from at least two source types.
```

Agent gọi:

```text
lookup → social_search
```

### V2 — Sửa evidence quality

Thêm rule:

```text
For technical or scientific claims, search for research papers before concluding.
```

Agent gọi:

```text
lookup → social_search → papers
```

### V3 — Thêm phán quyết có cấu trúc

Agent gọi:

```text
lookup
→ social_search
→ papers
→ evidence_judge
→ format
```

---

# Cải thiện để sát với bài lab

## Điều cần làm để đáp ứng đúng yêu cầu lab

1. Chắc chắn có ít nhất 5 tool trong `artifacts/tools.yaml`.
2. Thêm ít nhất 1 tool mới do nhóm tự viết và khai báo trong:
   - `tools/<tool_name>/TOOL.md`
   - `tools/__init__.py`
   - `artifacts/tools.yaml`
3. Xây `data/eval_group.json` đúng 10 case của nhóm:
   - 5 single-turn
   - 5 multi-turn
   - Mỗi case có `phase: "B"`, `failure_type`, `expect`, `metadata.what_it_tests`
4. Chạy baseline `v0`, rồi tối ưu ít nhất 3 vòng `v1`, `v2`, `v3`.
5. Ghi `artifacts/version_log.csv` mỗi vòng với lý do, giả thuyết và metric trước/sau.
6. Có UI chạy được, tốt nhất là Streamlit với entrypoint `app.py`.
7. Viết `artifacts/REPORT.md` dựa trên log thật và giải thích cải tiến.

## Cách làm cụ thể cho `AI Trend Detective`

### Mission statement

**AI Trend Detective giúp người dùng đánh giá xem một xu hướng AI có thực sự đáng đầu tư hay chỉ là hype, bằng cách thu thập thông tin từ web, social media và research paper, rồi tổng hợp verdict có cấu trúc.**

### Dòng công việc agent nên theo

1. Nếu user hỏi không rõ topic, hãy gọi `clarify`.
2. Dùng `lookup` để thu thập thông tin web.
3. Dùng `social_search` và `timeline` để tìm diễn đàn và quan điểm gần đây.
4. Dùng `papers` để kiểm tra bằng chứng nghiên cứu.
5. Dùng tool mới `evidence_judge` / `trend_verdict` để chấm điểm và kết luận.
6. Dùng `format` để xuất markdown report.

### Tool thiết kế phù hợp lab

- `clarify`: hỏi bổ sung thông tin hoặc xác nhận boundary.
- `lookup`: tìm nội dung web chung.
- `social_search`: tìm thảo luận mạng xã hội.
- `timeline`: lấy bài đăng mới của tài khoản quan trọng.
- `papers`: tìm paper liên quan.
- `format`: tạo báo cáo markdown.
- Tool mới: `evidence_judge` hoặc `trend_verdict`.

### Ví dụ tool mới trong lab

`evidence_judge` có thể nhận:
- `topic`
- `positive_evidence`
- `negative_evidence`
- `paper_count`
- `real_world_examples`

Và trả về:
- `evidence_score`
- `hype_score`
- `risk_score`
- `verdict`

### Sát lab hơn ở UI

UI cần hiển thị ít nhất:
- request và response cuối cùng
- trace của từng tool: tên, args, status, kết quả
- `artifact_version` và version agent đang chạy
- transcript hoặc run JSON

Streamlit là lựa chọn tốt, nhưng nếu dùng framework khác vẫn phải thể hiện đủ contract tương đương.

## Đề xuất versioning cho lab

- `v0`: baseline đơn giản, chỉ dùng `lookup` và kết luận thô.
- `v1`: cải thiện routing, thêm social evidence (social_search/timeline).
- `v2`: thêm yếu tố nghiên cứu, gọi `papers` trước khi kết luận.
- `v3`: thêm tool verdict có cấu trúc (`evidence_judge`) và báo cáo markdown.

## Đề xuất case eval nhóm

1. Single-turn rõ ràng: “Trend LLM agent năm 2026 có nên dùng cho doanh nghiệp nhỏ không?”
2. Single-turn cần boundary: “AI RAG có phù hợp với ngân hàng không?”
3. Single-turn cần tổng hợp evidence: “Xu hướng autoML hiện tại có thật sự đang tăng trưởng không?”
4. Multi-turn thiếu info: hỏi `clarify` làm rõ scope.
5. Multi-turn đối lập: user muốn biết “lợi ích và rủi ro” của cùng một trend.

---

# Kết luận

Ý tưởng `AI Trend Detective` rất phù hợp với lab. Chỉ cần làm rõ workflow, bổ sung checklist lab vào kế hoạch, và triển khai tool mới + eval case đúng chuẩn là đủ để sát yêu cầu.
Sau đó UI cho thấy metric tăng dần:

```text
Version     Routing    Args    Multiturn    Overall
v0           55%       60%       50%         55%
v1           72%       70%       65%         69%
v2           88%       82%       78%         83%
v3           96%       94%       92%         94%
```

Đây chính là thứ giảng viên muốn thấy: cùng một scenario được chạy qua nhiều version để chứng minh agent cải thiện bằng evidence, không chỉ nói bằng cảm giác. 

---

# Tên sản phẩm thật “wow”

Tên khuyến nghị:

## **HypeLens AI**

Slogan:

> **See beyond the hype. Decide with evidence.**

Tên tiếng Việt khi thuyết trình:

> **Kính soi xu hướng AI – phân biệt đột phá thật và hiệu ứng truyền thông.**

Một số tên khác:

* **Trend Detective**
* **RealityCheck AI**
* **Hype or Hope**
* **SignalX**
* **TruthScope**
* **Evidence Arena**

Trong đó **HypeLens AI** là đẹp, dễ làm logo và dễ trình bày nhất.

---

# Giao diện Streamlit nên làm

## Sidebar

```text
HypeLens AI

Research Mode:
○ Quick Scan
● Deep Investigation
○ Evidence Battle

Agent Version:
v0 / v1 / v2 / v3
```

## Khu vực chính

### 1. User Question

```text
Is Agentic RAG truly useful or mostly hype?
```

### 2. Investigation Pipeline

```text
🌐 Web Search
      ↓
💬 Social Signals
      ↓
📄 Research Papers
      ↓
⚖️ Evidence Judge
      ↓
📊 Final Report
```

### 3. Score cards

```text
HYPE         EVIDENCE        ADOPTION         RISK
82/100        68/100          59/100          46/100
```

### 4. Evidence Battle

```text
Evidence For                  Evidence Against
✓ Có nhiều framework mới     ⚠ Benchmark chưa thống nhất
✓ Nhiều paper năm gần đây    ⚠ Chi phí inference cao
✓ Có ứng dụng thực tế        ⚠ Khó kiểm soát hallucination
```

### 5. Tool Trace

```text
Round 1
Tool: lookup
Args: {"query": "Agentic RAG adoption"}
Status: Success

Round 2
Tool: papers
Args: {"query": "Agentic retrieval augmented generation"}
Status: Success

Round 3
Tool: evidence_judge
Status: Success
```

UI lab bắt buộc phải thể hiện request, response, tool name, arguments, result/error và version đang chạy. 

---

# 10 eval case có thể dùng

## 5 single-turn

### Case 1 — Phải research đa nguồn

```text
“Is AI coding agent a real productivity breakthrough or mostly hype?”
```

Expected:

```text
lookup → social_search → papers → evidence_judge
```

### Case 2 — Chỉ hỏi thông tin đơn giản

```text
“What is Agentic RAG?”
```

Expected:

```text
lookup
```

Không được gọi `evidence_judge`.

### Case 3 — Thiếu topic

```text
“Check whether it is overhyped.”
```

Expected:

```text
clarify
```

### Case 4 — Yêu cầu đọc URL cụ thể

```text
“Read this article and assess its claims: <URL>”
```

Expected:

```text
fetch → evidence_judge
```

### Case 5 — Ngoài phạm vi

```text
“Write Python code to build a game.”
```

Expected:

```text
no_tool
```

## 5 multi-turn

### Case 6 — Bổ sung topic ở lượt sau

```text
User: “Check whether this technology is hype.”
Assistant: asks what technology.
User: “AI agents for software development.”
```

Expected:

```text
lookup → social_search → papers
```

### Case 7 — Chưa đủ evidence

```text
User: “Judge Agentic RAG.”
Assistant: asks whether user wants quick or deep analysis.
User: “Deep, include papers.”
```

Expected:

```text
lookup → papers → evidence_judge
```

### Case 8 — Chỉ format dữ liệu có sẵn

User cung cấp sẵn 5 evidence và yêu cầu tạo digest.

Expected:

```text
format
```

Không gọi search.

### Case 9 — Yêu cầu gửi kết quả

```text
User: “Research AI agents.”
Assistant: returns report.
User: “Send it to Telegram.”
```

Expected:

```text
clarify(response_type="yes_no")
```

### Case 10 — Xác nhận gửi

```text
User: “Send the report.”
Assistant: asks confirmation.
User: “Yes, send it.”
```

Expected:

```text
send
```

---

# Cách nói khi demo

HypeLens AI là một research agent giúp người dùng phân biệt giữa một xu hướng công nghệ thực sự có giá trị và một xu hướng chỉ đang được truyền thông thổi phồng.

Thay vì chỉ tìm kiếm một vài bài viết rồi đưa ra kết luận, agent thu thập bằng chứng từ nhiều nguồn khác nhau như website, mạng xã hội và bài nghiên cứu. Sau đó, hệ thống chia bằng chứng thành hai phía: bằng chứng ủng hộ và bằng chứng phản biện.

Tool mới của nhóm, Evidence Judge, sẽ đánh giá độ mạnh của bằng chứng, mức độ ứng dụng thực tế, rủi ro và mức độ hype. Kết quả cuối cùng được thể hiện dưới dạng các chỉ số trực quan và một phán quyết rõ ràng như “Strong Opportunity”, “Promising but Uncertain” hoặc “Mostly Hype”.

Điểm đặc biệt của hệ thống không chỉ nằm ở câu trả lời cuối cùng, mà còn ở khả năng hiển thị toàn bộ quá trình suy luận bằng tool trace. Người dùng có thể thấy agent đã chọn tool nào, truyền arguments gì, nhận kết quả ra sao và phiên bản prompt nào đang được sử dụng.

Qua các phiên bản từ v0 đến v3, nhóm tập trung sửa từng lỗi routing cụ thể và đo lại bằng eval thay vì tối ưu theo cảm giác. Điều này giúp chứng minh rằng chất lượng của agent được cải thiện bằng dữ liệu và log thực tế.

---

# Kết luận

**Chốt làm: HypeLens AI – AI Trend Detective.**

Nó hội tụ đủ:

* Dễ code.
* Không cần huấn luyện model.
* Tool mới đơn giản.
* Tận dụng được tool có sẵn.
* Có câu chuyện demo rõ ràng.
* Có UI nhiều điểm nhấn.
* Dễ viết 10 eval case.
* Rất thuận lợi để chứng minh v0 → v3.
* Nhìn giống hệ thống multi-agent cao cấp dù implementation không phức tạp.

Quan trọng nhất: đừng cố thêm quá nhiều chức năng. Hãy làm **một câu hỏi điều tra thật mượt**, trace thật đẹp, và màn hình so sánh v0 với v3 thật rõ. Lab cũng khuyến nghị chuẩn bị 3–5 scenario cụ thể và dùng cùng một scenario xuyên suốt các version để thể hiện sự cải thiện. 
