from ultralytics import YOLO
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

if __name__ == '__main__':
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 使用绝对路径
    data_yaml = os.path.join(current_dir, "Student_Behaviour", "data.yaml")
    pre_model = os.path.join(current_dir, "yolo11s.pt")
    
    # 检查文件是否存在
    for file_path, name in [(pre_model, "yolo11s.pt"), (data_yaml, "data.yaml")]:
        if not os.path.exists(file_path):
            print(f"{name}文件不存在: {file_path}")
            exit(1)
    
    print(f"使用模型文件: {pre_model}")
    print(f"使用数据配置: {data_yaml}")
    
    model = YOLO(pre_model)

    results = model.train(
        data=data_yaml,
        epochs=50,
        imgsz=640,
        batch=8,
        workers=0,
        lr0=1e-4,
        lrf=0.1,
        optimizer='AdamW',
        device='cuda:0',
        amp=False,
        patience=50,
        save_period=30,
        cache='ram',
        augment=True,
        plots=True
    )