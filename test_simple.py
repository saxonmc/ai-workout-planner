#!/usr/bin/env python3
"""
Simple test script to isolate the error
"""

from ai_workout_planner_simple import SimpleAIWorkoutPlanner
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_workout_generation():
    """Test workout generation to isolate the error."""
    try:
        print("Initializing AI planner...")
        planner = SimpleAIWorkoutPlanner()
        
        print("Setting user preferences...")
        preferences = {
            'time_available': 30,
            'goal': 'bjj_performance',
            'equipment': ['bodyweight'],
            'experience_level': 'intermediate',
            'focus_areas': []
        }
        
        planner.set_user_preferences(preferences)
        
        print("Generating workout...")
        workout = planner.generate_workout()
        
        print("Workout generated successfully!")
        print(f"Workout ID: {workout.get('id', 'N/A')}")
        print(f"Strength exercises: {len(workout.get('strength_exercises', []))}")
        print(f"Metcon exercises: {len(workout.get('metcon_exercises', []))}")
        print(f"Accessory exercises: {len(workout.get('accessory_exercises', []))}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_workout_generation() 