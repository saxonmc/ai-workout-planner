#!/usr/bin/env python3
"""
Web App for AI Workout Planner

A Flask web application that provides the workout planner functionality
through a mobile-friendly web interface.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from workout_planner import WorkoutPlanner
import json
from datetime import datetime

app = Flask(__name__)
planner = WorkoutPlanner()

@app.route('/')
def index():
    """Home page with workout planner form."""
    return render_template('index.html')

@app.route('/generate_workout', methods=['POST'])
def generate_workout():
    """Generate workout based on form data."""
    try:
        # Get form data
        time_available = int(request.form.get('time_available', 30))
        goal = request.form.get('goal', 'general_fitness')
        experience_level = request.form.get('experience_level', 'beginner')
        equipment = request.form.getlist('equipment')
        focus_areas = request.form.getlist('focus_areas')
        workout_type = request.form.get('workout_type', '')
        
        # Set preferences
        preferences = {
            'time_available': time_available,
            'goal': goal,
            'equipment': equipment,
            'experience_level': experience_level,
            'focus_areas': focus_areas
        }
        
        if workout_type:
            preferences['workout_type'] = workout_type
        
        planner.set_user_preferences(preferences)
        
        # Generate workout
        workout = planner.generate_workout()
        
        # Save workout with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workout_{timestamp}.json"
        planner.save_workout(workout, filename)
        
        return render_template('workout_result.html', workout=workout, filename=filename)
        
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/generate_workout', methods=['POST'])
def api_generate_workout():
    """API endpoint for generating workouts."""
    try:
        data = request.get_json()
        
        preferences = {
            'time_available': data.get('time_available', 30),
            'goal': data.get('goal', 'general_fitness'),
            'equipment': data.get('equipment', ['bodyweight']),
            'experience_level': data.get('experience_level', 'beginner'),
            'focus_areas': data.get('focus_areas', [])
        }
        
        if data.get('workout_type'):
            preferences['workout_type'] = data['workout_type']
        
        planner.set_user_preferences(preferences)
        workout = planner.generate_workout()
        
        return jsonify(workout)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/weekly_plan')
def weekly_plan():
    """Generate weekly workout plan."""
    return render_template('weekly_plan.html')

@app.route('/generate_weekly', methods=['POST'])
def generate_weekly():
    """Generate weekly workout plan."""
    try:
        time_per_day = int(request.form.get('time_per_day', 30))
        goal = request.form.get('goal', 'general_fitness')
        experience_level = request.form.get('experience_level', 'beginner')
        equipment = request.form.getlist('equipment')
        
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
        
        # Save weekly plan
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weekly_plan_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(weekly_workouts, f, indent=2)
        
        return render_template('weekly_result.html', weekly_workouts=weekly_workouts, filename=filename)
        
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/saved_workouts')
def saved_workouts():
    """Show saved workouts."""
    import os
    workouts = []
    
    for filename in os.listdir('.'):
        if filename.startswith('workout_') and filename.endswith('.json'):
            with open(filename, 'r') as f:
                workout_data = json.load(f)
                workouts.append({
                    'filename': filename,
                    'date': workout_data.get('date', 'Unknown'),
                    'workout_type': workout_data.get('workout_type', 'Unknown'),
                    'goal': workout_data.get('goal', 'Unknown'),
                    'duration': workout_data.get('estimated_duration', 0)
                })
    
    workouts.sort(key=lambda x: x['date'], reverse=True)
    return render_template('saved_workouts.html', workouts=workouts)

@app.route('/view_workout/<filename>')
def view_workout(filename):
    """View a specific saved workout."""
    try:
        with open(filename, 'r') as f:
            workout = json.load(f)
        return render_template('workout_result.html', workout=workout, filename=filename)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 