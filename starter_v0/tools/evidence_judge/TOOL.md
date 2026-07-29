# evidence_judge

## Mục đích

`evidence_judge` là tool mới của nhóm để đánh giá tổng hợp evidence thu thập được cho một xu hướng AI.

## Khi nào dùng

- Khi agent đã thu thập thông tin từ nhiều nguồn như web, social, paper.
- Khi cần một verdict cấu trúc: evidence, hype, adoption, risk.
- Khi user muốn biết liệu trend có thật sự đáng chú ý hay chỉ là hype.

## Input

- `topic`: chủ đề nghiên cứu.
- `positive_evidence`: danh sách chuỗi mô tả evidence tích cực.
- `negative_evidence`: danh sách chuỗi mô tả evidence tiêu cực hoặc rủi ro.
- `paper_count`: số bài báo/research liên quan.
- `real_world_examples`: số ví dụ thực tế / sản phẩm đã dùng.
- `hype_signals`: số tín hiệu hype / quảng cáo.

## Output

Tool trả về JSON với các trường:

- `topic`
- `scores`: `evidence_score`, `hype_score`, `adoption_score`, `risk_score`
- `verdict`: kết luận chung
- `summary`: tóm tắt bằng chữ
- `scoring_method`: trọng số được dùng để tính từng điểm, giúp kết quả kiểm chứng được
- `positive_evidence`, `negative_evidence`, `paper_count`, `real_world_examples`, `hype_signals`

## Lưu ý

Tool này không truy vấn web hay social. Nó chỉ đánh giá evidence đã được thu thập bằng các tool khác.

Các trường đếm phải là số nguyên không âm. Danh sách evidence chỉ nhận chuỗi không rỗng; dữ liệu không hợp lệ sẽ trả lỗi thay vì tạo điểm số sai lệch.
