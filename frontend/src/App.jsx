import { useEffect, useState } from 'react'
import './App.css'
import BoardList from './BoardList'
import UpdateBoardsForm from './UpdateBoardsForm'
import CreateResultsForm from './CreateResultsFrom'

function formatDate(dateString) {
  const date = new Date(dateString);
  const formattedDate = date.toISOString().split('T')[0] + ' ' + date.toTimeString().split(' ')[0];
  return formattedDate;
}

function App() {
  const [boards, setBoards] = useState([])
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [lastUpdatedTime, setLastUpdatedTime] = useState("")
  const [hasSavedData, setHasSavedData] = useState(false)

  useEffect(() => {
    fetchBoards() // 앱 실행되면 이 함수 자동으로 실행함.
  }, [])

  const fetchBoards = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/boards')
      const data = await response.json()

      const formattedLastUpdatedTime = formatDate(data.metaData.lastUpdatedTime);

      setStartDate(data.metaData.startDate)
      setEndDate(data.metaData.endDate)
      setLastUpdatedTime(formattedLastUpdatedTime)
      if (startDate !== null && endDate !== null && lastUpdatedTime !== null) setHasSavedData(true)

      setBoards(data.boards)
    } catch (error) {
      console.error("Error fetching contacts:", error)
    }
  }
  

  return (
    <>
      <div className="modal">
        <h1 className='title'>전공소식공유 메이커 2.0</h1>
        <div className='title-div'>
          <span className='title-caption'></span>
          <span className='title-caption'></span>
          <span className='title-caption'>created by 교육진로국장 허우진</span>
        </div>
      </div>
      { hasSavedData && <div className='modal'>
          <h1 className='modal-title'>스크랩한 날짜의 범위: {startDate} ~ {endDate}</h1>
          <span className='modal-text'>last updated: {lastUpdatedTime}</span>
        </div>
      }
      <UpdateBoardsForm updateCallback={fetchBoards}/>
      <CreateResultsForm/>
      <BoardList boards={boards}/>
    </>
  )
}

export default App