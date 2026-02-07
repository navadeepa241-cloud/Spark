import pandas as pd
import json

# Read the CSV file
df = pd.read_csv("weather.csv")

# Convert date to datetime and extract day of week
df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.day_name()

# Classify each day based on temperature
def classify_mood(temp):
    if temp > 30:
        return "Hot"
    elif temp < 15:
        return "Cold"
    else:
        return "Normal"

df['mood'] = df['temperature_c'].apply(classify_mood)

# Format date back to string for display
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Get statistics
hot_count = len(df[df['mood'] == 'Hot'])
cold_count = len(df[df['mood'] == 'Cold'])
normal_count = len(df[df['mood'] == 'Normal'])
total_count = len(df)

# Convert dataframe to JSON for web display
data_json = df.to_json(orient='records')

# Create HTML page
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Mood Classifier</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            color: white;
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card.hot {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .stat-card.cold {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        
        .stat-card.normal {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }}
        
        .stat-card.total {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-label {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin-top: 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
        }}
        
        tr:hover {{
            background-color: #f5f5f5;
        }}
        
        .mood-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }}
        
        .mood-hot {{
            background-color: #f5576c;
            color: white;
        }}
        
        .mood-cold {{
            background-color: #4facfe;
            color: white;
        }}
        
        .mood-normal {{
            background-color: #43e97b;
            color: white;
        }}
        
        .filter-buttons {{
            margin: 20px 0;
            text-align: center;
        }}
        
        .filter-btn {{
            padding: 10px 25px;
            margin: 0 10px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .filter-btn:hover {{
            transform: scale(1.05);
        }}
        
        .filter-btn.active {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        
        .filter-btn.all {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
        }}
        
        .filter-btn.hot {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}
        
        .filter-btn.cold {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }}
        
        .filter-btn.normal {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather Mood Classifier</h1>
        
        <div class="stats-container">
            <div class="stat-card hot">
                <div class="stat-label">🔥 Hot Days</div>
                <div class="stat-number">{hot_count}</div>
                <div class="stat-label">&gt; 30°C</div>
            </div>
            <div class="stat-card cold">
                <div class="stat-label">❄️ Cold Days</div>
                <div class="stat-number">{cold_count}</div>
                <div class="stat-label">&lt; 15°C</div>
            </div>
            <div class="stat-card normal">
                <div class="stat-label">🌤️ Normal Days</div>
                <div class="stat-number">{normal_count}</div>
                <div class="stat-label">15-30°C</div>
            </div>
            <div class="stat-card total">
                <div class="stat-label">📅 Total Days</div>
                <div class="stat-number">{total_count}</div>
                <div class="stat-label">3 Months</div>
            </div>
        </div>
        
        <div class="filter-buttons">
            <button class="filter-btn all active" onclick="filterData('all')">All Days</button>
            <button class="filter-btn hot" onclick="filterData('Hot')">Hot</button>
            <button class="filter-btn cold" onclick="filterData('Cold')">Cold</button>
            <button class="filter-btn normal" onclick="filterData('Normal')">Normal</button>
        </div>
        
        <div class="table-container">
            <table id="weatherTable">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Day</th>
                        <th>Temperature (°C)</th>
                        <th>Mood</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        const weatherData = {data_json};
        let currentFilter = 'all';
        
        function displayData(data) {{
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            
            data.forEach(row => {{
                const tr = document.createElement('tr');
                const moodClass = 'mood-' + row.mood.toLowerCase();
                
                tr.innerHTML = `
                    <td>${{row.date}}</td>
                    <td>${{row.day_of_week}}</td>
                    <td>${{row.temperature_c}}°C</td>
                    <td><span class="mood-badge ${{moodClass}}">${{row.mood}}</span></td>
                `;
                tbody.appendChild(tr);
            }});
        }}
        
        function filterData(mood) {{
            currentFilter = mood;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Filter and display data
            if (mood === 'all') {{
                displayData(weatherData);
            }} else {{
                const filtered = weatherData.filter(row => row.mood === mood);
                displayData(filtered);
            }}
        }}
        
        // Initial display
        displayData(weatherData);
    </script>
</body>
</html>
"""

# Write HTML file
with open('weather_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Web page created successfully!")
print("📄 File: weather_dashboard.html")
print("\nTo view the page, open 'weather_dashboard.html' in your web browser")
