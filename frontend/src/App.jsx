import { useEffect, useState } from 'react'
import './App.css'
import BoardList from './BoardList'

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
  
  const updateBoards = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/update_boards', {
        method: 'POST',
      })
      
      if (!response.ok) { // 실패했을 경우
        const data = await response.json()
        alert(data.message)
      } else {
        fetchBoards() // 업데이트된 Boards들을 표시하기 위해 새로고침함.
      }
    } catch (error) {
      console.error("Error updating boards:", error)
      alert("An error occurred while updating boards.")
    }
  }
  
  return (
    <>
      <BoardList boards={boards}/>
      <button onClick={updateBoards}>Update Boards</button>
    </>
  )
}

export default App