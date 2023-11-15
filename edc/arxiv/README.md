# arxiver: arxiv 论文下载工具

## arxiv 功能

- [x] 搜索论文
- [x] 单个链接下载论文
- [x] Markdown 文件(夹)自动识别链接并批量下载论文, 同步更新 Markdown 文件内容

## 使用方法

1. 搜索论文
```
arxiv search <KEYWORDS> [<DIRECTORY>]
```
示例:
```
arxiv search "Attention Is All You Need"
```

2. 单个链接下载论文
```
arxiv fetch <ARXIV_URL> [<DIRECTORY>]
```
示例:
```
arxiv fetch https://arxiv.org/abs/1706.03762
```

3. Markdown 文件(夹)下载论文

```
arxiv markdown <MD_PATH_OR_DIR> [<DIRECTORY>]
```
示例:
```
arxiver markdown ./tests/mds/test.md
```
