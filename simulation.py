from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def gen_rates(symptoms: int, symptoms_per_disease: int) -> list:
    return [
        0.05 + 0.85 * i / symptoms_per_disease
        for i in range(1, symptoms_per_disease + 1)
    ] + [0.05] * (symptoms - symptoms_per_disease)


def gen_rate_table(symptoms: int, symptoms_per_disease: int, diseases: int) -> list:
    rate_table = [gen_rates(symptoms, symptoms_per_disease) for _ in range(diseases)]
    for rates in rate_table:
        random.shuffle(rates)

    return rate_table


def gen_patients(rates: list, patients_per_disease: int) -> list:
    return [
        [random.random() < rate for rate in rates] for _ in range(patients_per_disease)
    ]


def find_prob(rates: list, patient: list, measurements: list) -> float:
    prob = 1
    for rate, sympton, measurement in zip(rates, patient, measurements, strict=True):
        if measurement:
            prob *= rate if sympton else (1 - rate)

    return prob


def diagnose(rate_table: list, patient: list, measurements: list) -> int:
    probs = [find_prob(rates, patient, measurements) for rates in rate_table]
    m = max(probs)
    return random.choice([i for i in range(len(probs)) if probs[i] == m])


def find_accuracies(
    rate_table: list,
    patient_table: list,
    measurement_table: list,
) -> list:
    accuracies = []
    for i, patients, measurements_list in zip(
        range(len(rate_table)),
        patient_table,
        measurement_table,
        strict=True,
    ):
        results = [
            1 if diagnose(rate_table, patient, measurements) == i else 0
            for patient, measurements in zip(
                patients,
                measurements_list,
                strict=True,
            )
        ]
        accuracies.append(sum(results) / len(results))

    return accuracies


def simulate(rate_table: list, patients_per_disease: int, measure: Callable) -> None:
    patient_table = [gen_patients(rates, patients_per_disease) for rates in rate_table]
    measurement_table = [
        [measure(patient) for patient in patients] for patients in patient_table
    ]
    accuracies = find_accuracies(rate_table, patient_table, measurement_table)
    print(f"Average = {sum(accuracies) / len(accuracies)}")
    print(accuracies)


def first_i() -> None:
    rate_table = gen_rate_table(30, 10, 20)
    for i in range(31):
        print(f"{i}: ", end="")
        simulate(rate_table, 1000, lambda _, i=i: [True] * i + [False] * (30 - i))


first_i()
