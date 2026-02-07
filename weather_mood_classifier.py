from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Weather Mood Classifier") \
    .getOrCreate()

# Read the CSV file
df = spark.read.csv("weather.csv", header=True, inferSchema=True)

print("Original Data:")
df.show()

# Classify each day based on temperature
df_with_mood = df.withColumn(
    "mood",
    when(col("temperature_c") > 30, "Hot")
    .when(col("temperature_c") < 15, "Cold")
    .otherwise("Normal")
)

print("\nData with Mood Classification:")
df_with_mood.show()

# Count how many days fall into each category
mood_counts = df_with_mood.groupBy("mood").count()

print("\nMood Category Counts:")
mood_counts.show()

# Print detailed statistics
hot_count = df_with_mood.filter(col("mood") == "Hot").count()
cold_count = df_with_mood.filter(col("mood") == "Cold").count()
normal_count = df_with_mood.filter(col("mood") == "Normal").count()

print(f"\nSummary:")
print(f"Hot days: {hot_count}")
print(f"Cold days: {cold_count}")
print(f"Normal days: {normal_count}")
print(f"Total days: {df_with_mood.count()}")

# Write the result to a new CSV file
output_path = "weather_with_mood.csv"
df_with_mood.coalesce(1).write.csv(output_path, header=True, mode="overwrite")

print(f"\nOutput saved to: {output_path}")

# Stop Spark Session
spark.stop()
