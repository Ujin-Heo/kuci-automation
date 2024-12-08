import { useState } from "react";
import axios from "axios";
import FileSaver from "file-saver";

const CreateResultsForm = () => {
    const [month, setMonth] = useState("");
    const [week, setWeek] = useState("");
    const [writer, setWriter] = useState("");

    const downloadAnnouncement = async (e) => {
        e.preventDefault()

        const data = {
            month,
            week,
            writer
        }

        const downloadUrl = "http://127.0.0.1:5000/announcement";

        try {
            const response = await axios.post(downloadUrl, data, {
                responseType: "blob", // Ensure binary data is returned
            });
    
            const disposition = response.headers["content-disposition"];
            let filename = "announcement.txt"; // Default fallback filename
            if (disposition && disposition.includes("filename*=")) {
                // Handle UTF-8 encoded filename
                const matches = disposition.match(/filename\*=(?:UTF-8'')?(.+)/i);
                if (matches && matches[1]) {
                    filename = decodeURIComponent(matches[1]); // Decode the filename
                }
            } else if (disposition && disposition.includes("filename=")) {
                // Handle non-encoded filename
                const matches = disposition.match(/filename=['"]?([^'"]+)/i);
                if (matches && matches[1]) {
                    filename = matches[1];
                }
            }
    
            const blob = new Blob([response.data], { type: "text/plain" });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = filename; // Use the extracted filename
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error("Failed to download the announcement file:", error);
        }
    };

    const downloadPPT = async (e) => {
        e.preventDefault()

        const data = {
            month,
            week,
            writer
        }

        const response = await fetch("http://127.0.0.1:5000/ppt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
    
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            // link.download = "전공소식공유.pptx";
            document.body.appendChild(link);
            link.click();
            link.remove();
        } else {
            console.error("Failed to download the PPT file.");
        }
    }

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
            <button type="button" onClick={downloadAnnouncement}>공지글 작성하기</button>
            <button type="button" onClick={downloadPPT}>PPT 만들기</button>
        </form>
      );
};

export default CreateResultsForm