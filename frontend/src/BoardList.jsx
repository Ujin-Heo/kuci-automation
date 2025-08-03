const BoardList = ({ boards }) => {
    return (
        <div>
            {boards.map((board) => (
                <div key={board.id}>
                    <h2>{board.name}</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>날짜</th>
                                <th>제목</th>
                                <th>본문</th>
                                <th>바로가기</th>
                            </tr>
                        </thead>
                        <tbody>
                            {board.articles.map((article) => (
                                <tr key={article.id}>
                                    <td>{article.date}</td>
                                    <td>{article.title}</td>
                                    <td>
                                        {article.content && (
                                            <div>
                                                <h3 className="article__content">
                                                    <pre>
                                                        <strong>개요</strong>
                                                        {"  "}
                                                        {
                                                            article.content
                                                                .subject
                                                        }
                                                    </pre>
                                                </h3>
                                                <h3 className="article__content">
                                                    <pre>
                                                        <strong>
                                                            신청 기간
                                                        </strong>
                                                        {"  "}
                                                        {
                                                            article.content
                                                                .registrationPeriodOrDeadline
                                                        }
                                                    </pre>
                                                </h3>
                                                <h3 className="article__content">
                                                    <pre>
                                                        <strong>
                                                            행사 기간
                                                        </strong>
                                                        {"  "}
                                                        {
                                                            article.content
                                                                .eventPeriodOrDate
                                                        }
                                                    </pre>
                                                </h3>
                                                <h3 className="article__content">
                                                    <pre>
                                                        <strong>장소</strong>
                                                        {"  "}
                                                        {article.content.venue}
                                                    </pre>
                                                </h3>
                                                <h3 className="article__content">
                                                    <pre>
                                                        <strong>
                                                            신청 방법
                                                        </strong>
                                                        {"  "}
                                                        {
                                                            article.content
                                                                .registrationGuide
                                                        }
                                                    </pre>
                                                </h3>
                                            </div>
                                        )}
                                    </td>
                                    <td>
                                        <a
                                            href={article.link}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            <button>View</button>
                                        </a>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ))}
        </div>
    );
};

export default BoardList;
