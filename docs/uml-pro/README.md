# NutriSense Professional UML/SE Diagram Pack

This folder contains corrected, standards-following software engineering diagrams in PlantUML source format.

## Files

- 01_use_case_diagram.puml
- 02_dfd_level_0_context.puml
- 03_dfd_level_1.puml
- 04_er_diagram.puml
- 05_activity_diagram.puml
- 06_sequence_diagram.puml
- 07_class_diagram.puml
- 08_state_transition_diagram.puml
- 09_control_flow_diagram.puml
- 10_flowchart_component_logic.puml
- 11_package_diagram.puml
- 12_component_diagram.puml
- 13_deployment_diagram.puml

## SDS Section Mapping

- 2.2 Use Case diagram -> 01_use_case_diagram.puml
- 2.3 ER Model -> 04_er_diagram.puml
- 2.4 Data Flow Diagram -> 02_dfd_level_0_context.puml and 03_dfd_level_1.puml
- 2.5 Control Flow Diagram -> 09_control_flow_diagram.puml
- 2.6 State Transition Diagram -> 08_state_transition_diagram.puml
- 3.1.1 System Architectural Diagram -> 13_deployment_diagram.puml (and/or your existing architecture figure)
- 3.3.1 Flowchart -> 10_flowchart_component_logic.puml
- 2.3 Activity Diagram (OO section) -> 05_activity_diagram.puml
- 2.4 Sequence Diagram (OO section) -> 06_sequence_diagram.puml
- 2.5 Class Diagram (OO section) -> 07_class_diagram.puml
- 3.3.1 Package Diagram (OO section) -> 11_package_diagram.puml
- 3.3.2 Component Diagram (OO section) -> 12_component_diagram.puml
- 3.3.2 Deployment Diagram (OO section) -> 13_deployment_diagram.puml

## How to Export High-Quality Images

1. Open any .puml file in PlantUML online server or local PlantUML extension.
2. Export as PNG or SVG at high resolution.
3. Paste into corresponding SDS section.

Tip: SVG gives the cleanest print quality in Word/PDF.

## Notes on Correctness

- Use case has actor boundaries and include/extend relationships.
- DFD uses external entities, processes, and data stores with directional flows.
- Sequence diagram uses proper lifelines and message ordering.
- Class diagram uses associations/dependencies/compositions.
- State diagram uses valid transition events and terminal states.
- Control/activity/flow diagrams use explicit guards and decision branches.
