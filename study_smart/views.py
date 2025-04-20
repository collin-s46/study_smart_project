from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .models import Task, db, Event, User
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)



#welcome page
@views.route('/')
def home():
    return render_template('welcome.html')

#dashboard 
@views.route('/dashboard')
@login_required
def dashboard():
    # Fetch only incomplete tasks for the current user, sorted by priority_score in descending order
    tasks = Task.query.filter_by(user_id=current_user.id, completed=False).order_by(Task.priority_score.desc()).all()

    # Ensure priority_score is calculated for all tasks
    for task in tasks:
        task.calculate_priority_score()

    # Commit any changes to priority_score (if recalculated)
    db.session.commit()

    return render_template('dashboard.html', tasks=tasks)

#settings
@views.route('/settings')
@login_required
def settings():
    # Count the number of completed tasks for the current user
    completed_tasks_count = Task.query.filter_by(user_id=current_user.id, completed=True).count()
    return render_template('settings.html', completed_tasks_count=completed_tasks_count)

#about
@views.route('/about')
def about():
    return render_template('about.html')

#contact
@views.route('/contact')
def contact():
    return render_template('contact.html')

#add_task
@views.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        task_type = request.form.get('type')
        difficulty = request.form.get('difficulty')  # Keep as string (e.g., 'hard', 'medium', 'easy')
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

        # Create a new task object
        new_task = Task(
            name=name,
            type=task_type,
            difficulty=difficulty,  # Pass the string value directly
            due_date=due_date,
            user_id=current_user.id
        )

        # Calculate and set the priority score
        new_task.calculate_priority_score()

        # Add to the database
        db.session.add(new_task)
        db.session.commit()

        flash('Task added successfully!', 'success')
        return redirect(url_for('views.dashboard'))

    return render_template('add_task.html')

#complete_task
@views.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed  # Toggle completion status
    db.session.commit()
    return jsonify({'success': True, 'completed': task.completed})

#delete_task
@views.route('/delete_task/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'success': True})


#add_event feature
@views.route('/add_event', methods=['POST'])
@login_required
def add_event():
    try:
        title = request.form.get('title')
        date_str = request.form.get('date')
        
        # Convert string date to datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Create new event
        new_event = Event(
            title=title,
            date=date,
            user_id=current_user.id
        )
        
        # Save to database
        db.session.add(new_event)
        db.session.commit()
        
        return redirect(url_for('views.dashboard'))
        
    except Exception as e:
        print(f"Error adding event: {e}")
        return redirect(url_for('views.dashboard'))

# Route to get events as JSON for the calendar
@views.route('/get_events')
@login_required
def get_events():
    try:
        events = Event.query.filter_by(user_id=current_user.id).all()
        events_list = []
        
        for event in events:
            events_list.append({
                'id': event.id,
                'title': event.title,  # Use event title
                'start': event.date.isoformat(),  # Use event date as the start date
                'allDay': True,  # Events are all-day
                'color': '#007BFF',  # Blue for events
                'isEvent': True  # Add this property to distinguish events
            })
        
        return jsonify(events_list)
    except Exception as e:
        print(f"Error in /get_events: {e}")
        return jsonify([])

@views.route('/delete_event/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id, user_id=current_user.id).first_or_404()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'success': True})

# Route to get tasks as JSON for the calendar
@views.route('/get_tasks')
@login_required
def get_tasks():
    try:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        tasks_list = []
        
        for task in tasks:
            tasks_list.append({
                'id': task.id,
                'title': task.name,  # Use task name as the title
                'start': task.due_date.isoformat(),  # Use task due date as the start date
                'allDay': True,  # Tasks are all-day events
                'color': '#28a745',  # Green for tasks
                'isEvent': False,  # Add this property to distinguish tasks
                'completed': task.completed  # Add this property to indicate if the task is completed
            })
        
        return jsonify(tasks_list)
    except Exception as e:
        print(f"Error in /get_tasks: {e}")
        return jsonify([])

@views.route('/update_name', methods=['POST'])
@login_required
def update_name():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')

    if not first_name or not last_name:
        return jsonify({'success': False, 'message': 'First name and last name are required.'})

    current_user.first_name = first_name
    current_user.last_name = last_name
    db.session.commit()

    return jsonify({'success': True, 'message': 'Name updated successfully.'})

@views.route('/update_email', methods=['POST'])
@login_required
def update_email():
    email = request.form.get('email')  # Use request.form instead of request.json

    if not email:
        flash('Email is required.', 'error')
        return redirect(url_for('views.settings'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Email is already in use.', 'error')
        return redirect(url_for('views.settings'))

    current_user.email = email
    db.session.commit()
    flash('Email updated successfully!', 'success')
    return redirect(url_for('views.settings'))

