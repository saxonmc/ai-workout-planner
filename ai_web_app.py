#!/usr/bin/env python3
"""
AI Workout Planner Web App

A Flask web application that provides an AI-powered workout planning interface
with machine learning capabilities for personalized recommendations.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from ai_workout_planner import AIWorkoutPlanner
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'ai_workout_planner_secret_key_2024'

# Initialize AI planner
planner = AIWorkoutPlanner()

@app.route('/')
def index():
    """Main page with workout generation form."""
    return render_template('ai_index.html')

@app.route('/generate_workout', methods=['POST'])
def generate_workout():
    """Generate AI-powered workout."""
    try:
        # Get form data
        preferences = {
            'time_available': int(request.form.get('time_available', 45)),
            'goal': request.form.get('goal', 'bjj_performance'),
            'equipment': request.form.getlist('equipment'),
            'experience_level': request.form.get('experience_level', 'intermediate'),
            'focus_areas': request.form.getlist('focus_areas')
        }
        
        # Set user preferences
        planner.set_user_preferences(preferences)
        
        # Generate AI workout
        workout = planner.generate_workout()
        
        # Save workout
        planner.save_workout(workout)
        
        # Store in session for feedback
        session['current_workout'] = workout
        
        return render_template('ai_workout_result.html', workout=workout)
        
    except Exception as e:
        logger.error(f"Error generating workout: {e}")
        return render_template('ai_error.html', error=str(e))

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit workout feedback for AI learning."""
    try:
        workout_id = request.form.get('workout_id')
        
        # Get feedback data
        feedback = {
            'difficulty_rating': int(request.form.get('difficulty_rating', 5)),
            'enjoyment_rating': int(request.form.get('enjoyment_rating', 5)),
            'completion_rate': float(request.form.get('completion_rate', 0.5)),
            'performance_notes': request.form.get('performance_notes', ''),
            'exercise_ratings': {}
        }
        
        # Get exercise ratings
        for key, value in request.form.items():
            if key.startswith('exercise_rating_'):
                exercise_name = key.replace('exercise_rating_', '')
                feedback['exercise_ratings'][exercise_name] = int(value)
        
        # Record feedback for AI learning
        planner.record_workout_feedback(workout_id, feedback)
        
        return render_template('ai_feedback_success.html', feedback=feedback)
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return render_template('ai_error.html', error=str(e))

@app.route('/insights')
def user_insights():
    """Display AI-generated user insights."""
    try:
        insights = planner.get_user_insights()
        return render_template('ai_insights.html', insights=insights)
        
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        return render_template('ai_error.html', error=str(e))

@app.route('/history')
def workout_history():
    """Display workout history."""
    try:
        history = planner.user_history
        return render_template('ai_history.html', history=history)
        
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return render_template('ai_error.html', error=str(e))

@app.route('/api/workout', methods=['POST'])
def api_generate_workout():
    """API endpoint for generating workouts."""
    try:
        data = request.get_json()
        preferences = data.get('preferences', {})
        
        planner.set_user_preferences(preferences)
        workout = planner.generate_workout()
        
        return jsonify({
            'success': True,
            'workout': workout
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/feedback', methods=['POST'])
def api_submit_feedback():
    """API endpoint for submitting feedback."""
    try:
        data = request.get_json()
        workout_id = data.get('workout_id')
        feedback = data.get('feedback', {})
        
        planner.record_workout_feedback(workout_id, feedback)
        
        return jsonify({
            'success': True,
            'message': 'Feedback recorded successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/insights')
def api_get_insights():
    """API endpoint for getting user insights."""
    try:
        insights = planner.get_user_insights()
        
        return jsonify({
            'success': True,
            'insights': insights
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5001) 