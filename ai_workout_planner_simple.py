#!/usr/bin/env python3
"""
AI Workout Planner (Simplified)

An intelligent workout generator that creates personalized workouts based on:
- Available time
- Fitness goals
- Available equipment
- Experience level
- User feedback and learning
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging
import pickle
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleAIWorkoutPlanner:
    """AI-powered workout planner with simplified machine learning capabilities."""
    
    def __init__(self, data_file: str = 'workout_data.json', model_file: str = 'simple_ai_model.pkl'):
        """
        Initialize the AI workout planner.
        
        Args:
            data_file (str): Path to workout data file
            model_file (str): Path to save/load AI model
        """
        self.data = self._load_workout_data(data_file)
        # Assign top-level keys for convenience (must be before model loading)
        self.exercises = self.data.get('exercises', [])
        self.workout_types = self.data.get('workout_types', {})
        self.muscle_groups = self.data.get('muscle_groups', {})
        self.model_file = model_file
        self.user_preferences = {}
        self.user_history = []
        self.exercise_performance = {}
        self.progress_tracker = {}
        # Simple AI Models (no scikit-learn dependency)
        self.exercise_weights = {}
        self.difficulty_adjustments = {}
        self.user_patterns = {}
        # Load or initialize models
        self._load_or_initialize_models()
    
    def _load_workout_data(self, data_file: str) -> Dict:
        """Load workout data from JSON file."""
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Workout data file {data_file} not found. Creating default data.")
            return self._create_default_data()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing workout data file: {e}")
            return self._create_default_data()
    
    def _create_default_data(self) -> Dict:
        """Create default workout data structure."""
        return {
            "exercises": [
                # Strength exercises
                {"name": "Push-ups", "type": "strength", "muscle_group": "chest", "equipment": ["bodyweight"], 
                 "difficulty": "beginner", "time_per_set": 60, "category": "compound", "bjj_focus": "upper_body_power"},
                {"name": "Dumbbell Bench Press", "type": "strength", "muscle_group": "chest", "equipment": ["dumbbells", "bench"], 
                 "difficulty": "intermediate", "time_per_set": 90, "category": "compound", "bjj_focus": "upper_body_power"},
                {"name": "Barbell Bench Press", "type": "strength", "muscle_group": "chest", "equipment": ["barbell", "bench", "rack"], 
                 "difficulty": "intermediate", "time_per_set": 120, "category": "compound", "bjj_focus": "upper_body_power"},
                {"name": "Pull-ups", "type": "strength", "muscle_group": "back", "equipment": ["pull-up bar"], 
                 "difficulty": "intermediate", "time_per_set": 60, "category": "compound", "bjj_focus": "grip_strength"},
                {"name": "Barbell Deadlift", "type": "strength", "muscle_group": "legs", "equipment": ["barbell"], 
                 "difficulty": "advanced", "time_per_set": 150, "category": "compound", "bjj_focus": "hip_power"},
                {"name": "Barbell Squat", "type": "strength", "muscle_group": "legs", "equipment": ["barbell", "rack"], 
                 "difficulty": "intermediate", "time_per_set": 120, "category": "compound", "bjj_focus": "leg_power"},
                {"name": "Kettlebell Swing", "type": "strength", "muscle_group": "legs", "equipment": ["kettlebell"], 
                 "difficulty": "intermediate", "time_per_set": 60, "category": "functional", "bjj_focus": "hip_power"},
                {"name": "Overhead Press", "type": "strength", "muscle_group": "shoulders", "equipment": ["dumbbells"], 
                 "difficulty": "intermediate", "time_per_set": 90, "category": "compound", "bjj_focus": "upper_body_power"},
                
                # Conditioning exercises
                {"name": "Burpees", "type": "conditioning", "muscle_group": "full_body", "equipment": ["bodyweight"], 
                 "difficulty": "intermediate", "time_per_set": 60, "category": "metcon", "bjj_focus": "explosive_power"},
                {"name": "Assault Bike", "type": "conditioning", "muscle_group": "cardio", "equipment": ["assault_bike"], 
                 "difficulty": "intermediate", "time_per_set": 120, "category": "cardio", "bjj_focus": "endurance"},
                {"name": "Wall Balls", "type": "conditioning", "muscle_group": "full_body", "equipment": ["medicine_ball"], 
                 "difficulty": "intermediate", "time_per_set": 60, "category": "metcon", "bjj_focus": "explosive_power"},
                {"name": "Box Jumps", "type": "conditioning", "muscle_group": "legs", "equipment": ["box"], 
                 "difficulty": "intermediate", "time_per_set": 60, "category": "explosive", "bjj_focus": "explosive_power"},
                {"name": "Thrusters", "type": "conditioning", "muscle_group": "full_body", "equipment": ["dumbbells"], 
                 "difficulty": "advanced", "time_per_set": 90, "category": "metcon", "bjj_focus": "explosive_power"},
                
                # Accessory exercises
                {"name": "Planks", "type": "accessory", "muscle_group": "core", "equipment": ["bodyweight"], 
                 "difficulty": "beginner", "time_per_set": 60, "category": "bodyweight", "bjj_focus": "core_strength"},
                {"name": "Russian Twists", "type": "accessory", "muscle_group": "core", "equipment": ["bodyweight"], 
                 "difficulty": "intermediate", "time_per_set": 60, "category": "bodyweight", "bjj_focus": "core_strength"},
                {"name": "Hanging Leg Raises", "type": "accessory", "muscle_group": "core", "equipment": ["pull-up bar"], 
                 "difficulty": "advanced", "time_per_set": 60, "category": "bodyweight", "bjj_focus": "core_strength"},
                {"name": "Farmer's Walks", "type": "accessory", "muscle_group": "full_body", "equipment": ["dumbbells"], 
                 "difficulty": "intermediate", "time_per_set": 90, "category": "functional", "bjj_focus": "grip_strength"},
                {"name": "Turkish Get-ups", "type": "accessory", "muscle_group": "full_body", "equipment": ["kettlebell"], 
                 "difficulty": "advanced", "time_per_set": 120, "category": "functional", "bjj_focus": "stabilization"}
            ],
            "workout_types": {
                "bjj_performance": {
                    "description": "BJJ-focused performance training",
                    "focus": ["strength", "conditioning", "accessory"],
                    "rest_between_sets": 90,
                    "rest_between_exercises": 120
                }
            }
        }
    
    def _load_or_initialize_models(self):
        """Load existing AI models or initialize new ones."""
        try:
            with open(self.model_file, 'rb') as f:
                models = pickle.load(f)
                self.exercise_weights = models.get('exercise_weights', {})
                self.difficulty_adjustments = models.get('difficulty_adjustments', {})
                self.user_patterns = models.get('user_patterns', {})
                logger.info("Loaded existing AI models")
        except FileNotFoundError:
            logger.info("No existing models found. Initializing new AI models.")
            self._initialize_models()
    
    def _initialize_models(self):
        """Initialize new AI models."""
        # Initialize exercise weights (preference scores)
        if hasattr(self, 'exercises') and self.exercises:
            for exercise in self.exercises:
                self.exercise_weights[exercise['name']] = 1.0
        else:
            # Fallback if exercises not loaded yet
            logger.warning("Exercises not loaded, initializing empty weights")
        
        # Initialize difficulty adjustments
        self.difficulty_adjustments = {
            'beginner': 0.0,
            'intermediate': 0.0,
            'advanced': 0.0
        }
        
        # Initialize user patterns
        self.user_patterns = {
            'preferred_equipment': {},
            'preferred_difficulty': 5.0,
            'completion_rate': 0.8,
            'enjoyment_threshold': 6.0
        }
    
    def _save_models(self):
        """Save AI models to file."""
        models = {
            'exercise_weights': self.exercise_weights,
            'difficulty_adjustments': self.difficulty_adjustments,
            'user_patterns': self.user_patterns
        }
        with open(self.model_file, 'wb') as f:
            pickle.dump(models, f)
        logger.info("AI models saved successfully")
    
    def set_user_preferences(self, preferences: Dict):
        """Set user preferences for workout generation."""
        self.user_preferences = preferences
        logger.info(f"User preferences set: {preferences}")
    
    def record_workout_feedback(self, workout_id: str, feedback: Dict):
        """
        Record user feedback on a completed workout for AI learning.
        
        Args:
            workout_id (str): ID of the completed workout
            feedback (Dict): User feedback including:
                - difficulty_rating: 1-10
                - enjoyment_rating: 1-10
                - completion_rate: 0.0-1.0
                - performance_notes: str
                - exercise_ratings: Dict[exercise_name, rating]
        """
        feedback['workout_id'] = workout_id
        feedback['timestamp'] = datetime.now().isoformat()
        self.user_history.append(feedback)
        
        # Update exercise performance data
        for exercise_name, rating in feedback.get('exercise_ratings', {}).items():
            if exercise_name not in self.exercise_performance:
                self.exercise_performance[exercise_name] = []
            self.exercise_performance[exercise_name].append(rating)
        
        # Learn from feedback
        self._learn_from_feedback(feedback)
        
        logger.info(f"Workout feedback recorded and learned: {feedback}")
    
    def _learn_from_feedback(self, feedback: Dict):
        """Learn from user feedback to improve future recommendations."""
        # Update exercise weights based on enjoyment
        enjoyment_rating = feedback.get('enjoyment_rating', 5)
        difficulty_rating = feedback.get('difficulty_rating', 5)
        completion_rate = feedback.get('completion_rate', 0.5)
        
        # Update user patterns
        self.user_patterns['preferred_difficulty'] = (
            self.user_patterns['preferred_difficulty'] * 0.7 + difficulty_rating * 0.3
        )
        self.user_patterns['completion_rate'] = (
            self.user_patterns['completion_rate'] * 0.7 + completion_rate * 0.3
        )
        self.user_patterns['enjoyment_threshold'] = (
            self.user_patterns['enjoyment_threshold'] * 0.7 + enjoyment_rating * 0.3
        )
        
        # Update exercise weights based on individual exercise ratings
        for exercise_name, rating in feedback.get('exercise_ratings', {}).items():
            if exercise_name in self.exercise_weights:
                # Increase weight for exercises user enjoys
                enjoyment_factor = (rating - 5) / 5.0  # -1 to 1
                self.exercise_weights[exercise_name] += enjoyment_factor * 0.1
                self.exercise_weights[exercise_name] = max(0.1, min(2.0, self.exercise_weights[exercise_name]))
        
        # Update difficulty adjustments based on experience level
        experience_level = self.user_preferences.get('experience_level', 'intermediate')
        difficulty_adjustment = (difficulty_rating - 5) / 10.0  # -0.5 to 0.5
        self.difficulty_adjustments[experience_level] += difficulty_adjustment * 0.1
        
        # Save updated models
        self._save_models()
    
    def predict_exercise_difficulty(self, exercise: Dict, user_context: Dict) -> float:
        """Predict difficulty rating for an exercise based on user context."""
        base_difficulty = self._difficulty_to_numeric(exercise.get('difficulty', 'beginner'))
        experience_level = user_context.get('experience_level', 'intermediate')
        
        # Apply learned difficulty adjustments
        adjustment = self.difficulty_adjustments.get(experience_level, 0.0)
        predicted_difficulty = base_difficulty + adjustment
        
        # Consider user's preferred difficulty
        user_preference = self.user_patterns.get('preferred_difficulty', 5.0)
        preference_factor = (user_preference - 5.0) / 5.0  # -1 to 1
        predicted_difficulty += preference_factor * 2.0
        
        return max(1, min(10, predicted_difficulty))
    
    def _difficulty_to_numeric(self, difficulty: str) -> float:
        """Convert difficulty to numeric value."""
        difficulties = {'beginner': 3, 'intermediate': 6, 'advanced': 8}
        return difficulties.get(difficulty, 5)
    
    def recommend_exercises(self, available_exercises: List[Dict], num_recommendations: int) -> List[Dict]:
        """Recommend exercises based on AI learning."""
        if not available_exercises:
            return []
        
        # Calculate recommendation scores
        exercise_scores = []
        for exercise in available_exercises:
            score = self._calculate_exercise_score(exercise)
            exercise_scores.append((exercise, score))
        
        # Sort by score and return top recommendations
        exercise_scores.sort(key=lambda x: x[1], reverse=True)
        return [exercise for exercise, _ in exercise_scores[:num_recommendations]]
    
    def _calculate_exercise_score(self, exercise: Dict) -> float:
        """Calculate AI recommendation score for an exercise."""
        base_score = 1.0
        
        # Exercise weight from learning
        exercise_weight = self.exercise_weights.get(exercise['name'], 1.0)
        base_score *= exercise_weight
        
        # Equipment preference
        equipment = exercise.get('equipment', [])
        for eq in equipment:
            if eq in self.user_patterns.get('preferred_equipment', {}):
                base_score *= 1.2
        
        # Difficulty preference
        predicted_difficulty = self.predict_exercise_difficulty(exercise, self.user_preferences)
        preferred_difficulty = self.user_patterns.get('preferred_difficulty', 5.0)
        difficulty_match = 1.0 - abs(predicted_difficulty - preferred_difficulty) / 10.0
        base_score *= (0.5 + difficulty_match * 0.5)
        
        # Random factor for variety
        base_score *= random.uniform(0.8, 1.2)
        
        return base_score
    
    def predict_progress(self, current_workout: Dict) -> Dict:
        """Predict user progress based on current workout and history."""
        if len(self.user_history) < 3:
            return self._default_progress_prediction()
        
        # Analyze recent performance
        recent_feedback = self.user_history[-3:]
        avg_difficulty = np.mean([f.get('difficulty_rating', 5) for f in recent_feedback])
        avg_enjoyment = np.mean([f.get('enjoyment_rating', 5) for f in recent_feedback])
        avg_completion = np.mean([f.get('completion_rate', 0.5) for f in recent_feedback])
        
        # Calculate progress score
        progress_score = 0.0
        
        # Higher completion rate = progress
        progress_score += avg_completion * 0.4
        
        # Stable or decreasing difficulty = progress
        if avg_difficulty <= self.user_patterns.get('preferred_difficulty', 5.0):
            progress_score += 0.3
        
        # High enjoyment = good progress
        if avg_enjoyment >= self.user_patterns.get('enjoyment_threshold', 6.0):
            progress_score += 0.3
        
        return {
            'predicted_progress': progress_score * 10,  # Scale to 0-10
            'confidence': min(0.9, len(self.user_history) / 10.0),
            'recommendations': self._generate_progress_recommendations(progress_score, avg_difficulty, avg_enjoyment)
        }
    
    def _default_progress_prediction(self) -> Dict:
        """Default progress prediction when insufficient data."""
        return {
            'predicted_progress': 5.0,
            'confidence': 0.3,
            'recommendations': ['Complete more workouts to get personalized insights', 'Focus on consistency']
        }
    
    def _generate_progress_recommendations(self, progress_score: float, avg_difficulty: float, avg_enjoyment: float) -> List[str]:
        """Generate recommendations based on predicted progress."""
        recommendations = []
        
        if progress_score > 0.7:
            recommendations.append('Excellent progress! Consider increasing workout intensity')
            recommendations.append('Great consistency - keep up the momentum')
        elif progress_score > 0.4:
            recommendations.append('Steady progress - maintain current training intensity')
            recommendations.append('Focus on form and technique')
        else:
            recommendations.append('Consider adjusting workout difficulty')
            recommendations.append('Focus on completing workouts consistently')
        
        if avg_difficulty > 8:
            recommendations.append('Workouts may be too difficult - consider scaling back')
        elif avg_difficulty < 4:
            recommendations.append('Consider increasing difficulty to continue progress')
        
        if avg_enjoyment < 5:
            recommendations.append('Try different exercise variations to increase enjoyment')
        
        return recommendations
    
    def generate_workout(self) -> Dict:
        """Generate a personalized workout using AI recommendations."""
        if not self.user_preferences:
            raise ValueError("User preferences must be set before generating workout")
        
        time_available = self.user_preferences.get('time_available', 60)
        goal = self.user_preferences.get('goal', 'general_fitness')
        equipment = self.user_preferences.get('equipment', ['bodyweight'])
        experience_level = self.user_preferences.get('experience_level', 'beginner')
        focus_areas = self.user_preferences.get('focus_areas', [])
        
        # Calculate time allocation
        strength_time = int(time_available * 0.4)
        metcon_time = int(time_available * 0.4)
        accessory_time = int(time_available * 0.2)
        
        # Generate sections using AI recommendations
        strength_exercises = self._generate_ai_strength_section(
            equipment, experience_level, focus_areas, strength_time
        )
        
        metcon_exercises = self._generate_ai_metcon_section(
            equipment, experience_level, focus_areas, metcon_time
        )
        
        accessory_exercises = self._generate_ai_accessory_section(
            equipment, experience_level, focus_areas, accessory_time
        )
        
        # Create workout
        workout = {
            'id': f"ai_workout_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'user_preferences': self.user_preferences,
            'strength_exercises': strength_exercises,
            'metcon_exercises': metcon_exercises,
            'accessory_exercises': accessory_exercises,
            'total_duration': time_available,
            'ai_generated': True
        }
        
        # Predict progress for this workout
        try:
            progress_prediction = self.predict_progress(workout)
            workout['progress_prediction'] = progress_prediction
        except Exception as e:
            logger.warning(f"Could not predict progress: {e}")
            workout['progress_prediction'] = self._default_progress_prediction()
        
        return workout
    
    def _generate_ai_strength_section(self, equipment: List[str], experience_level: str, 
                                    focus_areas: List[str], available_time: int) -> List[Dict]:
        """Generate strength exercises using AI recommendations."""
        available_exercises = []
        
        # Filter exercises
        for exercise in self.exercises:
            if (exercise.get('type') == 'strength' and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Use AI to recommend exercises
        num_exercises = min(4, max(2, available_time // 8))
        recommended_exercises = self.recommend_exercises(available_exercises, num_exercises)
        
        exercises = []
        for exercise in recommended_exercises:
            # Predict difficulty and adjust sets/reps accordingly
            predicted_difficulty = self.predict_exercise_difficulty(exercise, self.user_preferences)
            sets, reps = self._ai_determine_sets_reps(exercise, predicted_difficulty)
            rest_time = self._ai_determine_rest_time(exercise, predicted_difficulty)
            
            exercises.append({
                'name': exercise['name'],
                'muscle_group': exercise['muscle_group'],
                'sets': sets,
                'reps': reps,
                'rest_time': rest_time,
                'equipment': exercise['equipment'],
                'difficulty': exercise['difficulty'],
                'predicted_difficulty': predicted_difficulty,
                'ai_recommended': True,
                'notes': self._generate_ai_exercise_notes(exercise, sets, reps, predicted_difficulty)
            })
        
        return exercises
    
    def _generate_ai_metcon_section(self, equipment: List[str], experience_level: str, 
                                  focus_areas: List[str], available_time: int) -> List[Dict]:
        """Generate metcon exercises using AI recommendations."""
        available_exercises = []
        
        # Filter exercises
        for exercise in self.exercises:
            if (exercise.get('type') == 'conditioning' and
                exercise.get('category') in ['metcon', 'explosive', 'functional'] and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Use AI to recommend exercises
        num_exercises = min(5, max(3, available_time // 5))
        recommended_exercises = self.recommend_exercises(available_exercises, num_exercises)
        
        # Determine workout format based on user history
        formats = ['amrap', 'emom', 'fortime']
        if self.user_history:
            # Analyze which formats user enjoys most
            format_preferences = self._analyze_format_preferences()
            workout_format = max(format_preferences, key=format_preferences.get)
        else:
            workout_format = random.choice(formats)
        
        exercises = []
        for exercise in recommended_exercises:
            predicted_difficulty = self.predict_exercise_difficulty(exercise, self.user_preferences)
            reps = self._ai_determine_metcon_reps(exercise, predicted_difficulty)
            
            exercises.append({
                'name': exercise['name'],
                'muscle_group': exercise['muscle_group'],
                'reps': reps,
                'equipment': exercise['equipment'],
                'difficulty': exercise['difficulty'],
                'bjj_focus': exercise.get('bjj_focus'),
                'workout_format': workout_format.upper(),
                'predicted_difficulty': predicted_difficulty,
                'ai_recommended': True,
                'notes': f"AI-recommended {workout_format.upper()}: {reps} reps per round"
            })
        
        return exercises
    
    def _generate_ai_accessory_section(self, equipment: List[str], experience_level: str, 
                                     focus_areas: List[str], available_time: int) -> List[Dict]:
        """Generate accessory exercises using AI recommendations."""
        available_exercises = []
        
        # Filter exercises
        for exercise in self.exercises:
            if (exercise.get('type') == 'accessory' and
                exercise.get('category') in ['bodyweight', 'functional'] and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Use AI to recommend exercises
        num_exercises = min(2, max(1, available_time // 10))
        recommended_exercises = self.recommend_exercises(available_exercises, num_exercises)
        
        exercises = []
        for exercise in recommended_exercises:
            predicted_difficulty = self.predict_exercise_difficulty(exercise, self.user_preferences)
            sets, reps = self._ai_determine_accessory_reps(exercise, predicted_difficulty)
            
            exercises.append({
                'name': exercise['name'],
                'muscle_group': exercise['muscle_group'],
                'sets': sets,
                'reps': reps,
                'equipment': exercise['equipment'],
                'difficulty': exercise['difficulty'],
                'bjj_focus': exercise.get('bjj_focus'),
                'workout_format': 'Accessory',
                'predicted_difficulty': predicted_difficulty,
                'ai_recommended': True,
                'notes': f"AI-recommended BJJ accessory: {sets}x{reps}, focus on form"
            })
        
        return exercises
    
    def _ai_determine_sets_reps(self, exercise: Dict, predicted_difficulty: float) -> Tuple[int, int]:
        """Determine sets and reps using AI predictions."""
        # Adjust based on predicted difficulty
        if predicted_difficulty <= 3:
            return (3, 12)
        elif predicted_difficulty <= 6:
            return (4, 10)
        else:
            return (3, 8)
    
    def _ai_determine_metcon_reps(self, exercise: Dict, predicted_difficulty: float) -> int:
        """Determine metcon reps using AI predictions."""
        if predicted_difficulty <= 3:
            return 10
        elif predicted_difficulty <= 6:
            return 8
        else:
            return 6
    
    def _ai_determine_accessory_reps(self, exercise: Dict, predicted_difficulty: float) -> Tuple[int, int]:
        """Determine accessory sets/reps using AI predictions."""
        if predicted_difficulty <= 3:
            return (2, 15)
        elif predicted_difficulty <= 6:
            return (3, 12)
        else:
            return (2, 10)
    
    def _ai_determine_rest_time(self, exercise: Dict, predicted_difficulty: float) -> int:
        """Determine rest time using AI predictions."""
        if predicted_difficulty <= 3:
            return 60
        elif predicted_difficulty <= 6:
            return 90
        else:
            return 120
    
    def _generate_ai_exercise_notes(self, exercise: Dict, sets: int, reps: int, predicted_difficulty: float) -> str:
        """Generate AI-powered exercise notes."""
        notes = f"AI-recommended: {sets}x{reps}"
        
        if predicted_difficulty > 7:
            notes += " (High difficulty - focus on form)"
        elif predicted_difficulty < 4:
            notes += " (Consider increasing weight/intensity)"
        
        return notes
    
    def _analyze_format_preferences(self) -> Dict[str, float]:
        """Analyze user preferences for workout formats."""
        format_scores = {'amrap': 0, 'emom': 0, 'fortime': 0}
        
        for feedback in self.user_history:
            enjoyment = feedback.get('enjoyment_rating', 5)
            # This is a simplified analysis - in a real system, you'd track format per workout
            format_scores['amrap'] += enjoyment * 0.33
            format_scores['emom'] += enjoyment * 0.33
            format_scores['fortime'] += enjoyment * 0.34
        
        return format_scores
    
    def _exercise_matches_criteria(self, exercise: Dict, equipment: List[str], experience_level: str) -> bool:
        """Check if exercise matches user criteria."""
        # Check equipment compatibility
        exercise_equipment = exercise.get('equipment', [])
        if not any(eq in equipment for eq in exercise_equipment):
            return False
        
        # Check experience level
        exercise_difficulty = exercise.get('difficulty', 'beginner')
        difficulty_levels = ['beginner', 'intermediate', 'advanced']
        
        user_level_index = difficulty_levels.index(experience_level)
        exercise_level_index = difficulty_levels.index(exercise_difficulty)
        
        return exercise_level_index <= user_level_index
    
    def save_workout(self, workout: Dict, filename: str = None):
        """Save workout to file."""
        if not filename:
            filename = f"ai_workout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(workout, f, indent=2)
        
        logger.info(f"AI workout saved to {filename}")
    
    def get_user_insights(self) -> Dict:
        """Get AI-generated insights about user's training."""
        if len(self.user_history) < 3:
            return {
                'message': 'Need more workout data to generate insights',
                'recommendations': ['Complete more workouts to get personalized insights']
            }
        
        # Analyze patterns
        avg_difficulty = np.mean([f.get('difficulty_rating', 5) for f in self.user_history])
        avg_enjoyment = np.mean([f.get('enjoyment_rating', 5) for f in self.user_history])
        avg_completion = np.mean([f.get('completion_rate', 0.5) for f in self.user_history])
        
        insights = {
            'total_workouts': len(self.user_history),
            'average_difficulty': avg_difficulty,
            'average_enjoyment': avg_enjoyment,
            'average_completion_rate': avg_completion,
            'trends': self._analyze_trends(),
            'recommendations': self._generate_insight_recommendations(avg_difficulty, avg_enjoyment, avg_completion)
        }
        
        return insights
    
    def _analyze_trends(self) -> Dict:
        """Analyze trends in user's training."""
        if len(self.user_history) < 5:
            return {'message': 'Need more data for trend analysis'}
        
        recent_feedback = self.user_history[-5:]
        older_feedback = self.user_history[-10:-5] if len(self.user_history) >= 10 else self.user_history[:-5]
        
        recent_avg = np.mean([f.get('difficulty_rating', 5) for f in recent_feedback])
        older_avg = np.mean([f.get('difficulty_rating', 5) for f in older_feedback])
        
        difficulty_trend = 'improving' if recent_avg < older_avg else 'stable' if abs(recent_avg - older_avg) < 1 else 'declining'
        
        return {
            'difficulty_trend': difficulty_trend,
            'progress_rate': (older_avg - recent_avg) / max(older_avg, 1)
        }
    
    def _generate_insight_recommendations(self, avg_difficulty: float, avg_enjoyment: float, avg_completion: float) -> List[str]:
        """Generate recommendations based on user insights."""
        recommendations = []
        
        if avg_difficulty < 4:
            recommendations.append("Consider increasing workout difficulty to continue progress")
        elif avg_difficulty > 8:
            recommendations.append("Workouts may be too difficult - consider scaling back")
        
        if avg_enjoyment < 5:
            recommendations.append("Try different exercise variations to increase enjoyment")
        
        if avg_completion < 0.7:
            recommendations.append("Consider shorter workouts or different time slots")
        
        if not recommendations:
            recommendations.append("Great progress! Keep up the consistent training")
        
        return recommendations

def main():
    """Example usage of the Simple AI Workout Planner."""
    # Initialize AI planner
    planner = SimpleAIWorkoutPlanner()
    
    # Set user preferences
    preferences = {
        'time_available': 45,
        'goal': 'bjj_performance',
        'equipment': ['bodyweight', 'barbell', 'kettlebell', 'pull-up bar', 'assault_bike'],
        'experience_level': 'advanced',
        'focus_areas': ['hip_power', 'grip_strength', 'explosive_power']
    }
    
    planner.set_user_preferences(preferences)
    
    # Generate AI workout
    workout = planner.generate_workout()
    
    # Print workout
    print("=== AI-GENERATED WORKOUT ===")
    print(f"Workout ID: {workout['id']}")
    print(f"Total Duration: {workout['total_duration']} minutes")
    print(f"AI Generated: {workout['ai_generated']}")
    
    print("\n=== STRENGTH SECTION ===")
    for exercise in workout['strength_exercises']:
        print(f"{exercise['name']} - {exercise['sets']}x{exercise['reps']} (Rest: {exercise['rest_time']}s)")
        print(f"  Predicted Difficulty: {exercise['predicted_difficulty']:.1f}/10")
        print(f"  Notes: {exercise['notes']}")
    
    print("\n=== METCON SECTION ===")
    for exercise in workout['metcon_exercises']:
        print(f"{exercise['name']} - {exercise['reps']} reps ({exercise['workout_format']})")
        print(f"  Predicted Difficulty: {exercise['predicted_difficulty']:.1f}/10")
        print(f"  Notes: {exercise['notes']}")
    
    print("\n=== ACCESSORY SECTION ===")
    for exercise in workout['accessory_exercises']:
        print(f"{exercise['name']} - {exercise['sets']}x{exercise['reps']}")
        print(f"  Predicted Difficulty: {exercise['predicted_difficulty']:.1f}/10")
        print(f"  Notes: {exercise['notes']}")
    
    print("\n=== PROGRESS PREDICTION ===")
    progress = workout['progress_prediction']
    print(f"Predicted Progress: {progress['predicted_progress']:.2f}")
    print(f"Confidence: {progress['confidence']:.2f}")
    print("Recommendations:")
    for rec in progress['recommendations']:
        print(f"  - {rec}")
    
    # Save workout
    planner.save_workout(workout)
    
    # Example feedback (simulate user completing workout)
    feedback = {
        'difficulty_rating': 7,
        'enjoyment_rating': 8,
        'completion_rate': 0.9,
        'performance_notes': 'Great workout, felt challenging but doable',
        'exercise_ratings': {
            'Barbell Deadlift': 8,
            'Kettlebell Swing': 7,
            'Burpees': 6
        }
    }
    
    planner.record_workout_feedback(workout['id'], feedback)
    
    # Get insights
    insights = planner.get_user_insights()
    print("\n=== USER INSIGHTS ===")
    print(f"Total Workouts: {insights['total_workouts']}")
    print(f"Average Difficulty: {insights['average_difficulty']:.1f}/10")
    print(f"Average Enjoyment: {insights['average_enjoyment']:.1f}/10")
    print(f"Average Completion Rate: {insights['average_completion_rate']:.1%}")
    print("Recommendations:")
    for rec in insights['recommendations']:
        print(f"  - {rec}")

if __name__ == "__main__":
    main() 