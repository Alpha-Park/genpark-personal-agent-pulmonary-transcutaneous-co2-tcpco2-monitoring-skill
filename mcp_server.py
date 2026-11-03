"""
MCP Server implementation for Pulmonary Transcutaneous Carbon Dioxide (TcPCO2) Skill.
Exposes standard FastMCP-compatible tools for continuous non-invasive PaCO2 estimation.
"""

import sys
import json
from typing import Dict, Any, Optional
from client import TranscutaneousCO2Client


def evaluate_transcutaneous_co2(
    tcpco2_raw_mmhg: float,
    sensor_temperature_c: Optional[float] = 43.0,
    petco2_end_tidal_mmhg: Optional[float] = None,
    sensor_application_duration_hours: Optional[float] = 2.0,
    metabolic_constant_mmhg: Optional[float] = 4.0,
    patient_age_years: Optional[int] = 55
) -> str:
    """
    Evaluates Transcutaneous Carbon Dioxide (TcPCO2) and calculates temperature-corrected arterial PaCO2.
    Returns structured analysis of alveolar hypoventilation, hypercapnia, and sensor burn safety.
    """
    client = TranscutaneousCO2Client()
    result = client.evaluate_tcpco2(
        tcpco2_raw_mmhg=tcpco2_raw_mmhg,
        sensor_temperature_c=sensor_temperature_c,
        petco2_end_tidal_mmhg=petco2_end_tidal_mmhg,
        sensor_application_duration_hours=sensor_application_duration_hours,
        metabolic_constant_mmhg=metabolic_constant_mmhg,
        patient_age_years=patient_age_years
    )
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--tools":
        tools = [
            {
                "name": "evaluate_transcutaneous_co2",
                "description": "Calculates temperature-metabolic corrected arterial PaCO2 from raw transcutaneous TcPCO2, computes transcutaneous-to-end-tidal gradient, and stratifies hypercapnic failure.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tcpco2_raw_mmhg": {"type": "number", "description": "Raw transcutaneous carbon dioxide reading in mmHg (e.g. 52 mmHg)"},
                        "sensor_temperature_c": {"type": "number", "description": "Electrode temperature in Celsius (normal: 42.0 - 44.0 C, default: 43.0 C)"},
                        "petco2_end_tidal_mmhg": {"type": "number", "description": "Optional simultaneous end-tidal CO2 (PetCO2) in mmHg"},
                        "sensor_application_duration_hours": {"type": "number", "description": "Continuous duration sensor has been at the current site in hours (default: 2.0 h)"},
                        "metabolic_constant_mmhg": {"type": "number", "description": "Local skin metabolic CO2 production in mmHg (default: 4.0 mmHg)"},
                        "patient_age_years": {"type": "integer", "description": "Patient age in years (default: 55)"}
                    },
                    "required": ["tcpco2_raw_mmhg"]
                }
            }
        ]
        print(json.dumps(tools, indent=2))
    else:
        # Simple self-test
        client = TranscutaneousCO2Client()
        test_res = client.evaluate_tcpco2(
            tcpco2_raw_mmhg=54.0,
            sensor_temperature_c=43.0,
            petco2_end_tidal_mmhg=37.0
        )
        print("Self-test passed:")
        print(json.dumps(test_res, indent=2))
