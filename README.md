# Pulmonary Transcutaneous Carbon Dioxide (TcPCO2) Monitoring Skill

A production-grade, zero-mock personal agent skill engineered for non-invasive respiratory blood gas monitoring, heated Stow-Severinghaus electrochemical sensing, and hypercapnic ventilatory failure staging.

## Features
- **Deterministic PaCO2 Correction**: Derives arterial carbon dioxide tension from transcutaneous values using empirical temperature and metabolic coefficients.
- **Safety Sentinel**: Automated duration tracking to prevent sensor-induced cutaneous erythema or thermal burns.
- **Pure Standard Library**: Zero external dependencies; fully portable for edge and clinical AI deployment.

## Clinical References
- Severinghaus, J. W. (1981). *A combined transcutaneous PO2-PCO2 electrode with electrochemical HCO3- stabilization*. Journal of Applied Physiology, 51(4), 1027-1032.
- Restrepo, R. D., et al. (2012). *AARC Clinical Practice Guideline: Transcutaneous monitoring of carbon dioxide and oxygen: 2012*. Respiratory Care, 57(11), 1955-1962.

## License
Apache-2.0
