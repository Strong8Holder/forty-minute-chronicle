#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def kyiv_tz():
    # простий зсув +2/+3 залежно від літнього часу (емулюємо EET/EEST)
    now_utc = datetime.now(timezone.utc)
    # умовно: березень-жовтень = +3, інакше +2 (неідеально, але без зовн. API)
    month = now_utc.month
    offset = 3 if 3 <= month <= 10 else 2
    return timezone(timedelta(hours=offset), name=f"UTC+{offset}")

def ny_tz():
    # умовний EST/EDT: березень-листопад = -4, інакше -5
    now_utc = datetime.now(timezone.utc)
    offset = -4 if 3 <= now_utc.month <= 11 else -5
    return timezone(timedelta(hours=offset), name=f"UTC{offset}")

def minute_bucket_40(dt_utc: datetime) -> int:
    # 40-хв пульс: 0..2 (00..39 -> 0, 40..59 -> 1, 20..39 наступної години -> 2)
    return (dt_utc.minute // 20) % 3

def build_payload() -> dict:
    now_utc = datetime.now(timezone.utc)
    kyiv = now_utc.astimezone(kyiv_tz())
    ny   = now_utc.astimezone(ny_tz())

    iso_week = int(now_utc.strftime("%V"))
    day_of_year = int(now_utc.strftime("%j"))
    unix = int(now_utc.timestamp())

    # короткий checksum, щоб відрізняти снапшоти навіть без реальних даних
    raw = f"{now_utc.isoformat()}|{iso_week}|{day_of_year}|{unix}"
    checksum = hashlib.sha256(raw.encode()).hexdigest()[:12]

    note = [
        "tick",
        "tock",
        "pulse",
    ][minute_bucket_40(now_utc)]

    return {
        "ts_utc": now_utc.isoformat(),
        "unix": unix,
        "iso_week": iso_week,
        "day_of_year": day_of_year,
        "zones": {
            "kyiv": kyiv.isoformat(),
            "new_york": ny.isoformat(),
        },
        "bucket40": minute_bucket_40(now_utc),  # 0..2
        "note": note,
        "checksum": checksum,
        "source": "chrono-beat-logger/stdlib",
        "repo_hint": "unique-format-v2",  # щоб явно відрізнялось від інших
    }

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def main() -> int:
    payload = build_payload()

    dt_utc = datetime.now(timezone.utc)
    folder = DATA / dt_utc.strftime("%Y-%m-%d")
    ensure_dir(folder)
    outfile = folder / f"{dt_utc.strftime('%H%M%S')}.json"

    with outfile.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[update.py] wrote file: {outfile.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
