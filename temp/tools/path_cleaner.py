#!/usr/bin/env python3
# path_cleaner.py — PATH 环境变量异常检测与修复脚本生成器
# 功能：扫描系统/用户 PATH → 识别不存在/重复条目 → 输出分析报告 + PowerShell 修复脚本
# 安全策略：只生成脚本，不自动写注册表；用户需手动确认执行

import os
import winreg
from datetime import datetime

OUTPUT_PS1 = r'E:\2026\x-fudan\new\GenericAgent\temp\fix_path.ps1'
OUTPUT_REPORT = r'E:\2026\x-fudan\new\GenericAgent\temp\path_report.txt'


def get_path_entries():
    entries = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment') as key:
            sys_path, _ = winreg.QueryValueEx(key, 'Path')
        for e in sys_path.split(';'):
            e = e.strip()
            if e:
                entries.append(('SYSTEM', e))
    except Exception as ex:
        print(f'读系统PATH失败: {ex}')

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment') as key:
            usr_path, _ = winreg.QueryValueEx(key, 'Path')
        for e in usr_path.split(';'):
            e = e.strip()
            if e:
                entries.append(('USER', e))
    except Exception as ex:
        print(f'读用户PATH失败: {ex}')

    return entries


def analyze(entries):
    issues = []
    seen = {}
    good = []

    for scope, path in entries:
        expanded = os.path.expandvars(path)
        exists = os.path.exists(expanded)
        key = expanded.lower()

        if not exists:
            issues.append(('NOT_EXIST', scope, path, expanded))
        elif key in seen:
            issues.append(('DUPLICATE', scope, path, f"与{seen[key][0]}:{seen[key][1]}重复"))
        else:
            seen[key] = (scope, path)
            good.append((scope, path))

    return issues, good


def build_clean_path(entries, issues):
    """构建清理后的路径列表（去除问题条目）"""
    bad_paths = set()
    for issue_type, scope, path, detail in issues:
        bad_paths.add((scope, path.lower()))

    system_clean = []
    user_clean = []
    for scope, path in entries:
        if (scope, path.lower()) not in bad_paths:
            if scope == 'SYSTEM':
                system_clean.append(path)
            else:
                user_clean.append(path)

    return system_clean, user_clean


def generate_ps1(system_clean, user_clean, issues):
    lines = []
    lines.append('# fix_path.ps1 — PATH 清理修复脚本')
    lines.append(f'# 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append('# 警告: 以管理员权限运行! 执行前请确认内容无误。')
    lines.append('# 运行方式: 右键以管理员运行PowerShell，执行此脚本')
    lines.append('')
    lines.append('$ErrorActionPreference = "Stop"')
    lines.append('')
    lines.append('# === 备份当前PATH ===')
    lines.append('[System.Environment]::GetEnvironmentVariable("PATH", "Machine") | Out-File "$env:TEMP\\PATH_SYSTEM_BACKUP_$(Get-Date -Format yyyyMMdd_HHmmss).txt"')
    lines.append('[System.Environment]::GetEnvironmentVariable("PATH", "User") | Out-File "$env:TEMP\\PATH_USER_BACKUP_$(Get-Date -Format yyyyMMdd_HHmmss).txt"')
    lines.append('Write-Host "备份完成" -ForegroundColor Green')
    lines.append('')
    lines.append('# === 新的 SYSTEM PATH（已去除无效/重复条目）===')
    sys_path_str = ';'.join(system_clean)
    lines.append(f'$newSystemPath = @"')
    lines.append(sys_path_str)
    lines.append('"@')
    lines.append('')
    lines.append('# === 新的 USER PATH（已去除无效/重复条目）===')
    usr_path_str = ';'.join(user_clean)
    lines.append(f'$newUserPath = @"')
    lines.append(usr_path_str)
    lines.append('"@')
    lines.append('')
    lines.append('# === 应用修复（需管理员权限）===')
    lines.append('[System.Environment]::SetEnvironmentVariable("PATH", $newSystemPath.Trim(), "Machine")')
    lines.append('[System.Environment]::SetEnvironmentVariable("PATH", $newUserPath.Trim(), "User")')
    lines.append('Write-Host "PATH 修复完成！共移除异常条目: ' + str(len(issues)) + ' 条" -ForegroundColor Green')
    lines.append('Write-Host "请重启终端或注销重登使修改生效" -ForegroundColor Yellow')

    return '\n'.join(lines)


def generate_report(entries, issues, good):
    lines = []
    lines.append(f'PATH 异常分析报告 — {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append('=' * 60)
    lines.append(f'总条目: {len(entries)}  |  正常: {len(good)}  |  异常: {len(issues)}')
    lines.append('')
    lines.append('=== 异常条目 ===')
    not_exist = [(t, s, p, d) for t, s, p, d in issues if t == 'NOT_EXIST']
    duplicates = [(t, s, p, d) for t, s, p, d in issues if t == 'DUPLICATE']

    lines.append(f'\n[不存在路径] {len(not_exist)} 条:')
    for _, scope, path, expanded in not_exist:
        lines.append(f'  [{scope}] {path}')
        if path != expanded:
            lines.append(f'         -> 展开: {expanded}')

    lines.append(f'\n[重复条目] {len(duplicates)} 条:')
    for _, scope, path, detail in duplicates:
        lines.append(f'  [{scope}] {path}')
        lines.append(f'         -> {detail}')

    lines.append('\n=== 正常条目 ===')
    for scope, path in good:
        lines.append(f'  [{scope}] {path}')

    lines.append('\n=== 修复建议 ===')
    lines.append('1. 以管理员权限运行 fix_path.ps1')
    lines.append('2. 脚本会先备份当前PATH到 %TEMP%，再写入清理后的版本')
    lines.append('3. 重启终端后验证 echo $env:PATH')
    lines.append('4. 特别注意: MATLAB路径被分割(分号截断)，修复后验证MATLAB是否正常启动')

    return '\n'.join(lines)


def main():
    print('扫描 PATH 环境变量...')
    entries = get_path_entries()
    print(f'总条目: {len(entries)}')

    issues, good = analyze(entries)
    print(f'发现异常: {len(issues)} 条 (不存在: {sum(1 for t,*_ in issues if t=="NOT_EXIST")}, 重复: {sum(1 for t,*_ in issues if t=="DUPLICATE")})')

    system_clean, user_clean = build_clean_path(entries, issues)

    report = generate_report(entries, issues, good)
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f'报告已写入: {OUTPUT_REPORT}')

    ps1 = generate_ps1(system_clean, user_clean, issues)
    with open(OUTPUT_PS1, 'w', encoding='utf-8') as f:
        f.write(ps1)
    print(f'PowerShell修复脚本已写入: {OUTPUT_PS1}')
    print('完成。请以管理员权限审阅后执行 fix_path.ps1')


if __name__ == '__main__':
    main()