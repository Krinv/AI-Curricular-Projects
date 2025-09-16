// 全局变量
let currentModel = null;
let isVideoPlaying = false;
let videoElement = null;
let videoDetectionInterval = null;
let detectionResults = [];
let confThreshold = 0.25;
let iouThreshold = 0.45;
let saveResults = false;

// API基础URL
const API_BASE = '/api';

// DOM元素
const elements = {
    // 按钮
    loadModelBtn: document.getElementById('load-model-btn'),
    imageDetectBtn: document.getElementById('image-detect-btn'),
    videoDetectBtn: document.getElementById('video-detect-btn'),
    cameraBtn: document.getElementById('camera-btn'),
    playPauseBtn: document.getElementById('play-pause-btn'),
    
    // 文件输入
    modelFile: document.getElementById('model-file'),
    imageFile: document.getElementById('image-file'),
    videoFile: document.getElementById('video-file'),
    
    // 滑块和复选框
    confSlider: document.getElementById('conf-slider'),
    iouSlider: document.getElementById('iou-slider'),
    saveResultsCheckbox: document.getElementById('save-results'),
    videoProgress: document.getElementById('video-progress'),
    
    // 显示区域
    displayArea: document.querySelector('.display-area'),
    imageDisplay: document.getElementById('image-display'),
    detectionResults: document.getElementById('detection-results'),
    behaviorStats: document.getElementById('behavior-stats'),
    tableBody: document.getElementById('table-body'),
    
    // 状态
    statusText: document.getElementById('status-text'),
    statusIndicator: document.getElementById('status-indicator'),
    confValue: document.getElementById('conf-value'),
    iouValue: document.getElementById('iou-value'),
    
    // 加载遮罩
    loadingOverlay: document.getElementById('loading-overlay')
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    checkBrowserCompatibility();
    updateStatus('系统就绪', 'success');
});

// 检查浏览器兼容性
function checkBrowserCompatibility() {
    // 检查getUserMedia支持
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        elements.cameraBtn.disabled = true;
        elements.cameraBtn.title = '您的浏览器不支持摄像头功能';
        elements.cameraBtn.innerHTML = '<i class="icon">📷</i> 摄像头 (不支持)';
        console.warn('Browser does not support getUserMedia');
        return;
    }
    
    // 检查HTTPS或localhost
    if (location.protocol !== 'https:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
        elements.cameraBtn.disabled = true;
        elements.cameraBtn.title = '摄像头功能需要HTTPS连接';
        elements.cameraBtn.innerHTML = '<i class="icon">📷</i> 摄像头 (需要HTTPS)';
        console.warn('Camera requires HTTPS or localhost');
        return;
    }
    
    // 浏览器支持摄像头
    elements.cameraBtn.title = '启动摄像头进行实时检测';
}

// 事件监听器
function initializeEventListeners() {
    // 模型加载
    elements.loadModelBtn.addEventListener('click', () => elements.modelFile.click());
    elements.modelFile.addEventListener('change', handleModelLoad);
    
    // 图片检测
    elements.imageDetectBtn.addEventListener('click', () => {
        if (!currentModel) {
            showAlert('请先加载YOLO模型');
            return;
        }
        elements.imageFile.click();
    });
    elements.imageFile.addEventListener('change', handleImageDetection);
    
    // 视频检测
    elements.videoDetectBtn.addEventListener('click', () => {
        if (!currentModel) {
            showAlert('请先加载YOLO模型');
            return;
        }
        elements.videoFile.click();
    });
    elements.videoFile.addEventListener('change', handleVideoDetection);
    
    // 摄像头检测
    elements.cameraBtn.addEventListener('click', () => {
        if (!currentModel) {
            showAlert('请先加载YOLO模型');
            return;
        }
        handleCameraDetection();
    });
    
    // 视频控制
    elements.playPauseBtn.addEventListener('click', toggleVideoPlayback);
    elements.videoProgress.addEventListener('input', handleVideoSeek);
    
    // 参数控制
    elements.confSlider.addEventListener('input', handleConfThresholdChange);
    elements.iouSlider.addEventListener('input', handleIouThresholdChange);
    elements.saveResultsCheckbox.addEventListener('change', handleSaveResultsChange);
}

// 模型加载处理
async function handleModelLoad(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    showLoading('正在加载模型...');
    
    try {
        const formData = new FormData();
        formData.append('model', file);
        
        const response = await fetch(`${API_BASE}/load_model`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentModel = result.model_info;
            updateStatus('模型加载成功', 'success');
            enableDetectionButtons();
        } else {
            updateStatus(`模型加载失败: ${result.error}`, 'error');
        }
    } catch (error) {
        updateStatus(`模型加载失败: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// 图片检测处理
async function handleImageDetection(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    showLoading('正在检测图片...');
    
    try {
        // 显示图片
        const imageUrl = URL.createObjectURL(file);
        displayImage(imageUrl);
        
        // 发送检测请求
        const formData = new FormData();
        formData.append('image', file);
        formData.append('conf_threshold', confThreshold);
        formData.append('iou_threshold', iouThreshold);
        formData.append('save_results', saveResults);
        
        const response = await fetch(`${API_BASE}/detect_image`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            detectionResults = result.detections;
            updateDetectionResults();
            updateStatus('图片检测完成', 'success');
            
            // 显示带检测框的图片
            if (result.annotated_image) {
                displayImage(`data:image/jpeg;base64,${result.annotated_image}`);
            }
        } else {
            updateStatus(`检测失败: ${result.error}`, 'error');
        }
    } catch (error) {
        updateStatus(`检测失败: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// 视频检测处理
async function handleVideoDetection(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    showLoading('正在处理视频...');
    
    try {
        const formData = new FormData();
        formData.append('video', file);
        formData.append('conf_threshold', confThreshold);
        formData.append('iou_threshold', iouThreshold);
        formData.append('save_results', 'true');
        
        const response = await fetch(`${API_BASE}/detect_video`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 显示视频
            const videoUrl = URL.createObjectURL(file);
            displayVideo(videoUrl);
            
            // 启用视频控制
            elements.playPauseBtn.disabled = false;
            elements.videoProgress.disabled = false;
            
            // 更新检测结果（初始显示）
            detectionResults = result.detections || [];
            updateDetectionResults();
            
            updateStatus(`视频已加载，准备实时检测`, 'success');
            
            if (result.saved_to) {
                console.log('结果已保存到:', result.saved_to);
            }
        } else {
            updateStatus(`视频检测失败: ${result.error}`, 'error');
        }
    } catch (error) {
        updateStatus(`视频检测失败: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// 摄像头检测处理
async function handleCameraDetection() {
    try {
        // 检查浏览器是否支持getUserMedia
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('您的浏览器不支持摄像头功能。请使用Chrome、Firefox、Safari或Edge等现代浏览器。');
        }
        
        // 检查是否为HTTPS或localhost
        if (location.protocol !== 'https:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
            throw new Error('摄像头功能需要HTTPS连接或本地环境。请使用https://或在localhost上访问。');
        }
        
        updateStatus('正在请求摄像头权限...', 'warning');
        
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            },
            audio: false
        });
        
        displayVideoStream(stream);
        
        // 启用视频控制
        elements.playPauseBtn.disabled = false;
        elements.videoProgress.disabled = true; // 摄像头模式下禁用进度条
        
        updateStatus('摄像头已启动', 'success');
        startRealtimeDetection();
    } catch (error) {
        console.error('Camera error:', error);
        
        let errorMessage = '摄像头启动失败: ';
        
        if (error.name === 'NotAllowedError') {
            errorMessage += '用户拒绝了摄像头权限。请在浏览器设置中允许摄像头访问。';
        } else if (error.name === 'NotFoundError') {
            errorMessage += '未找到摄像头设备。请确保摄像头已连接。';
        } else if (error.name === 'NotReadableError') {
            errorMessage += '摄像头被其他应用占用。请关闭其他使用摄像头的程序。';
        } else if (error.name === 'OverconstrainedError') {
            errorMessage += '摄像头不支持请求的配置。';
        } else if (error.name === 'SecurityError') {
            errorMessage += '安全限制。请确保在HTTPS环境下访问。';
        } else {
            errorMessage += error.message || '未知错误';
        }
        
        updateStatus(errorMessage, 'error');
    }
}

// 实时检测
async function startRealtimeDetection() {
    if (!videoElement) return;
    
    // 创建用于检测的canvas
    const detectCanvas = document.createElement('canvas');
    const detectCtx = detectCanvas.getContext('2d');
    
    // 创建用于绘制检测框的overlay canvas
    createDetectionOverlay();
    
    const detectFrame = async () => {
        if (!isVideoPlaying) return;
        
        detectCanvas.width = videoElement.videoWidth;
        detectCanvas.height = videoElement.videoHeight;
        detectCtx.drawImage(videoElement, 0, 0);
        
        detectCanvas.toBlob(async (blob) => {
            try {
                const formData = new FormData();
                formData.append('image', blob);
                formData.append('conf_threshold', confThreshold);
                formData.append('iou_threshold', iouThreshold);
                
                const response = await fetch(`${API_BASE}/detect_frame`, {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    detectionResults = result.detections;
                    updateDetectionResults();
                    drawDetectionBoxes(result.detections); // 绘制检测框
                }
            } catch (error) {
                console.error('Frame detection error:', error);
            }
        }, 'image/jpeg', 0.8);
        
        // 继续检测下一帧
        setTimeout(detectFrame, 100); // 10 FPS
    };
    
    detectFrame();
}

// 视频文件实时检测
function startVideoDetection() {
    if (!videoElement || videoElement.srcObject) return; // 只对视频文件有效
    
    // 清除之前的检测间隔
    if (videoDetectionInterval) {
        clearInterval(videoDetectionInterval);
    }
    
    // 创建用于检测的canvas
    const detectCanvas = document.createElement('canvas');
    const detectCtx = detectCanvas.getContext('2d');
    
    // 确保检测框overlay存在
    createDetectionOverlay();
    
    const detectCurrentFrame = async () => {
        if (!isVideoPlaying || !videoElement) return;
        
        try {
            detectCanvas.width = videoElement.videoWidth;
            detectCanvas.height = videoElement.videoHeight;
            detectCtx.drawImage(videoElement, 0, 0);
            
            detectCanvas.toBlob(async (blob) => {
                try {
                    const formData = new FormData();
                    formData.append('image', blob);
                    formData.append('conf_threshold', confThreshold);
                    formData.append('iou_threshold', iouThreshold);
                    
                    const response = await fetch(`${API_BASE}/detect_frame`, {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        detectionResults = result.detections;
                        updateDetectionResults();
                        drawDetectionBoxes(result.detections);
                    }
                } catch (error) {
                    console.error('Frame detection error:', error);
                }
            }, 'image/jpeg', 0.8);
        } catch (error) {
            console.error('Canvas error:', error);
        }
    };
    
    // 每500ms检测一次（2 FPS）
    videoDetectionInterval = setInterval(detectCurrentFrame, 500);
}

function stopVideoDetection() {
    if (videoDetectionInterval) {
        clearInterval(videoDetectionInterval);
        videoDetectionInterval = null;
    }
}

// 视频播放控制
function toggleVideoPlayback() {
    if (!videoElement) return;
    
    // 如果是摄像头模式
    if (videoElement.srcObject && videoElement.stream) {
        if (isVideoPlaying) {
            // 停止摄像头
            stopCamera();
        } else {
            // 重新启动摄像头
            handleCameraDetection();
        }
        return;
    }
    
    // 视频文件模式
    if (isVideoPlaying) {
        videoElement.pause();
        isVideoPlaying = false;
        elements.playPauseBtn.innerHTML = '<i class="icon">▶️</i>';
        updateStatus('视频已暂停', 'warning');
        stopVideoDetection(); // 停止检测
    } else {
        videoElement.play();
        isVideoPlaying = true;
        elements.playPauseBtn.innerHTML = '<i class="icon">⏸️</i>';
        updateStatus('视频播放中', 'success');
        startVideoDetection(); // 开始检测
    }
}

// 视频进度控制
function handleVideoSeek(event) {
    if (!videoElement || videoElement.srcObject) return; // 摄像头模式下不支持拖拽
    
    const progress = event.target.value / 100;
    videoElement.currentTime = progress * videoElement.duration;
    
    // 如果视频正在播放，触发一次检测更新
    if (isVideoPlaying) {
        setTimeout(() => {
            // 延迟一点确保视频帧已更新
            const detectCanvas = document.createElement('canvas');
            const detectCtx = detectCanvas.getContext('2d');
            
            if (videoElement.videoWidth > 0 && videoElement.videoHeight > 0) {
                detectCanvas.width = videoElement.videoWidth;
                detectCanvas.height = videoElement.videoHeight;
                detectCtx.drawImage(videoElement, 0, 0);
                
                detectCanvas.toBlob(async (blob) => {
                    try {
                        const formData = new FormData();
                        formData.append('image', blob);
                        formData.append('conf_threshold', confThreshold);
                        formData.append('iou_threshold', iouThreshold);
                        
                        const response = await fetch(`${API_BASE}/detect_frame`, {
                            method: 'POST',
                            body: formData
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            detectionResults = result.detections;
                            updateDetectionResults();
                            drawDetectionBoxes(result.detections);
                        }
                    } catch (error) {
                        console.error('Seek detection error:', error);
                    }
                }, 'image/jpeg', 0.8);
            }
        }, 100);
    }
}

// 参数控制
function handleConfThresholdChange(event) {
    confThreshold = event.target.value / 100;
    elements.confValue.textContent = confThreshold.toFixed(2);
}

function handleIouThresholdChange(event) {
    iouThreshold = event.target.value / 100;
    elements.iouValue.textContent = iouThreshold.toFixed(2);
}

function handleSaveResultsChange(event) {
    saveResults = event.target.checked;
}

// 显示函数
function displayImage(src) {
    elements.imageDisplay.innerHTML = `<img id="display-image" src="${src}" alt="检测图片">`;
}

function displayVideo(src) {
    const video = document.createElement('video');
    video.id = 'display-video';
    video.src = src;
    video.controls = false;
    video.muted = true;
    
    video.addEventListener('loadedmetadata', () => {
        elements.videoProgress.max = video.duration;
        createDetectionOverlay();
    });
    
    video.addEventListener('timeupdate', () => {
        if (!video.srcObject) { // 只有文件视频才更新进度
            elements.videoProgress.value = (video.currentTime / video.duration) * 100;
        }
    });
    
    // 监听播放状态变化
    video.addEventListener('play', () => {
        isVideoPlaying = true;
        elements.playPauseBtn.innerHTML = '<i class="icon">⏸️</i>';
        startVideoDetection();
    });
    
    video.addEventListener('pause', () => {
        isVideoPlaying = false;
        elements.playPauseBtn.innerHTML = '<i class="icon">▶️</i>';
        stopVideoDetection();
    });
    
    elements.imageDisplay.innerHTML = '';
    elements.imageDisplay.appendChild(video);
    videoElement = video;
}

function displayVideoStream(stream) {
    // 清除之前的视频元素和overlay
    const existingVideo = elements.displayArea.querySelector('video');
    const existingOverlay = elements.displayArea.querySelector('.detection-overlay');
    if (existingVideo) {
        existingVideo.remove();
    }
    if (existingOverlay) {
        existingOverlay.remove();
    }
    
    // 创建新的视频元素
    videoElement = document.createElement('video');
    videoElement.srcObject = stream;
    videoElement.stream = stream; // 保存流引用
    videoElement.autoplay = true;
    videoElement.muted = true;
    videoElement.style.width = '100%';
    videoElement.style.height = '100%';
    videoElement.style.objectFit = 'contain';
    videoElement.style.position = 'relative';
    
    elements.displayArea.appendChild(videoElement);
    
    isVideoPlaying = true;
    elements.playPauseBtn.innerHTML = '<i class="icon">⏸️</i>';
    updateStatus('摄像头已启动', 'success');
}

// 停止摄像头
function stopCamera() {
    if (videoElement && videoElement.stream) {
        // 停止所有轨道
        videoElement.stream.getTracks().forEach(track => {
            track.stop();
        });
        
        // 清除video元素
        videoElement.srcObject = null;
        videoElement = null;
        
        // 清除检测框overlay
        const overlay = elements.displayArea.querySelector('.detection-overlay');
        if (overlay) {
            overlay.remove();
        }
        
        // 重置状态
        isVideoPlaying = false;
        elements.playPauseBtn.innerHTML = '<i class="icon">▶️</i>';
        elements.playPauseBtn.disabled = true;
        
        updateStatus('摄像头已停止', 'success');
    }
}

// 结果更新
function updateDetectionResults() {
    // 更新检测结果区域
    if (detectionResults.length === 0) {
        elements.detectionResults.innerHTML = '<div class="no-results"><p>未检测到行为</p></div>';
        elements.behaviorStats.innerHTML = '<div class="no-stats"><p>暂无统计数据</p></div>';
        elements.tableBody.innerHTML = '';
        return;
    }
    
    // 检测结果
    const resultsHtml = detectionResults
        .sort((a, b) => b.confidence - a.confidence)
        .slice(0, 4)
        .map(det => `
            <div class="detection-item">
                <span class="behavior-name">${det.class_name}</span>
                <span class="confidence">${det.confidence.toFixed(2)}</span>
            </div>
        `).join('');
    
    elements.detectionResults.innerHTML = `
        <div style="color: #FF69B4; font-weight: bold; text-align: center; margin-bottom: 10px; border-bottom: 1px dashed #FFB6C1; padding-bottom: 5px;">
            检测结果
        </div>
        ${resultsHtml}
    `;
    
    // 行为统计
    const behaviorCounts = {};
    detectionResults.forEach(det => {
        behaviorCounts[det.class_name] = (behaviorCounts[det.class_name] || 0) + 1;
    });
    
    const statsHtml = Object.entries(behaviorCounts)
        .sort((a, b) => b[1] - a[1])
        .map(([behavior, count]) => `
            <div class="stat-item">
                <span class="stat-name">${behavior}</span>
                <span class="stat-count">${count}次</span>
            </div>
        `).join('');
    
    elements.behaviorStats.innerHTML = `
        <div style="color: #FF69B4; font-weight: bold; text-align: center; margin-bottom: 10px; border-bottom: 1px dashed #FFB6C1; padding-bottom: 5px;">
            行为统计
        </div>
        ${statsHtml}
        <div style="color: #FF69B4; text-align: center; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #FFB6C1;">
            总计: ${detectionResults.length}个行为
        </div>
    `;
    
    // 详细表格
    const tableHtml = detectionResults.map((det, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>${det.class_name}</td>
            <td>${det.confidence.toFixed(2)}</td>
            <td>(${det.bbox[0]},${det.bbox[1]})-(${det.bbox[2]},${det.bbox[3]})</td>
        </tr>
    `).join('');
    
    elements.tableBody.innerHTML = tableHtml;
}

// 创建检测框overlay
function createDetectionOverlay() {
    // 确定容器元素（摄像头模式用displayArea，视频文件模式用imageDisplay）
    const container = videoElement && videoElement.srcObject ? elements.displayArea : elements.imageDisplay;
    
    // 移除已存在的overlay
    const existingOverlay = container.querySelector('.detection-overlay');
    if (existingOverlay) {
        existingOverlay.remove();
    }
    
    // 创建新的overlay canvas
    const overlay = document.createElement('canvas');
    overlay.className = 'detection-overlay';
    overlay.style.position = 'absolute';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.pointerEvents = 'none';
    overlay.style.zIndex = '10';
    
    container.appendChild(overlay);
    
    // 监听视频尺寸变化
    if (videoElement) {
        const resizeOverlay = () => {
            const rect = videoElement.getBoundingClientRect();
            const displayRect = container.getBoundingClientRect();
            
            // 设置canvas的实际像素尺寸为视频的原始尺寸
            overlay.width = videoElement.videoWidth || rect.width;
            overlay.height = videoElement.videoHeight || rect.height;
            
            // 设置canvas的显示尺寸和位置
            overlay.style.width = rect.width + 'px';
            overlay.style.height = rect.height + 'px';
            overlay.style.left = (rect.left - displayRect.left) + 'px';
            overlay.style.top = (rect.top - displayRect.top) + 'px';
        };
        
        videoElement.addEventListener('loadedmetadata', resizeOverlay);
        window.addEventListener('resize', resizeOverlay);
        
        // 初始调整
        setTimeout(resizeOverlay, 100);
    }
}

// 绘制检测框
function drawDetectionBoxes(detections) {
    // 确定容器元素（摄像头模式用displayArea，视频文件模式用imageDisplay）
    const container = videoElement && videoElement.srcObject ? elements.displayArea : elements.imageDisplay;
    const overlay = container.querySelector('.detection-overlay');
    if (!overlay || !videoElement) return;
    
    const ctx = overlay.getContext('2d');
    
    // 清除之前的绘制
    ctx.clearRect(0, 0, overlay.width, overlay.height);
    
    if (!detections || detections.length === 0) return;
    
    // 获取视频和overlay的尺寸比例
    // overlay.width/height现在是视频的原始尺寸，检测框坐标也是基于原始尺寸
    // 所以缩放比例应该是1:1
    const scaleX = 1;
    const scaleY = 1;
    
    // 颜色映射
    const colors = {
        0: '#FF3232',   // 使用手机 - 红色
        4: '#32FF32',   // 举手 - 绿色
        8: '#3232FF',   // 睡觉 - 蓝色
        10: '#FFFF32'   // 端正坐姿 - 黄色
    };
    
    detections.forEach(detection => {
        const [x1, y1, x2, y2] = detection.bbox;
        const color = colors[detection.class_id] || '#666666';
        
        // 缩放坐标
        const scaledX1 = x1 * scaleX;
        const scaledY1 = y1 * scaleY;
        const scaledX2 = x2 * scaleX;
        const scaledY2 = y2 * scaleY;
        
        // 绘制矩形框
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.strokeRect(scaledX1, scaledY1, scaledX2 - scaledX1, scaledY2 - scaledY1);
        
        // 绘制标签背景
        const label = `${detection.class_name} ${detection.confidence.toFixed(2)}`;
        ctx.font = '16px Arial';
        const textMetrics = ctx.measureText(label);
        const textWidth = textMetrics.width;
        const textHeight = 20;
        
        ctx.fillStyle = color;
        ctx.fillRect(scaledX1, scaledY1 - textHeight - 5, textWidth + 10, textHeight + 5);
        
        // 绘制标签文字
        ctx.fillStyle = '#FFFFFF';
        ctx.fillText(label, scaledX1 + 5, scaledY1 - 8);
    });
}

// 状态更新
function updateStatus(message, type = 'info') {
    elements.statusText.textContent = message;
    
    // 更新状态指示器颜色
    const colors = {
        success: '#48bb78',
        error: '#f56565',
        warning: '#ed8936',
        info: '#4299e1'
    };
    
    elements.statusIndicator.style.background = colors[type] || colors.info;
}

// 启用检测按钮
function enableDetectionButtons() {
    elements.imageDetectBtn.disabled = false;
    elements.videoDetectBtn.disabled = false;
    elements.cameraBtn.disabled = false;
}

// 加载遮罩控制
function showLoading(message = '处理中...') {
    elements.loadingOverlay.style.display = 'flex';
    elements.loadingOverlay.querySelector('p').textContent = message;
}

function hideLoading() {
    elements.loadingOverlay.style.display = 'none';
}

// 警告提示
function showAlert(message) {
    alert(message); // 可以替换为更美观的模态框
}

// 错误处理
window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', event.error);
    updateStatus('发生未知错误', 'error');
    hideLoading();
});

// 网络错误处理
window.addEventListener('unhandledrejection', function(event) {
    console.error('Promise Rejection:', event.reason);
    updateStatus('网络请求失败', 'error');
    hideLoading();
});