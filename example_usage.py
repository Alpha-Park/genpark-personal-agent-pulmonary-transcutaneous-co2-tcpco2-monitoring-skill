"""
Example usage for Pulmonary Transcutaneous Carbon Dioxide (TcPCO2) Skill.
"""

from client import TranscutaneousCO2Client


def main():
    client = TranscutaneousCO2Client()

    print("--- Case 1: Eucapnic Normal Alveolar Ventilation ---")
    normal_case = client.evaluate_tcpco2(
        tcpco2_raw_mmhg=52.5,
        sensor_temperature_c=43.0,
        petco2_end_tidal_mmhg=38.0,
        sensor_application_duration_hours=2.0,
        patient_age_years=48
    )
    print("Estimated Arterial PaCO2:", normal_case["blood_gas_parameters"]["estimated_arterial_paco2_mmhg"], "mmHg")
    print("Ptc-etCO2 Gradient:", normal_case["blood_gas_parameters"]["transcutaneous_end_tidal_gradient_mmhg"], "mmHg")
    print("Ventilatory Status:", normal_case["clinical_assessment"]["ventilatory_status"])
    print("Site Rotation Required:", normal_case["sensor_safety"]["site_rotation_required_now"])
    print()

    print("--- Case 2: Nocturnal Hypoventilation / Severe Hypercapnia (COPD) ---")
    hypercapnia_case = client.evaluate_tcpco2(
        tcpco2_raw_mmhg=82.0,
        sensor_temperature_c=43.0,
        petco2_end_tidal_mmhg=46.0,
        sensor_application_duration_hours=3.5,
        patient_age_years=68
    )
    print("Estimated Arterial PaCO2:", hypercapnia_case["blood_gas_parameters"]["estimated_arterial_paco2_mmhg"], "mmHg")
    print("Ventilatory Status:", hypercapnia_case["clinical_assessment"]["ventilatory_status"])
    print("Pathophysiology:", hypercapnia_case["clinical_assessment"]["pathophysiology_summary"])
    print()

    print("--- Case 3: Sensor Burn Prevention Warning Triggered ---")
    burn_alert_case = client.evaluate_tcpco2(
        tcpco2_raw_mmhg=54.0,
        sensor_temperature_c=43.0,
        sensor_application_duration_hours=4.5,
        patient_age_years=72
    )
    print("Application Duration:", burn_alert_case["sensor_safety"]["application_duration_hours"], "hours")
    print("Max Recommended:", burn_alert_case["sensor_safety"]["max_recommended_duration_hours"], "hours")
    print("Site Rotation Required NOW:", burn_alert_case["sensor_safety"]["site_rotation_required_now"])


if __name__ == "__main__":
    main()
