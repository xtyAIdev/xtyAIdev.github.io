<<<<<<< HEAD
# AI梦境档案馆 (AI Dream Journal)

一个全自动化的AI艺术项目，每天由AI创作独特的梦境并以文字和图像形式记录。

## 🌟 项目特色

- **完全自动化**: 无需人工干预，每日自动生成新内容
- **零运营成本**: 使用GitHub Pages和GitHub Actions免费服务
- **AI艺术创作**: 结合DeepSeek和通义千问AI模型
- **Git作为数据库**: 完整版本历史和内容追踪
- **响应式设计**: 支持所有设备访问

## 🛠️ 技术栈

- **自动化工作流**: GitHub Actions
- **核心脚本**: Python 3.10+
- **AI服务**: DeepSeek Chat, 通义千问
- **前端技术**: HTML5, CSS3, JavaScript
- **数据存储**: JSON文件 + Git版本控制
- **网站托管**: GitHub Pages

## 📁 项目结构

```
.
├── .github/workflows/main.yml    # GitHub Actions工作流
├── generate_dream.py             # 梦境生成主脚本
├── index.html                    # 主页 - 显示最新梦境
├── archive.html                  # 档案馆 - 所有梦境记录
├── about.html                    # 关于页面
├── main.js                       # 主页JavaScript
├── archive.js                    # 档案馆JavaScript
├── styles.css                    # 样式文件
├── data/dreams.json              # 梦境数据文件
├── assets/images/                # 梦境图像存储
├── .env                          # API密钥配置
└── README.md                     # 项目说明
```

## ⚙️ 安装和配置

### 1. 克隆仓库
```bash
git clone <your-repo-url>
cd ai-dream-archive
```

### 2. 配置API密钥
在GitHub仓库的Settings > Secrets and variables > Actions中添加以下Secrets:
- `DEEPSEEK_API_KEY`: DeepSeek API密钥
- `TONGYI_API_KEY`: 通义千问API密钥

### 3. 本地测试
```bash
# 安装依赖
pip install requests pillow

# 设置环境变量
export DEEPSEEK_API_KEY="your-deepseek-key"
export TONGYI_API_KEY="your-tongyi-key"

# 运行生成脚本
python generate_dream.py
```

## 🔧 工作流程

1. **每日定时触发**: GitHub Actions每天UTC时间00:01自动运行
2. **获取种子词汇**: 从维基百科获取随机文章标题作为创作灵感
3. **生成梦境文本**: 使用DeepSeek AI创作超现实梦境描述
4. **创建图像提示**: 将文本转化为适合图像生成的英文提示词
5. **生成梦境图像**: 使用通义千问生成对应的梦境图像
6. **更新数据文件**: 将新内容添加到JSON数据文件中
7. **自动提交**: 将更改提交回GitHub仓库
8. **自动部署**: GitHub Pages检测到更改后自动重新部署网站

## 🌐 网站功能

### 主页 (index.html)
- 显示最新生成的梦境
- 包含梦境图像、文本描述和种子词汇
- 响应式设计，支持移动设备

### 档案馆 (archive.html)
- 以网格画廊形式展示所有历史梦境
- 支持搜索和浏览功能
- 每张卡片显示日期、预览文本和种子词汇

### 关于页面 (about.html)
- 项目介绍和技术说明
- 作者信息和GitHub链接

## 📊 数据格式

每个梦境记录包含以下字段：
```json
{
  "date": "2025-08-22",
  "seeds": ["dream", "fantasy", "memory"],
  "text": "梦境描述文本...",
  "image_prompt": "英文图像生成提示词",
  "image_path": "assets/images/2025-08-22.png"
}
```

## 🚀 部署

1. 将代码推送到GitHub仓库
2. 在仓库设置中启用GitHub Pages
3. 配置API密钥到GitHub Secrets
4. 工作流将自动运行并部署网站

## 📝 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📞 联系

如有问题或建议，请通过GitHub Issues联系。

---

*由AI每日自动生成 · 零成本自动化项目*
