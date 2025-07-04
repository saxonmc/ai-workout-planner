#!/usr/bin/env python3
"""
AI Workout Planner with Machine Learning

A sophisticated workout generator that learns from user feedback and adapts
workouts based on performance, progress, and preferences.
"""

import json
import random
import numpy as np
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIWorkoutPlanner:
    """AI-powered workout planner with machine learning capabilities."""
    
    def __init__(self, data_file: str = 'workout_data.json', model_file: str = 'ai_model.pkl'):
        """
        Initialize the AI workout planner.
        
        Args:
            data_file (str): Path to workout data file
            model_file (str): Path to save/load ML model
        """
        self.data = self._load_workout_data(data_file)
        self.model_file = model_file
        self.user_preferences = {}
        self.user_history = []
        self.exercise_performance = {}
        self.progress_tracker = {}
        
        # ML Models
        self.difficulty_model = None
        self.exercise_recommendation_model = None
        self.progress_prediction_model = None
        self.scaler = StandardScaler()
        
        # Load or initialize models
        self._load_or_initialize_models()
        
        # Assign top-level keys for convenience
        self.exercises = self.data.get('exercises', [])
        self.workout_types = self.data.get('workout_types', {})
        self.muscle_groups = self.data.get('muscle_groups', {})
    
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
        """Load existing ML models or initialize new ones."""
        try:
            with open(self.model_file, 'rb') as f:
                models = pickle.load(f)
                self.difficulty_model = models.get('difficulty_model')
                self.exercise_recommendation_model = models.get('exercise_recommendation_model')
                self.progress_prediction_model = models.get('progress_prediction_model')
                self.scaler = models.get('scaler', StandardScaler())
                logger.info("Loaded existing ML models")
        except FileNotFoundError:
            logger.info("No existing models found. Initializing new models.")
            self._initialize_models()
    
    def _initialize_models(self):
        """Initialize new ML models."""
        self.difficulty_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.exercise_recommendation_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.progress_prediction_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
    
    def _save_models(self):
        """Save ML models to file."""
        models = {
            'difficulty_model': self.difficulty_model,
            'exercise_recommendation_model': self.exercise_recommendation_model,
            'progress_prediction_model': self.progress_prediction_model,
            'scaler': self.scaler
        }
        with open(self.model_file, 'wb') as f:
            pickle.dump(models, f)
        logger.info("Models saved successfully")
    
    def set_user_preferences(self, preferences: Dict):
        """Set user preferences for workout generation."""
        self.user_preferences = preferences
        logger.info(f"User preferences set: {preferences}")
    
    def record_workout_feedback(self, workout_id: str, feedback: Dict):
        """
        Record user feedback on a completed workout.
        
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
        
        # Retrain models with new data
        self._retrain_models()
        
        logger.info(f"Workout feedback recorded: {feedback}")
    
    def _retrain_models(self):
        """Retrain ML models with updated user data."""
        if len(self.user_history) < 5:  # Need minimum data to train
            return
        
        # Prepare training data
        X, y_difficulty, y_recommendation, y_progress = self._prepare_training_data()
        
        if len(X) < 10:  # Need more data
            return
        
        # Split data
        X_train, X_test, y_d_train, y_d_test = train_test_split(X, y_difficulty, test_size=0.2, random_state=42)
        _, _, y_r_train, y_r_test = train_test_split(X, y_recommendation, test_size=0.2, random_state=42)
        _, _, y_p_train, y_p_test = train_test_split(X, y_progress, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train models
        self.difficulty_model.fit(X_train_scaled, y_d_train)
        self.exercise_recommendation_model.fit(X_train_scaled, y_r_train)
        self.progress_prediction_model.fit(X_train_scaled, y_p_train)
        
        # Evaluate models
        difficulty_score = self.difficulty_model.score(X_test_scaled, y_d_test)
        recommendation_score = self.exercise_recommendation_model.score(X_test_scaled, y_r_test)
        progress_score = self.progress_prediction_model.score(X_test_scaled, y_p_test)
        
        logger.info(f"Model retraining completed - Scores: Difficulty={difficulty_score:.3f}, "
                   f"Recommendation={recommendation_score:.3f}, Progress={progress_score:.3f}")
        
        # Save updated models
        self._save_models()
    
    def _prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Prepare training data from user history."""
        features = []
        difficulty_targets = []
        recommendation_targets = []
        progress_targets = []
        
        for i, feedback in enumerate(self.user_history):
            # Extract features
            feature_vector = self._extract_features(feedback)
            features.append(feature_vector)
            
            # Extract targets
            difficulty_targets.append(feedback.get('difficulty_rating', 5))
            recommendation_targets.append(feedback.get('enjoyment_rating', 5))
            
            # Calculate progress (improvement over time)
            if i > 0:
                prev_difficulty = self.user_history[i-1].get('difficulty_rating', 5)
                current_difficulty = feedback.get('difficulty_rating', 5)
                progress = prev_difficulty - current_difficulty  # Lower difficulty = progress
                progress_targets.append(progress)
            else:
                progress_targets.append(0)
        
        return (np.array(features), np.array(difficulty_targets), 
                np.array(recommendation_targets), np.array(progress_targets))
    
    def _extract_features(self, feedback: Dict) -> List[float]:
        """Extract features from user feedback for ML training."""
        features = [
            feedback.get('difficulty_rating', 5),
            feedback.get('enjoyment_rating', 5),
            feedback.get('completion_rate', 0.5),
            len(feedback.get('exercise_ratings', {})),
            np.mean(list(feedback.get('exercise_ratings', {}).values())) if feedback.get('exercise_ratings') else 5,
            self.user_preferences.get('time_available', 60),
            len(self.user_preferences.get('equipment', [])),
            self._experience_level_to_numeric(self.user_preferences.get('experience_level', 'beginner')),
            len(self.user_preferences.get('focus_areas', []))
        ]
        return features
    
    def _experience_level_to_numeric(self, level: str) -> int:
        """Convert experience level to numeric value."""
        levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        return levels.get(level, 1)
    
    def predict_exercise_difficulty(self, exercise: Dict, user_context: Dict) -> float:
        """Predict difficulty rating for an exercise based on user context."""
        if self.difficulty_model is None:
            return self._default_difficulty_prediction(exercise)
        
        features = self._extract_exercise_features(exercise, user_context)
        features_scaled = self.scaler.transform([features])
        prediction = self.difficulty_model.predict(features_scaled)[0]
        return max(1, min(10, prediction))  # Clamp between 1-10
    
    def _extract_exercise_features(self, exercise: Dict, user_context: Dict) -> List[float]:
        """Extract features for exercise difficulty prediction."""
        return [
            self._experience_level_to_numeric(user_context.get('experience_level', 'beginner')),
            len(user_context.get('equipment', [])),
            len(user_context.get('focus_areas', [])),
            user_context.get('time_available', 60),
            self._difficulty_to_numeric(exercise.get('difficulty', 'beginner')),
            len(exercise.get('equipment', [])),
            exercise.get('time_per_set', 60)
        ]
    
    def _difficulty_to_numeric(self, difficulty: str) -> int:
        """Convert difficulty to numeric value."""
        difficulties = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        return difficulties.get(difficulty, 1)
    
    def _default_difficulty_prediction(self, exercise: Dict) -> float:
        """Default difficulty prediction when ML model is not available."""
        difficulty_map = {'beginner': 3, 'intermediate': 6, 'advanced': 8}
        return difficulty_map.get(exercise.get('difficulty', 'beginner'), 5)
    
    def recommend_exercises(self, available_exercises: List[Dict], num_recommendations: int) -> List[Dict]:
        """Recommend exercises based on user preferences and history."""
        if not available_exercises:
            return []
        
        if self.exercise_recommendation_model is None or len(self.user_history) < 3:
            # Use rule-based recommendation
            return self._rule_based_exercise_recommendation(available_exercises, num_recommendations)
        
        # Use ML-based recommendation
        exercise_scores = []
        for exercise in available_exercises:
            features = self._extract_exercise_features(exercise, self.user_preferences)
            features_scaled = self.scaler.transform([features])
            score = self.exercise_recommendation_model.predict(features_scaled)[0]
            exercise_scores.append((exercise, score))
        
        # Sort by score and return top recommendations
        exercise_scores.sort(key=lambda x: x[1], reverse=True)
        return [exercise for exercise, _ in exercise_scores[:num_recommendations]]
    
    def _rule_based_exercise_recommendation(self, available_exercises: List[Dict], num_recommendations: int) -> List[Dict]:
        """Rule-based exercise recommendation when ML is not available."""
        # Consider user history and preferences
        recommended = []
        
        # Prioritize exercises that match focus areas
        focus_areas = self.user_preferences.get('focus_areas', [])
        if focus_areas:
            focus_exercises = [ex for ex in available_exercises 
                             if ex.get('muscle_group') in focus_areas or ex.get('bjj_focus') in focus_areas]
            recommended.extend(focus_exercises[:num_recommendations//2])
        
        # Add variety from other exercises
        remaining = [ex for ex in available_exercises if ex not in recommended]
        recommended.extend(random.sample(remaining, min(num_recommendations - len(recommended), len(remaining))))
        
        return recommended[:num_recommendations]
    
    def predict_progress(self, current_workout: Dict) -> Dict:
        """Predict user progress based on current workout and history."""
        if self.progress_prediction_model is None or len(self.user_history) < 5:
            return self._default_progress_prediction()
        
        # Extract features from current workout
        features = self._extract_workout_features(current_workout)
        features_scaled = self.scaler.transform([features])
        
        # Predict progress
        progress_score = self.progress_prediction_model.predict(features_scaled)[0]
        
        return {
            'predicted_progress': progress_score,
            'confidence': 0.7,  # Placeholder confidence score
            'recommendations': self._generate_progress_recommendations(progress_score)
        }
    
    def _extract_workout_features(self, workout: Dict) -> List[float]:
        """Extract features from workout for progress prediction."""
        total_exercises = len(workout.get('strength_exercises', [])) + \
                         len(workout.get('metcon_exercises', [])) + \
                         len(workout.get('accessory_exercises', []))
        
        return [
            total_exercises,
            workout.get('total_duration', 60),
            len(self.user_preferences.get('equipment', [])),
            self._experience_level_to_numeric(self.user_preferences.get('experience_level', 'beginner')),
            len(self.user_preferences.get('focus_areas', []))
        ]
    
    def _default_progress_prediction(self) -> Dict:
        """Default progress prediction when ML model is not available."""
        return {
            'predicted_progress': 0.5,
            'confidence': 0.3,
            'recommendations': ['Continue with current routine', 'Focus on form and technique']
        }
    
    def _generate_progress_recommendations(self, progress_score: float) -> List[str]:
        """Generate recommendations based on predicted progress."""
        if progress_score > 0.7:
            return ['Great progress! Consider increasing difficulty', 'Add more challenging exercises']
        elif progress_score > 0.3:
            return ['Steady progress, maintain current intensity', 'Focus on consistency']
        else:
            return ['Consider adjusting workout difficulty', 'Focus on form and technique', 'Ensure adequate recovery']
    
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
            'id': f"workout_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'user_preferences': self.user_preferences,
            'strength_exercises': strength_exercises,
            'metcon_exercises': metcon_exercises,
            'accessory_exercises': accessory_exercises,
            'total_duration': time_available,
            'ai_generated': True
        }
        
        # Predict progress for this workout
        progress_prediction = self.predict_progress(workout)
        workout['progress_prediction'] = progress_prediction
        
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
    """Example usage of the AI Workout Planner."""
    # Initialize AI planner
    planner = AIWorkoutPlanner()
    
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