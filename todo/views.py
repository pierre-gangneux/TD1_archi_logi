from flask import jsonify , abort , make_response , request, Flask, url_for, redirect
from .app import app, db
from .models import QuestionMultiple, QuestionSimple, Questionnaire, Question, getQuestionnaires, get_questionnaire, get_questions_questionnaire, get_questions, get_question, delete_question_row, delete_questionnaire_row, edit_question_row, edit_questionnaire_row


@app.route("/")
def home():
    return redirect(url_for("questionnaires"))

@app.route("/api/questionnaires", methods = ['GET'])
def questionnaires():
    """Permet d'obtenir la liste des questionnaires avec la méthode GET
    Un questionnaire est composé d'un identifiant, d'un nom 
    ainsi qu'une URI permettant d'obtenir les questions du questionnaire

    Returns:
        json: la liste des questionnaires
    """
    questionnaires = getQuestionnaires()
    for questionnaire in questionnaires:
        questionnaire["uri"] = "/api/questionnaires/"+str(questionnaire["id"])+"/questions"
    return jsonify(questionnaires), 200

@app.route("/api/questionnaires/<int:questionnaire_id>", methods = ["GET"])
def questionnaire(questionnaire_id:int):
    """Permet obtenir un questionnaire en renseignant son id avec la méthode GET

    Args:
        questionnaire_id (int): l'id du questionnaire que l'on veut récupérer

    Returns:
        json: questionnaire
    """
    questionnaire = get_questionnaire(questionnaire_id)
    if questionnaire is None:
        # Le questionnaire n'existe pas
        abort(404)
    
    return jsonify(questionnaire), 200

@app.route("/api/questionnaires/<int:questionnaire_id>/questions", methods = ["GET"])
def questionnaire_questions(questionnaire_id:int):
    """Permet d'obtenir les questions d'un questionnaire avec la méthode GET

    Args:
        questionnaire_id (int): l'id du questionnaire contenant les questions

    Returns:
        json: liste des questions du questionnaire
    """
    questionnaire = get_questions_questionnaire(questionnaire_id)
    if questionnaire is None:
        # Le questionnaire n'existe pas
        abort(404)
    return jsonify(questionnaire), 200

@app.route("/api/questionnaires/<int:id_questionnaires>/questions", methods = ['GET'])
def questions(id_questionnaires):
    return jsonify(get_questions(id_questionnaires)), 200

@app.route("/api/questionnaires/<int:id_questionnaires>/questions/<int:id_question>", methods = ['GET'])
def question(id_question:int, id_questionnaires:int):
    """Permet d'obtenir le json d'un question avec la méthode GET

    Args:
        id_question (int): l'id de la question que l'on veut récupérer

    Returns:
        json: la question
    """
    question = get_question(id_questionnaires, id_question)
    if question is None:
        # La question n'existe pas
        abort(404)
    return jsonify(question), 200

# Ajouter des questions et des questionnaires #

# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"test"}' http://localhost:5000/api/questionnaires
@app.route("/api/questionnaires", methods = ['POST'])
def create_questionnaires():
    """Permet de créer un questionnaire avec la méthode POST
    Nécessite un nom pour créer le questionnaire

    Returns:
        json: le questionnaire une fois créer
    """
    if not request.json or not 'name' in request.json:
        abort(400)
    questionnaire = Questionnaire(request.json["name"])
    db.session.add(questionnaire)
    db.session.commit()
    questionnaire = questionnaire.to_json()
    questionnaire["uri"] = "/api/questionnaires/"+str(questionnaire["id"])+"/questions"
    return jsonify(questionnaire), 201


@app.route("/api/questionnaires/<int:id_questionnaires>/questions", methods = ['POST'])
def create_question(id_questionnaires):
    """Permet de créer une question avec la méthode POST
    Nécessite un titre, un type et l'id d'un questionnaire pour créer la question

    Returns:
        json: la question une fois créer
    """
    if (
        not request.json
        or not 'title' in request.json 
        or not 'type' in request.json 
    ):
        abort(400)
    
    match request.json["type"]:
        case "multiple":
            question = QuestionMultiple(request.json["title"], request.json["type"], id_questionnaires)
        case _:
            question = QuestionSimple(request.json["title"], request.json["type"], id_questionnaires)


    db.session.add(question)
    db.session.commit()
    return jsonify(question.to_json()), 201

# Modifier les questions et les questionnaires #

# curl -i -H "Content-Type: application/json" -X PUT -d '{"questionnaire_id":1,"name":"new_name"}' http://localhost:5000/api/questionnaires
@app.route("/api/questionnaires", methods = ["PUT"])
def edit_questionnaire():
    """Permet de modifier un questionnaire

    Returns:
        json: le json du questionnaire une fois modifier
    """
    if not request.json or not 'questionnaire_id' in request.json or len(request.json) <= 1:
        abort(400)
    questionnaire = edit_questionnaire_row(request.json)
    if questionnaire is None:
        abort(404)
    questionnaire["uri"] = "/api/questionnaires/"+str(questionnaire["id"])+"/questions"
    return jsonify(questionnaire), 200

# curl -i -H "Content-Type: application/json" -X PUT -d '{"question_id":1, "title":"testQ", "type":"text", "questionnaire_id":1}' http://localhost:5000/api/questions
@app.route("/api/questions", methods = ['PUT'])
def edit_question():
    """Permet de modifier une question

    Returns:
        json: le json de la question une fois modifier
    """
    if not request.json or not 'question_id' in request.json or len(request.json) <= 1:
        abort(400)
    question = edit_question_row(request.json)
    if question is None:
        abort(404)
    return jsonify(question), 200

# Supprimer les questions et les questionnaires #

# curl -i -H "Content-Type: application/json" -X DELETE -d '{"questionnaire_id":"1"}' http://localhost:5000/api/questionnaires
@app.route("/api/questionnaires", methods = ["DELETE"])
def delete_questionnaire():
    """Permet de supprimer un questionnaire

    Returns:
        json: le json du questionnaire une fois supprimer
    """
    if not request.json or not 'questionnaire_id' in request.json:
        abort(400)
    questionnaire = delete_questionnaire_row(request.json["questionnaire_id"])
    if questionnaire is None:
        abort(404)
    return jsonify(questionnaire), 200

# curl -i -H "Content-Type: application/json" -X DELETE -d '{"question_id":"2"}' http://localhost:5000/api/questions
@app.route("/api/questions", methods = ['DELETE'])
def delete_question():
    """Permet de supprimer une question

    Returns:
        json: le json de la question une fois supprimer
    """
    if not request.json or not 'question_id' in request.json:
        abort(400)
    question = delete_question_row(request.json["question_id"])
    if question is None:
        abort(404)
    return jsonify(question), 200

# Handler error #

@app.errorhandler(404)
def not_found(error):
    """Erreur déclencher lorsque la ressource n'existe

    Args:
        error (error): l'erreur

    Returns:
        json: Une description de l'erreur
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    """Erreur déclencher lorsque la requête n'est pas bien formulée

    Args:
        error (error): l'erreur

    Returns:
        json: Une description de l'erreur
    """
    return make_response(jsonify({'error': 'Bad request'}), 400)



























def make_public_task(task):
    new_task = {}
    for field in task :
        if field == 'id':
            new_task ['url'] = url_for('get_tasks', task_id = task['id'] , _external = True)
        else:
            new_task [field] = task[field]
    return new_task


@app.route('/todo/api/v1.0/tasks' , methods = ['GET'])
def get_tasks():
    return jsonify(tasks =[make_public_task(t) for t in tasks ])
@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description' , ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
# @app.errorhandler(400)
# def not_found(error):
#     return make_response(jsonify({'error': 'Bad request'}), 400)
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    task = [ task for task in tasks if task ['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json :
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['escription'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': make_public_task(task[0])})