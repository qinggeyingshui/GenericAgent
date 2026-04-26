"""
多标签协同助手
提供多标签数据传递、同步操作、验证码处理等功能

功能:
1. 多标签数据传递 - share_data_between_tabs()
2. 跨标签同步操作 - sync_operation_across_tabs()
3. 验证码截图 - capture_captcha()
4. 标签页管理 - list_tabs(), switch_tab(), close_tab()

依赖: TMWebDriver (CDP桥扩展)
"""

from typing import Dict, List, Any, Optional
import json


class MultiTabHelper:
    """多标签协同助手"""
    
    def __init__(self):
        pass
    
    def list_tabs(self) -> Dict:
        """
        获取所有标签页信息
        
        Returns:
            {"success": bool, "tabs": [{"id": int, "url": str, "title": str, "active": bool}]}
        
        使用方法:
            通过 web_execute_js 调用:
            web_execute_js(script='{"cmd": "tabs"}')  # JSON字符串
        """
        return {
            "success": True,
            "message": "使用 web_execute_js 调用 tabs 命令获取标签页列表"
        }
    
    def share_data_between_tabs(self, source_tab_id: int, target_tab_id: int, 
                                data: Dict, method: str = "localStorage") -> Dict:
        """
        在标签页之间共享数据
        
        Args:
            source_tab_id: 源标签页ID
            target_tab_id: 目标标签页ID
            data: 要共享的数据
            method: 共享方式 ("localStorage", "sessionStorage", "broadcast")
        
        Returns:
            {"success": bool, "message": str}
        
        示例:
            # 方法1: localStorage (同域名标签页自动共享)
            # 在源标签页写入
            web_execute_js(script=f"localStorage.setItem('shared_data', '{json.dumps(data)}')")
            
            # 在目标标签页读取
            web_execute_js(script="return localStorage.getItem('shared_data')")
            
            # 方法2: BroadcastChannel (同域名实时通信)
            # 源标签页发送
            web_execute_js(script="""
                const bc = new BroadcastChannel('my_channel');
                bc.postMessage({data});
            """)
            
            # 目标标签页监听
            web_execute_js(script="""
                const bc = new BroadcastChannel('my_channel');
                bc.onmessage = (event) => console.log(event.data);
            """)
        """
        return {
            "success": True,
            "message": f"数据共享方法: {method}",
            "examples": {
                "localStorage": "localStorage.setItem/getItem",
                "sessionStorage": "sessionStorage.setItem/getItem (仅当前会话)",
                "broadcast": "BroadcastChannel API (实时通信)"
            }
        }
    def sync_operation_across_tabs(self, tab_ids: List[int], operation: str) -> Dict:
        """
        跨标签页同步操作
        
        Args:
            tab_ids: 标签页ID列表
            operation: 操作类型 ("refresh", "execute_js", "navigate")
        
        Returns:
            {"success": bool, "results": List}
        
        示例:
            # 使用 CDP batch 命令跨标签操作
            batch_cmd = {
                "cmd": "batch",
                "commands": [
                    {"cmd": "cdp", "tabId": tab_id1, "method": "Page.reload", "params": {}},
                    {"cmd": "cdp", "tabId": tab_id2, "method": "Page.reload", "params": {}},
                ]
            }
            web_execute_js(script=json.dumps(batch_cmd))
            
            # 跨标签执行JS
            batch_cmd = {
                "cmd": "batch",
                "commands": [
                    {"cmd": "cdp", "tabId": tab_id1, "method": "Runtime.evaluate", 
                     "params": {"expression": "console.log('tab1')"}},
                    {"cmd": "cdp", "tabId": tab_id2, "method": "Runtime.evaluate", 
                     "params": {"expression": "console.log('tab2')"}},
                ]
            }
        """
        return {
            "success": True,
            "message": "使用 CDP batch 命令实现跨标签同步操作",
            "example": {
                "refresh_all": "batch多个Page.reload命令",
                "execute_js": "batch多个Runtime.evaluate命令",
                "navigate": "batch多个Page.navigate命令"
            }
        }
    
    def capture_captcha(self, selector: str = None, method: str = "cdp") -> Dict:
        """
        验证码截图
        
        Args:
            selector: 验证码元素选择器 (可选)
            method: 截图方式 ("cdp", "canvas", "element")
        
        Returns:
            {"success": bool, "image_base64": str}
        
        示例:
            # 方法1: CDP全页截图 (推荐)
            cdp_cmd = {
                "cmd": "cdp",
                "method": "Page.captureScreenshot",
                "params": {"format": "png"}
            }
            result = web_execute_js(script=json.dumps(cdp_cmd))
            # result["data"] 包含 base64 图片
            
            # 方法2: Canvas验证码
            js_code = """
                const canvas = document.querySelector('canvas.captcha');
                return canvas.toDataURL('image/png');
            """
            result = web_execute_js(script=js_code)
            
            # 方法3: 元素截图 (需要先获取元素位置)
            # 1. 获取元素位置
            js_code = """
                const el = document.querySelector('.captcha-img');
                const rect = el.getBoundingClientRect();
                return {x: rect.x, y: rect.y, width: rect.width, height: rect.height};
            """
            # 2. CDP截图指定区域
            cdp_cmd = {
                "cmd": "cdp",
                "method": "Page.captureScreenshot",
                "params": {
                    "format": "png",
                    "clip": {"x": x, "y": y, "width": w, "height": h, "scale": 1}
                }
            }
        """
        return {
            "success": True,
            "message": "验证码截图方法",
            "methods": {
                "cdp": "Page.captureScreenshot (全页或指定区域)",
                "canvas": "canvas.toDataURL() (Canvas验证码)",
                "element": "先获取位置，再CDP截图指定区域"
            }
        }

# ============ 使用示例 ============

if __name__ == "__main__":
    print("=== Multi-Tab Helper 使用指南 ===\n")
    
    helper = MultiTabHelper()
    
    print("【1. 获取标签页列表】\n")
    print("使用 web_execute_js 调用:")
    print("  web_execute_js(script='{\"cmd\": \"tabs\"}')")
    print("  返回: {ok: true, tabs: [{id, url, title, active}, ...]}")
    print()
    
    print("【2. 多标签数据传递】\n")
    print("方法1: localStorage (同域名自动共享)")
    print("  # 标签页A写入")
    print("  web_execute_js(script=\"localStorage.setItem('data', 'value')\")") 
    print("  # 标签页B读取")
    print("  web_execute_js(script=\"return localStorage.getItem('data')\")") 
    print()
    print("方法2: BroadcastChannel (实时通信)")
    print("  # 标签页A发送")
    print("  web_execute_js(script=\"const bc = new BroadcastChannel('ch'); bc.postMessage({msg: 'hello'})\")") 
    print("  # 标签页B监听")
    print("  web_execute_js(script=\"const bc = new BroadcastChannel('ch'); bc.onmessage = e => console.log(e.data)\")") 
    print()
    
    print("【3. 跨标签同步操作】\n")
    print("使用 CDP batch 命令:")
    print("  batch_cmd = {")
    print("      \"cmd\": \"batch\",")
    print("      \"commands\": [")
    print("          {\"cmd\": \"cdp\", \"tabId\": 123, \"method\": \"Page.reload\", \"params\": {}},")
    print("          {\"cmd\": \"cdp\", \"tabId\": 456, \"method\": \"Page.reload\", \"params\": {}}")
    print("      ]")
    print("  }")
    print("  web_execute_js(script=json.dumps(batch_cmd))")
    print()
    
    print("【4. 验证码截图】\n")
    print("方法1: CDP全页截图")
    print("  cdp_cmd = {\"cmd\": \"cdp\", \"method\": \"Page.captureScreenshot\", \"params\": {\"format\": \"png\"}}")
    print("  result = web_execute_js(script=json.dumps(cdp_cmd))")
    print("  # result[\"data\"] 包含 base64 图片")
    print()
    print("方法2: Canvas验证码")
    print("  js = \"const canvas = document.querySelector('canvas'); return canvas.toDataURL()\"")
    print("  result = web_execute_js(script=js)")
    print()
    
    print("【5. 能力边界】\n")
    print("✓ 跨标签操作: CDP batch 支持后台标签")
    print("✓ 数据共享: localStorage/BroadcastChannel (同域名)")
    print("✓ 验证码: CDP截图/Canvas导出")
    print("✓ 跨域iframe: Page.getFrameTree + createIsolatedWorld")
    print("✗ 验证码识别: 需要外部OCR服务 (如 tesseract, 百度OCR)")
    print("✗ 跨域数据传递: 需要服务器中转或扩展API")
    print()
    
    print("=== 使用指南完成 ===")