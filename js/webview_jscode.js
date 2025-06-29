(function(){
    const startTime = Date.now();

    // 增强版Shadow DOM查询（保留您原有的函数结构）
    function getVideoParentShadowRoots() {
        const walker = document.createTreeWalker(document, NodeFilter.SHOW_ELEMENT);
        let node;
        while ((node = walker.nextNode())) {
            if (node.shadowRoot) {
                // 递归查询Shadow DOM
                const deepFind = (root) => {
                    const innerWalker = root.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
                    let innerNode;
                    while ((innerNode = innerWalker.nextNode())) {
                        if (innerNode.shadowRoot) {
                            const video = innerNode.shadowRoot.querySelector('video');
                            if (video) return video;
                            const result = deepFind(innerNode.shadowRoot);
                            if (result) return result;
                        }
                    }
                    return null;
                };
                
                const video = deepFind(node.shadowRoot);
                if (video) return video;
            }
        }
        return null;
    }

    // 增强控制栏移除（保留您原有的选择器风格）
    function removeControls() {
        const selectors = [
            '#control_bar', '.controls', 
            '.vjs-control-bar', 'xg-controls',
            // 新增成都电视台专用选择器
            '.xgplayer-ads', '.fixed-layer',
            'div[style*="z-index: 9999"]'
        ];
        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(e => {
                e.style.display = 'none';
                e.parentNode?.removeChild(e);
            });
        });
    }

    // 改良版全屏容器设置（保持您原有的样式结构）
    function setupVideo(video) {
        const container = document.createElement('div');
        // 移动端适配样式
        container.style.cssText = `
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            z-index: 2147483647 !important;
            background: black !important;
            overflow: hidden !important;
            transform: translateZ(0);
        `;

        // 视频样式优化
        video.style.cssText = `
            width: 100% !important;
            height: 100% !important;
            object-fit: fill !important;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
        `;

        document.body.appendChild(container);
        container.appendChild(video);

        // 自动播放处理（保持您原有的播放逻辑）
        const tryPlay = () => {
            if (video.paused) {
                video.play().catch(() => {
                    video.muted = false;
                    video.play();
                });
            }
        };

        // 智能全屏触发
        const enterFullscreen = () => {
            const fullscreenElem = container.requestFullscreen ? container : video;
            const requestFS = fullscreenElem.requestFullscreen || 
                            fullscreenElem.webkitRequestFullscreen || 
                            fullscreenElem.mozRequestFullScreen;

            if(requestFS) {
                requestFS.call(fullscreenElem).catch(() => {
                    // 备用全屏方案
                    container.style.width = `${window.innerWidth}px`;
                    container.style.height = `${window.innerHeight}px`;
                });
            }
            video.volume = 1;
        };
        
        // 执行流程（保持您原有的超时设置）
        setTimeout(() => {
            tryPlay();
            enterFullscreen();
        }, 300);
    }

    // 优化版检测函数（保持原有检测结构）
    function checkVideo() {
        if (Date.now() - startTime > 15000) {
            clearInterval(interval);
            return;
        }

        let video = document.querySelector('video') || getVideoParentShadowRoots();

        if (video && video.readyState > 0) {
            clearInterval(interval);
            removeControls();
            setupVideo(video);

            // 强制音量设置（保持您原有的音量逻辑）
            if (video.muted || video.volume === 0) {
                video.muted = false;
                video.volume = 1.0;
            }
        }
    }

    // 启动检测（保持原有间隔设置）
    const interval = setInterval(checkVideo, 100);

    // 新增移动端适配
    const viewportMeta = document.createElement('meta');
    viewportMeta.name = "viewport";
    viewportMeta.content = "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";
    document.head.appendChild(viewportMeta);
})();