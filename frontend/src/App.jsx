import { useEffect, useState } from 'react'
import './App.css'
import BoardList from './BoardList'
import UpdateBoardsForm from './UpdateBoardsForm'

function App() {
  const [boards, setBoards] = useState([])

  useEffect(() => {
    fetchBoards() // 앱 실행되면 이 함수 자동으로 실행함.
  }, [])

  const fetchBoards = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/boards')
      const data = await response.json()
      setBoards(data.boards)
    } catch (error) {
      console.error("Error fetching contacts:", error)
    }
  }
  

  return (
    <>
      <UpdateBoardsForm updateCallback={fetchBoards}/>
      <BoardList boards={boards}/>
    </>
  )
}

export default App