from flask import Blueprint, request, jsonify
from ..models.game import NeuroCognixGame
from typing import Dict, Any

api = Blueprint('api', __name__)
game = NeuroCognixGame()


@api.route('/start-game', methods=['POST'])
def start_game() -> Dict[str, Any]:
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        game.set_player_profile(
            age_group=data.get('age_group', 'adult'),
            education_level=data.get('education_level', 'high_school'),
            language_proficiency=data.get(
                'language_proficiency', 'intermediate')
        )
        sequence = game.generate_sequence()

        return jsonify({
            "sequence": sequence,
            "category": game.current_category,
            "difficulty": game.difficulty
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/submit-answer', methods=['POST'])
def submit_answer() -> Dict[str, Any]:
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        player_input = data['answer']
        start_time = data['startTime']
        end_time = data['endTime']

        is_correct = game.check_sequence(player_input)
        score = game.calculate_score(start_time, end_time)
        feedback = game.generate_feedback(player_input)
        difficulty_message = game.adjust_difficulty()

        return jsonify({
            "correct": is_correct,
            "score": score,
            "totalScore": game.state.score,
            "difficultyChange": difficulty_message,
            "newDifficulty": game.difficulty,
            "feedback": feedback,
            "cognitiveLoad": game.state.cognitive_load,
            "fatigueFactor": game.state.fatigue_factor,
            "expectedTime": game.calculate_expected_time()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/generate-sequence', methods=['GET'])
def generate_sequence() -> Dict[str, Any]:
    try:
        sequence = game.generate_sequence()
        return jsonify({
            "sequence": sequence,
            "category": game.current_category,
            "difficulty": game.difficulty,
            "expected_time": game.calculate_expected_time()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/player-stats', methods=['GET'])
def player_stats() -> Dict[str, Any]:
    try:
        return jsonify({
            "totalScore": game.state.score,
            "averageScore": sum(game.state.score_history) / len(game.state.score_history)
            if game.state.score_history else 0,
            "gamesPlayed": len(game.state.score_history),
            "currentDifficulty": game.difficulty
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
