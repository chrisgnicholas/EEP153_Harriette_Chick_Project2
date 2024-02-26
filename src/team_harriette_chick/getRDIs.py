from eep153_tools.sheets import read_sheets
from typing import Any


usage_msg = """usage: get_nutrients(sex, age) where sex in ["c", "m", "f"] and 0 < age < 100'"""
DRI_url = "https://docs.google.com/spreadsheets/d/1y95IsQ4HKspPW3HHDtH7QMtlDA66IUsCHJLutVL-MMc/"

DRIs = read_sheets(DRI_url)
# Define *minimums*
diet_max = DRIs['diet_maximums']
diet_min = DRIs['diet_minimums']

def get_col(sex: str, age: int) -> str | None:
    ###Get the right column for this age/sex combination."""
    # here we assume relevant columns have names of the form: F 14-18
    # and other columns never start with the single letters C, F, of M.
    # Walk through the column names and see if one satisfies
    # Parameters:
    #    sex: string   The sex of the person in question
    #    age: int	The age of the person in question

    if sex not in ['C', 'F', 'M']:
        raise ValueError(usage_msg)

    found = False
    correct_col = None
    for col in list(diet_min.columns):
        if found:
            pass
        else:
            split_col = col.split()
            if split_col[0] == sex:
                age_ranges = split_col[1].split('-')
                lower_age = int(age_ranges[0])
                upper_age = int(age_ranges[1])
                if (age >= lower_age) and (age <= upper_age):
                    correct_col = col
                    found = True

    return(correct_col)

def get_nutrient_reqs(sex: str, age: int):
    col_2_get = get_col(sex, age)
    nutrient_df = None
    if col_2_get:
        min_nutrient_df = diet_min[['Nutrition', col_2_get]]
        min_renamed = min_nutrient_df.rename(columns={col_2_get: 'amount'})
        max_nutrient_df = diet_max[['Nutrition', col_2_get]]
        max_renamed = max_nutrient_df.rename(columns={col_2_get: 'amount'})
    return min_renamed, max_renamed

if __name__ == '__main__':
    mindf, maxdf = get_nutrient_reqs('F', 28)
    print(mindf, maxdf)
    print ('done')
