let todos = [];

function addTodo() {

    const input = document.getElementById("todoInput");

    const todoText = input.value.trim();

    if (todoText === "") {
        alert("Please enter a todo");
        return;
    }

    const todo = {
        text: todoText,
        completed: false
    };

    todos.push(todo);

    input.value = "";

    displayTodos();
}


function displayTodos() {

    const todoList = document.getElementById("todoList");

    todoList.innerHTML = "";

    if (todos.length === 0) {

        todoList.innerHTML =
            '<p class="no-todos">No todos available.</p>';

        return;
    }

    todos.forEach(function(todo, index) {

        const li = document.createElement("li");

        li.className = "todo-item";

        const span = document.createElement("span");

        span.className = "todo-text";

        span.textContent = todo.text;

        if (todo.completed) {
            span.classList.add("completed");
        }

        span.onclick = function() {
            toggleTodo(index);
        };


        const deleteButton = document.createElement("button");

        deleteButton.className = "delete-btn";

        deleteButton.textContent = "Delete";

        deleteButton.onclick = function() {
            deleteTodo(index);
        };


        li.appendChild(span);

        li.appendChild(deleteButton);

        todoList.appendChild(li);

    });
}


function toggleTodo(index) {

    todos[index].completed =
        !todos[index].completed;

    displayTodos();
}


function deleteTodo(index) {

    todos.splice(index, 1);

    displayTodos();
}


function clearCompleted() {

    todos = todos.filter(function(todo) {

        return !todo.completed;

    });

    displayTodos();
}


document.getElementById("todoInput").addEventListener(
    "keyup",
    function(event) {

        if (event.key === "Enter") {

            addTodo();

        }

    }
);


displayTodos();