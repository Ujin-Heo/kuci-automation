import { useState } from "react";

const UpdateBoardsForm = ({updateCallback}) => {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const onSubmit = async (e) => {
        e.preventDefault()
    
        const data = {
          startDate,
          endDate
        }
    
        const response = await fetch('http://127.0.0.1:5000/update_boards', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        
        if (!response.ok) { // 실패했을 경우
          const data = await response.json()
          alert(data.message)
        } else {
          updateCallback() // fetchBoards() 업데이트된 Boards들을 표시하기 위해 새로고침함.
        }
    
        // try {
              // 여기 안에 위 코드 작성
        // } catch (error) {
        //   console.error("Error updating boards:", error)
        //   alert("An error occurred while updating boards.")
        // }
      }

      return (
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="startDate">Start Date:</label>
                <input
                    type="date"
                    id="startDate"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="endDate">End Date:</label>
                <input
                    type="date"
                    id="endDate"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </div>
            <button type="submit">Update Boards</button>
        </form>
      );
};

export default UpdateBoardsForm