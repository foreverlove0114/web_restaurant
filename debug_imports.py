# debug_imports.py（放在项目根目录）
import sys
import os

print("=== 调试导入问题 ===")
print(f"当前工作目录: {os.getcwd()}")
print(f"Python 路径:")
for path in sys.path:
    print(f"  {path}")

# 检查 Pages 目录是否存在
pages_path = os.path.join('end_to_end', 'Pages')
print(f"\nPages 目录存在: {os.path.exists(pages_path)}")
if os.path.exists(pages_path):
    print(f"Pages 目录内容: {os.listdir(pages_path)}")

# 尝试导入
try:
    sys.path.insert(0, 'end_to_end')
    from Pages.HomePage import HomePage
    print("✅ 成功导入 HomePage")
except ImportError as e:
    print(f"❌ 导入失败: {e}")