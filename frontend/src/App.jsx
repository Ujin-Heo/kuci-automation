import { useEffect, useState } from "react";
import "./App.css";
import BoardList from "./BoardList";
import UpdateBoardsForm from "./UpdateBoardsForm";
import CreateResultsForm from "./CreateResultsFrom";

function formatDate(dateString) {
    const date = new Date(dateString);
    const formattedDate =
        date.toISOString().split("T")[0] +
        " " +
        date.toTimeString().split(" ")[0];
    return formattedDate;
}

function App() {
    const [boards, setBoards] = useState([]);
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [lastUpdatedTime, setLastUpdatedTime] = useState("");
    const [hasSavedData, setHasSavedData] = useState(false);

    useEffect(() => {
        fetchBoards();
    }, []);

    const fetchBoards = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_BASE_URL}/get_boards`
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Unknown server error");
            }

            const data = await response.json();

            if (data.metaData) {
                const formattedLastUpdatedTime = formatDate(
                    data.metaData.lastUpdatedTime
                );

                setStartDate(data.metaData.startDate);
                setEndDate(data.metaData.endDate);
                setLastUpdatedTime(formattedLastUpdatedTime);
            }

            if (
                startDate !== null &&
                endDate !== null &&
                lastUpdatedTime !== null
            )
                setHasSavedData(true);

            setBoards(data.boards);

            // console.log(data.message); // [서버 메시지] 게시글을 성공적으로 불러왔습니다. <- 이건데 성가셔서 일단 꺼놓음
        } catch (error) {
            console.error("게시글을 불러오는 데 실패했습니다.:", error);
        }
    };

    const initializeBoards = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_BASE_URL}/initialize_boards`
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Unknown server error");
            }

            const data = await response.json();
            console.log(data.message);

            fetchBoards();
        } catch (error) {
            console.error("게시판을 초기화하는 데 실패했습니다.:", error);
        }
    };

    return (
        <>
            <div className="modal">
                <h1 className="title">전공소식공유 메이커 3.0</h1>
                <div className="title-div">
                    <span className="title-caption"></span>
                    <span className="title-caption"></span>
                    <span className="title-caption">
                        created by 교육진로국장 허우진
                    </span>
                </div>
                <button onClick={initializeBoards}>DB 초기화</button>
            </div>
            {hasSavedData && (
                <div className="modal">
                    <h1 className="modal-title">
                        스크랩한 날짜의 범위: {startDate} ~ {endDate}
                    </h1>
                    <span className="modal-text">
                        last updated: {lastUpdatedTime}
                    </span>
                </div>
            )}
            <UpdateBoardsForm updateCallback={fetchBoards} />
            <CreateResultsForm />
            <BoardList boards={boards} />
        </>
    );
}

export default App;
