/**
 * Flask Web App - Main JavaScript
 */

// 通用 AJAX 工具
const api = {
    async get(url) {
        const res = await fetch(url);
        return res.json();
    },
    
    async post(url, data) {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    }
};

// 工具函数
const utils = {
    // 显示提示消息
    showMessage(el, message, type = 'success') {
        el.innerHTML = `<p class="${type}">${message}</p>`;
        setTimeout(() => el.innerHTML = '', 5000);
    },
    
    // 防抖函数
    debounce(fn, delay) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => fn(...args), delay);
        };
    }
};

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    console.log('Flask Web App loaded');
    
    // 自动隐藏 flash 消息
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });
});

// 导出供其他模块使用
window.api = api;
window.utils = utils;
