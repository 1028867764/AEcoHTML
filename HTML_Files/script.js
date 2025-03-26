function loadContent() {
  {
    // 获取当前页面的标题（来自<head><title>）
    const pageTitle = document.title;

    // 获取当前HTML文件名（不含扩展名）
    const currentPage = location.pathname
      .split("/")
      .pop() // 提取文件名
      .replace(".html", ""); // 移除扩展名

    // 加载JSON数据
    fetch("https://1028867764.github.io/AEcoHTML/HTML_Files/data.json")
      .then((response) => response.json())
      .then((data) => {
        const entries = data[currentPage]; // 获取当前页面对应的数组
        if (!entries || !entries.length) {
          throw new Error("未找到数据");
        }
        // 打开新窗口并显示内容；获取当前页面对应的内容
        const newWindow = window.open("", "_blank");
        newWindow.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>${pageTitle}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 20px }}

                        .itemTitle {
                        background-color: lightblue;  /* 浅蓝色背景 */
                        text-align: center;    /* 可选：内容居中 */
                        }

                        .card-container {
                            display: grid;
                            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                            gap: 20px;
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
                        }

                        .card p {
                            margin: 8px 0;
                            color: #666;
                        }

                        .card img {
                            max-width: 100%;
                            height: auto;
                            border-radius: 4px;
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
                <div>
                    <pre>${JSON.stringify(data[currentPage], null, 2)}</pre> 
                </div>
                <div class="card-container">
                        ${entries.map((entry) => renderCard(entry)).join("")}
                    </div>
                </body>
                </html>
            `);
        newWindow.document.close();
      })
      .catch((error) => {
        {
          console.error("加载数据失败:", error);
          alert("加载报价数据失败，请检查控制台");
        }
      });
  }
}

// 渲染单个卡片
function renderCard(entry) {
  return `
        <div class="card">
            <h3>${entry.text || "未命名条目"}</h3>
            
            <!-- 时间信息 -->
            ${entry.when
              .map(
                (time) => `
                <p>📅 时间: ${time.year}年${time.month}月${time.day}日 ${time.hour}时</p>
            `
              )
              .join("")}

            <!-- 地点信息 -->
            ${entry.where
              .map(
                (location) => `
                <p>🌍 地点: ${location.city}市, ${location.province}</p>
                <p>📍 坐标: ${location.coordinate[0].latitude}, ${location.coordinate[0].longitude}</p>
            `
              )
              .join("")}

            <!-- 价格/规格 -->
            <p>💰 价格: ${entry.price} ${entry.unit}</p>
            <p>📏 规格: ${entry.norm}</p>

            <!-- 图片 -->
            ${
              item.image && item.image.length > 0
                ? `
                <div class="data-section">
                    <h3>图片/视频</h3>
                    <div class="link-container">
                        ${item.image
                          .map(
                            (link) => `
                            <div class="link-item">
                                <a href="${link}" target="_blank" rel="noopener noreferrer">
                                    ${link}
                                </a>
                            </div>
                        `
                          )
                          .join("")}
                    </div>
                </div>
            `
                : ""
            }
        </div>
    `;
}
