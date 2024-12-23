// 在这里添加任何需要的JavaScript功能
console.log('应用已加载'); 

// 添加站点自动完成功能
async function initStationAutocomplete() {
    const response = await fetch('/api/stations');
    const stations = await response.json();
    
    const departureInput = document.getElementById('departure');
    const arrivalInput = document.getElementById('arrival');
    
    // 使用datalist实现自动完成
    const datalist = document.createElement('datalist');
    datalist.id = 'stations-list';
    stations.forEach(station => {
        const option = document.createElement('option');
        option.value = station.name;
        datalist.appendChild(option);
    });
    
    document.body.appendChild(datalist);
    departureInput.setAttribute('list', 'stations-list');
    arrivalInput.setAttribute('list', 'stations-list');
}

// 添加高级搜索功能
async function searchByType(type) {
    const departure = document.getElementById('departure').value;
    const arrival = document.getElementById('arrival').value;
    
    const response = await fetch('/api/advanced_search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `type=${type}&departure=${departure}&arrival=${arrival}`
    });
    
    const data = await response.json();
    if (data.status === 'success') {
        displaySearchResults(data.data);
    } else {
        alert('查询失败，请重试');
    }
}

// 显示查询结果
function displaySearchResults(trains) {
    const resultsDiv = document.getElementById('search-results');
    if (!resultsDiv) return;
    
    let html = '<table class="train-table">';
    html += `<thead>
        <tr>
            <th>车次</th>
            <th>出发站</th>
            <th>到达站</th>
            <th>用时</th>
        </tr>
    </thead>
    <tbody>`;
    
    trains.forEach(train => {
        html += `<tr>
            <td>${train.train_no}</td>
            <td>${train.departure}</td>
            <td>${train.arrival}</td>
            <td>${train.duration}</td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    resultsDiv.innerHTML = html;
}

// 添加中转查询功能
async function searchTransfer() {
    const departure = document.getElementById('departure').value;
    const arrival = document.getElementById('arrival').value;
    
    const response = await fetch('/api/transfer_search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `departure=${departure}&arrival=${arrival}`
    });
    
    const data = await response.json();
    if (data.status === 'success') {
        displayTransferResults(data.data);
    }
}

function displayTransferResults(routes) {
    const resultsDiv = document.getElementById('search-results');
    if (!resultsDiv) return;
    
    let html = '<h3>中转路线查询结果</h3>';
    html += '<div class="transfer-routes">';
    
    routes.forEach((route, index) => {
        html += `
            <div class="transfer-route">
                <h4>方案 ${index + 1}</h4>
                <div class="transfer-info">
                    <p>中转站：${route.transfer_station}</p>
                    <div class="route-leg">
                        <h5>第一程</h5>
                        <p>车次：${route.first_train.train_no}</p>
                        <p>${route.first_train.departure} → ${route.first_train.arrival}</p>
                        <p>时间：${route.first_train.departure_time} - ${route.first_train.arrival_time}</p>
                    </div>
                    <div class="route-leg">
                        <h5>第二程</h5>
                        <p>车次：${route.second_train.train_no}</p>
                        <p>${route.second_train.departure} → ${route.second_train.arrival}</p>
                        <p>时间：${route.second_train.departure_time} - ${route.second_train.arrival_time}</p>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    resultsDiv.innerHTML = html;
}

// 站点切换功能
function switchStations() {
    const departure = document.getElementById('departure');
    const arrival = document.getElementById('arrival');
    const temp = departure.value;
    departure.value = arrival.value;
    arrival.value = temp;
}

// 日期初始化
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date();
        const maxDate = new Date();
        maxDate.setDate(today.getDate() + 15); // 最多预订15天后的票

        const todayStr = today.toISOString().split('T')[0];
        const maxDateStr = maxDate.toISOString().split('T')[0];

        dateInput.value = todayStr;
        dateInput.min = todayStr;
        dateInput.max = maxDateStr;
    }
    
    initStationAutocomplete();
});

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initStationAutocomplete();
    
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
        dateInput.min = today;
    }
}); 