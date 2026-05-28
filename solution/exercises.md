# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Em thấy khi temperature tăng, phản hồi có xu hướng đa dạng hơn về nội dung: ở 0.0 và 1.0/1.5 đều xoay quanh Hang Son Doong nhưng chi tiết thay đổi, còn 0.5 chuyển sang Vinh Ha Long. Do đó, temperature cao làm output bớt “cố định” theo một ý, mở rộng ý tưởng và nội dung, trong khi temperature thấp thì ổn định và ít biến thể, sáng tạo hơn. Ở ví dụ này, các response đều có độ dài và cấu trúc tương đối đầy đủ, nhưng thông tin được cung cấp có biến động.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Em sẽ đặt temperature khoảng 0.2-0.4 vì chatbot hỗ trợ khách hàng cần có sự nhất quán và chính xác, không được lan man khiến chủ đề cuộc hội thoại bị ảnh hưởng nên để temperature thấp sẽ giữ dc sự ổn định và giảm thiểu sự sai lệch khi cung cấp thông tin, vẫn giữ được sự tự nhiên khi diễn đạt.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Em tính theo giá output: GPT-4o $0.010/1K token, mini $0.0006/1K token. Tỉ lệ chi phí = 0.010 / 0.0006 ≈ 16.7 lần, nên GPT-4o đắt hơn khoảng 16–17 lần cho cùng workload (số token giống nhau).

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> Em thấy GPT-4o xứng đáng khi cần chất lượng lập luận cao, nhiều ràng buộc hoặc xử lý ngôn ngữ phức tạp (ví dụ: tư vấn pháp lý/kỹ thuật cần giải thích chính xác và đầy đủ). GPT-4o-mini phù hợp cho các tác vụ thường ngày, trả lời nhanh, ngắn gọn hoặc không quá nhạy cảm về sai số (ví dụ: FAQ, trả lời hướng dẫn cơ bản, tóm tắt đơn giản).

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Em thấy streaming quan trọng nhất khi người dùng cần cảm giác phản hồi nhanh và muốn theo dõi quá trình tạo trả lời (ví dụ: chat tư vấn trực tiếp, giải thích dài, hỗ trợ kỹ thuật), vì nó giảm độ trễ cảm nhận và tăng trải nghiệm tương tác. Non-streaming phù hợp hơn khi cần kết quả hoàn chỉnh một lần, hoặc cần post-process/trích xuất có cấu trúc (ví dụ: trả về JSON, báo cáo tổng hợp, tạo file), vì lúc này việc chờ phản hồi trọn vẹn giúp giảm lỗi định dạng và dễ xử lý.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
