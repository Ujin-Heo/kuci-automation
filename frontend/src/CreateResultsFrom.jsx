import { useState } from "react";

const CreateResultsForm = () => {
    const [month, setMonth] = useState("");
    const [week, setWeek] = useState("");
    const [writer, setWriter] = useState("");

    const downloadAnnouncement = async (e) => {
        e.preventDefault();

        const data = { month, week, writer };

        const response = await fetch(
            `${import.meta.env.VITE_API_BASE_URL}/announcement`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            }
        );

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = `${month}월_${week}주차_전공소식공유.txt`; // Default filename
            document.body.appendChild(link);
            link.click();
            link.remove();
        } else {
            console.error("Failed to download the announcement file.");
        }
    };

    const downloadPPT = async (e) => {
        e.preventDefault();

        const data = { month, week, writer };

        const response = await fetch(
            `${import.meta.env.VITE_API_BASE_URL}/ppt`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            }
        );

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = `${month}월_${week}주차_전공소식공유.pptx`;
            document.body.appendChild(link);
            link.click();
            link.remove();
        } else {
            console.error("Failed to download the PPT file.");
        }
    };

    return (
        <form onSubmit={(e) => e.preventDefault()}>
            <div>
                <label htmlFor="month">월:</label>
                <input
                    type="text"
                    id="month"
                    value={month}
                    onChange={(e) => setMonth(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="week">주차:</label>
                <input
                    type="text"
                    id="week"
                    value={week}
                    onChange={(e) => setWeek(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="writer">작성자:</label>
                <input
                    type="text"
                    id="writer"
                    value={writer}
                    onChange={(e) => setWriter(e.target.value)}
                />
            </div>
            <button type="button" onClick={downloadAnnouncement}>
                공지글 작성하기
            </button>
            <button type="button" onClick={downloadPPT}>
                PPT 만들기
            </button>
        </form>
    );
};

export default CreateResultsForm;
