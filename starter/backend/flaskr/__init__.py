import json
import os
from sre_parse import CATEGORIES
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from collections.abc import Mapping

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10



def paginate_questions(request, selection):
    pages = request.args.get('page', 1, type=int)
    start_page = (pages - 1) *  QUESTIONS_PER_PAGE
    end_page = pages + QUESTIONS_PER_PAGE

    format_question = [question.format() for question in selection]
    current_question = format_question[start_page:end_page]
    
    return current_question
        
    
        

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, origins="*")

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-header", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-methods", "GET,POST,DELETE")
        return response 

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=["GET"])
    def get_categories():
        selection = Category.query.order_by(Category.id).all()

        formatted_categories = {}
        for category in selection:
            formatted_categories[category.id] = category.type
        if len(Category.query.all()) == 0:
            abort (404)
        else:
            return  jsonify(
                {
                    'categories': formatted_categories,
                    'total_categories': len(Category.query.all())
                }
        )


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection1 = Question.query.order_by(Question.id).all()
        selection2 = Category.query.order_by(Category.id).all()
        current_question = paginate_questions(request, selection1)

        if len(current_question) == 0:
            abort(404)

        return jsonify (
            {
                'question' : current_question,
                'total_question': len(Question.query.all()),
                'categories': {category.id: category.type for category in selection2}
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question_query = Question.query.get(question_id)
            question_query.delete()

            return jsonify (
            {
                'success': True,
                'deleted': question_id,
                'total_question' : len(Question.query.all())
            })

        except: 
            abort(422)


        
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        try:
            search_term = body.get('searchTerm', None)
            if search_term:
                questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
                current_questions = paginate_questions(request, questions)              
                return jsonify(
                    {
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(questions),
                        'search_term': search_term
                    }
            )

            else:
                new_question = body.get('question', None)
                new_answer = body.get('answer', None)
                new_category = body.get('category', None)
                new_difficulty = body.get('difficulty', None)

                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)
            
            
            return jsonify({
                'question': new_question,
                'answer': new_answer,
                'category': new_category,
                'difficulty': new_difficulty,
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_catgories(category_id):
        try:       
            questions = Question.query.filter(Question.category == category_id).all()
            current_category = Category.query.get(category_id).type
        
        except:
            abort(404)

        return jsonify(
            {
                "questions": [question.format() for question in questions],
                "totalQuestions": len(questions),
                "currentCategory": current_category
            }
        )

        


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzez', methods=['POST'])
    def quiz():
        data = request.json
        category_id = data["quiz_category"]["id"]
        previous_questions_id = data["previous_questions"]

        if category_id != 0:
            questions_left_in_category = Question.query.filter(
                Question.category == category_id).filter(
                    Question.id.notin_(previous_questions_id)).all()
        else:
            questions_left_in_category = Question.query.filter(
                Question.id.notin_(previous_questions_id)).all()

        question = random.choice(questions_left_in_category).format() if len(
            questions_left_in_category) else False

        return jsonify({"question" : question})

        
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success":False,
        "error":404,
        "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success":False,
        "error":422,
        "message": "unprocessable"
        }), 422


    return app

