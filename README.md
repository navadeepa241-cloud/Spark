# Weather Mood Classifier

A simple PySpark project that classifies daily weather based on temperature.

## Requirements
- Python 3.x
- PySpark

## Installation
```bash
pip install pyspark
```

## Usage
Run the program:
```bash
python weather_mood_classifier.py
```

## Classification Rules
- **Hot**: temperature > 30°C
- **Cold**: temperature < 15°C
- **Normal**: 15°C ≤ temperature ≤ 30°C

## Input
`weather.csv` - Contains columns:
- date
- temperature_c

## Output
`weather_with_mood.csv` - Original data plus:
- mood (Hot/Cold/Normal)

The program also prints statistics showing how many days fall into each category.
