import { useState } from "react";

const UpdateBoardsForm = ({ updateCallback }) => {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const onSubmit = async (e) => {
        try {
            e.preventDefault();

            console.log("정보대 홈피 게시판을 스크래핑하는 중입니다!");

            const query = new URLSearchParams({
                start_date: startDate,
                end_date: endDate,
            }).toString();

            const response = await fetch(
                `${import.meta.env.VITE_API_BASE_URL}/update_boards?${query}`
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Unknown server error");
            }

            const data = await response.json();
            console.log(data.message);

            updateCallback(); // fetchBoards() 업데이트된 Boards들을 표시하기 위해 새로고침함.
        } catch (error) {
            console.error("게시판을 스크래핑하는 데 실패했습니다.:", error);
        }
    };

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
            <button type="submit">
                게시판 스크랩하기 (1분정도 소요됩니다.)
            </button>
        </form>
    );
};

export default UpdateBoardsForm;
