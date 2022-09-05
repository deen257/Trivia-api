import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from collections.abc import Mapping


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'Elephant04$','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_Question ={"question": "Who is considered the founder of the modern study of genetics?", "answer": "Gregor Mendel", "category": 1, "difficulty": 2}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """test fot getting categories endpoint"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_categories'], 6)

    def test_get_paginated_questions(self):
        """test for getting paginated questions endpoint"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['question']))
        self.assertTrue(data['categories'])
    
    def test_delete_question(self):
        """Test successful request to delete a question"""
        res = self.client().delete('/questions/18')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 18).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], 18)
        self.assertTrue(data['total_question'])
        self.assertEqual(question, None)

    def test_422_deletion_for_a_question_that_does_not_exist(self):
        """Test unsuccessful request to delete a question that doesn't exist"""
        res = self.client().delete('/questions/200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question(self):
        """Test successful request to create a question"""
        res = self.client().post('/questions', json=self.new_Question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['answer'])
        self.assertTrue(data['category'])
        self.assertTrue(data['difficulty'])
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_serach(self):
        """Test successful request to search for a question with results"""
        res = self.client().post('/questions', json={'searchTerm': 'founder'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['total_questions']))
        self.assertTrue(data['questions'])
        self.assertTrue(data['search_term'])
    
    def test_search_without_results(self):
        """Test successful request to search for a question with no results"""
        res = self.client().post('/questions', json={'searchTerm': 'fat'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertTrue(data['search_term'])

    def test_get_questions_for_category(self):
        """Test successful request to get all questions for a category"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'], 'Science')

    def test_404_if_category_does_not_exist(self):
        """Test unsuccessful request to get all questions for an unknown category"""
        res = self.client().get('/categories/500/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_play_trivia(self):
        """Test successful request to play the game"""
        res = self.client().post('/quizzez', json={'previous_questions': [2, 4], 'quiz_category':{'type': 'Entertainment', 'id': '5'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()