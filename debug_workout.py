#!/usr/bin/env python3
"""
Debug script to see the actual workout structure
"""

from ai_workout_planner_simple import SimpleAIWorkoutPlanner
import json

def debug_workout_structure():
    """Debug the workout structure to see what's causing the error."""
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
        
        print("\n=== WORKOUT STRUCTURE ===")
        print(f"Workout type: {type(workout)}")
        print(f"Workout keys: {list(workout.keys())}")
        
        print("\n=== WORKOUT DATA ===")
        print(json.dumps(workout, indent=2))
        
        # Test accessing goal
        print("\n=== TESTING GOAL ACCESS ===")
        try:
            goal = workout.get('goal')
            print(f"workout.get('goal'): {goal}")
        except Exception as e:
            print(f"Error accessing goal: {e}")
        
        try:
            goal = workout.get('user_preferences', {}).get('goal')
            print(f"workout.get('user_preferences', {{}}).get('goal'): {goal}")
        except Exception as e:
            print(f"Error accessing user_preferences.goal: {e}")
        
        # Test template rendering
        print("\n=== TESTING TEMPLATE ACCESS ===")
        from flask import Flask, render_template_string
        
        app = Flask(__name__)
        with app.app_context():
            template = """
            <div>
                <p>Goal: {{ workout.get('goal', 'No goal') }}</p>
                <p>User Goal: {{ workout.get('user_preferences', {}).get('goal', 'No user goal') }}</p>
            </div>
            """
            try:
                result = render_template_string(template, workout=workout)
                print("Template rendering successful")
                print(result)
            except Exception as e:
                print(f"Template rendering error: {e}")
        
    except Exception as e:
        print(f"Error in debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_workout_structure() 