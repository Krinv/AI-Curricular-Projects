# -*- mode: python -*-
# encoding: utf-8 -*-

# 导入必要模块
from PyInstaller.utils.hooks import collect_data_files

# 定义项目根目录（建议使用全英文路径，避免中文用户名导致的路径问题）
PROJECT_ROOT = os.path.abspath("F:/shenduxuexi/student_hehaviour_v11_side_end")  # 替换为你的项目实际路径

# 添加资源文件（使用绝对路径确保兼容性）
datas = [
    (os.path.join(PROJECT_ROOT, "web"), "web"),                # Web 前端文件（含 index.html）
    (os.path.join(PROJECT_ROOT, "Student_Behaviour"), "Student_Behaviour"),  # 数据集目录
    (os.path.join(PROJECT_ROOT, "test_images"), "test_images"),     # 测试图片
    (os.path.join(PROJECT_ROOT, "test_videos"), "test_videos"),     # 测试视频
    (os.path.join(PROJECT_ROOT, "class_cv.pt"), "."),         # 主模型文件
    (os.path.join(PROJECT_ROOT, "yolo11s.pt"), ".")          # 辅助模型文件
]

# 添加隐藏依赖（解决 PyTorch/YOLO/Flask 的导入问题）
hiddenimports = [
    'ultralytics',
    'cv2',
    'numpy',
    'flask',
    'PIL',
    'docx',
    'werkzeug.utils',
    'itsdangerous',
    'jinja2'
]

# 分析模块
a = Analysis(
    ['main.py'],  # 主程序入口
    pathex=[PROJECT_ROOT],  # 项目根目录作为模块搜索路径
    binaries=[],  # 二进制文件（可选：手动添加缺失的 DLL）
    datas=datas,  # 资源文件
    hiddenimports=hiddenimports,  # 隐藏依赖
    hookspath=[],  # 钩子脚本路径
    hooksconfig={},  # 钩子配置
    runtime_hooks=[],  # 运行时钩子
    excludes=[],  # 排除的模块
    noarchive=False,  # 启用归档（加速启动）
    optimize=0,  # 优化级别（0=无优化）
)

# 创建 PYZ 归档
pyz = PYZ(a.pure)

# 创建 EXE 文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ClassroomBehaviorSystem',  # 可执行文件名
    debug=False,  # 禁用调试模式
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 启用 UPX 压缩
    upx_exclude=[],  # 不压缩的文件
    runtime_tmpdir=None,  # 不使用临时目录
    console=True,  # 显示控制台窗口（便于调试）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)