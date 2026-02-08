import re
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests import Session
from requests.exceptions import HTTPError


def normalize_engine(power_unit_text: str) -> str:
    t = power_unit_text.lower()
    if 'mercedes' in t:
        return 'Mercedes'
    if 'ferrari' in t:
        return 'Ferrari'
    if 'renault' in t:
        return 'Renault'
    if 'honda' in t:
        return 'Honda'
    return 'Other/Unknown'


def parse_engines_from_season_page(url: str, year: int, session: Session | None = None) -> pd.DataFrame:
    """
    Parse Wikipedia season page table (Constructor + Power unit) -> DataFrame:
    year, constructor_wiki, power_unit_raw, engine_mfr

    Uses requests.Session if provided (recommended) to reduce blocks.
    """
    if session is None:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (F1 engine reliability study; educational)"
        })

    resp = session.get(url, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    target_table = None
    for table in soup.find_all('table', class_='wikitable'):
        header_row = table.find('tr')
        if not header_row:
            continue
        ths = header_row.find_all('th')
        header_names = [th.get_text(" ", strip=True) for th in ths]
        if 'Constructor' in header_names and 'Power unit' in header_names:
            target_table = table
            break

    if target_table is None:
        raise ValueError("Not found table with columns 'Constructor' and 'Power unit'.")

    header_row = target_table.find('tr')
    header_names = [th.get_text(" ", strip=True) for th in header_row.find_all('th')]
    constructor_idx = header_names.index('Constructor')
    power_unit_idx = header_names.index('Power unit')

    rows_out = []
    for row in target_table.find_all('tr')[1:]:
        # Important: first column can be in <th> for data rows
        cells = row.find_all(['th', 'td'])
        if not cells:
            continue

        if max(constructor_idx, power_unit_idx) >= len(cells):
            continue

        constructor = cells[constructor_idx].get_text(" ", strip=True)
        power_unit_raw = cells[power_unit_idx].get_text(" ", strip=True)

        # remove footnotes like [1], [a], etc.
        constructor = re.sub(r'\[[^\]]+\]', '', constructor).strip()
        power_unit_raw = re.sub(r'\[[^\]]+\]', '', power_unit_raw).strip()

        if not constructor or not power_unit_raw:
            continue

        rows_out.append({
            'year': year,
            'constructor_wiki': constructor,
            'power_unit_raw': power_unit_raw,
            'engine_mfr': normalize_engine(power_unit_raw)
        })

    return pd.DataFrame(rows_out).drop_duplicates()


def parse_engines_for_years(years: list[int], base_url: str = "https://en.wikipedia.org/wiki/") -> pd.DataFrame:
    """
    Convenience: parse multiple years using stable World Championship URLs
    with polite delays + retry/backoff. Returns concatenated DataFrame.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (F1 engine reliability study; educational)"
    })

    dfs: list[pd.DataFrame] = []

    for year in years:
        url = f"{base_url}{year}_Formula_One_World_Championship"
        print(f"Parsing {year}...")

        for attempt in range(1, 6):
            try:
                df_year = parse_engines_from_season_page(url, year, session=session)
                dfs.append(df_year)
                break
            except HTTPError as e:
                status = getattr(e.response, "status_code", None)
                if status in (403, 429):
                    sleep_s = (10 * attempt) + random.uniform(0.5, 2.0)  # 10,20,30,40,50 sec
                    print(f"Rate limited ({status}). Sleep {sleep_s:.1f}s (attempt {attempt}/5)")
                    time.sleep(sleep_s)
                    continue
                raise
            except Exception as e:
                print(f"Failed for {year}: {e}")
                break

        # polite delay even after success
        time.sleep(6 + random.uniform(0.5, 2.0))

    if not dfs:
        return pd.DataFrame(columns=['year', 'constructor_wiki', 'power_unit_raw', 'engine_mfr'])

    return pd.concat(dfs, ignore_index=True)
