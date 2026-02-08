import pandas as pd
from src.data_loader import load_data


def race_results_summary_by_accident(data, circuits):
    df = (
        data
        .groupby('raceId')
        .agg(
            year=('year', 'first'),
            race_name=('name', 'first'),
            circuitId=('circuitId', 'first'),

            finished_count=('statusGroup', lambda x: (x == 'Finished').sum()),
            notfinished_count=('statusGroup', lambda x: (x == 'NotFinishedNotDNF').sum()),
            dnf_count=('statusGroup', lambda x: (x == 'DNF').sum()),

            total_entries=('statusGroup', 'size'),

            accidents_dnf=('dnfStatus', lambda x: x.isin(['Accident / Collision', 'Car Damage']).sum()),
            mechanical_dnf=('dnfStatus', lambda x: (x == 'Mechanical Failure').sum()),
            other_dnf=('dnfStatus', lambda x: x.isin(['Regulations / Technical', 'Strategic / Race']).sum())
        )
        .reset_index()
    )

    df['total_started'] = df['finished_count'] + df['dnf_count']



    df = df.merge(circuits[['circuitId', 'name']], on='circuitId', how='left')
    df = df.rename(columns={'name':'circuitName'})
    df['dnf_percent'] = ((df['dnf_count'] / df['total_started']) * 100).round(2)
    df['accidents_percent'] = ((df['accidents_dnf'] / df['total_started']) * 100).round(2)
    df['mechanical_percent'] = ((df['mechanical_dnf'] / df['total_started']) * 100).round(2)

    df = df[
        ['year', 'race_name', 'circuitName','circuitId', 'total_started', 'dnf_count',
         'accidents_dnf', 'mechanical_dnf', 'other_dnf', 'notfinished_count', 'total_entries', 'accidents_percent','mechanical_percent']
    ]
    return df


def summary_accidents_by_circuits(data):
    df = (
        data
        .groupby('circuitId')
        .agg(
            circuitName=('circuitName', 'first'),
            total_started=('total_started', 'sum'),
            dnf_count=('dnf_count', 'sum'),
            accidents_count=('accidents_dnf', 'sum'),
            mechanical_count=('mechanical_dnf', 'sum'),
            other_count=('other_dnf', 'sum'),
            num_races=('race_name', 'count')
        )
        .reset_index()
    )

    df['dnf_percent'] = ((df['dnf_count'] / df['total_started']) * 100).round(2)
    df['accident_percent'] = ((df['accidents_count'] / df['total_started']) * 100).round(2)
    df['mechanical_percent'] = ((df['mechanical_count'] / df['total_started']) * 100).round(2)
    df['other_percent'] = ((df['other_count'] / df['total_started']) * 100).round(2)

    df = df[df['num_races'] >=5]
    df = df.sort_values('dnf_percent', ascending=True)
    return df