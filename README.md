# 🤖 AI Workout Planner

An intelligent workout generator that creates personalized workouts based on your time, goals, equipment, and experience level.

## ✨ Features

- **🎯 Goal-Based Planning**: Generate workouts for strength, muscle gain, weight loss, cardio, endurance, and general fitness
- **⏰ Time Optimization**: Create workouts that fit your available time (15 minutes to 2+ hours)
- **🏋️ Equipment Matching**: Automatically selects exercises based on your available equipment
- **📊 Experience Level**: Adapts workout difficulty to your fitness level (beginner, intermediate, advanced)
- **🎨 Multiple Workout Types**: Strength, cardio, HIIT, full body, upper/lower body, and core-focused workouts
- **📅 Weekly Planning**: Generate complete weekly workout schedules
- **💾 Save & Export**: Save workouts as JSON files for future reference
- **📱 Easy to Use**: Simple command-line interface with interactive prompts

## 🚀 Quick Start

### Installation

1. **Clone or download** this repository
2. **Install Python dependencies** (if needed):
   ```bash
   pip install json datetime random logging
   ```
   *Note: All dependencies are built-in Python modules*

### Basic Usage

Run the main workout planner:

```bash
python workout_planner.py
```

The script will prompt you for:
- Available time (in minutes)
- Your fitness goal
- Experience level
- Available equipment

### Example Usage

```bash
# Generate a 30-minute bodyweight workout
python workout_planner.py

# Run example workouts
python example_workout.py

# Generate a weekly plan
python example_workout.py  # Choose option 2
```

## 🎯 Supported Goals

| Goal | Description | Recommended Workout Types |
|------|-------------|---------------------------|
| **Strength** | Build maximum strength | Strength training |
| **Muscle Gain** | Build muscle mass | Strength, Full Body |
| **Weight Loss** | Lose weight and burn calories | HIIT, Cardio |
| **Cardio** | Improve cardiovascular fitness | Cardio, HIIT |
| **Endurance** | Build muscular and cardiovascular endurance | Cardio, Full Body |
| **General Fitness** | Overall fitness and health | Full Body, Cardio |
| **Toning** | Tone muscles and improve definition | Full Body, Strength |

## 🏋️ Supported Equipment

| Equipment | Description | Exercise Examples |
|-----------|-------------|-------------------|
| **bodyweight** | No equipment needed | Push-ups, squats, planks |
| **dumbbells** | Adjustable or fixed weights | Dumbbell press, rows, curls |
| **barbell** | Olympic or standard barbell | Deadlifts, squats, bench press |
| **bench** | Flat, incline, or decline bench | Bench press, dumbbell flyes |
| **rack** | Power rack or squat rack | Barbell squats, overhead press |
| **pull-up bar** | Doorway or wall-mounted | Pull-ups, chin-ups |
| **cable machine** | Gym cable machine | Lat pulldowns, face pulls |
| **treadmill** | Running machine | Running, walking |
| **bike** | Stationary or outdoor bike | Cycling |
| **jump rope** | Skipping rope | Jump rope cardio |

## 📊 Workout Types

### Strength Training
- **Focus**: Build muscle and strength
- **Sets**: 3-5 sets
- **Reps**: 1-6 reps (heavy weight)
- **Rest**: 2-3 minutes between sets

### Cardio
- **Focus**: Improve cardiovascular fitness
- **Duration**: 20-60 minutes
- **Intensity**: Moderate to high
- **Rest**: Minimal rest periods

### HIIT (High-Intensity Interval Training)
- **Focus**: Maximum calorie burn
- **Work**: 30-60 seconds high intensity
- **Rest**: 15-30 seconds rest
- **Rounds**: 3-5 rounds per exercise

### Full Body
- **Focus**: Complete body workout
- **Muscle Groups**: All major muscle groups
- **Sets**: 2-3 sets per exercise
- **Rest**: 1-2 minutes between exercises

### Upper Body
- **Focus**: Chest, back, shoulders, arms
- **Exercises**: Push-ups, rows, presses
- **Sets**: 3-4 sets per exercise
- **Rest**: 1-2 minutes between sets

### Lower Body
- **Focus**: Legs and core
- **Exercises**: Squats, lunges, deadlifts
- **Sets**: 3-4 sets per exercise
- **Rest**: 1-2 minutes between sets

### Core
- **Focus**: Abdominal and core muscles
- **Exercises**: Planks, crunches, twists
- **Sets**: 2-3 sets per exercise
- **Rest**: 30-60 seconds between sets

## 🎨 Customization Options

### Focus Areas
You can specify which muscle groups to focus on:
- `chest` - Pectoral muscles
- `back` - Latissimus dorsi, rhomboids
- `legs` - Quadriceps, hamstrings, glutes
- `shoulders` - Deltoids
- `arms` - Biceps, triceps
- `core` - Abdominals, obliques

### Experience Levels
- **Beginner**: Focus on form, lighter weights, more reps
- **Intermediate**: Moderate weights, balanced sets/reps
- **Advanced**: Heavy weights, lower reps, complex movements

### Time Optimization
The planner automatically:
- Calculates exercise duration based on your available time
- Adjusts sets and reps to fit your schedule
- Includes warm-up and cool-down periods
- Estimates total workout duration

## 📁 File Structure

```
workout-planner/
├── workout_planner.py      # Main workout planner script
├── workout_data.json       # Exercise database and configurations
├── example_workout.py      # Example usage and weekly planner
└── README.md              # This documentation
```

## 🔧 Advanced Usage

### Programmatic Usage

```python
from workout_planner import WorkoutPlanner

# Create planner instance
planner = WorkoutPlanner()

# Set user preferences
preferences = {
    'time_available': 45,
    'goal': 'muscle_gain',
    'equipment': ['dumbbells', 'bench'],
    'experience_level': 'intermediate',
    'focus_areas': ['chest', 'back']
}

planner.set_user_preferences(preferences)

# Generate workout
workout = planner.generate_workout()

# Display workout
planner.print_workout(workout)

# Save workout
planner.save_workout(workout, 'my_workout.json')
```

### Weekly Planning

```python
# Generate a complete weekly plan
weekly_schedule = {
    'Monday': {'type': 'full_body', 'focus': None},
    'Tuesday': {'type': 'cardio', 'focus': None},
    'Wednesday': {'type': 'upper_body', 'focus': ['chest', 'back']},
    'Thursday': {'type': 'cardio', 'focus': None},
    'Friday': {'type': 'lower_body', 'focus': ['legs']},
    'Saturday': {'type': 'hiit', 'focus': None},
    'Sunday': {'type': 'core', 'focus': ['core']}
}
```

## 📊 Output Format

The planner generates structured workout data:

```json
{
  "date": "2024-01-15",
  "workout_type": "full_body",
  "goal": "muscle_gain",
  "total_time": 45,
  "experience_level": "intermediate",
  "equipment_used": ["dumbbells", "bench"],
  "warmup": [...],
  "exercises": [
    {
      "name": "Dumbbell Bench Press",
      "muscle_group": "chest",
      "sets": 3,
      "reps": 10,
      "rest_time": 90,
      "equipment": ["dumbbells", "bench"],
      "difficulty": "intermediate",
      "notes": "Focus on controlled movement"
    }
  ],
  "cooldown": [...],
  "estimated_duration": 42
}
```

## 🛠️ Customization

### Adding New Exercises

Edit `workout_data.json` to add new exercises:

```json
{
  "name": "Your Exercise",
  "equipment": ["required_equipment"],
  "difficulty": "beginner|intermediate|advanced",
  "time_per_set": 60,
  "description": "Exercise description"
}
```

### Modifying Workout Types

Update workout type configurations in `workout_data.json`:

```json
{
  "your_workout_type": {
    "description": "Your workout description",
    "focus": ["strength|cardio"],
    "rest_between_sets": 90,
    "rest_between_exercises": 120
  }
}
```

## 🎯 Tips for Best Results

1. **Be Honest About Equipment**: Only list equipment you actually have access to
2. **Realistic Time Estimates**: Include travel time and setup in your time calculation
3. **Progressive Overload**: Gradually increase weights or difficulty over time
4. **Consistency**: Stick to your workout schedule for best results
5. **Rest Days**: Include rest days in your weekly plan
6. **Form First**: Always prioritize proper form over weight or speed

## 🔒 Safety Notes

- **Consult a Doctor**: Get medical clearance before starting a new exercise program
- **Proper Form**: Learn proper exercise form before increasing weight
- **Warm Up**: Always include a proper warm-up
- **Listen to Your Body**: Stop if you feel pain or discomfort
- **Hydration**: Stay hydrated during workouts
- **Progression**: Gradually increase intensity over time

## 🤝 Contributing

To add new exercises or improve the planner:

1. **Add Exercises**: Update `workout_data.json` with new exercises
2. **Improve Logic**: Enhance the workout generation algorithms
3. **Add Features**: Implement new workout types or customization options
4. **Bug Fixes**: Report and fix any issues

## 📝 License

This project is provided as-is for educational and personal use.

## 🆘 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the example files
3. Test with different parameters
4. Ensure all required files are present

---

**Happy Training! 💪** 