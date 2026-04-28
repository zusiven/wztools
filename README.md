# wztools

个人用 Python 工具库

## 模块

- **utils** - 通用工具函数
  - `run_cmd` - 执行命令行命令并实时返回结果
  - `logger` / `get_logger` - 日志配置（Rich 终端输出）
  - `get_loguru` - loguru 日志（按需使用，需额外安装 loguru）
  - `load_toml` - 读取 TOML 配置文件
  - `error_info` - 错误信息提取
  - `measure_time` / `format_time` - 时间相关工具
  - `set_datetime_double_xaxis` - matplotlib 双 x 轴时间格式
  - `fetch_nearest_point` - 空间最近点查询

- **datalake** - 本地数据存储管理
  - 按时间组织数据文件
  - 支持日、月、年维度创建和获取数据

## 变更记录

- [v2026.04.28]
  - command.py stdout 日志级别改为 warning
  - 添加 command.py 测试

- [v2026.04.10]
  - datalake warning 信息优化

- [v2025.12.01]
  - 增加 datalake 模块

- [v2025.10.29]
  - 添加 load_toml
