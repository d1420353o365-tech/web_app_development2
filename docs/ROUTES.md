# 路由設計文件 (Routes) - 個人 AI 學習助理系統

## 1. 路由總覽表格

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **主頁面** | GET | `/` | `index.html` | 顯示首頁或個人的學習進度儀表板 |
| **會員登入** | GET, POST | `/auth/login` | `auth/login.html` | 顯示登入表單與接收登入請求 |
| **會員註冊** | GET, POST | `/auth/register` | `auth/register.html` | 顯示註冊表單與接收註冊請求 |
| **會員登出** | GET | `/auth/logout` | — | 執行登出並重導向至登入頁 |
| **筆記列表** | GET | `/notes` | `notes/index.html` | 顯示個人的所有筆記與摘要清單 |
| **新增筆記** | GET, POST | `/notes/create` | `notes/create.html` | 輸入原文，POST後由 AI 產生摘要 |
| **筆記詳情** | GET | `/notes/<id>` | `notes/detail.html` | 顯示單篇筆記的完整內容與摘要 |
| **刪除筆記** | POST | `/notes/<id>/delete` | — | 刪除單篇筆記 |
| **計畫列表** | GET | `/plan` | `plans/index.html` | 顯示所有已排定的學習計畫 |
| **產生計畫** | GET, POST | `/plan/generate` | `plans/generate.html` | 填寫目標與時間，產生 AI 規劃 |
| **刪除計畫** | POST | `/plan/<id>/delete` | — | 刪除指定的學習計畫 |
| **建立測驗** | GET, POST | `/quiz/generate` | `quizes/generate.html` | 選擇範圍並交由 AI 產生測驗題 |
| **進行測驗** | GET, POST | `/quiz/<id>` | `quizes/take.html` | 呈現題目供填答，POST 送出結果 |
| **測驗結果** | GET | `/quiz/<id>/result` | `quizes/result.html` | 顯示對錯與 AI 分析詳解 |
| **錯題本** | GET | `/quiz/mistakes` | `quizes/mistakes.html` | 列出使用者歷史的答錯題目 |
| **對話輔助** | GET, POST | `/chat` | `chat/chat.html` | 提供 AI 對話發問介面 (POST 處理請求) |

## 2. 路由詳細說明

### 2.1 主頁面 / 儀表板 (Main)
- **GET `/`**：
  - 輸入：Session 中的用戶身分。
  - 處理：若未登入導向 `/auth/login`。若已登入，讀取使用者的進度、計畫數據。
  - 輸出：渲染 `index.html`。

### 2.2 會員模組 (Auth)
- **POST `/auth/login`**：
  - 輸入：表單欄位 (`email`, `password`)。
  - 處理：呼叫 `User.get_by_email`，驗證密碼，寫入 Session。
  - 輸出：成功重導向 `/`，失敗重新渲染 `auth/login.html` 附帶錯誤訊息。

### 2.3 筆記模組 (Notes)
- **POST `/notes/create`**：
  - 輸入：表單欄位 (`title`, `original_content`)。
  - 處理：發送內容至外部 AI 服務提取摘要。呼叫 `Note.create` 將原文與摘要存入 SQLite。
  - 輸出：重導向至單篇詳情頁 `/notes/<id>`。

### 2.4 計畫模組 (Plan)
- **POST `/plan/generate`**：
  - 輸入：表單欄位 (`goal`, `time_allocated`)。
  - 處理：將目標與可用時數組合 Prompt 交由 AI 生成 Schedule。然後呼叫 `Plan.create` 存入 DB。
  - 輸出：重導向至計畫列表 `/plan`。

### 2.5 測驗與錯題模組 (Quiz)
- **POST `/quiz/generate`**：
  - 輸入：表單選取的 `note_id` 或手動輸入的內容條件。
  - 處理：利用 AI 依條件產生選擇題。建立 Quiz 並將題目存入 QuizQuestion。
  - 輸出：重導向至 `/quiz/<new_id>` 開始作答。
- **POST `/quiz/<id>`**：
  - 輸入：各題的選填答案 (`answer_1`, `answer_2`...)。
  - 處理：比對正確答案，計算 `total_score`。錯題則建立 Mistake 實體紀錄。
  - 輸出：重導向至 `/quiz/<id>/result`。

## 3. Jinja2 模板清單

所有的模板將繼承自一個基礎版型 `base.html`，以保持視覺一致性與共用選單。

- `base.html`：包含 Navbar (首頁、筆記、計畫、測驗錯題、智能對話、登出) 及全域 CSS/JS。
- **Main**: `index.html` (儀表板)
- **Auth**: `auth/login.html`, `auth/register.html`
- **Notes**: `notes/index.html`, `notes/create.html`, `notes/detail.html`
- **Plans**: `plans/index.html`, `plans/generate.html`
- **Quizes**: `quizes/generate.html`, `quizes/take.html`, `quizes/result.html`, `quizes/mistakes.html`
- **Chat**: `chat/chat.html`

## 4. 程式骨架說明
各模組路由骨架皆以 Blueprint 結構建立於 `app/routes/` 內。
