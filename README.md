# Football Manager Player Analysis Tool

This tool helps analyze player attributes from Football Manager 2024 by calculating role suitability scores for various positions and roles. It processes HTML exports from the game and provides a comprehensive analysis of player capabilities.

## Features

- Processes Football Manager 2024 HTML player exports
- Calculates role suitability scores (1-20 scale) for various positions:
  - Goalkeeper: Sweeper Keeper (Support)
  - Defense: Ball Playing Defender (Defend)
  - Wing: Wing Back (Attack)
  - Midfield: Central Midfielder (Defend), Attacking Midfielder (Attack)
  - Forward: Inside Forward (Attack), Advanced Forward (Attack)
- Calculates a combined "Speed" rating based on Pace and Acceleration
- Displays results in an interactive PandasGUI interface

## Requirements

- Python 3.x
- Required Python packages:
  - pandas
  - pandasgui
  - tkinter
  - io

## Installation

1. Clone this repository or download the script
2. Install required packages:
```bash
pip install pandas pandasgui
```

## Usage

1. Export your player list from Football Manager 2024 as an HTML file
2. Run the script:
```bash
python script_name.py
```
3. Use the file dialog to select your exported HTML file
4. View and analyze the results in the PandasGUI interface

## Role Score Calculation

The tool uses a weighted scoring system for each role:
- Category A attributes (5x weight): Primary attributes crucial for the role
- Category B attributes (3x weight): Important supporting attributes
- Category C attributes (1x weight): Useful additional attributes

Scores are normalized on a 1-20 scale to match Football Manager's attribute system.

### Available Roles

#### Goalkeeper
- **SK-S (Sweeper Keeper - Support)**
  - Primary: Agility, Reflexes
  - Secondary: Command of Area, Kicking, One on Ones, Anticipation, Concentration, Positioning
  - Tertiary: Aerial Reach, First Touch, Handling, Passing, Rushing Out, Decisions, Vision, Acceleration

#### Defense
- **BPD-D (Ball Playing Defender - Defend)**
  - Primary: Acceleration, Pace, Jumping Reach, Composure
  - Secondary: Heading, Passing, Marking, Tackling, Positioning, Strength
  - Tertiary: Technique, Aggression, Anticipation, Bravery, Concentration, Decisions, Vision

#### Midfield
- **CM-D (Central Midfielder - Defend)**
  - Primary: Acceleration, Pace, Stamina, Work Rate
  - Secondary: Tackling, Concentration, Decisions, Positioning, Teamwork
  - Tertiary: First Touch, Marking, Passing, Technique, Aggression, Anticipation, Composure

#### Attack
- **IF-A (Inside Forward - Attack)**
  - Primary: Acceleration, Pace, Stamina, Work Rate
  - Secondary: Dribbling, Finishing, First Touch, Technique, Anticipation, Off The Ball, Agility
  - Tertiary: Long Shots, Passing, Composure, Flair, Balance

## Additional Information

- The tool handles missing values and range values (e.g., "14-15") by taking averages
- Default value for missing attributes is set to 9
- Speed calculation is based on the average of Pace and Acceleration attributes
- The interface displays key player information including transfer value, wage, nationality, and calculated role scores

## Note

This tool is designed to work with Football Manager 2024 HTML exports. Make sure your export includes all necessary attributes for accurate role calculations.
