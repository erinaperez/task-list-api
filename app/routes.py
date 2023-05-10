from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# VALIDATE MODEL
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


# CREATE TASK
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    task_message = {}
    task_message["task"] = new_task.to_dict()

    return jsonify(task_message), 201


# GET SAVED TASKS
@tasks_bp.route("", methods=["GET"])
def get_saved_tasks():
    tasks = Task.query.all()
    tasks_list_response = []

    for task in tasks:
        tasks_list_response.append(task.to_dict())

    return jsonify(tasks_list_response)


# GET ONE TASK
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    task_message = {"task": task.to_dict()}

    return jsonify(task_message)


# UPDATE TASK
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    task_message = {"task": task.to_dict()}

    return jsonify(task_message)


# DELETE TASK
