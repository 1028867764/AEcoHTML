function loadContent() {
    const pageTitle = document.title;
    const currentPage = location.pathname.split("/").pop().replace(".html", "");

    fetch("https://1028867764.github.io/AEcoHTML/HTML_Files/data.json")
        .then(response => response.json())
        .then(data => {
            const entries = data[currentPage];
            if (!entries || !entries.length) throw new Error("未找到数据");

            const newWindow = window.open("", "_blank");
            newWindow.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>${pageTitle}</title>
                    <style>
                        body { 
                            font-family: Arial, sans-serif; 
                            padding: 20px;
                            background-color: #f5f5f5;
                        }
                        .itemTitle {
                            background-color: lightblue;
                            text-align: center;
                            padding: 15px;
                            margin-bottom: 20px;
                            border-radius: 8px;
                        }
                        .card-container {
                            display: grid;
                            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                            gap: 20px;
                            margin: 0 auto;
                        }
                        .card {
                            background: white;
                            border-radius: 8px;
                            padding: 20px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .card h3 {
                            color: #333;
                            border-bottom: 1px solid #eee;
                            padding-bottom: 10px;
                            margin-top: 0;
                        }
                        .card p {
                            margin: 8px 0;
                            color: #666;
                        }
                        .link-container {
                            margin-top: 10px;
                        }
                        .link-item {
                            margin-bottom: 8px;
                            word-break: break-all;
                        }
                        .link-item a {
                            color: #3498db;
                            text-decoration: none;
                            padding: 4px 8px;
                            border-radius: 4px;
                            display: inline-block;
                            border: 1px solid #3498db;
                            transition: all 0.3s;
                        }
                        .link-item a:hover {
                            background-color: #3498db;
                            color: white;
                            text-decoration: underline;
                        }
                    </style>
                </head>
                <body>
                    <div class="itemTitle">
                        <h1>${pageTitle}</h1>
                    </div>
                    <div class="card-container">
                        ${entries.map(entry => renderCard(entry)).join("")}
                    </div>
                </body>
                </html>
            `);
            newWindow.document.close();
        })
        .catch(error => {
            console.error("加载数据失败:", error);
            alert("加载数据失败: " + error.message);
        });
}

// 修正后的renderCard函数
function renderCard(entry) {
    return `
        <div class="card">
            <h3>${entry.text || "未命名条目"}</h3>
            
            <!-- 时间信息 -->
            ${entry.when.map(time => `
                <p>📅 时间: ${time.year}年${time.month}月${time.day}日 ${time.hour}时</p>
            `).join("")}

            <!-- 地点信息 -->
            ${entry.where.map(location => `
                <p>🌍 地点: ${location.city}市, ${location.province}</p>
                <p>📍 坐标: 纬度 ${location.coordinate[0].latitude}, 经度 ${location.coordinate[0].longitude}</p>
                <p>🏠 详细地址: ${location.detail || "暂无"}</p>
            `).join("")}

            <!-- 产品信息 -->
            <p>💰 价格: ${entry.price || "暂无"} ${entry.unit || ""}</p>
            <p>📏 规格: ${entry.norm || "暂无"}</p>

            <!-- 链接 -->
            ${entry.image && entry.image.length > 0 ? `
                <div class="link-container">
                    <p>🔗 相关链接:</p>
                    ${entry.image.map(link => `
                        <div class="link-item">
                            <a href="${link}" target="_blank" rel="noopener noreferrer">
                                ${link}
                            </a>
                        </div>
                    `).join("")}
                </div>
            ` : ""}
        </div>
    `;
}