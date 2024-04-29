import pandas as pd
from pandasgui import show
from tkinter import Tk, filedialog
from io import StringIO
import re

column_name_mapping = {
    #GK technicals:
    'Aer': 'AerialReach',
    'Cmd': 'CommandOfArea',
    'Com': 'Communication',
    'Ecc': 'Eccentricity',
    'Han': 'Handling',
    'Kic': 'Kicking',
    '1v1': 'OneOnOnes',
    'Pun': 'Punching',
    'Ref': 'Reflexes',
    'TRO': 'RushingOut',
    'Thr': 'Throwing',
    #Outfield player Technicals:
    'Cor': 'Corners',
    'Cro': 'Crossing',
    'Dri': 'Dribbling',
    'Fin': 'Finishing',
    'Fir': 'FirstTouch',
    'Fre': 'FreeKicks',
    'Hea': 'Heading',
    'Lon': 'LongShots',
    'L Th': 'LongThrows',
    'Mar': 'Marking',
    'Pas': 'Passing',
    'Pen': 'PenaltyTaking',
    'Tck': 'Tackling',
    'Tec': 'Technique',
    #Player Mentals:
    'Agg': 'Aggression',
    'Ant': 'Anticipation',
    'Bra': 'Bravery',
    'Cmp': 'Composure',
    'Cnt': 'Concentration',
    'Dec': 'Decisions',
    'Det': 'Determination',
    'Fla': 'Flair',
    'Ldr': 'Leadership',
    'OtB': 'OffTheBall',
    'Pos': 'Positioning',
    'Tea': 'Teamwork',
    'Vis': 'Vision',
    'Wor': 'WorkRate',
    #PLayer Physicals:
    'Acc': 'Acceleration',
    'Agi': 'Agility',
    'Bal': 'Balance',
    'Jum': 'JumpingReach',
    'Nat': 'NaturalFitness',
    'Pac': 'Pace',
    'Sta': 'Stamina',
    'Str': 'Strength'
}


def parse_attribute(value):
    if pd.isna(value) or value == '--':
        return 9  # Handle missing values or placeholders like "--"
    elif isinstance(value, str) and '-' in value:
        try:
            low, high = map(int, value.split('-'))
            return (low + high) / 2  # Handle range by returning the average
        except ValueError:
            return 9  # Handle malformed ranges
    else:
        try:
            return int(value)  # Convert numeric strings to integers
        except ValueError:
            return 9  # Handle other non-numeric strings



def calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights, max_attribute_value=20):
    # Calculate the sum for each category using the mapped attribute names
    a_score = sum(parse_attribute(row.get(attr, 9)) for attr in a_attributes)  # Use get with default
    b_score = sum(parse_attribute(row.get(attr, 9)) for attr in b_attributes)
    c_score = sum(parse_attribute(row.get(attr, 9)) for attr in c_attributes)

    # Calculate the maximum possible scores for each category
    max_a_score = len(a_attributes) * max_attribute_value
    max_b_score = len(b_attributes) * max_attribute_value
    max_c_score = len(c_attributes) * max_attribute_value

    # Apply weights to both calculated and maximum scores
    total_score = (a_score * weights['a'] + b_score * weights['b'] + c_score * weights['c'])
    max_possible_score = (max_a_score * weights['a'] + max_b_score * weights['b'] + max_c_score * weights['c'])

    # Normalize the overall score
    normalized_score = (total_score / max_possible_score) * 19 + 1

    return round(normalized_score, 1)


# Function to calculate and normalize GK role suitability score
def calculate_sweeper_keeper_support_score(row):
    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri') mapped to full names
    a_attributes = ['Agility', 'Reflexes']
    b_attributes = ['CommandOfArea', 'Kicking', 'OneOnOnes', 'Anticipation', 'Concentration', 'Positioning']
    c_attributes = ['AerialReach', 'FirstTouch', 'Handling', 'Passing', 'RushingOut', 'Decisions', 'Vision', 'Acceleration']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)


def calculate_ball_playing_defender_defend_score(row):

    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri')
    a_attributes = ['Acceleration', 'Pace', 'JumpingReach', 'Composure']
    b_attributes = ['Heading', 'Passing', 'Marking', 'Tackling', 'Tackling', 'Positioning', 'Strength']
    c_attributes = ['Technique', 'Aggression', 'Anticipation', 'Bravery', 'Concentration', 'Decisions', 'Vision']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)


'''
def calculate_wing_back_support_score(row):

    a_attributes = ['Acceleration', 'Pace', 'Stamina', 'WorkRate']
    b_attributes = ['Crossing', 'Dribbling', 'Marking', 'Tackling', 'OffTheBall', 'Teamwork']
    c_attributes = ['FirstTouch', 'Passing', 'Technique', 'Anticipation', 'Concentration', 'Decisions', 'Positioning', 'Agility', 'Balance']

    weights = {'a': 5, 'b': 3, 'c': 1}

    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)
'''


def calculate_wing_back_attack_score(row):
    a_attributes = ['Acceleration', 'Pace', 'Stamina', 'WorkRate']
    b_attributes = ['Crossing', 'Dribbling', 'Tackling', 'Technique', 'OffTheBall', 'Teamwork']
    c_attributes = ['FirstTouch', 'Marking', 'Passing', 'Anticipation', 'Concentration', 'Decisions',
                    'Flair', 'Positioning', 'Agility', 'Balance']

    weights = {'a': 5, 'b': 3, 'c': 1}

    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)

'''
def calculate_inverted_wb_support_score(row):

    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri')
    a_attributes = ['Acceleration', 'Pace', 'Stamina', 'WorkRate']
    b_attributes = ['FirstTouch', 'Passing', 'Dribbling', 'Tackling', 'Composure', 'Decisions', 'Teamwork']
    c_attributes = ['Marking', 'Technique', 'Anticipation', 'Concentration', 'OffTTheBall', 'Positioning', 'Vision', 'Agility']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)
'''
'''BWM_D
def calculate_ball_winning_midfielder_defend_score(row):
    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri') using full attribute names
    a_attributes = ['WorkRate', 'Stamina', 'Acceleration', 'Pace']  # Key attributes
    b_attributes = ['Tackling', 'Aggression', 'Anticipation', 'Teamwork']  # Green attributes
    c_attributes = ['Marking', 'Bravery', 'Concentration', 'Positioning', 'Agility', 'Strength']  # Blue attributes

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)
'''


def calculate_central_midfielder_defend_score(row):
    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri') mapped to full names
    a_attributes = ['Acceleration', 'Pace', 'Stamina', 'WorkRate']
    b_attributes = ['Tackling', 'Concentration', 'Decisions', 'Positioning', 'Teamwork']
    c_attributes = ['FirstTouch', 'Marking', 'Passing', 'Technique', 'Aggression', 'Anticipation', 'Composure']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)


'''
def calculate_deep_lying_playmaker_support_score(row):
    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri') using full attribute names
    a_attributes = ['WorkRate', 'Stamina', 'Acceleration', 'Pace']
    b_attributes = ['FirstTouch', 'Passing', 'Technique', 'Composure', 'Decisions', 'Teamwork', 'Vision']
    c_attributes = ['Anticipation', 'OffTheBall', 'Positioning', 'Balance']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)
'''
'''Mezzala-S
def calculate_mezzala_support_score(row):
    # Using the column_name_mapping for full attribute names
    a_attributes = ['Acceleration', 'Pace', 'Stamina', 'WorkRate']
    b_attributes = ['Passing', 'Technique', 'Decisions', 'OffTheBall']
    c_attributes = ['Dribbling', 'FirstTouch', 'LongShots', 'Tackling', 'Anticipation', 'Composure', 'Vision', 'Balance']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)
'''


def calculate_attacking_midfielder_attack_score(row):
    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri') mapped to full names
    a_attributes = ['Acceleration', 'Pace', 'Stamina', 'WorkRate']
    b_attributes = ['Dribbling', 'FirstTouch', 'LongShots', 'Passing', 'Technique', 'Anticipation', 'Decisions', 'Flair', 'OffTheBall']
    c_attributes = ['Finishing', 'Composure', 'Vision', 'Agility']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)


def calculate_inside_forward_attack_score(row):
    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri') mapped to full names
    a_attributes = ['Acceleration', 'Pace', 'Stamina', 'WorkRate']
    b_attributes = ['Dribbling', 'Finishing', 'FirstTouch', 'Technique', 'Anticipation', 'OffTheBall', 'Agility']
    c_attributes = ['LongShots', 'Passing', 'Composure', 'Flair', 'Balance']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)


'''
def calculate_winger_attack_score(row):
    # Using the column_name_mapping for full attribute names
    a_attributes = ['Acceleration', 'Pace', 'Stamina', 'WorkRate']
    b_attributes = ['Crossing', 'Dribbling', 'Technique', 'Agility']
    c_attributes = ['FirstTouch', 'Passing', 'Anticipation', 'Flair', 'OffTheBall', 'Balance']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)
'''
'''
def calculate_pressing_forward_attack_score(row):
    # Assuming each attribute can have a maximum value of 20
    max_attribute_value = 20

    # Attributes and their importance
    a_attributes = ['Acceleration', 'Pace', 'Finishing']
    b_attributes = ['Aggression', 'Anticipation', 'Bravery', 'OffTheBall', 'Teamwork', 'WorkRate', 'Stamina']
    c_attributes = ['FirstTouch', 'Composure', 'Concentration', 'Decisions', 'Agility', 'Balance', 'Strength']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)
'''


def calculate_advanced_forward_attack_score(row):
    # Attributes categorized by their importance ('a-pri', 'b-pri', 'c-pri') mapped to full names
    a_attributes = ['Acceleration', 'Pace', 'Finishing']
    b_attributes = ['Dribbling', 'FirstTouch', 'Technique', 'Composure', 'OffTheBall']
    c_attributes = ['Passing', 'Anticipation', 'Decisions', 'WorkRate', 'Agility', 'Balance', 'Stamina']

    # Define weights for each category
    weights = {'a': 5, 'b': 3, 'c': 1}

    # Call the generalized function with role-specific attributes and weights
    return calculate_role_score(row, a_attributes, b_attributes, c_attributes, weights)


def load_html_to_pandasgui():
    root = Tk()
    root.withdraw()

    initial_dir = r'C:\Users\Sander Drange\Documents\Sports Interactive\Football Manager 2024\HTML-files'  #Direct access to where I keep my fm HTML files
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Select file",
                                           filetypes=[("HTML files", "*.html")])

    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        df_list = pd.read_html(StringIO(html_content))

        if df_list:
            df = df_list[0]

            # Adjust columns for 'Nationality' and 'Natural Fitness' before applying the full column_name_mapping
            # Since 'Nationality' is the sixth column, we directly rename it.
            df.columns.values[9] = 'Nationality'

            # Now apply column_name_mapping for other columns
            # Ensure 'Nat' for 'NaturalFitness' is included in mapping if it's after 'Nationality'
            df.rename(columns=column_name_mapping, inplace=True)

            # Calculate 'Sweeper Keeper - Support' score for each player
            df['SK-S'] = df.apply(calculate_sweeper_keeper_support_score, axis=1)

            df['BPD-D'] = df.apply(calculate_ball_playing_defender_defend_score, axis=1)

            # df['WB-S'] = df.apply(calculate_wing_back_support_score, axis=1)

            df['WB-A'] = df.apply(calculate_wing_back_attack_score, axis=1)

            #df['IWB'] = df.apply(calculate_inverted_wb_support_score, axis=1)

            #df['BWM-S'] = df.apply(calculate_ball_winning_midfielder_defend_score, axis=1)

            df['CM-D'] = df.apply(calculate_central_midfielder_defend_score, axis=1)

            #df['DPL-S'] = df.apply(calculate_deep_lying_playmaker_support_score, axis=1)

            #df['MEZ-S'] = df.apply(calculate_mezzala_support_score, axis=1)

            df['AM-A'] = df.apply(calculate_attacking_midfielder_attack_score, axis=1)

            df['IF-A'] = df.apply(calculate_inside_forward_attack_score, axis=1)

            #df['W-A'] = df.apply(calculate_winger_attack_score, axis=1)

            #df['PF-A'] = df.apply(calculate_pressing_forward_attack_score, axis=1)

            df['AF-A'] = df.apply(calculate_advanced_forward_attack_score, axis=1)

            # Apply the parse_attribute function to the 'Pace' and 'Acceleration' columns
            df['Pace'] = df['Pace'].apply(parse_attribute)
            df['Acceleration'] = df['Acceleration'].apply(parse_attribute)

            # Now calculate the 'Speed' as the mean of 'Pace' and 'Acceleration'
            df['Speed'] = df[['Pace', 'Acceleration']].mean(axis=1)


            # Assuming Speed is calculated as the average of Pace and Acceleration
            if 'Pace' in df.columns and 'Acceleration' in df.columns:
                df['Speed'] = df[['Pace', 'Acceleration']].mean(axis=1)

            # Specify the columns to display, ensuring you adjust based on the columns present in your DataFrame
            columns_to_display = ['Inf', 'Name', 'Age', 'Club', 'Transfer Value', 'Wage', 'Nationality', 'Position', 'Personality',
                                  #'Media Handling',
                                  'Left Foot', 'Right Foot',
                                  'Speed', 'Strength',
                                  'WorkRate', 'Height', 'SK-S', 'BPD-D', 'WB-A', 'CM-D',
                                  'AM-A', 'IF-A', 'AF-A']

            filtered_columns = [col for col in columns_to_display if col in df.columns]
            df_display = df[filtered_columns]

            show(df_display)
        else:
            print("No tables found in the HTML file.")
    else:
        print("No file selected.")


if __name__ == "__main__":
    load_html_to_pandasgui()
