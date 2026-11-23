
const API_URL = "";

const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const chatMessages = document.getElementById("chatMessages");
const welcomeSection = document.getElementById("welcomeSection");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");

const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");


// Safely escape text before rendering
function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}


// Render basic Markdown safely
function renderMarkdown(markdown) {
    const lines = String(markdown).replace(/\r/g, "").split("\n");
    let html = "";
    let paragraph = [];
    let listType = null;
    let listItems = [];
    let i = 0;

    function inlineFormat(value) {
    const brToken = "\uE000";

    const normalized = String(value).replace(
        /<br\s*\/?>/gi,
        brToken
    );

    return escapeHTML(normalized)
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.+?)\*/g, "<em>$1</em>")
        .replace(/`(.+?)`/g, "<code>$1</code>")
        .split(brToken).join("<br>");
}

    function flushParagraph() {
        if (paragraph.length) {
            html += `<p>${inlineFormat(paragraph.join(" "))}</p>`;
            paragraph = [];
        }
    }

    function flushList() {
        if (listType && listItems.length) {
            html += `<${listType}>`;
            listItems.forEach(item => {
                html += `<li>${inlineFormat(item)}</li>`;
            });
            html += `</${listType}>`;
        }

        listType = null;
        listItems = [];
    }

    while (i < lines.length) {
        const line = lines[i];
        const trimmed = line.trim();

        // Markdown table
        if (
            trimmed.startsWith("|") &&
            i + 1 < lines.length &&
            /^\|[\s|:-]+\|?$/.test(lines[i + 1].trim())
        ) {
            flushParagraph();
            flushList();

            const headers = trimmed.split("|")
                .slice(1, -1)
                .map(cell => cell.trim());

            html += "<div class='table-scroll'><table><thead><tr>";

            headers.forEach(header => {
                html += `<th>${inlineFormat(header)}</th>`;
            });

            html += "</tr></thead><tbody>";

            i += 2;

            while (i < lines.length && lines[i].trim().startsWith("|")) {
                const cells = lines[i].trim()
                    .split("|")
                    .slice(1, -1)
                    .map(cell => cell.trim());

                html += "<tr>";

                cells.forEach(cell => {
                    html += `<td>${inlineFormat(cell)}</td>`;
                });

                html += "</tr>";
                i++;
            }

            html += "</tbody></table></div>";
            continue;
        }

        if (!trimmed) {
            flushParagraph();
            flushList();
            i++;
            continue;
        }

        // Headings
        const heading = trimmed.match(/^(#{1,3})\s+(.+)$/);

        if (heading) {
            flushParagraph();
            flushList();

            const level = heading[1].length;
            html += `<h${level}>${inlineFormat(heading[2])}</h${level}>`;

            i++;
            continue;
        }

        // Lists
        const bullet = trimmed.match(/^[-*]\s+(.+)$/);
        const numbered = trimmed.match(/^\d+[.)]\s+(.+)$/);

        if (bullet || numbered) {
            flushParagraph();

            const newType = numbered ? "ol" : "ul";

            if (listType && listType !== newType) {
                flushList();
            }

            listType = newType;
            listItems.push((bullet || numbered)[1]);

            i++;
            continue;
        }

        flushList();
        paragraph.push(trimmed);
        i++;
    }

    flushParagraph();
    flushList();

    return html;
}


// Check backend health
async function checkHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        const data = await response.json();

        if (data.status !== "healthy") {
            throw new Error("Service unhealthy");
        }

        statusDot.className = "status-dot online";
        statusText.textContent = "AI Assistant Online";

    } catch (error) {
        statusDot.className = "status-dot offline";
        statusText.textContent = "Connection unavailable";
    }
}


// Add a message to chat
function addMessage(role, content, citations = []) {
    const message = document.createElement("div");

    message.className = role === "user"
        ? "message user-message"
        : "message assistant-message";

    if (role === "assistant") {
        const label = document.createElement("span");
        label.className = "message-label";
        label.textContent = "SHRAMIKSATHI AI";

        message.appendChild(label);

        const answer = document.createElement("div");
        answer.className = "answer-content";
        answer.innerHTML = renderMarkdown(content);

        message.appendChild(answer);

        // Display citations
        if (citations.length > 0) {
            const sourcesBox = document.createElement("div");
            sourcesBox.className = "sources-box";

            const heading = document.createElement("h4");
            heading.textContent = "📚 Official Sources";
            sourcesBox.appendChild(heading);

            citations.forEach((citation, index) => {
                const source = document.createElement("div");
                source.className = "source-item";

                const title = document.createElement("strong");
                title.textContent =
                    `${index + 1}. ${citation.title || "Official document"}`;

                const details = document.createElement("span");
                details.textContent =
                    `${citation.source || "Source unavailable"} · Page ${citation.page ?? "N/A"}`;

                source.appendChild(title);
                source.appendChild(details);
                sourcesBox.appendChild(source);
            });

            message.appendChild(sourcesBox);
        }

    } else {
        message.textContent = content;
    }

    chatMessages.appendChild(message);

    message.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });
}


// Send question to FastAPI
async function askQuestion(question) {
    if (!question || question.length > 500) {
        return;
    }

    welcomeSection.style.display = "none";

    addMessage("user", question);

    const loading = document.createElement("div");
    loading.className = "message assistant-message loading-message";
    loading.textContent = "ShramikSathi is finding the relevant information...";

    chatMessages.appendChild(loading);

    sendBtn.disabled = true;
    sendBtn.querySelector("span").textContent = "Thinking...";

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
                errorData.detail || `Request failed (${response.status})`
            );
        }

        const result = await response.json();

        loading.remove();

        const answer = result.answer || "No answer received.";

        addMessage(
            "assistant",
            answer,
            result.citations || []
        );

        if (result.answerable === false) {
            statusText.textContent = "Limited information available";
        } else {
            statusText.textContent = "AI Assistant Online";
        }

    } catch (error) {
        loading.remove();

        addMessage(
            "assistant",
            `Unable to process your question. ${error.message || "Please try again."}`
        );

        statusDot.className = "status-dot offline";
        statusText.textContent = "Request failed";

    } finally {
        sendBtn.disabled = false;
        sendBtn.querySelector("span").textContent = "Send";
        questionInput.focus();
    }
}


// Submit chat form
chatForm.addEventListener("submit", event => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    questionInput.value = "";
    questionInput.style.height = "43px";

    askQuestion(question);
});


// Enter submits; Shift + Enter creates a new line
questionInput.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});


// Auto-expand textarea
questionInput.addEventListener("input", () => {
    questionInput.style.height = "43px";
    questionInput.style.height =
        `${Math.min(questionInput.scrollHeight, 120)}px`;
});


// Topic and suggestion buttons
document.querySelectorAll("[data-question]").forEach(button => {
    button.addEventListener("click", () => {
        const question = button.dataset.question;

        if (question) {
            askQuestion(question);
        }
    });
});


// Start a new conversation
newChatBtn.addEventListener("click", () => {
    chatMessages.innerHTML = "";
    welcomeSection.style.display = "block";
    questionInput.value = "";
    questionInput.focus();
});


// Initial health check
checkHealth();

// Recheck service periodically
setInterval(checkHealth, 30000);
