---
name: genpark-personal-agent-pulmonary-transcutaneous-co2-tcpco2-monitoring-skill
description: Evaluates continuous non-invasive transcutaneous carbon dioxide tension (TcPCO2), calculates Severinghaus temperature-corrected PaCO2, and tracks sensor burn safety site rotation.
---

# Pulmonary Transcutaneous Carbon Dioxide (TcPCO2) Monitoring Skill

This skill computes non-invasive arterial carbon dioxide estimations ($PaCO_2$) from heated transcutaneous electrochemical sensor readings ($TcPCO_2$) to detect alveolar hypoventilation, hypercapnic respiratory failure, and nocturnal sleep-disordered breathing.

## Core Capabilities
- Converts raw $TcPCO_2$ to temperature-corrected arterial $PaCO_2$ via the Severinghaus equation ($S_{temp} = 10^{0.021 \cdot \Delta T}$).
- Computes transcutaneous-to-end-tidal gradient ($\Delta PCO_2 = PaCO_{2,est} - PetCO_2$) to assess ventilation-perfusion mismatch.
- Stratifies eucapnia ($35 - 45\text{ mmHg}$), mild hypercapnia ($45.1 - 50.0\text{ mmHg}$), and severe respiratory failure ($> 50.0\text{ mmHg}$).
- Embedded thermal burn sentinel alerts when site rotation threshold is exceeded ($\ge 4\text{ hours}$ at $43^\circ C$).

## Zero-Mock Architecture
Standard Python standard library only with zero external dependencies.
