import { useState, useEffect } from 'react'
import './App.css'
import { NewTodoForm } from './NewTodoForm';
import { TodoList } from './Todolist';
import axios from "axios"
import { use } from 'react';



function App() {

  const [todos, setTodos] = useState([]);

  const fetchAPI = async () => {
    try {
      const response = await axios.get("http://localhost:3000/getNotes");

      const notes = response.data; // should be an array of { key, value }

      notes.forEach((note) => {
        addTodo({ id: note.key, title: note.value, completed: false });
      });
    } catch (error) {
      console.error("Failed to fetch notes:", error);
    }
  };


  useEffect(() => {
    fetchAPI();
  }, [])


  function createTodo(title) {
    const id = crypto.randomUUID();
    const todo = { id, title, completed: false };

    axios.post("http://localhost:3000/addNote", { id, title});

    setTodos((currentTodos) => [...currentTodos, todo]);
  }


  function addTodo(todo) {
    setTodos((currentTodos) => [...currentTodos, todo]);
  }



  function toggleToDo(id, completed) {
    setTodos(currentTodos => {
      return currentTodos.map(todo => {
        if (todo.id === id) {
          return { ...todo, completed }
        }
        return todo
      })
    })
  }

  function deleteTodo(id) {
    setTodos(currentTodos => {
      return currentTodos.filter(todo => todo.id !== id)
    })
  }

  return <>
    <NewTodoForm onSubmit={createTodo} />
    <h1 className='header'>Todo List</h1>
    <TodoList todos={todos} toggleTodo={toggleToDo} deleteTodo={deleteTodo} />
  </>
}

export default App
