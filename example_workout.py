#!/usr/bin/env python3
"""
Example usage of the AI Workout Planner

This script demonstrates different ways to use the workout planner
to generate personalized workouts.
"""

from workout_planner import WorkoutPlanner
import json

def main():
    """Demonstrate different workout generation scenarios."""
    
    planner = WorkoutPlanner()
    
    print("🤖 AI Workout Planner Examples")
    print("=" * 50)
    
    # Example 1: Quick 20-minute bodyweight workout
    print("\n1. Quick 20-minute bodyweight workout")
    print("-" * 40)
    
    preferences_1 = {
        'time_available': 20,
        'goal': 'general_fitness',
        'equipment': ['bodyweight'],
        'experience_level': 'beginner'
    }
    
    planner.set_user_preferences(preferences_1)
    workout_1 = planner.generate_workout()
    planner.print_workout(workout_1)
    
    # Example 2: Strength training with dumbbells
    print("\n2. 45-minute strength training with dumbbells")
    print("-" * 40)
    
    preferences_2 = {
        'time_available': 45,
        'goal': 'muscle_gain',
        'equipment': ['dumbbells', 'bench'],
        'experience_level': 'intermediate',
        'focus_areas': ['chest', 'back', 'shoulders']
    }
    
    planner.set_user_preferences(preferences_2)
    workout_2 = planner.generate_workout()
    planner.print_workout(workout_2)
    
    # Example 3: HIIT cardio workout
    print("\n3. 30-minute HIIT cardio workout")
    print("-" * 40)
    
    preferences_3 = {
        'time_available': 30,
        'goal': 'weight_loss',
        'equipment': ['bodyweight', 'jump rope'],
        'experience_level': 'intermediate',
        'workout_type': 'hiit'
    }
    
    planner.set_user_preferences(preferences_3)
    workout_3 = planner.generate_workout()
    planner.print_workout(workout_3)
    
    # Example 4: Full gym workout
    print("\n4. 60-minute full gym workout")
    print("-" * 40)
    
    preferences_4 = {
        'time_available': 60,
        'goal': 'strength',
        'equipment': ['barbell', 'rack', 'bench', 'dumbbells', 'cable machine'],
        'experience_level': 'advanced',
        'workout_type': 'full_body'
    }
    
    planner.set_user_preferences(preferences_4)
    workout_4 = planner.generate_workout()
    planner.print_workout(workout_4)
    
    # Example 5: Core-focused workout
    print("\n5. 25-minute core-focused workout")
    print("-" * 40)
    
    preferences_5 = {
        'time_available': 25,
        'goal': 'toning',
        'equipment': ['bodyweight'],
        'experience_level': 'beginner',
        'focus_areas': ['core']
    }
    
    planner.set_user_preferences(preferences_5)
    workout_5 = planner.generate_workout()
    planner.print_workout(workout_5)
    
    # Save all workouts
    print("\n💾 Saving all workouts...")
    workouts = [workout_1, workout_2, workout_3, workout_4, workout_5]
    
    for i, workout in enumerate(workouts, 1):
        filename = f"example_workout_{i}.json"
        planner.save_workout(workout, filename)
        print(f"   Saved {filename}")
    
    print("\n🎉 All examples completed!")
    print("Check the generated JSON files for the complete workout data.")

def generate_weekly_plan():
    """Generate a weekly workout plan."""
    
    planner = WorkoutPlanner()
    
    print("\n📅 Weekly Workout Plan Generator")
    print("=" * 50)
    
    # Get user preferences for the week
    time_per_day = int(input("How much time do you have per day? (minutes): "))
    goal = input("What's your main goal? (strength/cardio/weight_loss/muscle_gain/general_fitness): ").lower()
    experience_level = input("What's your experience level? (beginner/intermediate/advanced): ").lower()
    
    print("\nWhat equipment do you have? (comma-separated)")
    equipment_input = input("Equipment: ").strip()
    equipment = [eq.strip() for eq in equipment_input.split(',') if eq.strip()]
    
    # Define weekly schedule
    weekly_schedule = {
        'Monday': {'type': 'full_body', 'focus': None},
        'Tuesday': {'type': 'cardio', 'focus': None},
        'Wednesday': {'type': 'upper_body', 'focus': ['chest', 'back', 'shoulders']},
        'Thursday': {'type': 'cardio', 'focus': None},
        'Friday': {'type': 'lower_body', 'focus': ['legs', 'core']},
        'Saturday': {'type': 'hiit', 'focus': None},
        'Sunday': {'type': 'core', 'focus': ['core']}
    }
    
    weekly_workouts = {}
    
    for day, schedule in weekly_schedule.items():
        print(f"\n🏋️  Generating {day}'s workout...")
        
        preferences = {
            'time_available': time_per_day,
            'goal': goal,
            'equipment': equipment,
            'experience_level': experience_level,
            'workout_type': schedule['type'],
            'focus_areas': schedule['focus']
        }
        
        planner.set_user_preferences(preferences)
        workout = planner.generate_workout()
        
        weekly_workouts[day] = workout
        planner.print_workout(workout)
    
    # Save weekly plan
    weekly_filename = f"weekly_plan_{datetime.now().strftime('%Y%m%d')}.json"
    with open(weekly_filename, 'w') as f:
        json.dump(weekly_workouts, f, indent=2)
    
    print(f"\n💾 Weekly plan saved to {weekly_filename}")

if __name__ == "__main__":
    from datetime import datetime
    
    print("Choose an option:")
    print("1. Run example workouts")
    print("2. Generate weekly plan")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        main()
    elif choice == "2":
        generate_weekly_plan()
    else:
        print("Invalid choice. Running examples...")
        main() 