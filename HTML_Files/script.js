function loadContent() {
    const pageTitle = document.title;
    const currentPage = location.pathname.split("/").pop().replace(".html", "");

    fetch("https://1028867764.github.io/AEcoHTML/HTML_Files/data.json")
        .then(response => response.json())
        .then(data => {
            const entries = data[currentPage];
            if (!entries || !entries.length) throw new Error("未找到数据");

            // 默认按时间从新到旧排序
            const sortedByDate = [...entries].sort((a, b) => {
                const latestA = getLatestTimestamp(a.when);
                const latestB = getLatestTimestamp(b.when);
                return latestB - latestA; // 新日期在前
            });

            const newWindow = window.open("", "_blank");
            
            // 将 renderCard 函数转换为字符串以便注入
            const renderCardString = renderCard.toString();
            
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
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            gap: 20px;
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }
                        .card {
                            background: white;
                            border-radius: 8px;
                            padding: 20px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            width: 100%;
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
                        .sort-buttons {
                            display: flex;
                            justify-content: center;
                            gap: 10px;
                            margin-bottom: 20px;
                        }
                        .sort-btn {
                            padding: 8px 16px;
                            background-color: #3498db;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            cursor: pointer;
                            transition: background-color 0.3s;
                        }
                        .sort-btn:hover {
                            background-color: #2980b9;
                        }
                    </style>
                </head>
                <body>
                    <div class="itemTitle">
                        <h1>${pageTitle}</h1>
                    </div>
                    <div class="sort-buttons">
                        <button class="sort-btn" onclick="sortByPrice('asc')">价格升序</button>
                        <button class="sort-btn" onclick="sortByPrice('desc')">价格降序</button>
                        <button class="sort-btn" id="timeSortBtn" onclick="toggleTimeSort()">日期从新到旧</button>
                    </div>
                    <div class="card-container" id="cardContainer">
                        ${sortedByDate.map(entry => renderCard(entry)).join("")}
                    </div>

                    <script>
                        // 注入 renderCard 函数
                        ${renderCardString}
                        
                        let allEntries = ${JSON.stringify(sortedByDate)};
                        let isNewToOld = true; // 初始状态是从新到旧
                        
                        // 获取最新时间戳
                        function getLatestTimestamp(whenArray) {
                            if (!whenArray || !whenArray.length) return 0;
                            const latest = whenArray.reduce((latest, time) => {
                                const timestamp = new Date(
                                    time.year, 
                                    time.month - 1, 
                                    time.day, 
                                    time.hour
                                ).getTime();
                                return timestamp > latest ? timestamp : latest;
                            }, 0);
                            return latest;
                        }
                        
                        // 价格排序
                        function sortByPrice(order) {
                            const sorted = [...allEntries].sort((a, b) => {
                                const priceA = parseFloat(a.price) || 0;
                                const priceB = parseFloat(b.price) || 0;
                                return order === 'asc' ? priceA - priceB : priceB - priceA;
                            });
                            document.getElementById('cardContainer').innerHTML = 
                                sorted.map(entry => renderCard(entry)).join('');
                            
                            // 重置时间排序状态
                            isNewToOld = true;
                            document.getElementById('timeSortBtn').textContent = '日期从新到旧';
                        }
                        
                        // 切换时间排序
                        function toggleTimeSort() {
                            isNewToOld = !isNewToOld;
                            const btn = document.getElementById('timeSortBtn');
                            btn.textContent = isNewToOld ? '日期从新到旧' : '日期从旧到新';
                            
                            const sorted = [...allEntries].sort((a, b) => {
                                const latestA = getLatestTimestamp(a.when);
                                const latestB = getLatestTimestamp(b.when);
                                return isNewToOld ? latestB - latestA : latestA - latestB;
                            });
                            
                            document.getElementById('cardContainer').innerHTML = 
                                sorted.map(entry => renderCard(entry)).join('');
                        }
                    </script>
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

// 辅助函数：获取最新时间戳
function getLatestTimestamp(whenArray) {
    if (!whenArray || !whenArray.length) return 0;
    const latest = whenArray.reduce((latest, time) => {
        const timestamp = new Date(
            time.year, 
            time.month - 1, // 月份从0开始
            time.day, 
            time.hour
        ).getTime();
        return timestamp > latest ? timestamp : latest;
    }, 0);
    return latest;
}

// 渲染卡片函数
function renderCard(entry) {
    return `
        <div class="card">
            <h3>${entry.text || "未命名条目"}</h3>
            
            <!-- 时间信息 -->
            ${entry.when.map(time => `
                <p>📅 时间: ${time.year}年${time.month}月${time.day}日${time.hour}时</p>
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