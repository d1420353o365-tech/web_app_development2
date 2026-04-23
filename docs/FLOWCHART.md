# 流程圖文件 (Flowchart) - 個人 AI 學習助理系統

本文件基於 PRD 與系統架構設計，視覺化「使用者如何操作系統」以及「內部資料如何流動」，並整理出 API 路由對應表。

## 1. 使用者流程圖 (User Flow)

此流程圖描述使用者從點擊進入網站，到使用各項核心功能的操作路徑。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> CheckAuth{是否已登入？}
    
    %% 註冊登入流程
    CheckAuth -->|否| Login[登入 / 註冊頁]
    Login -->|成功| Dashboard
    
    %% 核心流程
    CheckAuth -->|是| Dashboard[首頁 - 學習儀表板]
    Dashboard -->|查看| Chart[學習進度視覺化圖表]
    
    Dashboard --> Menu{選擇功能模組}
    
    %% 筆記模組
    Menu -->|筆記整理| NotesList[筆記列表]
    NotesList -->|新增| UploadNote[輸入/上傳長篇內容]
    UploadNote -->|AI 處理| ViewNote[查看 AI 重點摘要]
    
    %% 學習計畫模組
    Menu -->|學習計畫| PlanList[學習計畫列表]
    PlanList -->|建立| CreatePlan[設定目標與時間]
    CreatePlan -->|AI 生成| ViewPlan[查看自動安排進度]
    
    %% 測驗與錯題模組
    Menu -->|自動化測驗| CreateQuiz[設定測驗範圍/單元]
    CreateQuiz --> TakeQuiz[進行選擇題測驗]
    TakeQuiz -->|送出答案| QuizResult[測驗結果與詳解]
    QuizResult -->|加入錯題本| MistakeBook[錯題紀錄庫與弱點分析]
    
    %% 對話輔助模組
    Dashboard -.->|浮動視窗 / 獨立頁| AIChat[與 AI 對話發問]
    ViewNote -.->|針對筆記提問| AIChat
    TakeQuiz -.->|解題求助| AIChat
```

## 2. 系統序列圖 (System Sequence Diagram)

此圖以「**使用者新增筆記並獲取 AI 摘要**」為例，展示前端、Flask 控制器、AI 服務以及資料庫之間的完整資料流向。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask (Controller)
    participant AI as 第三方 AI (OpenAI API)
    participant DB as SQLite DB
    
    User->>Browser: 在表單中貼上長篇課堂筆記並送出
    Browser->>Flask: POST /notes/create (包含筆記內容)
    Flask->>Flask: 驗證內容長度與使用者身分
    
    Flask->>AI: 呼叫 API 請求內容摘要擷取
    AI-->>Flask: 回傳重點摘要 (JSON 或文本)
    
    Flask->>DB: INSERT INTO notes (user_id, 原文, 摘要內容)
    DB-->>Flask: 儲存成功
    
    Flask-->>Browser: HTTP 302 重導向至 /notes/<id> (單篇筆記頁)
    Browser->>Flask: GET /notes/<id>
    Flask->>DB: 查詢該筆記資料
    DB-->>Flask: 回傳 Note 物件
    Flask->>Flask: 使用 Jinja2 渲染 note_detail.html
    Flask-->>Browser: 回傳完整 HTML 網頁
    Browser-->>User: 畫面顯示 AI 整理好的筆記摘要
```

## 3. 功能清單對照表

根據上述功能需求，規劃 Flask 的 URL 路由、HTTP 方法及對應的操作：

| 功能模組 | 操作描述 | HTTP 方法 | URL 路徑 (Route) | 對應的樣板 (Template) |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與授權** | 首頁 / 學習儀表板進度圖表 | GET | `/` | `index.html` |
| | 會員登入 | GET / POST | `/auth/login` | `auth/login.html` |
| | 會員註冊 | GET / POST | `/auth/register` | `auth/register.html` |
| | 會員登出 | GET | `/auth/logout` | 重導向至登入頁 |
| **AI 筆記整理** | 筆記列表 | GET | `/notes` | `notes/list.html` |
| | 新增筆記與產生摘要 | GET / POST | `/notes/create` | `notes/create.html` |
| | 查看單篇筆記與摘要 | GET | `/notes/<id>` | `notes/detail.html` |
| **智能學習計畫** | 計畫列表 | GET | `/plan` | `plans/list.html` |
| | 新增自訂學習目標與計畫 | GET / POST | `/plan/generate` | `plans/generate.html` |
| **自動出題與測驗** | 產生新測驗卷 | GET / POST | `/quiz/generate` | `quizes/generate.html` |
| | 進行測驗與送出答案 | GET / POST | `/quiz/<id>` | `quizes/take.html` |
| | 測驗結果 (含詳解) | GET | `/quiz/<id>/result` | `quizes/result.html` |
| | 錯題本與弱點追蹤 | GET | `/quiz/mistakes` | `quizes/mistakes.html` |
| **對話式輔助** | 語音/文字對話介面 | GET / POST | `/chat` | `chat/chat.html` |
