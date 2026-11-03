"""
Pulmonary Transcutaneous Carbon Dioxide (TcPCO2) & Arterial PaCO2 Estimator Client.
Zero-mock pure Python standard library implementation.
Calculates Severinghaus temperature-metabolic corrected arterial PaCO2 (mmHg),
Alveolar-Transcutaneous PCO2 gradient (Ptc-etCO2), and hypercapnic ventilatory failure staging.
"""

import math
from typing import Dict, Any, Optional


class TranscutaneousCO2Client:
    """
    Evaluates non-invasive continuous carbon dioxide tension:
    - TcPCO2 (mmHg): raw transcutaneous potentiometric sensor reading
    - PaCO2_est (mmHg): (TcPCO2 - C_metabolic) / S_temp
        * S_temp = 10^(0.021 * (T_sensor - 37.0))
        * C_metabolic = ~4.0 mmHg
    - PaCO2 Normal: 35.0 - 45.0 mmHg
    - Mild Hypercapnia: 45.1 - 50.0 mmHg
    - Severe Hypercapnic Failure: > 50.0 mmHg (triggers NIV / BiPAP titration)
    - Sensor Burn Prevention Sentinel: Site rotation tracker (<= 4h at 43C, <= 8h at 42C).
    """

    def __init__(self):
        pass

    def evaluate_tcpco2(
        self,
        tcpco2_raw_mmhg: float,
        sensor_temperature_c: Optional[float] = 43.0,
        petco2_end_tidal_mmhg: Optional[float] = None,
        sensor_application_duration_hours: Optional[float] = 2.0,
        metabolic_constant_mmhg: Optional[float] = 4.0,
        patient_age_years: Optional[int] = 55
    ) -> Dict[str, Any]:
        """
        Calculates corrected arterial PaCO2 and hypercapnia risk.
        tcpco2_raw_mmhg: measured transcutaneous PCO2 in mmHg (e.g. 52.0 mmHg).
        sensor_temperature_c: electrode heating temperature in C (default 43.0 C).
        petco2_end_tidal_mmhg: optional capnography PetCO2 in mmHg (e.g. 38.0 mmHg).
        sensor_application_duration_hours: hours sensor has remained at current site.
        """
        if tcpco2_raw_mmhg <= 0:
            raise ValueError("TcPCO2 must be strictly positive.")
        if sensor_temperature_c < 37.0 or sensor_temperature_c > 45.0:
            raise ValueError("Sensor temperature must be between 37.0C and 45.0C.")

        # Severinghaus temperature correction coefficient
        temp_delta = sensor_temperature_c - 37.0
        s_temp = 10.0 ** (0.021 * temp_delta)

        # Corrected arterial PaCO2 estimation
        paco2_est = (tcpco2_raw_mmhg - metabolic_constant_mmhg) / s_temp
        paco2_est = round(paco2_est, 1)

        # Transcutaneous - End-Tidal gradient (TcPCO2 - PetCO2)
        transcutaneous_et_gradient = None
        if petco2_end_tidal_mmhg is not None:
            transcutaneous_et_gradient = round(paco2_est - petco2_end_tidal_mmhg, 1)

        # Clinical Hypercapnia Staging (ATS / ERS Guidelines):
        if paco2_est > 55.0:
            ventilatory_status = "Severe Acute-on-Chronic Hypercapnic Respiratory Failure"
            clinical_risk = "Critical alveolar hypoventilation; imminent respiratory acidosis risk. Immediate indication for non-invasive ventilation (NIV/BiPAP) or ventilator adjustments."
        elif paco2_est > 45.0:
            ventilatory_status = "Mild-to-Moderate Hypercapnia (Alveolar Hypoventilation)"
            clinical_risk = "Elevated arterial carbon dioxide; monitor respiratory drive, obstructive sleep apnea episodes, or nocturnal hypoventilation."
        elif paco2_est < 35.0:
            ventilatory_status = "Hypocapnia / Alveolar Hyperventilation"
            clinical_risk = "Respiratory alkalosis risk; may reflect tachypneic compensatory drive, pain, anxiety, or mechanical overventilation."
        else:
            ventilatory_status = "Eucapnia / Normal Alveolar Ventilation (35 - 45 mmHg)"
            clinical_risk = "Optimal carbon dioxide clearance and balanced medullary respiratory drive."

        # Burn Safety Sentinel:
        max_safe_hours = 4.0 if sensor_temperature_c >= 43.0 else 8.0
        site_rotation_needed = (sensor_application_duration_hours or 0.0) >= max_safe_hours

        return {
            "status": "success",
            "blood_gas_parameters": {
                "tcpco2_raw_mmhg": round(tcpco2_raw_mmhg, 1),
                "estimated_arterial_paco2_mmhg": paco2_est,
                "sensor_temperature_c": round(sensor_temperature_c, 1),
                "temperature_correction_factor_s_temp": round(s_temp, 3),
                "transcutaneous_end_tidal_gradient_mmhg": transcutaneous_et_gradient
            },
            "sensor_safety": {
                "application_duration_hours": sensor_application_duration_hours,
                "max_recommended_duration_hours": max_safe_hours,
                "site_rotation_required_now": site_rotation_needed
            },
            "clinical_assessment": {
                "ventilatory_status": ventilatory_status,
                "pathophysiology_summary": clinical_risk
            }
        }
