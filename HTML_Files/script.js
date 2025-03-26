function loadContent() {{
    // 获取当前HTML文件名（不含扩展名）
    const currentPage = location.pathname
        .split('/').pop()          // 提取文件名
        .replace('.html', '');     // 移除扩展名
    

    // 加载JSON数据
    fetch('../data.json')
        .then(response => response.json())
        .then(data => {{
            // 获取当前页面对应的内容
            const content = data[currentPage];
            
            // 打开新窗口并显示内容
            const newWindow = window.open('', '_blank');
            newWindow.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>${{currentPage}} 报价数据</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 20px }}
                    </style>
                </head>
                <body>
                    <h1>${{currentPage}} 报价数据</h1>
                    <p>${{content}} 详情</p>
                </body>
                </html>
            `);
            newWindow.document.close();
        }})
        .catch(error => {{
            console.error('加载数据失败:', error);
            alert('加载报价数据失败，请检查控制台');
        }});
}}