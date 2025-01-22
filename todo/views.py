from flask import jsonify , abort , make_response , request
from flask import Flask, url_for
from .app import app
from .models import Questionnaire, Question, getQuestionnaires


# def make_public_task(task):
#     new_task = {}
#     for field in task :
#         if field == 'id':
#             new_task ['url'] = url_for('get_tasks', task_id = task['id'] , _external = True)
#         else:
#             new_task [field] = task[field]
#     return new_task


@app.route("/")
def home():
    questionnaires = {}
    for question in getQuestionnaires():
        questionnaires.add(question.to_json())
    return jsonify(questionnaires)


# @app.route('/todo/api/v1.0/tasks' , methods = ['GET'])
# def get_tasks():
#     return jsonify(tasks =[make_public_task(t) for t in tasks ])

# @app.route('/todo/api/v1.0/tasks', methods = ['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description' , ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': make_public_task(task)}), 201



# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)

# @app.errorhandler(400)
# def not_found(error):
#     return make_response(jsonify({'error': 'Bad request'}), 400)

# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
# def update_task(task_id):
#     task = [ task for task in tasks if task ['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     if not request.json :
#         abort(400)
#     if 'title' in request.json and type(request.json['title']) != str:
#         abort(400)
#     if 'description' in request.json and type(request.json['description']) is not str:
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description', task[0]['escription'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify({'task': make_public_task(task[0])})