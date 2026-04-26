# [Self-Improvement Log]
该文件旨在实现自我进化，记录模型在执行任务时的错误、用户的纠正、成功的路径及用户偏好，确保在跨会话中持续学习。

## 0. 抽象规律 (Meta Patterns)
| 规律 | 触发条件 | 正确做法 |
| :--- | :--- | :--- |
| 禁止重复错误 | 连续失败≥2次 | 分析错误→改参数/方法→切换方案 |
| 多方案必决策 | 存在多个库/工具/路径 | 先搜索对比，禁凭印象选择 |
| 工具调用必验证 | 调用新工具/API前 | 读源码确认参数和返回值，验证可用性 |
| Spawn子进程用venv | 后台运行Python时 | 用.venv/Scripts/python.exe |
| file_patch禁全文 | 修改文件时 | >30行用code_run；截断内容禁作old_content |
| file_write必带标签 | 使用file_write时 | 必须<file_content>标签；程序化内容用code_run |
| code_run必有代码 | 使用code_run时 | 必须提供代码块或script参数 |
| subprocess参数独立 | 构造命令行时 | 每参数独立，错:`['/PID 480']` 对:`['/PID','480']` |
| f-string引号规则 | 生成f-string代码时 | {}内禁反斜杠，外单内双或反之 |
| 批量操作必验证 | 批量删除/修改后 | 重新查询验证实际影响数量 |
| helper模块函数必验证 | 调用helper.py函数前 | 先file_read helper.py确认函数存在 |
| SOP示例代码必验证 | 执行SOP中的import/API调用示例前 | 先file_read目标模块确认存在，SOP示例可能过时或错误 |
| file_patch前必读 | 使用file_patch修改文件前 | 必须先file_read确认精确内容，禁止凭印象构造old_content |
| helper函数参数签名必验证 | 调用helper.py中的函数前（尤其是complete_task/get_todo等） | file_read helper.py确认完整签名(参数名+类型)，禁凭印象假设参数名；历史教训：task_id/tasktitle都是错的，正确是taskname |
| 新建SOP必含skill_mapping | 创建新SOP文件时 | 末尾添加[skill_mapping]标签(category/skill/tools)，否则skill_tree无法更新 |

## 1. 错误与纠正 (Errors & Corrections)
| 日期 | 错误描述 | 用户的纠正/正确方案 |
| :--- | :--- | :--- |
| 2026-04-01 | web2md.py/simphtml.py 路径及导入错误 | 物理路径位于 ../，导入前需 sys.path.append(os.path.dirname(os.getcwd()))。应优先 read 源码确认 export 名称。 |
| 2026-04-19 | requests.get()访问特定网站返回403 Forbidden（如wsj.com/ft.com等），服务器拒绝Python默认User-Agent。 | **解决方案**：添加浏览器User-Agent header。示例：`headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}`，`requests.get(url, headers=headers)` |
| 2026-04-21 | file_read 使用 Windows 绝对路径（如 `E:\2026\...\file.py`）调用失败，返回错误内容（temp/ 目录列表而非文件内容）。 | **解决方案**：优先使用相对路径（如 `../memory/file.py`），从当前工作目录（cwd）出发。**预防措施**：①所有文件操作优先使用相对路径；②file_read 失败时立即切换为相对路径重试 |
| 2026-04-21 | Reflection触发机制误触发严重：触发条件过于宽松（ga.py:519只检查content是否包含['error','exception','traceback','failed']关键词），无法区分真实错误和正常内容。 | **解决方案**：①改进ga.py触发条件：检查status=="error"或exit_code!=0，排除file_read的"File not found"（带"Did you mean"的是正常查找失败）；②在reflection_helper.py添加错误验证；③添加冷却机制：5分钟内不重复触发 |
| 2026-04-21 | Python进程不会自动重新加载修改后的源代码。递归保护添加后旧进程仍触发新reflection。 | **正确理解**：①代码修复只对**新启动的进程**生效；②旧进程会自然完成或失败；③不需要强制kill旧进程。**预防措施**：关键保护机制必须在第一次部署时就正确实现 |
| 2026-04-21 | R201任务创建content_workflow.py时，假设ai_copywriter.py有AICopywriter类，导致`ImportError: cannot import name 'AICopywriter'`。实际该工具是函数式接口（4个generate_*函数）。 | **失败类型**：使用方式错误（接口假设错误）。**解决方案**：①集成前必须读取源码验证接口类型；②用正则`^class\s+`和`^def\s+`统计；③函数式工具直接导入函数，类式工具需实例化。**验证结果**：ai_copywriter.py(0类4函数)、platform_adapter.py(0类6函数)、account_manager.py(3类2函数) |
| 2026-04-21 | Batch 18完成后检查剩余TODO时，调用`get_todo()`后直接使用`.get()`方法导致`AttributeError: 'str' object has no attribute 'get'`。同时查找TODO.md文件失败（实际是TODO.txt）。 | **失败类型**：使用方式错误（API返回值假设错误）。**根因**：①未读取helper.py源码就使用get_todo()，错误假设返回dict列表；②错误假设文件名TODO.md而非TODO.txt。**解决方案**：①使用helper函数前必须先`file_read helper.py`确认接口；②get_todo()返回str需解析，不能直接迭代；③文件名/路径不确定时用`os.listdir()`或`glob`探测。**验证结果**：TODO.txt存在于./目录，get_todo()返回完整文本内容 |
| 2026-04-21 | Batch 18规划任务调用`complete_task(tasktitle=...)`导致`TypeError: complete_task() got an unexpected keyword argument 'tasktitle'`。实际参数名是`taskname`。 | **失败类型**：文档-代码不一致 + 使用方式错误。**根因**：①autonomous_operation_sop.md第8行示例写错参数名（tasktitle vs taskname）；②Agent依赖SOP示例而非源码验证。**解决方案**：①SOP文档仅作流程参考，具体API调用前必须读源码确认；②发现文档错误立即修正；③已修正SOP文档并添加"SOP文档可能过时"规律。**验证结果**：helper.py第154行确认参数是`taskname: str` |
| 2026-04-21 | Batch 18规划任务中两次API调用失败：①`SkillTree.get_statistics()`导致AttributeError（方法不存在）；②`get_next_report_id()`导致NameError（函数不存在）。 | **失败类型**：使用方式错误（未探测API）。**根因**：导入模块/类后凭记忆/假设调用方法，未先探测可用接口。**验证结果**：①SkillTree实际方法：list_all_skills, get_tree_summary等（无get_statistics）；②helper.py实际函数：get_todo, complete_task等（无get_next_report_id，有私有函数_next_report_number）。**解决方案**：①导入后先用`dir(obj)`或`file_read`源码探测方法；②添加"API方法必须探测"规律；③正确做法：导入→探测→确认→调用 |
| 2026-04-21 | file_patch全文替换skill_planning_reviewer.py失败，错误"未找到匹配的旧文本块"。old_content为整个文件内容，含`\\\\n`等多重转义，与实际文件字节不匹配。 | **解决方案**：切换code_run直接写文件成功。**根因**：①file_patch要求字节级精确匹配，全文内容作old_content极易因转义差异失败；②全文重写应用code_run，不应用file_patch。**新增规律**："file_patch全文替换陷阱" |
| 2026-04-21 | 创建skill_planning_reviewer.py时调用`file_write(mode='overwrite', path='./skill_planning_reviewer.py')`失败，错误："No content found. Put content inside <file_content>...</file_content> tags"。 | **失败类型**：工具使用错误（违反已有规则）。**根因**：①未提供`<file_content>`标签内容；②程序化生成的代码应该用code_run而非file_write（违反第25行规则②）；③未检查现有规则就选择工具。**解决方案**：Agent正确切换到`code_run(script=...)`成功创建文件。**预防措施**：①程序化内容（变量拼接、循环生成）→必须用code_run；②file_write仅用于手动编写的短文本+必须带标签；③工具选择前回顾第25行规则 |
| 2026-04-22 | file_patch因old_content含截断内容失败；file_write连续3次/code_run连续2次违反已有规则25/31（未提供内容标签/代码块），未及时切换策略。 | **失败类型**：使用方式错误（重复违反已知规则）。**根因**：①file_read截断输出直接用于file_patch；②已知规则被连续违反而未触发切换。**解决方案**：①截断时先精确re-read再patch；②同一工具同一错误第2次即切换code_run；③新增"file_read截断输出禁用于file_patch"规律 |

## 2. 用户偏好 (User Preferences)
- **回复风格**：简练、无表情包。
- **任务导向**：支持生活自动化与自我进化，具有实用价值。

## 3. 成功路径 (Success Patterns)
- **GitHub README 读取**：当 web_scan/JS 无法获取完整内容时，优先使用 Python `requests` 访问 `raw.githubusercontent.com`。
- **Reflection机制验证**（2026-04-21）：通过故意触发NameError测试，验证了agent_main的自动reflection机制能在对话结束后正确检测工具调用失败（exit_code=1）并自动启动reflection任务。机制工作正常。
- **Reflection嵌套问题修复**（2026-04-21）：发现reflection_helper.py的历史提取逻辑存在严重嵌套问题（最多12层reflection套reflection，input.txt达52KB）。修复方案：①用"=== Prompt === 时间戳"作为可靠边界 ②从后往前遍历，跳过包含"# 自动触发的Reflection任务"的段落 ③限制提取最近3轮非reflection对话。验证结果：压缩比90%（52KB→5KB）
- **Reflection输出冗余修复**（2026-04-21）：修复方案：①过滤逻辑检查文件开头而非全文，避免误判源码中的字符串；②截断保留边界标记便于调试。验证结果：修复前82.7KB，修复后6.4KB，压缩比92.3%
- **Reflection递归触发修复**（2026-04-21）：发现reflection任务本身执行时遇到错误会再次触发reflection，形成无限递归。修复方案：①在agentmain.py存储任务名；②添加递归保护`is_reflection_task = getattr(self, 'task_name', '').startswith('reflection')`，仅在非reflection任务时触发

