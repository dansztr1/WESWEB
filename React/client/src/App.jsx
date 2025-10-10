import { useState, useEffect } from 'react'
import './App.css'
import { NewTodoForm } from './NewTodoForm';
import { TodoList } from './Todolist';
import axios from "axios"
import { use } from 'react';



function App() {

  const [todos, setTodos] = useState([]);

  const fetchAPI = async () => {
    const response = await axios.get("http://localhost:3000/api")
    addTodo(response.data.Fruits[0])
    addTodo(response.data.Fruits[1])
    addTodo(response.data.Fruits[2])
  }

  useEffect(() => {
    fetchAPI();
  }, [])


  function addTodo(title) {
    setTodos((currentTodos) => {
      return [
        ...currentTodos,
        { id: crypto.randomUUID(), title: title, completed: false }
      ]
    })
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
    <NewTodoForm onSubmit={addTodo} />
    <h1 className='header'>Todo List</h1>
    <TodoList todos={todos} toggleTodo={toggleToDo} deleteTodo={deleteTodo} />
  </>
}

export default App
