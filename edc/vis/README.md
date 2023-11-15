
# cv_utils

## 图像读取、保存、显示

支持 str/Path 形式的图像文件路径


## 常见视觉任务可视化

- 2d 框
- 关键点
- 文本、文本表格


## 交互式显示图像流

相比于普通的循环显示图像流，只需修改几行代码，即可实现对图像流的交互式显示（空格：暂停/继续，左/右键：上/下一帧，Esc键：退出）

- demo1（循环显示）
```Python
img_paths = sorted(Path(img_dir).iterdir())
for frame_idx, img_path in enumerate(img_paths):
    img = cv.imread(img_path)

    cv.put_text(img, (0, 0), f'Frame: {frame_idx}', cv.Font.M, cv.Color.Red, bg_alpha=1, bg_color=cv.Color.White)
    cv.imshow(img, wait_ms=100)
```

- demo2（交互式显示）
```Python
with cv.ImageFlow(img_dir, save_path='video.mp4') as img_flow:
    for frame_idx, img_path in img_flow:
        img = cv.imread(img_path)

        cv.put_text(img, (0, 0), f'Frame: {frame_idx}', cv.Font.M, cv.Color.Red, bg_alpha=1, bg_color=cv.Color.White)
        img_flow.imshow(frame_idx, img)
```