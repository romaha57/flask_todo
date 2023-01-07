from flask import Flask, render_template, request, redirect

from database import connect_to_mongodb, insert_in_db, get_tasks, get_desired_task, \
    delete_from_db, complete_task, return_task_in_active


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form.get('note')
        insert_in_db(collection, note)
        return redirect('/')
    else:
        records = get_tasks(collection, is_active=True)
        return render_template('index.html', records=records)


@app.route('/search/', methods=['GET', 'POST'])
def result_of_search():
    search_text = request.form.get('search_text')
    records = get_desired_task(collection, search_text)
    return render_template('history_and_search_result.html', records=records)


@app.route('/history/')
def show_history_notes():
    records = get_tasks(collection, is_active=False)
    return render_template('history_and_search_result.html', records=records)


@app.route('/delete/<string:task_id>/', methods=['GET', 'POST'])
def delete_task(task_id):
    delete_from_db(collection, task_id)
    return redirect('/')


@app.route('/complete/<string:task_id>/', methods=['GET', 'POST'])
def complete_task_func(task_id):
    complete_task(collection, task_id)
    return redirect('/')


@app.route('/return/<string:task_id>/', methods=['GET', 'POST'])
def return_task(task_id):
    return_task_in_active(collection, task_id)
    return redirect('/')


if __name__ == '__main__':
    collection = connect_to_mongodb()
    app.run(debug=True, port=8000)
