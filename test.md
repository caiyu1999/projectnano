# Matplotlib 网站爬虫使用说明

## 功能特点

这个爬虫脚本可以爬取 matplotlib 官方网站的内容，包括：

- 页面标题和主要内容
- 代码示例
- 图片链接
- 页面中的所有链接

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 直接运行脚本
```bash
python crawl.py
```

### 2. 自定义爬取URL
修改 `crawl.py` 文件中的 `target_url` 变量：

```python
target_url = "https://matplotlib.org/stable/gallery/lines_bars_and_markers/axline.html"
```

### 3. 在代码中使用
```python
from crawl import MatplotlibCrawler

crawler = MatplotlibCrawler()
result = crawler.crawl_page("https://your-target-url.com")
```

## 输出文件

运行脚本后会生成两个文件：

1. **matplotlib_axline_data.json** - 完整的结构化数据
2. **matplotlib_axline_content.txt** - 纯文本格式的内容

## 注意事项

- 请遵守网站的robots.txt规则
- 不要过于频繁地请求，建议在请求之间添加延时
- 某些网站可能有反爬虫机制，需要调整请求头或使用代理

## 扩展功能

可以根据需要扩展以下功能：

- 批量爬取多个页面
- 下载图片文件
- 保存为其他格式（CSV、Excel等）
- 添加数据库存储
- 实现增量爬取
