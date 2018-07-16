function dragStart(e) {
    e.stopPropagation();
    var boxObj = this,
        todo_id = this.id,
        html = e.target.innerHTML;
    e.dataTransfer.effectAllowed = 'copy';
    e.dataTransfer.setData('html', html);
    e.dataTransfer.setData('todo_id', todo_id);
}

function dragEnd(e) {
    e.stopPropagation();
    var boxObj = this;
    var todo = document.querySelectorAll('.remove-old')[0];
    if (todo) {
        boxObj.remove();
        todo.className = 'todo';
    }
}

function dragEnter(e) {
    if (e.stopPropagation) e.stopPropagation();
}

function dragLeave(e) {
    if (e.stopPropagation) e.stopPropagation();
}

function dragOver(e) {
    if (e.stopPropagation) e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    return false;
}

function drop(e) {
    if (e.stopPropagation) e.stopPropagation();

    var dataObj = e.dataTransfer,
        target = e.target,
        todo_id = dataObj.getData('todo_id'),
        html = dataObj.getData('html');

    // This happens only if we drop in a column
    if (target.className == 'column') {
        // Create a duplicate of the original todo div
        var new_todo = document.createElement('div');
        new_todo.className = 'todo remove-old';
        new_todo.id = todo_id;
        new_todo.draggable = true;
        new_todo.innerHTML = html;
        new_todo.addEventListener('dragstart', dragStart, false);
        new_todo.addEventListener('dragend', dragEnd, false);
        // Add newly created div to a column
        target.appendChild(new_todo);
        updateTodo(todo_id, target.id);
    }

}

function updateTodo(todo_id, column_id) {
    url_dynamic = todo_id + '?column_id=' + column_id

    var xhttp = new XMLHttpRequest();
    xhttp.open('GET', 'update/' + url_dynamic, true);
    xhttp.send();
}

function init() {

    var todos = document.querySelectorAll('.todo'),
        columns = document.querySelectorAll('.column');

    for(var i = 0; i < todos.length; i += 1){
        todos[i].addEventListener('dragstart', dragStart, false);
        todos[i].addEventListener('dragend', dragEnd, false);
    }

    for(var i = 0; i < columns.length; i += 1){
        columns[i].addEventListener('dragenter', dragEnter, false);
        columns[i].addEventListener('dragleave', dragLeave, false);
        columns[i].addEventListener('dragover', dragOver, false);
        columns[i].addEventListener('drop', drop, false);
    }

}

init();
