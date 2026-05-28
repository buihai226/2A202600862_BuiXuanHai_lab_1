# Báo cáo lab 1

## 1) Tổng quan phần đã hoàn thành

* Hoàn thiện 4 hàm bắt buộc: `call_openai`, `call_openai_mini`, `compare_models`, `streaming_chatbot`.
* Hoàn thiện 3 hàm bonus: `retry_with_backoff`, `batch_compare`, `format_comparison_table`.
* Tạo file `solution/solution.py` theo đúng yêu cầu nộp bài.
* Tạo file `.env` và thêm đoạn đọc `.env` trong `template.py` để tự động lấy `OPENAI_API_KEY` khi chạy thủ công.
* Điền trả lời Phần 2 trong `solution/exercises.md` dựa trên kết quả `response_AI.md`.

## 2) Chi tiết từng phần

* call_openai: gọi OpenAI Chat Completions, đo thời gian bằng `time.perf_counter`, trả về `(text, latency)`.
* call_openai_mini: gọi lại `call_openai` với model `gpt-4o-mini`.
* compare_models: gọi cả 2 model, trả dict theo spec, ước tính chi phí theo công thức word/0.75 -> token.
* streaming_chatbot: chat streaming, in từng token, lưu lịch sử 3 lượt gần nhất.
* retry_with_backoff: retry tối đa 3 lần, delay theo cấp số nhân (0.1s, 0.2s, 0.4s).
* batch_compare: chạy `compare_models` cho danh sách prompt.
* format_comparison_table: tạo bảng text, cắt ngắn nội dung dài tới 40 ký tự.
* Đọc `.env`: tự động nạp `OPENAI_API_KEY` nếu có, không cần `python-dotenv`.

## 3) Số liệu từ Phần 2 (Bài tập mở rộng)

* Temperature đã thử: 0.0, 0.5, 1.0, 1.5.
* Nhận xét: temperature cao tạo output đa dạng nội dung hơn (0.5 chuyển sang Vịnh Hạ Long), temperature thấp ổn định hơn (0.0, 1.0, 1.5 tập trung Hang Sơn Đoòng).
* Đề xuất cho CS chatbot: temperature 0.2-0.4 để giữ nhất quán và giảm sai lệch.
* Tỉ lệ chi phí GPT-4o vs mini: 0.010 / 0.0006 = 16.7x (xấp xỉ 16-17 lần).
* Ví dụ cho GPT-4o: tư vấn pháp lý/kỹ thuật cần giải thích chính xác và đầy đủ.
* Ví dụ cho mini: FAQ, hướng dẫn cơ bản, tóm tắt đơn giản.

## 4) Danh sách file liên quan

* `template.py`: code chính, thêm đọc `.env`, các hàm đã hoàn thiện.
* `solution/solution.py`: bản sao nộp bài.
* `solution/exercises.md`: 
* `.env`: chứa `OPENAI_API_KEY`.
* `requirements.txt`: giữ nguyên theo yêu cầu.

## 5) Hướng dẫn chạy/test

```bash
conda activate lab1
pip install -r requirements.txt
pytest tests/ -v
```

Chạy thủ công:

```bash
python template.py
# hoặc
python solution/solution.py
```

## 6) Vấn đề gặp và cách xử lý

* Lỗi thiếu `OPENAI_API_KEY`: đã xử lý bằng cách đọc từ file `.env`.
* Push GitHub bị fail do xác thực: cần dùng PAT hoặc SSH (đã push thành công sau khi xác thực).

## 7) Kết quả test

* Đã chạy `pytest tests/ -v`: 19/19 tests pass.
