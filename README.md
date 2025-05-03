# Cách chạy

```bash
py othello.py <black_engine> <white_engine> [options]
```
## Tham số bắt buộc:

<black_engine>: Tên engine cho quân đen (human, minimax, alpha)

<white_engine>: Tên engine cho quân trắng (human, minimax, alpha)

## Tùy chọn thêm:

| Tham số     | Mô tả |
|-------------|------|
| `-aB`       | Bật Alpha-Beta Pruning cho người chơi đen |
| `-aW`       | Bật Alpha-Beta Pruning cho người chơi trắng |
| `-t <int>`  | Giới hạn thời gian mỗi lượt chơi (giây). Mặc định: `300` |
| `-v`        | Hiển thị bàn cờ sau mỗi lượt |
| `-lB <int>` | Độ sâu thuật toán của người chơi đen. Mặc định: `4` |
| `-lW <int>` | Độ sâu thuật toán của người chơi trắng. Mặc định: `4` |
| `-dup <int>`| Số lần lặp lại khi chạy chương trình. Với lựa chọn này thì -v sẽ không còn tác dụng|
