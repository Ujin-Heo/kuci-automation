import { useState } from "react";

const UpdateBoardsForm = ({ updateCallback }) => {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const onSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log("정보대 홈피 게시판을 스크래핑하는 중입니다!");

            const query = new URLSearchParams({
                start_date: startDate,
                end_date: endDate,
            }).toString();

            const socket = new WebSocket(
                `${import.meta.env.VITE_WS_BASE_URL}/update_boards?${query}`
            );

            socket.onopen = () => {
                console.log("WebSocket 연결됨: 게시판 스크래핑 시작");
            };

            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);

                if (data.status === "success") {
                    console.log(data.message);
                    updateCallback();
                } else if (data.status === "error") {
                    console.error(data.message);
                } else if (data.status === "done") {
                    console.log(data.message);
                    updateCallback();
                }
            };

            socket.onclose = () => {
                console.log("WebSocket 연결 종료됨: 스크래핑 완료");
                updateCallback(); // fetchBoards() 업데이트된 Boards들을 표시하기 위해 새로고침함.
            };

            socket.onerror = (err) => {
                console.error("WebSocket 에러:", err);
            };
        } catch (error) {
            console.error(
                "WebSocket으로 게시판을 스크래핑하는 데 실패했습니다.:",
                error
            );
        }
    };

    const onSummaryBtnClick = async (e) => {
        e.preventDefault();

        try {
            console.log(
                "다음 게시판의 게시물을 요약하여 불러오는 중입니다.: 행사 및 소식, 진로정보(공모전), 진로정보(교육)"
            );

            const socket = new WebSocket(
                `${import.meta.env.VITE_WS_BASE_URL}/summarize`
            );

            socket.onopen = () => {
                console.log("WebSocket 연결됨: 게시물 요약 시작");
            };

            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);

                if (data.status === "success") {
                    console.log(data.message);
                    updateCallback();
                } else if (data.status === "error") {
                    console.error(data.message);
                } else if (data.status === "done") {
                    console.log(data.message);
                    updateCallback();
                }
            };

            socket.onclose = () => {
                console.log("WebSocket 연결 종료됨: 게시물 요약 불러오기 완료");
                updateCallback();
            };

            socket.onerror = (err) => {
                console.error("WebSocket 에러:", err);
            };
        } catch (error) {
            console.error(
                "WebSocket으로 게시물 요약을 불러오는 데 실패했습니다.:",
                error
            );
        }
    };

    return (
        <form onSubmit={(e) => e.preventDefault()}>
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
            <div>
                <button type="button" onClick={onSubmit}>
                    게시판 스크랩하기
                </button>
                <button type="button" onClick={onSummaryBtnClick}>
                    게시물 AI 요약
                </button>
            </div>
        </form>
    );
};

export default UpdateBoardsForm;
