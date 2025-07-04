#!/usr/bin/env python3
"""
AI Workout Planner

An intelligent workout generator that creates personalized workouts based on:
- Available time
- Fitness goals
- Available equipment
- Experience level
- Preferences
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Optional
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkoutPlanner:
    """AI-powered workout planner that generates personalized workouts."""
    
    def __init__(self, data_file: str = 'workout_data.json'):
        """
        Initialize the workout planner.
        
        Args:
            data_file (str): Path to workout data file
        """
        self.data = self._load_workout_data(data_file)
        self.user_preferences = {}
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
            "exercises": {
                "strength": {
                    "chest": [
                        {"name": "Push-ups", "equipment": ["bodyweight"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Dumbbell Bench Press", "equipment": ["dumbbells", "bench"], "difficulty": "intermediate", "time_per_set": 90},
                        {"name": "Barbell Bench Press", "equipment": ["barbell", "bench", "rack"], "difficulty": "intermediate", "time_per_set": 120},
                        {"name": "Incline Push-ups", "equipment": ["bodyweight"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Decline Push-ups", "equipment": ["bodyweight"], "difficulty": "intermediate", "time_per_set": 60}
                    ],
                    "back": [
                        {"name": "Pull-ups", "equipment": ["pull-up bar"], "difficulty": "intermediate", "time_per_set": 60},
                        {"name": "Dumbbell Rows", "equipment": ["dumbbells"], "difficulty": "beginner", "time_per_set": 90},
                        {"name": "Barbell Rows", "equipment": ["barbell"], "difficulty": "intermediate", "time_per_set": 120},
                        {"name": "Lat Pulldowns", "equipment": ["cable machine"], "difficulty": "beginner", "time_per_set": 90},
                        {"name": "Face Pulls", "equipment": ["cable machine"], "difficulty": "beginner", "time_per_set": 60}
                    ],
                    "legs": [
                        {"name": "Squats", "equipment": ["bodyweight"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Dumbbell Squats", "equipment": ["dumbbells"], "difficulty": "beginner", "time_per_set": 90},
                        {"name": "Barbell Squats", "equipment": ["barbell", "rack"], "difficulty": "intermediate", "time_per_set": 120},
                        {"name": "Lunges", "equipment": ["bodyweight"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Deadlifts", "equipment": ["barbell"], "difficulty": "advanced", "time_per_set": 150},
                        {"name": "Romanian Deadlifts", "equipment": ["dumbbells"], "difficulty": "intermediate", "time_per_set": 90}
                    ],
                    "shoulders": [
                        {"name": "Overhead Press", "equipment": ["dumbbells"], "difficulty": "intermediate", "time_per_set": 90},
                        {"name": "Lateral Raises", "equipment": ["dumbbells"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Front Raises", "equipment": ["dumbbells"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Rear Delt Flyes", "equipment": ["dumbbells"], "difficulty": "beginner", "time_per_set": 60}
                    ],
                    "arms": [
                        {"name": "Bicep Curls", "equipment": ["dumbbells"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Tricep Dips", "equipment": ["bodyweight"], "difficulty": "intermediate", "time_per_set": 60},
                        {"name": "Hammer Curls", "equipment": ["dumbbells"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Skull Crushers", "equipment": ["dumbbells"], "difficulty": "intermediate", "time_per_set": 90}
                    ],
                    "core": [
                        {"name": "Planks", "equipment": ["bodyweight"], "difficulty": "beginner", "time_per_set": 60},
                        {"name": "Crunches", "equipment": ["bodyweight"], "difipment": "beginner", "time_per_set": 60},
                        {"name": "Russian Twists", "equipment": ["bodyweight"], "difficulty": "intermediate", "time_per_set": 60},
                        {"name": "Mountain Climbers", "equipment": ["bodyweight"], "difficulty": "intermediate", "time_per_set": 60},
                        {"name": "Leg Raises", "equipment": ["bodyweight"], "difficulty": "intermediate", "time_per_set": 60}
                    ]
                },
                "cardio": [
                    {"name": "Running", "equipment": ["treadmill", "outdoor"], "difficulty": "beginner", "time_per_set": 300},
                    {"name": "Cycling", "equipment": ["bike", "stationary bike"], "difficulty": "beginner", "time_per_set": 300},
                    {"name": "Jump Rope", "equipment": ["jump rope"], "difficulty": "intermediate", "time_per_set": 120},
                    {"name": "Burpees", "equipment": ["bodyweight"], "difficulty": "intermediate", "time_per_set": 60},
                    {"name": "Mountain Climbers", "equipment": ["bodyweight"], "difficulty": "intermediate", "time_per_set": 60},
                    {"name": "High Knees", "equipment": ["bodyweight"], "difficulty": "beginner", "time_per_set": 60}
                ]
            },
            "workout_types": {
                "strength": {
                    "description": "Build muscle and strength",
                    "focus": ["strength"],
                    "rest_between_sets": 120,
                    "rest_between_exercises": 180
                },
                "cardio": {
                    "description": "Improve cardiovascular fitness",
                    "focus": ["cardio"],
                    "rest_between_sets": 30,
                    "rest_between_exercises": 60
                },
                "hiit": {
                    "description": "High-intensity interval training",
                    "focus": ["cardio"],
                    "rest_between_sets": 30,
                    "rest_between_exercises": 60
                },
                "full_body": {
                    "description": "Full body workout",
                    "focus": ["strength"],
                    "rest_between_sets": 90,
                    "rest_between_exercises": 120
                },
                "upper_body": {
                    "description": "Upper body focus",
                    "focus": ["strength"],
                    "rest_between_sets": 90,
                    "rest_between_exercises": 120
                },
                "lower_body": {
                    "description": "Lower body focus",
                    "focus": ["strength"],
                    "rest_between_sets": 90,
                    "rest_between_exercises": 120
                }
            }
        }
    
    def set_user_preferences(self, preferences: Dict):
        """
        Set user preferences for workout generation.
        
        Args:
            preferences (Dict): User preferences including:
                - time_available: minutes
                - goal: str (strength, cardio, weight_loss, muscle_gain, etc.)
                - equipment: List[str]
                - experience_level: str (beginner, intermediate, advanced)
                - focus_areas: List[str] (optional)
                - workout_type: str (optional)
        """
        self.user_preferences = preferences
        logger.info(f"User preferences set: {preferences}")
    
    def generate_workout(self) -> Dict:
        """
        Generate a personalized workout based on user preferences.
        
        Returns:
            Dict: Complete workout plan
        """
        if not self.user_preferences:
            raise ValueError("User preferences must be set before generating workout")
        
        time_available = self.user_preferences.get('time_available', 60)
        goal = self.user_preferences.get('goal', 'general_fitness')
        equipment = self.user_preferences.get('equipment', ['bodyweight'])
        experience_level = self.user_preferences.get('experience_level', 'beginner')
        focus_areas = self.user_preferences.get('focus_areas', [])
        workout_type = self.user_preferences.get('workout_type')
        
        # Determine workout type based on goal if not specified
        if not workout_type:
            workout_type = self._determine_workout_type(goal)
        
        # Get workout template
        workout_template = self.workout_types[workout_type]
        
        # Calculate time allocation for each section
        strength_time = int(time_available * 0.4)  # 40% for strength
        metcon_time = int(time_available * 0.4)    # 40% for metcon
        accessory_time = int(time_available * 0.2) # 20% for accessory
        
        # Generate each section
        strength_exercises = self._generate_strength_section(
            equipment, experience_level, focus_areas, strength_time
        )
        
        metcon_exercises = self._generate_metcon_section(
            equipment, experience_level, focus_areas, metcon_time
        )
        
        accessory_exercises = self._generate_accessory_section(
            equipment, experience_level, focus_areas, accessory_time
        )
        
        # Create workout plan
        workout = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'workout_type': workout_type,
            'goal': goal,
            'experience_level': experience_level,
            'equipment_used': equipment,
            'focus_areas': focus_areas,
            'estimated_duration': time_available,
            'strength': {
                'name': 'Strength',
                'description': 'Heavy compound movements for maximal strength',
                'exercises': strength_exercises,
                'estimated_duration': strength_time
            },
            'metcon': {
                'name': 'Metcon',
                'description': 'High-intensity conditioning',
                'exercises': metcon_exercises,
                'estimated_duration': metcon_time
            },
            'accessory': {
                'name': 'Accessory',
                'description': 'BJJ-specific movements and skill work',
                'exercises': accessory_exercises,
                'estimated_duration': accessory_time
            }
        }
        
        return workout
    
    def _determine_workout_type(self, goal: str) -> str:
        """Determine workout type based on goal."""
        goal_mapping = {
            'strength': 'strength',
            'muscle_gain': 'strength',
            'weight_loss': 'metcon',
            'cardio': 'endurance',
            'endurance': 'endurance',
            'general_fitness': 'metcon',
            'toning': 'metcon',
            'bjj_performance': 'metcon',
            'explosive_power': 'strength',
            'grip_strength': 'strength',
            'conditioning': 'metcon'
        }
        return goal_mapping.get(goal, 'metcon')
    
    def _generate_strength_section(self, equipment: List[str], experience_level: str, 
                                  focus_areas: List[str], available_time: int) -> List[Dict]:
        """Generate strength exercises."""
        exercises = []
        available_exercises = []
        
        # Determine muscle groups to target
        muscle_groups = ['chest', 'back', 'legs', 'shoulders', 'arms', 'core']
        
        # Filter by focus areas if specified
        if focus_areas:
            muscle_groups = [mg for mg in muscle_groups if mg in focus_areas]
        
        # Collect available exercises from the flat structure
        for exercise in self.exercises:
            if (exercise.get('type') == 'strength' and 
                exercise.get('muscle_group') in muscle_groups and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Calculate exercises per muscle group
        exercises_per_group = max(1, len(muscle_groups) // 2)
        total_exercises = min(len(available_exercises), exercises_per_group * len(muscle_groups))
        
        # Select exercises
        selected_exercises = random.sample(available_exercises, min(total_exercises, len(available_exercises)))
        
        # Create exercise entries
        for exercise in selected_exercises:
            sets, reps = self._determine_sets_reps(exercise['difficulty'], experience_level)
            rest_time = self._determine_rest_time(exercise['difficulty'], experience_level)
            
            exercises.append({
                'name': exercise['name'],
                'muscle_group': exercise['muscle_group'],
                'sets': sets,
                'reps': reps,
                'rest_time': rest_time,
                'equipment': exercise['equipment'],
                'difficulty': exercise['difficulty'],
                'notes': self._generate_exercise_notes(exercise, sets, reps)
            })
        
        return exercises
    
    def _generate_metcon_section(self, equipment: List[str], experience_level: str, 
                                focus_areas: List[str], available_time: int) -> List[Dict]:
        """Generate CrossFit-style metcon workout."""
        exercises = []
        available_exercises = []
        
        # Get BJJ-focused exercises
        bjj_focuses = ['takedown_power', 'hip_power', 'explosive_power', 'grip_strength', 
                      'core_strength', 'endurance', 'stabilization']
        
        if focus_areas:
            bjj_focuses = [focus for focus in bjj_focuses if focus in focus_areas]
        
        # Collect available metcon exercises
        for exercise in self.exercises:
            if (exercise.get('type') in ['conditioning', 'olympic'] and
                exercise.get('category') in ['metcon', 'explosive', 'functional'] and
                exercise.get('bjj_focus') in bjj_focuses and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Select 3-5 exercises for metcon
        num_exercises = min(5, max(3, available_time // 5))
        selected_exercises = random.sample(available_exercises, min(num_exercises, len(available_exercises)))
        
        # Determine workout format
        formats = ['amrap', 'emom', 'fortime']
        workout_format = random.choice(formats)
        
        for exercise in selected_exercises:
            if workout_format == 'amrap':
                reps = self._determine_metcon_reps(exercise, experience_level)
                exercises.append({
                    'name': exercise['name'],
                    'muscle_group': exercise['muscle_group'],
                    'reps': reps,
                    'equipment': exercise['equipment'],
                    'difficulty': exercise['difficulty'],
                    'bjj_focus': exercise.get('bjj_focus'),
                    'workout_format': 'AMRAP',
                    'notes': f"Part of AMRAP: {reps} reps per round"
                })
            elif workout_format == 'emom':
                exercises.append({
                    'name': exercise['name'],
                    'muscle_group': exercise['muscle_group'],
                    'reps': 5,  # Standard EMOM reps
                    'equipment': exercise['equipment'],
                    'difficulty': exercise['difficulty'],
                    'bjj_focus': exercise.get('bjj_focus'),
                    'workout_format': 'EMOM',
                    'notes': "Every Minute On the Minute"
                })
            else:  # fortime
                reps = self._determine_metcon_reps(exercise, experience_level)
                exercises.append({
                    'name': exercise['name'],
                    'muscle_group': exercise['muscle_group'],
                    'reps': reps,
                    'equipment': exercise['equipment'],
                    'difficulty': exercise['difficulty'],
                    'bjj_focus': exercise.get('bjj_focus'),
                    'workout_format': 'For Time',
                    'notes': f"For Time: {reps} reps"
                })
        
        return exercises
    
    def _generate_accessory_section(self, equipment: List[str], experience_level: str, 
                                    focus_areas: List[str], available_time: int) -> List[Dict]:
        """Generate accessory exercises for BJJ-specific movements."""
        exercises = []
        available_exercises = []
        
        # Collect accessory exercises (BJJ-specific movements)
        for exercise in self.exercises:
            if (exercise.get('category') in ['bodyweight', 'functional'] and
                exercise.get('bjj_focus') in ['grip_strength', 'core_strength', 'stabilization'] and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Select 1-2 accessory exercises
        selected_exercises = random.sample(available_exercises, min(2, len(available_exercises)))
        
        for exercise in selected_exercises:
            sets, reps = self._determine_skill_reps(exercise, experience_level)
            exercises.append({
                'name': exercise['name'],
                'muscle_group': exercise['muscle_group'],
                'sets': sets,
                'reps': reps,
                'equipment': exercise['equipment'],
                'difficulty': exercise['difficulty'],
                'bjj_focus': exercise.get('bjj_focus'),
                'workout_format': 'Accessory',
                'notes': f"BJJ-specific: {sets}x{reps}, focus on form"
            })
        
        return exercises
    
    def _generate_steady_cardio(self, available_exercises: List[Dict], 
                              available_time: int, workout_template: Dict) -> List[Dict]:
        """Generate steady state cardio workout."""
        exercises = []
        
        # Select 1-2 cardio exercises
        selected_exercises = random.sample(available_exercises, min(2, len(available_exercises)))
        
        for exercise in selected_exercises:
            duration = available_time // len(selected_exercises)
            
            exercises.append({
                'name': exercise['name'],
                'muscle_group': 'cardio',
                'duration': duration,
                'equipment': exercise['equipment'],
                'difficulty': exercise['difficulty'],
                'notes': f"Steady state cardio for {duration} minutes"
            })
        
        return exercises
    
    def _exercise_matches_criteria(self, exercise: Dict, equipment: List[str], 
                                 experience_level: str) -> bool:
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
        
        # Allow exercises at or below user's level
        return exercise_level_index <= user_level_index
    
    def _determine_sets_reps(self, exercise_difficulty: str, experience_level: str) -> tuple:
        """Determine sets and reps based on difficulty and experience."""
        if experience_level == 'beginner':
            if exercise_difficulty == 'beginner':
                return (3, 10)
            else:
                return (2, 8)
        elif experience_level == 'intermediate':
            if exercise_difficulty == 'beginner':
                return (4, 12)
            elif exercise_difficulty == 'intermediate':
                return (3, 10)
            else:
                return (3, 8)
        else:  # advanced
            if exercise_difficulty == 'beginner':
                return (4, 15)
            elif exercise_difficulty == 'intermediate':
                return (4, 12)
            else:
                return (4, 10)
    
    def _generate_exercise_notes(self, exercise: Dict, sets: int, reps: int) -> str:
        """Generate helpful notes for the exercise."""
        notes = []
        
        if exercise['difficulty'] == 'beginner':
            notes.append("Focus on proper form")
        elif exercise['difficulty'] == 'intermediate':
            notes.append("Maintain controlled movement")
        else:
            notes.append("Push yourself while maintaining form")
        
        if 'bodyweight' in exercise['equipment']:
            notes.append("Can be modified for difficulty")
        
        return ". ".join(notes)
    
    def _generate_warmup(self, workout_type: str, total_time: int) -> List[Dict]:
        """Generate warmup routine."""
        warmup_exercises = [
            {"name": "Light Jogging", "duration": 2, "notes": "Get blood flowing"},
            {"name": "Arm Circles", "duration": 1, "notes": "Loosen shoulders"},
            {"name": "Hip Circles", "duration": 1, "notes": "Loosen hips"},
            {"name": "Bodyweight Squats", "duration": 1, "notes": "Warm up legs"}
        ]
        
        return warmup_exercises
    
    def _generate_cooldown(self, total_time: int) -> List[Dict]:
        """Generate cooldown routine."""
        cooldown_exercises = [
            {"name": "Light Stretching", "duration": 3, "notes": "Stretch major muscle groups"},
            {"name": "Deep Breathing", "duration": 2, "notes": "Lower heart rate"}
        ]
        
        return cooldown_exercises
    
    def _calculate_duration(self, exercises: List[Dict], workout_template: Dict) -> int:
        """Calculate estimated workout duration."""
        total_time = 0
        
        for exercise in exercises:
            if 'sets' in exercise:
                # Strength exercise
                set_time = exercise.get('work_time', 60)  # Default 60 seconds per set
                rest_time = exercise.get('rest_time', 90)  # Default 90 seconds rest
                # Ensure rest_time is an integer
                if isinstance(rest_time, str):
                    # Try to extract number from string like "60-90 seconds"
                    numbers = re.findall(r'\d+', rest_time)
                    rest_time = int(numbers[0]) if numbers else 90
                total_time += (set_time + rest_time) * exercise['sets']
            else:
                # Cardio exercise
                total_time += exercise.get('duration', 0) * 60  # Convert minutes to seconds
        
        # Add rest between exercises (default 60 seconds)
        rest_between_exercises = workout_template.get('rest_between_exercises', 60)
        total_time += rest_between_exercises * (len(exercises) - 1)
        
        return total_time // 60  # Convert back to minutes
    
    def save_workout(self, workout: Dict, filename: str = None):
        """Save workout to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"workout_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(workout, f, indent=2)
        
        logger.info(f"Workout saved to {filename}")
    
    def print_workout(self, workout: Dict):
        """Print workout in a readable format."""
        print("\n" + "="*50)
        print(f"🏋️  WORKOUT PLAN - {workout['date']}")
        print("="*50)
        # Handle both regular and AI workout structures
        workout_type = workout.get('workout_type', 'AI Generated')
        goal = workout.get('goal', workout.get('user_preferences', {}).get('goal', 'bjj_performance'))
        duration = workout.get('estimated_duration', workout.get('total_duration', 45))
        level = workout.get('experience_level', workout.get('user_preferences', {}).get('experience_level', 'intermediate'))
        equipment = workout.get('equipment_used', workout.get('user_preferences', {}).get('equipment', ['bodyweight']))
        
        print(f"Type: {workout_type.title()}")
        print(f"Goal: {goal.replace('_', ' ').title()}")
        print(f"Duration: {duration} minutes")
        print(f"Level: {level.title()}")
        print(f"Equipment: {', '.join(equipment)}")
        
        # Handle AI workout structure (strength, metcon, accessory sections)
        if 'strength_exercises' in workout:
            print("\n💪 STRENGTH")
            print("-" * 20)
            for i, exercise in enumerate(workout['strength_exercises'], 1):
                print(f"{i}. {exercise['name']}")
                if 'sets' in exercise:
                    print(f"   {exercise['sets']} sets × {exercise['reps']} reps")
                    print(f"   Rest: {exercise.get('rest_time', 90)} seconds")
                if exercise.get('muscle_group'):
                    print(f"   Target: {exercise['muscle_group'].title()}")
                if exercise.get('notes'):
                    print(f"   Note: {exercise['notes']}")
                print()
            
            print("\n🔥 METCON")
            print("-" * 20)
            for i, exercise in enumerate(workout['metcon_exercises'], 1):
                print(f"{i}. {exercise['name']}")
                print(f"   {exercise.get('workout_format', 'AMRAP')}: {exercise['reps']} reps")
                if exercise.get('muscle_group'):
                    print(f"   Target: {exercise['muscle_group'].title()}")
                if exercise.get('notes'):
                    print(f"   Note: {exercise['notes']}")
                print()
            
            print("\n🥋 ACCESSORY")
            print("-" * 20)
            for i, exercise in enumerate(workout['accessory_exercises'], 1):
                print(f"{i}. {exercise['name']}")
                if 'sets' in exercise:
                    print(f"   {exercise['sets']} sets × {exercise['reps']} reps")
                if exercise.get('muscle_group'):
                    print(f"   Target: {exercise['muscle_group'].title()}")
                if exercise.get('notes'):
                    print(f"   Note: {exercise['notes']}")
                print()
        else:
            # Handle regular workout structure (warmup, exercises, cooldown)
            print("\n🔥 WARMUP")
            print("-" * 20)
            for exercise in workout.get('warmup', []):
                print(f"• {exercise['name']} - {exercise['duration']} min")
                if exercise.get('notes'):
                    print(f"  Note: {exercise['notes']}")
            
            print("\n💪 EXERCISES")
            print("-" * 20)
            for i, exercise in enumerate(workout.get('exercises', []), 1):
                print(f"{i}. {exercise['name']}")
                if 'sets' in exercise:
                    print(f"   {exercise['sets']} sets × {exercise['reps']} reps")
                    print(f"   Rest: {exercise['rest_time']} seconds")
                else:
                    print(f"   Duration: {exercise['duration']} minutes")
                
                if exercise.get('muscle_group'):
                    print(f"   Target: {exercise['muscle_group'].title()}")
                
                if exercise.get('notes'):
                    print(f"   Note: {exercise['notes']}")
                print()
            
            print("\n🧘 COOLDOWN")
            print("-" * 20)
            for exercise in workout.get('cooldown', []):
                print(f"• {exercise['name']} - {exercise['duration']} min")
                if exercise.get('notes'):
                    print(f"  Note: {exercise['notes']}")
        
        print("\n" + "="*50)
    
    def _generate_metcon_workout(self, equipment: List[str], experience_level: str, 
                                focus_areas: List[str], available_time: int, 
                                workout_template: Dict) -> List[Dict]:
        """Generate CrossFit-style metcon workout."""
        exercises = []
        available_exercises = []
        
        # Get BJJ-focused exercises
        bjj_focuses = ['takedown_power', 'hip_power', 'explosive_power', 'grip_strength', 
                      'core_strength', 'endurance', 'stabilization']
        
        if focus_areas:
            bjj_focuses = [focus for focus in bjj_focuses if focus in focus_areas]
        
        # Collect available metcon exercises
        for exercise in self.exercises:
            if (exercise.get('type') in ['conditioning', 'olympic'] and
                exercise.get('category') in ['metcon', 'explosive', 'functional'] and
                exercise.get('bjj_focus') in bjj_focuses and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Select 3-5 exercises for metcon
        num_exercises = min(5, max(3, available_time // 5))
        selected_exercises = random.sample(available_exercises, min(num_exercises, len(available_exercises)))
        
        # Determine workout format
        formats = ['amrap', 'emom', 'fortime']
        workout_format = random.choice(formats)
        
        for exercise in selected_exercises:
            if workout_format == 'amrap':
                reps = self._determine_metcon_reps(exercise, experience_level)
                exercises.append({
                    'name': exercise['name'],
                    'muscle_group': exercise['muscle_group'],
                    'reps': reps,
                    'equipment': exercise['equipment'],
                    'difficulty': exercise['difficulty'],
                    'bjj_focus': exercise.get('bjj_focus'),
                    'workout_format': 'AMRAP',
                    'notes': f"Part of AMRAP: {reps} reps per round"
                })
            elif workout_format == 'emom':
                exercises.append({
                    'name': exercise['name'],
                    'muscle_group': exercise['muscle_group'],
                    'reps': 5,  # Standard EMOM reps
                    'equipment': exercise['equipment'],
                    'difficulty': exercise['difficulty'],
                    'bjj_focus': exercise.get('bjj_focus'),
                    'workout_format': 'EMOM',
                    'notes': "Every Minute On the Minute"
                })
            else:  # fortime
                reps = self._determine_metcon_reps(exercise, experience_level)
                exercises.append({
                    'name': exercise['name'],
                    'muscle_group': exercise['muscle_group'],
                    'reps': reps,
                    'equipment': exercise['equipment'],
                    'difficulty': exercise['difficulty'],
                    'bjj_focus': exercise.get('bjj_focus'),
                    'workout_format': 'For Time',
                    'notes': f"For Time: {reps} reps"
                })
        
        return exercises
    
    def _generate_endurance_workout(self, equipment: List[str], experience_level: str, 
                                  available_time: int, workout_template: Dict) -> List[Dict]:
        """Generate endurance workout for BJJ athletes."""
        exercises = []
        available_exercises = []
        
        # Collect cardio exercises
        for exercise in self.exercises:
            if (exercise.get('type') == 'conditioning' and
                exercise.get('category') == 'cardio' and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Select 1-2 endurance exercises
        selected_exercises = random.sample(available_exercises, min(2, len(available_exercises)))
        
        for exercise in selected_exercises:
            duration = available_time // len(selected_exercises)
            exercises.append({
                'name': exercise['name'],
                'muscle_group': exercise['muscle_group'],
                'duration': duration,
                'equipment': exercise['equipment'],
                'difficulty': exercise['difficulty'],
                'bjj_focus': exercise.get('bjj_focus'),
                'workout_format': 'Steady State',
                'notes': f"Endurance: {duration} minutes at moderate intensity"
            })
        
        return exercises
    
    def _generate_skill_workout(self, equipment: List[str], experience_level: str, 
                               available_time: int, workout_template: Dict) -> List[Dict]:
        """Generate skill-based workout for technique development."""
        exercises = []
        available_exercises = []
        
        # Collect skill-based exercises
        for exercise in self.exercises:
            if (exercise.get('category') in ['skill', 'olympic', 'bodyweight'] and
                self._exercise_matches_criteria(exercise, equipment, experience_level)):
                available_exercises.append(exercise)
        
        # Select 2-3 skill exercises
        selected_exercises = random.sample(available_exercises, min(3, len(available_exercises)))
        
        for exercise in selected_exercises:
            sets, reps = self._determine_skill_reps(exercise, experience_level)
            exercises.append({
                'name': exercise['name'],
                'muscle_group': exercise['muscle_group'],
                'sets': sets,
                'reps': reps,
                'equipment': exercise['equipment'],
                'difficulty': exercise['difficulty'],
                'bjj_focus': exercise.get('bjj_focus'),
                'workout_format': 'Skill Practice',
                'notes': f"Focus on technique and form, {sets}x{reps}"
            })
        
        return exercises
    
    def _determine_metcon_reps(self, exercise: Dict, experience_level: str) -> int:
        """Determine reps for metcon exercises."""
        base_reps = {
            'beginner': 10,
            'intermediate': 15,
            'advanced': 20
        }
        
        # Adjust based on exercise difficulty
        difficulty_multiplier = {
            'beginner': 1.0,
            'intermediate': 0.8,
            'advanced': 0.6
        }
        
        base = base_reps.get(experience_level, 15)
        multiplier = difficulty_multiplier.get(exercise.get('difficulty', 'beginner'), 1.0)
        
        return int(base * multiplier)
    
    def _determine_skill_reps(self, exercise: Dict, experience_level: str) -> tuple:
        """Determine sets and reps for skill work."""
        if experience_level == 'beginner':
            return (3, 5)
        elif experience_level == 'intermediate':
            return (4, 8)
        else:  # advanced
            return (5, 10)
    
    def _determine_rest_time(self, exercise_difficulty: str, experience_level: str) -> int:
        """Determine rest time based on difficulty and experience."""
        # Base rest times (in seconds)
        base_rest = {
            'beginner': 120,    # 2 minutes
            'intermediate': 180, # 3 minutes  
            'advanced': 240     # 4 minutes
        }
        
        # Adjust based on exercise difficulty
        difficulty_multiplier = {
            'beginner': 0.8,     # Less rest for easier exercises
            'intermediate': 1.0,  # Standard rest
            'advanced': 1.2      # More rest for harder exercises
        }
        
        base = base_rest.get(experience_level, 180)
        multiplier = difficulty_multiplier.get(exercise_difficulty, 1.0)
        
        return int(base * multiplier)


def main():
    """Main function to run the workout planner."""
    planner = WorkoutPlanner()
    
    print("🤖 AI Workout Planner")
    print("=" * 30)
    
    # Get user input
    print("\nLet's create your personalized workout!")
    
    time_available = int(input("How much time do you have? (minutes): "))
    goal = input("What's your goal? (strength/cardio/weight_loss/muscle_gain/general_fitness): ").lower()
    experience_level = input("What's your experience level? (beginner/intermediate/advanced): ").lower()
    
    print("\nWhat equipment do you have? (comma-separated)")
    print("Options: bodyweight, dumbbells, barbell, bench, rack, pull-up bar, cable machine, treadmill, bike, jump rope")
    equipment_input = input("Equipment: ").strip()
    equipment = [eq.strip() for eq in equipment_input.split(',') if eq.strip()]
    
    # Set preferences
    preferences = {
        'time_available': time_available,
        'goal': goal,
        'equipment': equipment,
        'experience_level': experience_level
    }
    
    planner.set_user_preferences(preferences)
    
    # Generate workout
    workout = planner.generate_workout()
    
    # Display workout
    planner.print_workout(workout)
    
    # Save workout
    save = input("\nWould you like to save this workout? (y/n): ").lower()
    if save == 'y':
        planner.save_workout(workout)


if __name__ == "__main__":
    main() 