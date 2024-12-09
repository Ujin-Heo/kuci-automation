import React from "react";

const BoardList = ({boards}) => {
    return <div>
        {boards.map((board) => (
            <div key={board.id}>
                <h2>{board.name}</h2>
                <table>
                    <thead>
                        <tr>
                            <th>날짜</th>
                            <th>제목</th>
                            <th>링크</th>
                            <th>바로가기</th>
                        </tr>
                    </thead>
                    <tbody>
                        {board.articles.map((article) => (
                            <tr key={article.id}>
                                <td>{article.date}</td>
                                <td>{article.title}</td>
                                <td>{article.link}</td>
                                <td>
                                    <a href={article.link} target="_blank" rel="noopener noreferrer"><button>View</button></a>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

            </div>
        ))}
    </div>
}

export default BoardList