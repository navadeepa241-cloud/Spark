import pandas as pd

# Read the CSV file
df = pd.read_csv("weather.csv")

# Convert date to datetime and extract day of week
df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.day_name()

print("Original Data:")
print(df[['date', 'day_of_week', 'temperature_c']])
print()

# Classify each day based on temperature
def classify_mood(temp):
    if temp > 30:
        return "Hot"
    elif temp < 15:
        return "Cold"
    else:
        return "Normal"

df['mood'] = df['temperature_c'].apply(classify_mood)

# Reorder columns for better display
df = df[['date', 'day_of_week', 'temperature_c', 'mood']]

print("Data with Mood Classification:")
print(df)
print()

# Count how many days fall into each category
mood_counts = df['mood'].value_counts()

print("Mood Category Counts:")
print(mood_counts)
print()

# Print detailed statistics
hot_count = len(df[df['mood'] == 'Hot'])
cold_count = len(df[df['mood'] == 'Cold'])
normal_count = len(df[df['mood'] == 'Normal'])

print("Summary:")
print(f"Hot days: {hot_count}")
print(f"Cold days: {cold_count}")
print(f"Normal days: {normal_count}")
print(f"Total days: {len(df)}")
print()

# Write the result to a new CSV file
output_path = "weather_with_mood.csv"
df.to_csv(output_path, index=False)

print(f"Output saved to: {output_path}")
