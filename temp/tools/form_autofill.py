"""
表单自动填充工具
支持JSON配置驱动，填充text/select/checkbox/radio等表单类型
依赖: web_scan, web_execute_js
"""
import json
from typing import Dict, List, Optional


def fill_form_js(config: Dict, selector_prefix: str = "form") -> str:
    """生成表单填充JS代码"""
    js_lines = [
        f'const form = document.querySelector(\'{selector_prefix}\');',
        'if (!form) throw new Error(\'表单未找到\');',
        'const results = [];',
    ]
    
    for field, value in config.items():
        # 转义值中的单引号
        safe_value = str(value).replace("'", "\\'")
        
        js_lines.extend([
            f'// 填充字段: {field}',
            f'let el = form.querySelector(\'[name="{field}"]\')',
            f'    || form.querySelector(\'#{field}\')',
            f'    || form.querySelector(\'[id*="{field}"]\')',
            f'    || document.querySelector(\'[name="{field}"]\')',
            f'    || document.querySelector(\'#{field}\');',
            'if (el) {',
            '  const tagName = el.tagName.toLowerCase();',
            '  const type = el.type ? el.type.toLowerCase() : \'\';',
            '  if (tagName === \'select\') {',
            f'    el.value = \'{safe_value}\';',
            '    el.dispatchEvent(new Event(\'change\', {bubbles: true}));',
            f'    results.push({{field: \'{field}\', type: \'select\', success: true}});',
            '  } else if (type === \'checkbox\' || type === \'radio\') {',
            f'    el.checked = {str(value).lower()};',
            '    el.dispatchEvent(new Event(\'change\', {bubbles: true}));',
            f'    results.push({{field: \'{field}\', type: type, success: true}});',
            '  } else if (type === \'file\') {',
            f'    results.push({{field: \'{field}\', type: \'file\', success: false, msg: \'需CDP\'}});',
            '  } else {',
            f'    el.value = \'{safe_value}\';',
            '    el.dispatchEvent(new Event(\'input\', {bubbles: true}));',
            '    el.dispatchEvent(new Event(\'change\', {bubbles: true}));',
            f'    results.push({{field: \'{field}\', type: \'text\', success: true}});',
            '  }',
            '} else {',
            f'  results.push({{field: \'{field}\', success: false, msg: \'未找到\'}});',
            '}',
        ])
    
    js_lines.append('return results;')
    return '\n'.join(js_lines)


def fill_form_config(config_path: str, selector_prefix: str = "form") -> str:
    """从JSON文件读取配置并生成填充JS"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return fill_form_js(config, selector_prefix)


def generate_form_config_template(output_path: str = "./form_config_template.json"):
    """生成表单配置模板"""
    template = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123",
        "age": "25",
        "gender": "male",
        "agree": True,
        "country": "China"
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    return output_path


if __name__ == "__main__":
    config = {"username": "张三", "email": "test@example.com", "agree": True}
    js_code = fill_form_js(config)
    print("=== 生成的JS代码示例 ===")
    print(js_code[:300])
    
    template_path = generate_form_config_template()
    print(f"\n✓ 配置模板: {template_path}")
    
    js_code2 = fill_form_config(template_path)
    print(f"✓ 从配置生成JS ({len(js_code2)} 字符)")