## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`.
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource Not Found"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns a list of for all available categories
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

    Sample: `curl http://127.0.0.1:5000/categories`
    ``` {
        "categories":{
            "1":"Science",
            "2":"Art",
            "3":"Geography",
            "4":"History",
            "5":"Entertainment"
            ,"6":"Sports"},
            "total_categories":6}
        }
    ```
#### GET /questions
- General:
    - Returns return a list of questions,number of total questions, categories
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from the first. 
- Sample: `curl http://127.0.0.1:5000/books`
  ```{
    "categories":{
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
        },
        "question":[
            {"answer":"Apollo 13"
            ,"category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},
            {"answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},{"answer":"Edward Scissorhands",
            "category":5,
            "difficulty":3,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},{"answer":"Muhammad Ali",
            "category":4,
            "difficulty":1,
            "id":9,"question":"What boxer's original name is Cassius Clay?"},
            {"answer":"Brazil","category":6,"difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"},
            {"answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"},
            {"answer":"George Washington Carver",
            "category":4,
            "difficulty":2,
            "id":12,
            "question":"Who invented Peanut Butter?"},
            {"answer":"Lake Victoria",
            "category":3,
            "difficulty":2,
            "id":13,
            "question":"What is the largest lake in Africa?"},
            {"answer":"The Palace of Versailles",
            "category":3,
            "difficulty":3,
            "id":14,
            "question":"In which royal palace would you find the Hall of Mirrors?"},
            {"answer":"Escher",
            "category":2,
            "difficulty":1,
            "id":16,
            "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"},
            {"answer":"Jackson Pollock",
            "category":2,
            "difficulty":2,
            "id":19,
            "question":"Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"}],"total_question":32}
  }```

#### DELETE /questions/{question_id}
- General:
    - Deletes a question based on question ID if it exists.
    - Results contains the question id , success value, total questions.
- Sample:`curl -X DELETE http://127.0.0.1:5000/questions/31`
    ```{
        "deleted":31,
        "success":true,
        "total_question":31
    }```

#### POST /questions
- General:
  - Creates a new question using the submitted question, answer, difficulty and category.
  - Results contain the new question contents (answer, category, id, difficulty, question), success value, total number of questions. All will  be updated in the frontend. 
- Sample: `curl -X POST "http://127.0.0.1:5000/questions?page=3" -d "{\"question\":\"Who is considered the founder of the modern study of genetics?\", \"answer\": \"Gregor Mendel\", \"difficulty\": 2, \"category\": 1}" -H "Content-Type: application/json"`
    ```{
        {"answer":"Gregor Mendel",
        "category":1,
        "created":43,
        "difficulty":2,
        "question":"Who is considered the founder of the modern study of genetics?",
        "success":true,
        "total_questions":32}
    }```

#### POST /questions/search
- General:
  - This endpoint gets questions based on a search term
  - return any questions for whom the search term is a substring of the question.
  - Sample: `curl -X POST "http://127.0.0.1:5000/questions" -d "{\"searchTerm\":\"oscar\"}" -H "Content-Type: application/json"`

  ```{
    {"questions":[
        {"answer":"Apollo 13"
        ,"category":5,
        "difficulty":4,
        "id":2,
        "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"}],
        "search_term":"oscar",
        "success":true,
        "total_questions":1}
  }```

#### GET /categories/{category_id}/questions
- General:
  - Returns questions that are in the selected category.
  - Results contain the question, answer, category, difficulty and id, paginated in sets, success value, number of questions that are part of the category and the category selected.
  - Category IDs can be located at the GET /category endpoint.
  - Sample: `curl -X GET "http://127.0.0.1:5000/categories/2/questions"`

  ```{
    {"currentCategory":"Art",
    "questions":[
        {"answer":"Escher",
        "category":2,
        "difficulty":1,
        "id":16,
        "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"},
        {"answer":"Jackson Pollock",
        "category":2,
        "difficulty":2,
        "id":19,
        "question":"Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"}],
        "totalQuestions":2}
  }```

#### POST /quizzez
- General:
  - Returns a random question from the list of questions that belong in a chosen category.
  - Results contain the question, answer, category, difficulty and id
  - Sample: `curl -X POST "http://127.0.0.1:5000/quizzes" -d "{\"quiz_category\":{\"type\": \"Entertainment\", \"id\": \"5\"},\"previous_questions\":[2]}" -H "Content-Type: application/json"`

  ```{
    "question":
    {"answer":"Edward Scissorhands",
    "category":5,
    "difficulty":3,
    "id":6,
    "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"}
  }```

## Deployment N/A

## Authors
Folorunsho Ayomide

## Acknowledgements 
The teaching staff at Udacity for a great core breakdown about api. 






