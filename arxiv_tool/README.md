# arxiv_tool: arxiv 论文搜索整理下载工具

## arxiv_tool 功能

- [x] 搜索论文
- [x] 单个链接直接下载论文
- [x] Markdown 文件(夹)自动识别链接并批量下载论文, 同步更新 Markdown 文件内容

## 使用方法

1. 搜索论文
```
arxiv_tool search <KEYWORDS> [<DIRECTORY>]
```
示例:
```
arxiv_tool search "Attention Is All You Need"
```

2. 单个链接下载论文
```
arxiv_tool fetch <ARXIV_URL> [<DIRECTORY>]
```
示例:
```
arxiv_tool fetch https://arxiv.org/abs/1706.03762
```

3. Markdown 文件(夹)下载论文

```
arxiv_tool markdown <MD_PATH_OR_DIR> [-d] [-p <DIRECTORY>]
```
示例:
```
arxiv_tool markdown ./mds/ -d -p ./pdfs/
```
