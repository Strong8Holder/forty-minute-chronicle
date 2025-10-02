# chrono-beat-logger

Snapshots кожні **40 хв** (UTC) з часовими полями:
- UTC/Unix, ISO week, day-of-year
- Локальні часи для Києва та Нью-Йорка (приблизний зсув)
- `bucket40` (0..2) та короткий `checksum`

## Як запустити

1. Створи репозиторій і додай ці файли.
2. У `.github/workflows/snapshot.yml` **замінити**:
   - `YOUR_LOGIN` → твій GitHub login
   - `YOUR_ID+YOUR_LOGIN@users.noreply.github.com` → твій no-reply email (див. Profile → Emails)
3. Зайди **Settings → Secrets and variables → Actions → New repository secret**:
   - **Name:** `GH_TOKEN`
   - **Value:** твій *fine-grained* Personal Access Token (repo: *Only select repositories* → цей репо; **Contents: Read and write**).
4. **Actions → Enable** (якщо питатиме).
5. Запусти вручну (**Actions → snapshot → Run workflow**) і дочекайся авто-ранів о `*/40`.

> Якщо змінював `snapshot.yml`, зроби коміт у `main`, щоб GitHub підхопив cron.
