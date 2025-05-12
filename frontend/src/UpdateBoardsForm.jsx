import { useState } from "react";

const UpdateBoardsForm = ({updateCallback}) => {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const onSubmit = async (e) => {
        e.preventDefault()

        console.log("정보대 홈피 게시판을 스크래핑하는 중입니다!")
    
        const data = {
          startDate,
          endDate
        }
    
        const response = await fetch('https://kuci-automation.onrender.com/update_boards', {
          // mode: 'no-cors',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })

        updateCallback() // fetchBoards() 업데이트된 Boards들을 표시하기 위해 새로고침함.
        
        if (!response.ok) { // 실패했을 경우
          console.log("게시판 스크래핑에 실패했습니다!")
          const data = await response.json()
          alert(data.message)
        } else {
          console.log("게시판 스크래핑이 완료되었습니다!")
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
            <button type="submit">게시판 스크랩하기 (1분정도 소요됩니다.)</button>
        </form>
      );
};

export default UpdateBoardsForm