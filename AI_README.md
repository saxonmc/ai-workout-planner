# AI Workout Planner - BJJ Performance Training

A sophisticated AI-powered workout planning system that uses machine learning to create personalized BJJ performance training programs. This system learns from user feedback and adapts workouts based on performance, preferences, and progress.

## 🤖 AI Features

### Machine Learning Capabilities
- **Smart Exercise Recommendations**: ML models learn from your feedback to suggest optimal exercises
- **Difficulty Prediction**: AI predicts exercise difficulty based on your experience and performance history
- **Progress Tracking**: Analyzes performance trends and predicts future progress
- **Adaptive Workouts**: Automatically adjusts workout difficulty based on your feedback
- **Personalized Insights**: Provides AI-generated recommendations for your training

### Learning System
- **Feedback Collection**: Collects detailed feedback on each workout
- **Performance Analysis**: Tracks difficulty ratings, enjoyment, and completion rates
- **Trend Analysis**: Identifies patterns in your training progress
- **Model Retraining**: Continuously improves recommendations based on new data

## 🚀 Quick Start

### Installation

1. **Install Dependencies**:
   ```bash
   pip install -r ai_requirements.txt
   ```

2. **Run the AI Web App**:
   ```bash
   python ai_web_app.py
   ```

3. **Access the Application**:
   - Open your browser to `http://localhost:5001`
   - The app will be available on your local network for mobile access

### Basic Usage

1. **Generate Your First Workout**:
   - Select your available time (30-90 minutes)
   - Choose your training goal (BJJ Performance, Strength, Conditioning)
   - Select available equipment
   - Set your experience level
   - Optionally choose focus areas
   - Click "Generate AI Workout"

2. **Complete the Workout**:
   - Follow the AI-generated workout plan
   - Each exercise includes AI-predicted difficulty ratings
   - Rest times and workout formats are optimized for your level

3. **Provide Feedback**:
   - Rate the overall difficulty (1-10)
   - Rate your enjoyment level (1-10)
   - Set completion rate (0-100%)
   - Add performance notes
   - Submit feedback to help the AI learn

4. **View AI Insights**:
   - Check your progress trends
   - See personalized recommendations
   - Monitor training consistency
   - Track performance metrics

## 📊 AI System Architecture

### Core Components

1. **AIWorkoutPlanner Class**:
   - Main AI engine with machine learning capabilities
   - Handles workout generation, feedback processing, and model training
   - Manages user preferences and performance history

2. **Machine Learning Models**:
   - **Difficulty Model**: Predicts exercise difficulty based on user context
   - **Recommendation Model**: Suggests optimal exercises for user preferences
   - **Progress Model**: Predicts user progress and provides recommendations

3. **Data Processing**:
   - Feature extraction from user feedback
   - Performance trend analysis
   - Model retraining with new data

### Learning Process

1. **Data Collection**:
   ```
   User Feedback → Feature Extraction → Model Training → Improved Recommendations
   ```

2. **Feedback Loop**:
   - User completes workout
   - Provides detailed feedback
   - AI analyzes patterns
   - Models retrain with new data
   - Next workout is more personalized

3. **Progressive Improvement**:
   - Models improve with more data
   - Recommendations become more accurate
   - Workout difficulty adapts to user progress

## 🎯 Workout Structure

### BJJ Performance Focus
- **Strength Section (40%)**: Compound movements for power and strength
- **MetCon Section (40%)**: High-intensity conditioning for endurance
- **Accessory Section (20%)**: BJJ-specific movements and stabilization

### AI-Generated Features
- **Predicted Difficulty**: Each exercise shows AI-predicted difficulty rating
- **Smart Rest Times**: Optimized based on exercise difficulty and user level
- **Workout Formats**: AMRAP, EMOM, For Time based on user preferences
- **BJJ Focus Areas**: Hip power, grip strength, explosive power, core strength

## 📱 Mobile-Friendly Features

### Responsive Design
- Works perfectly on phones and tablets
- Touch-optimized interface
- Mobile-friendly navigation

### Network Access
- Access from any device on your local network
- Share with training partners
- Use on gym WiFi

## 🔧 Advanced Features

### API Endpoints
```python
# Generate workout via API
POST /api/workout
{
    "preferences": {
        "time_available": 45,
        "goal": "bjj_performance",
        "equipment": ["barbell", "kettlebell"],
        "experience_level": "advanced"
    }
}

# Submit feedback via API
POST /api/feedback
{
    "workout_id": "workout_20241203_143022",
    "feedback": {
        "difficulty_rating": 7,
        "enjoyment_rating": 8,
        "completion_rate": 0.9
    }
}

# Get AI insights via API
GET /api/insights
```

### Customization Options
- **Equipment Selection**: Choose from 8+ equipment types
- **Focus Areas**: Target specific BJJ performance aspects
- **Experience Levels**: Beginner, Intermediate, Advanced
- **Time Flexibility**: 30-90 minute workouts

## 📈 Progress Tracking

### Metrics Tracked
- **Workout Completion Rate**: How often you finish workouts
- **Difficulty Trends**: Whether workouts are getting easier/harder
- **Enjoyment Levels**: How much you enjoy different exercises
- **Performance Patterns**: Which exercises work best for you

### AI Insights
- **Progress Predictions**: AI estimates your future progress
- **Personalized Recommendations**: Specific suggestions for improvement
- **Trend Analysis**: Identifies patterns in your training
- **Adaptive Suggestions**: Recommendations that change as you improve

## 🛠️ Technical Details

### Machine Learning Models
- **Random Forest Regressors**: For difficulty prediction and recommendations
- **Feature Engineering**: Extracts meaningful features from user data
- **Model Persistence**: Saves trained models for future use
- **Incremental Learning**: Models improve with each new data point

### Data Storage
- **Workout History**: JSON files for each generated workout
- **User Feedback**: Stored in memory with model training
- **ML Models**: Pickled files for persistence
- **Performance Data**: Tracked for trend analysis

### Performance Optimization
- **Lazy Loading**: Models only train when sufficient data is available
- **Efficient Feature Extraction**: Optimized for real-time predictions
- **Memory Management**: Efficient handling of user history
- **Fast Response Times**: Quick workout generation and feedback processing

## 🔮 Future Enhancements

### Planned Features
- **Exercise Video Integration**: Links to demonstration videos
- **Social Features**: Share workouts with training partners
- **Advanced Analytics**: More detailed performance insights
- **Integration APIs**: Connect with fitness tracking apps
- **Voice Commands**: Voice-controlled workout generation

### AI Improvements
- **Deep Learning Models**: More sophisticated recommendation algorithms
- **Real-time Adaptation**: Dynamic workout adjustments during training
- **Predictive Analytics**: Advanced progress forecasting
- **Personalized Coaching**: AI-generated training advice

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Change port in ai_web_app.py
   app.run(debug=True, host='0.0.0.0', port=5002)
   ```

2. **Missing Dependencies**:
   ```bash
   pip install -r ai_requirements.txt
   ```

3. **Model Training Issues**:
   - Ensure you have at least 3-5 completed workouts with feedback
   - Check that feedback includes difficulty and enjoyment ratings

4. **Mobile Access Issues**:
   - Ensure devices are on the same network
   - Check firewall settings
   - Use the computer's IP address instead of localhost

### Performance Tips
- **Regular Feedback**: Provide feedback after each workout for better AI learning
- **Consistent Training**: Regular workouts help the AI understand your patterns
- **Detailed Notes**: Include performance notes for more personalized recommendations

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional exercise database
- Enhanced ML models
- UI/UX improvements
- Mobile app development
- Integration with fitness platforms

---

**Built with ❤️ for BJJ athletes who want to train smarter, not harder.** 