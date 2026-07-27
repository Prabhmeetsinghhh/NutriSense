SYNOPSIS TEMPLATE B.TECH (VII sem) PROJECT WORK-I

NUTRISENSE: PERSONALIZED DIET AND FITNESS PLANNER FOR INDIAN USERS

A Synopsis for
Minor Project

BACHELOR OF TECHNOLOGY in COMPUTER SCIENCE & ENGINEERING

BY
Prabhmeet Singh
EN23CS301742

Under the Guidance of
Vishal Sharma Sir and Anusha Jain Mam

Department of Computer Science & Engineering, Faculty of Engineering
MEDICAPS UNIVERSITY, INDORE-453331

MARCH 2026

---

1. Introduction

Health and fitness planning is often difficult for students and working professionals because most available applications are either generic, expensive, or not localized for Indian food habits and budget constraints. NutriSense is a full-stack web application designed to provide personalized daily diet and weekly fitness plans based on a user's body profile, fitness level, goal, and diet preference. The system focuses on practical Indian meal options and simple workout routines that can be followed without advanced equipment.

NutriSense uses rule-based logic for calculating BMI, daily calorie requirements, and protein targets, then distributes nutrition goals across four daily meals: breakfast, lunch, evening meal, and dinner. The application also generates a weekly workout schedule and fitness guidance. This integrated approach helps users move from random food choices to a structured and goal-oriented lifestyle [1], [2].

2. Literature Review

Several studies and practical systems show that personalized nutrition and structured exercise planning improve adherence and long-term outcomes compared to generic plans. Energy expenditure models such as Mifflin-St Jeor are commonly used to estimate daily calorie requirements and are considered reliable for adult populations [3]. BMI-based classification is widely used for first-level goal mapping in health systems [4].

Modern diet applications increasingly combine behavior-aware recommendations, macro-based planning, and user preferences to improve usability. However, many tools are not optimized for Indian dietary patterns, affordability, and mixed lifestyle constraints faced by students. NutriSense addresses this gap by integrating localized meal options, budget-aware suggestions, and beginner-friendly fitness routines in one platform [5], [6].

3. Problem Definition

Existing fitness and diet tools have the following limitations:

- One-size-fits-all plans that ignore user profile details.
- Limited support for Indian meal patterns and common food availability.
- Poor alignment with student budget constraints.
- Weak integration between diet recommendation and fitness planning.
- Complex interfaces that reduce consistency and user engagement.

Problem Statement:
Design and develop a personalized, affordable, and easy-to-use web platform that generates Indian diet and fitness plans from user-specific inputs such as age, height, weight, fitness level, and food preference.

4. Objectives

The major objectives of this project are:

- To build a web-based personalized health planner named NutriSense.
- To compute BMI, daily calorie needs, and protein targets using rule-based formulas.
- To generate four-meal daily diet plans (breakfast, lunch, evening, dinner).
- To support multiple diet preferences (veg, non-veg, vegan, eggetarian).
- To generate a weekly workout schedule aligned with user goal and activity level.
- To provide budget-oriented recommendations suitable for Indian users.
- To present results through an interactive and user-friendly frontend.

5. Methodology

The project is implemented as a client-server web application.

5.1 Technology Stack

- Frontend: React + TypeScript + Vite
- Backend: FastAPI (Python)
- API Communication: REST (JSON)
- Core modules: Diet service, fitness service, Indian food model, API router

5.2 Functional Workflow

- User enters profile: name, age, weight, height, fitness level, goal, diet type.
- Backend computes BMI and maps it to a goal category.
- Protein requirement is calculated using experience-level multipliers:
  - Beginner: 1.2 g/kg
  - Intermediate: 1.5 g/kg
  - Advanced: 1.8 g/kg
- Calorie target is estimated using TDEE and goal adjustment.
- Protein is distributed across meals in a 25-30-20-25 ratio.
- Meal templates are selected according to diet preference.
- A weekly workout schedule and recovery tips are generated.
- Frontend displays detailed meal macros, estimated cost, and fitness routine.

5.3 Current Outcomes

- Rule-based diet generation implemented and integrated.
- Four-meal output available across diet categories.
- BMI and goal-specific planning active.
- Weekly fitness scheduling integrated with the diet module.
- Frontend visualization completed with complete API flow.

6. References

[1]. World Health Organization, "Obesity and overweight," WHO Fact Sheets, 2024.

[2]. Harvard T.H. Chan School of Public Health, "The Nutrition Source: Healthy Eating Plate," 2023.

[3]. Mifflin, M. D., St Jeor, S. T., et al., "A new predictive equation for resting energy expenditure in healthy individuals," The American Journal of Clinical Nutrition, vol. 51, no. 2, pp. 241-247, 1990.

[4]. National Institutes of Health, "Clinical guidelines on the identification, evaluation, and treatment of overweight and obesity in adults," NIH Publication, 1998.

[5]. Celis-Morales, C., Livingstone, K., et al., "Personalized nutrition and health outcomes: A review of approaches and evidence," Proc. Nutrition Society, 2021.

[6]. Ministry of Health and Family Welfare, Government of India, "Diet and Wellness Guidelines for Adults," 2022.
