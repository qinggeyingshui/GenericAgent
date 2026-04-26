# R28 | PC环境深度扫描

**日期**: 2025-07-11  
**类型**: 环境探测  
**状态**: 完成  

## 目标
全面扫描PC环境，生成 `environment_profile.md`（≥50条有效信息），为后续任务提供环境上下文。

## 方法
1. PowerShell 收集系统信息（OS/CPU/RAM/GPU/磁盘）
2. 注册表 + `Get-Package` 扫描已安装软件（395条）
3. 命令行探测关键工具版本（Python/Node/Java/Docker/Git/conda/uv等）
4. 文件系统扫描 E:\2026 项目结构 + D:/E: 盘关键目录
5. Edge 浏览器书签数据库读取（74条）
6. VS Code extensions 扫描（45个）
7. Conda 环境列表（8个）
8. Git 全局配置
9. PATH 环境变量分析（73条，7条异常）

## 关键发现

### 环境概况
- **系统**: Win10 Build 26200, Intel 13th Gen i7, 32GB RAM, Intel Iris Xe
- **存储**: C:200G(24G free⚠️), D:275G(31G free⚠️), E:800G(340G free)
- **Python**: 3.11(venv), 3.12(Anaconda), 3.13(standalone) 三版本并存
- **Node**: v20.12.2(NVM) + v18.20.2(standalone)
- **Java**: JDK 17
- **Docker**: 28.0.1
- **数据库**: MySQL 8.0, Neo4j, Redis

### 开发工具链
- **IDE**: VS Code(45扩展) + IntelliJ IDEA 2024.3.4 + Cursor
- **包管理**: Conda 24.9.2 + uv 0.6.17 + pip + Maven 3.8.1 + NVM + npm
- **8个conda环境**: base, aiWatch, antifraud, ctf, fodd, fs, kn_env, xiaozhi-esp32-server
- **Git**: user=qinggeyingshui, proxy=127.0.0.1:7890, credential=git.tongji.edu.cn

### 兴趣领域（从项目+书签推断）
- **AI/ML研究**: VQA, Graph ML(KDD/PANTHER), Topology pretraining, GenericAgent
- **IoT/嵌入式**: ESP32(xiaozhi-esp32, ESP32arduinocam), PlatformIO, ESP-IDF
- **CTF/安全**: Nmap, Wireshark, AntSword, 专用conda环境
- **教育系统**: 自动组卷, AI智课, 教务管理
- **硬件设计**: Verilog, CPU设计(cpu31/cpu54), MASM/TASM
- **Web开发**: Vue, webpack, 微信小程序

### 健康问题
| 问题 | 严重度 | 建议 |
|------|--------|------|
| C盘仅24GB/200GB (12%) | 🔴 HIGH | 清理临时文件、移动大型软件到E盘 |
| D盘仅31GB/275GB (11%) | 🔴 HIGH | 清理或迁移部分工具 |
| 7条PATH异常（断裂/失效/重复） | 🟡 MEDIUM | 清理无效PATH条目 |
| PATH重复条目（nvm×3, Nmap×2等） | 🟢 LOW | 去重优化 |

## 产出物
- `./autonomous_reports/environment_profile.md` — 104条结构化环境信息，20个分类

## 记忆更新建议（待用户审批）
建议向 `global_mem.txt` 写入以下环境事实：
```
[环境] Win10/i7-13th/32GB/IrisXe | C:200G D:275G E:800G(主工作盘)
[环境] Python: 3.11(venv)+3.12(conda)+3.13 | Node: v20(NVM) | JDK17 | Docker28
[环境] DB: MySQL8.0+Neo4j+Redis | IDE: VSCode+IDEA+Cursor
[环境] Git: qinggeyingshui | proxy: 127.0.0.1:7890 | 同济大学
[环境] Conda环境: aiWatch/antifraud/ctf/fodd/fs/kn_env/xiaozhi-esp32-server
[环境] 详细profile: temp/autonomous_reports/environment_profile.md
```